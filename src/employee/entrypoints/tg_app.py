import asyncio
from enum import Enum
import logging
import sys

from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.filters.command import Command
from aiogram.filters.callback_data import CallbackData
from src.employee.adapters.repository import SqlAlchemyRepository
from src.employee.domain.model import StatusNotAvailibleError

from src.settings import Settings
from src.employee.service_layer.services import (
    get_active_employees_departaments,
    get_availible_statuses,
    set_status_employee,
)
from src.employee.service_layer.unit_of_work import (
    DEFAULT_SESSION_FACTORY,
    SqlAlchemyUnitOfWork,
)


# All handlers should be attached to the Router (or Dispatcher)
employee_router = Router(name="employee")

choice_availible_status_command = Command("choise_availible_status")
get_active_employees_departament_command = Command("get_active_employees_departament")


class EmployeeAction(str, Enum):
    set_status = "set_status"


class EmployeeCallbackData(CallbackData, prefix="emp"):
    action: EmployeeAction
    data: int


@employee_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """

    await message.answer(
        f"Приветствую, {hbold(message.from_user.full_name)}!\n"
        f"Для регистрации в системе необходимо передать Ваш telegram id - {message.chat.id} ответсвенному сотруднику",
    )


@employee_router.message(choice_availible_status_command)
async def choise_status_handler(message: Message) -> None:
    tg_id = message.chat.id
    statuses_inline_keyboard = get_availible_statuses_inline_keyboard(tg_id)
    await message.answer(
        "Выберите статус из доступных:",
        reply_markup=statuses_inline_keyboard,
    )


@employee_router.callback_query(
    EmployeeCallbackData.filter(F.action == EmployeeAction.set_status)
)
async def set_status_handler(
    query: CallbackQuery, callback_data: EmployeeCallbackData
) -> None:
    tg_id = query.from_user.id

    status_id = callback_data.data
    try:
        set_status_employee(
            tg_id,
            status_id,
            uow=SqlAlchemyUnitOfWork(),
        )
    except StatusNotAvailibleError:
        await query.answer("Статус недоступен")
        await query.message.delete()
    else:
        await query.answer("Статус успешно изменен")
        statuses_inline_keyboard = get_availible_statuses_inline_keyboard(tg_id)
        await query.message.edit_reply_markup(
            reply_markup=statuses_inline_keyboard,
        )


@employee_router.message(get_active_employees_departament_command)
async def get_active_employees_departament_handler(message: Message) -> None:
    tg_id = message.chat.id
    session = DEFAULT_SESSION_FACTORY()
    active_employees_departaments = get_active_employees_departaments(
        tg_id,
        repo=SqlAlchemyRepository(session),
    )
    text = ""
    for employee in active_employees_departaments:
        last_status = employee.last_status
        if last_status is None:
            status_title = "Не установлен"
            status_set_at = ""
        else:
            status_title = last_status.status.title
            status_set_at = last_status.set_at.strftime("%d.%m.%Y %H:%M")
        text += (
            f"Сотрудник: {employee.first_name} {employee.last_name}\n"
            f"Статус: {status_title}\n"
            f"Был изменен в: {status_set_at}\n\n"
        )
    session.close()
    await message.answer(text)


def get_availible_statuses_inline_keyboard(tg_id: int):
    session = DEFAULT_SESSION_FACTORY()
    availible_statuses = get_availible_statuses(
        tg_id,
        repo=SqlAlchemyRepository(session),
    )
    availible_statuses = sorted(list(availible_statuses), key=id)
    keyboard = []
    for status in availible_statuses:
        set_status_callback = EmployeeCallbackData(
            action=EmployeeAction.set_status,
            data=status.id,
        )
        status_button = InlineKeyboardButton(
            text=status.title, callback_data=set_status_callback.pack()
        )
        keyboard.append([status_button])
    session.close()
    inline_markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
    return inline_markup


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    settings = Settings()
    bot = Bot(settings.bot_token, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
