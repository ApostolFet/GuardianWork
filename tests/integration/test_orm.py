from sqlalchemy import text
from src.employee.domain import model


def test_roles_mapper_can_load_roles(session):
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


def test_roles_mapper_can_save_roles(session):
    role_title = "Управляющий"
    new_line = model.Role(role_title)
    session.add(new_line)
    session.commit()

    rows = list(session.execute(text('SELECT title FROM "roles"')))
    assert rows == [(role_title,)]
