import logging
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Table,
    Column,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import registry, relationship

from src.employee.domain import model

logger = logging.getLogger(__name__)

mapper_registry = registry()

departaments = Table(
    "departaments",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), nullable=False),
    Column("manager_id", Integer, ForeignKey("employees.id"), nullable=True),
)

roles = Table(
    "roles",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), nullable=False),
)

statuses = Table(
    "statuses",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("is_working", Boolean, nullable=False),
)

history_status = Table(
    "history_status",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("status_id", Integer, ForeignKey("statuses.id")),
    Column("employee_id", Integer, ForeignKey("employees.id")),
    Column("set_at", DateTime, default=func.now()),
)

employees = Table(
    "employees",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("tg_id", Integer),
    Column("first_name", String(255), nullable=False),
    Column("last_name", String(255), nullable=False),
    Column("departament_id", Integer, ForeignKey("departaments.id")),
    Column("role_id", Integer, ForeignKey("roles.id"), nullable=False),
)


def start_mappers(bind):
    logger.info("Start mapping")
    dep_mapper = mapper_registry.map_imperatively(
        model.Departament,
        departaments,
        properties={"manager": relationship("employees", back_populates="departament")},
    )

    role_mapper = mapper_registry.map_imperatively(model.Role, roles)

    status_mapper = mapper_registry.map_imperatively(model.Status, statuses)

    history_status_mapper = mapper_registry.map_imperatively(
        model.HistoryStatus,
        history_status,
        properties={"status": relationship(status_mapper)},
    )

    mapper_registry.map_imperatively(
        model.Employee,
        employees,
        properties={
            "role": relationship(role_mapper),
            "departament": relationship(dep_mapper, back_populates="manager"),
            "_history_status": relationship(
                history_status_mapper,
                collection_class=list,
            ),
        },
    )
    mapper_registry.metadata.drop_all(bind)
    mapper_registry.metadata.create_all(bind)
