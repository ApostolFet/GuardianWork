from src.employee.adapters.repository import AbstractRepository
from src.employee.domain import model
from src.employee.service_layer.unit_of_work import AbstractUnitOfWork


def add_employee(
    first_name: str,
    last_name: str,
    tg_id: int,
    role_id: int,
    departament_id: int,
    uow: AbstractUnitOfWork,
) -> int:
    with uow:
        role = uow.repo.get(model.Role, role_id)
        departament = uow.repo.get(model.Departament, departament_id)
        new_employee = model.Employee(
            first_name=first_name,
            last_name=last_name,
            tg_id=tg_id,
            role=role,
            status=model.Status("Зарегестрирован", is_working=False),
            departament=departament,
        )
        uow.repo.add(new_employee)
        new_employee_id = new_employee._id
        uow.commit()
    return new_employee_id


def get_availible_statuses(
    tg_id: int,
    repo: AbstractRepository,
) -> set[model.Status]:
    employee = repo.get_employee_by_tg_id(tg_id)
    available_statuses = employee.get_available_statuses()
    return available_statuses


def set_status_employee(
    tg_id: int,
    status_id: int,
    uow: AbstractUnitOfWork,
):
    with uow:
        status = uow.repo.get(model.Status, status_id)
        employee = uow.repo.get_employee_by_tg_id(tg_id)
        employee.status = status
        uow.commit()


def get_active_employees_departaments(
    tg_id: int,
    repo: AbstractRepository,
):
    requesting_employee = repo.get_employee_by_tg_id(tg_id)
    employees_departaments = requesting_employee.departament.get_employees(
        requesting_employee
    )
    return employees_departaments
