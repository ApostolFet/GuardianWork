"""create init database structure

Revision ID: 3c107bbdbf21
Revises: 
Create Date: 2024-02-03 22:02:02.078755

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Column,
    Integer,
    String,
    func,
)

# revision identifiers, used by Alembic.
revision: str = "3c107bbdbf21"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "roles",
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("title", String(255), nullable=False),
    )

    op.create_table(
        "statuses",
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("is_working", Boolean, nullable=False),
    )

    op.create_table(
        "departaments",
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("title", String(255), nullable=False),
    )

    op.create_table(
        "employees",
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("tg_id", Integer),
        Column("first_name", String(255), nullable=False),
        Column("last_name", String(255), nullable=False),
        Column("departament_id", Integer, ForeignKey("departaments.id")),
        Column("role_id", Integer, ForeignKey("roles.id"), nullable=False),
    )

    op.create_table(
        "history_status",
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("status_id", Integer, ForeignKey("statuses.id")),
        Column("employee_id", Integer, ForeignKey("employees.id")),
        Column("set_at", DateTime, default=func.now()),
    )


def downgrade() -> None:
    op.drop_table("history_status")
    op.drop_table("employees")
    op.drop_table("departaments")
    op.drop_table("roles")
    op.drop_table("statuses")
