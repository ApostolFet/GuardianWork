from faker import Faker
import pytest
from src.employee.domain.model import (
    Departament,
    Employee,
    EmployeePermissonError,
    Role,
    Status,
)


fake = Faker("ru_RU")


def test_get_all_employees():
    dep = Departament("FFru")
    manager_role = Role("Управляющий")
    status = Status(title="Ушел с работы", is_working=False)
    manager = Employee(
        id=fake.random_int(),
        first_name=fake.first_name_male(),
        last_name=fake.last_name_male(),
        telegram_id=fake.random_int(),
        departament=dep,
        role=manager_role,
        status=status,
    )
    dep.add_manager(manager)
    worker_role = Role("Работник")
    expected_emp = set()
    len_employee = 5
    for _ in range(len_employee):
        emp = Employee(
            id=fake.random_int(),
            first_name=fake.first_name_male(),
            last_name=fake.last_name_male(),
            telegram_id=fake.random_int(),
            role=worker_role,
            departament=dep,
            status=status,
        )
        dep.add_employee(emp)
        expected_emp.add(emp)

    result = dep.get_employees(manager)
    assert expected_emp == result


def test_get_all_employees_with_recursive_structure():
    dep = Departament("FFru")
    manager_role = Role("Управляющий")
    status = Status(title="Ушел с работы", is_working=False)
    manager = Employee(
        id=fake.random_int(),
        first_name=fake.first_name_male(),
        last_name=fake.last_name_male(),
        telegram_id=fake.random_int(),
        status=status,
        departament=dep,
        role=manager_role,
    )
    dep.add_manager(manager)
    worker_role = Role("Работник")
    expected_emp = set()
    len_employee = 5
    for _ in range(len_employee):
        tmp_dep = Departament(fake.random_int(), fake.job())
        emp = Employee(
            id=fake.random_int(),
            first_name=fake.first_name_male(),
            last_name=fake.last_name_male(),
            telegram_id=fake.random_int(),
            status=status,
            departament=dep,
            role=worker_role,
        )
        tmp_dep.add_employee(emp)
        dep.add_child_departament(tmp_dep)
        expected_emp.add(emp)

    result = dep.get_employees(manager)
    assert expected_emp == result


def test_get_employees_manager_no_permission():
    dep = Departament("FFru")
    manager_role = Role("Управляющий")
    status = Status(title="Ушел с работы", is_working=False)
    manager = Employee(
        id=fake.random_int(),
        first_name=fake.first_name_male(),
        last_name=fake.last_name_male(),
        telegram_id=fake.random_int(),
        status=status,
        departament=dep,
        role=manager_role,
    )
    dep.add_manager(manager)
    worker_role = Role("Работник")
    expected_emp = set()
    len_employee = 5
    for _ in range(len_employee):
        emp = Employee(
            id=fake.random_int(),
            first_name=fake.first_name_male(),
            last_name=fake.last_name_male(),
            telegram_id=fake.random_int(),
            status=status,
            departament=dep,
            role=worker_role,
        )
        dep.add_employee(emp)
        expected_emp.add(emp)

    manager_wiht_out_permisson = Employee(
        id=fake.random_int(),
        first_name=fake.first_name_male(),
        last_name=fake.last_name_male(),
        status=status,
        departament=dep,
        telegram_id=fake.random_int(),
        role=manager_role,
    )
    with pytest.raises(
        EmployeePermissonError,
        match=str(manager_wiht_out_permisson),
    ):
        dep.get_employees(manager_wiht_out_permisson)
