import pytest

from src.employee.domain.model import (
    Employee,
    Role,
    Status,
    StatusNotAvailibleError,
)


def create_employee():
    role = Role("Програмист")
    emp = Employee(1, "Maxim", "Ageev", 123456, role)

    start_status = Status("start", is_working=False)
    work = Status("work", is_working=True)
    end_status = Status("end", is_working=True)

    emp._availible_statuses = set([start_status, work, end_status])

    return emp


def test_set_availible_status():
    emp = create_employee()
    availible_statuses = emp.get_available_statuses()

    for status in availible_statuses:
        emp.status = status
        assert status == emp.status
    assert len(availible_statuses) == len(emp._history_status)


def test_set_unavailible_status():
    unavailible_status = Status("unavailible", is_working=False)
    emp = create_employee()
    with pytest.raises(
        StatusNotAvailibleError,
        match=unavailible_status.title,
    ):
        emp.status = unavailible_status
