"""add column manager id to departament

Revision ID: 1f1d7e173060
Revises: 3c107bbdbf21
Create Date: 2024-02-03 22:34:56.991145

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1f1d7e173060"
down_revision: Union[str, None] = "3c107bbdbf21"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "departaments",
        sa.Column(
            "manager_id", sa.Integer, sa.ForeignKey("employees.id"), nullable=True
        ),
    )


def downgrade() -> None:
    op.drop_column("departaments", "manager_id")
