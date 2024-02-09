from sqlalchemy import text
from src.employee.domain import model


def test_mapper_can_load_roles(session):
    session.execute(
        text(
            "INSERT INTO roles (title) VALUES "
            '("Управляющий"),'
            '("Менеджер"),'
            '("Сотрудник")'
        )
    )
    expected = [
        model.Role("Управляющий"),
        model.Role("Менеджер"),
        model.Role("Сотрудник"),
    ]
    assert session.query(model.Role).all() == expected


def test_can_save_roles(session):
    role_title = "Управляющий"
    new_line = model.Role(role_title)
    session.add(new_line)
    session.commit()

    rows = list(session.execute(text('SELECT title FROM "roles"')))
    assert rows == [(role_title,)]


def test_can_load_statuses(session):
    session.execute(
        text(
            "INSERT INTO statuses (title, is_working) VALUES"
            '("Начать смену", 0),'
            '("Работаю", 1),'
            '("Закончить смену", 0)'
        )
    )
    expected = [
        model.Status("Начать смену", is_working=False),
        model.Status("Работаю", is_working=True),
        model.Status("Закончить смену", is_working=False),
    ]
    assert session.query(model.Status).all() == expected


def test_mapper_can_save_statuses(session):
    status_title = "Начать смену"
    is_working = False
    new_line = model.Status(status_title, is_working)
    session.add(new_line)
    session.commit()

    rows = list(session.execute(text('SELECT title, is_working FROM "statuses"')))
    assert rows == [(status_title, is_working)]


def test_mapper_can_load_departaments(session):
    session.execute(
        text(
            "INSERT INTO departaments (title, parent_id) VALUES"
            '("Организация", null),'
            '("Склад", 1),'
            '("Продажи", 1)'
        )
    )

    org = model.Departament("Организация", 1)
    sklad = model.Departament("Склад", 2)
    sale = model.Departament("Продажи", 3)
    org._child_departments = {sklad, sale}
    expected = [
        org,
        sklad,
        sale,
    ]
    assert session.query(model.Departament).all() == expected


def test_mapper_can_save_departaments(session):
    org = model.Departament("Организация", 1)
    session.add(org)
    sklad = model.Departament("Склад")
    sale = model.Departament("Продажи")
    org._child_departments = {sklad, sale}
    session.commit()

    rows = list(
        session.execute(text('SELECT id, title, parent_id FROM "departaments"'))
    )
    assert rows == [(1, "Организация", None), (2, "Склад", 1), (3, "Продажи", 1)]


def test_mapper_can_load_employees(session):
    session.execute(
        text("INSERT INTO statuses (title, is_working) VALUES" '("Начать смену", 0)')
    )

    session.execute(text("INSERT INTO roles (title) VALUES " '("Сотрудник")'))

    session.execute(text("INSERT INTO departaments (title) VALUES " '("Склад")'))

    session.execute(
        text(
            "INSERT INTO employees (tg_id, first_name, last_name, departament_id, role_id, status_id) VALUES"
            '(1, "Ivan", "Ivan",1, 1, 1)'
        )
    )
    start_status = model.Status("Начать смену", False)
    role = model.Role("Сотрудники")
    departament = model.Departament("Склад", 1)
    expected_employee = model.Employee(
        "Ivan", "Ivan", 1, role, departament, start_status, 1
    )

    employee = session.query(model.Employee).one()
    assert employee == expected_employee


def test_mapper_can_save_employees(session):
    start_status = model.Status("Начать смену", False)
    role = model.Role("Сотрудники")
    departament = model.Departament("Склад", 1)
    employee = model.Employee("Ivan", "Ivan", 1, role, departament, start_status, 1)
    session.add(employee)
    session.commit()

    rows = list(
        session.execute(
            text(
                'SELECT id, tg_id, first_name, last_name, departament_id, role_id, status_id FROM "employees"'
            )
        )
    )
    assert rows == [(1, 1, "Ivan", "Ivan", 1, 1, 1)]


def test_retrieving_availible_statuses(session):
    session.execute(
        text(
            "INSERT INTO statuses (title, is_working) VALUES"
            '("Начать смену", 0),'
            '("Работаю", 1),'
            '("Закончить смену", 0)'
        )
    )

    session.execute(text("INSERT INTO roles (title) VALUES " '("Сотрудник")'))

    session.execute(text("INSERT INTO departaments (title) VALUES " '("Склад")'))

    session.execute(
        text(
            "INSERT INTO employees (tg_id, first_name, last_name, departament_id, role_id, status_id) VALUES"
            '(1, "Ivan", "Ivan",1, 1, 1)'
        )
    )

    session.execute(
        text(
            "INSERT INTO availible_statuses (role_id, status_id, availible_status_id) VALUES"
            "(1, 1, 2),"
            "(1, 1, 3),"
            "(1, 2, 3),"
            "(1, 3, 1)"
        )
    )

    start_status = model.Status("Начать смену", False)
    working_status = model.Status("Работаю", True)
    end_status = model.Status("Закончить смену", False)

    employee = session.query(model.Employee).one()
    assert employee._availible_statuses == {working_status, end_status}

    session.execute(text("UPDATE employees  SET status_id = 2 WHERE id = 1"))
    session.commit()

    assert employee._availible_statuses == {end_status}

    session.execute(text("UPDATE employees SET status_id = 3 WHERE id = 1"))
    session.commit()

    assert employee._availible_statuses == {start_status}
