from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(unsafe_hash=True)
class Role:
    title: str


@dataclass(unsafe_hash=True)
class Status:
    title: str
    is_working: bool


@dataclass(unsafe_hash=True)
class HistoryStatus:
    status: Status
    set_at: datetime


@dataclass(unsafe_hash=True)
class AvailibleStatus:
    role: Role
    status: Status
    availible_status: Status


class StatusNotAvailibleError(Exception):
    pass


class EmployeePermissonError(Exception):
    pass


class Employee:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        telegram_id: int,
        role: Role,
        departament: "Departament",
        status: Status,
        id: Optional[int] = None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.tg_id = telegram_id
        self.role = role
        self.departament = departament
        self._id = id
        self._status = status
        self._history_status: list[HistoryStatus] = list()
        self._availible_statuses: set[Status] = set()

    def __repr__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __eq__(self, other):
        if not isinstance(other, Employee):
            return False
        return other._id == self._id

    def __hash__(self):
        return hash(self._id)

    @property
    def status(self) -> Optional[Status]:
        return self._status

    @status.setter
    def status(self, status: Status):
        if status not in self._availible_statuses:
            raise StatusNotAvailibleError("Unavailible status: {}".format(status.title))
        self._status = status
        self._history_status.append(HistoryStatus(status=status, set_at=datetime.now()))

    def get_available_statuses(self) -> set[Status]:
        return self._availible_statuses

    @property
    def last_status(self) -> Optional[HistoryStatus]:
        if len(self._history_status) < 1:
            return None
        return self._history_status[-1]


class Departament:
    def __init__(
        self,
        title: str,
        id: Optional[int] = None,
        parent_id: Optional[int] = None,
    ) -> None:
        self.title = title
        self._id = id
        self._parent_id = parent_id
        self._employees: set[Employee] = set()
        self._managers: set[Employee] = set()
        self._child_departments: set[Departament] = set()

    def __repr__(self) -> str:
        return self.title

    def __eq__(self, other):
        if not isinstance(other, Departament):
            return False
        return other._id == self._id

    def __hash__(self):
        return hash(self._id)

    def add_employee(self, employee: Employee):
        self._employees.add(employee)

    def remove_employee(self, employee: Employee):
        self._employees.remove(employee)

    def add_manager(self, employee: Employee):
        self._managers.add(employee)

    def remove_manager(self, employee: Employee):
        self._managers.remove(employee)

    def add_child_departament(self, departament: "Departament"):
        departament._parent_id = self._id
        self._child_departments.add(departament)

    def remove_child_departament(self, departament: "Departament"):
        departament._parent_id = None
        self._child_departments.remove(departament)

    def get_employees(self, requesting_employee: Employee):
        if requesting_employee not in self._managers:
            raise EmployeePermissonError(
                f"У пользователя {requesting_employee} не достаточно прав"
            )
        all_employees = set()
        all_employees.update(self._employees)
        for child in self._child_departments:
            all_employees.update(child._employees)

        return all_employees
