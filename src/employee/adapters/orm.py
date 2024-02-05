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
    select,
    and_,
)
from sqlalchemy.orm import registry, relationship

from src.employee.domain import model

logger = logging.getLogger(__name__)

mapper_registry = registry()

departaments = Table(
    "departaments",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("parent_id", Integer, ForeignKey("departaments.id"), nullable=True),
    Column("title", String(255), nullable=False),
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
    Column("status_id", Integer, ForeignKey("statuses.id"), nullable=True),
)

managers_departaments = Table(
    "managers_departaments",
    mapper_registry.metadata,
    Column("departament_id", ForeignKey("departaments.id"), primary_key=True),
    Column("employee_id", ForeignKey("employees.id"), primary_key=True),
)

availible_statuses = Table(
    "availible_statuses",
    mapper_registry.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("status_id", ForeignKey("statuses.id"), primary_key=True),
    Column("availible_status_id", ForeignKey("statuses.id"), primary_key=True),
)


def start_mappers(bind):
    logger.info("Start mapping")
    dep_mapper = mapper_registry.map_imperatively(
        model.Departament,
        departaments,
        properties={
            "_managers": relationship(
                model.Employee,
                secondary=managers_departaments,
                collection_class=set,
            ),
            "_child_departments": relationship(
                model.Departament,
                collection_class=set,
            ),
            "_employees": relationship(
                model.Employee,
                collection_class=set,
                back_populates="departament",
                primaryjoin="model.Departament.id == model.Employee.departament_id",
            ),
        },
    )

    role_mapper = mapper_registry.map_imperatively(model.Role, roles)

    status_mapper = mapper_registry.map_imperatively(model.Status, statuses)

    history_status_mapper = mapper_registry.map_imperatively(
        model.HistoryStatus,
        history_status,
        properties={"status": relationship(status_mapper)},
    )

    availible_statuses_mapper = mapper_registry.map_imperatively(
        model.AvailibleStatus,
        availible_statuses,
        properties={
            "role": relationship(role_mapper),
            "status": relationship(
                status_mapper,
                primaryjoin="model.AvailibleStatus.status_id == model.Status.id",
            ),
            "availible_status": relationship(
                status_mapper,
                primaryjoin="model.AvailibleStatus.availible_status_id == model.Status.id",
            ),
        },
    )

    mapper_registry.map_imperatively(
        model.Employee,
        employees,
        properties={
            "role": relationship(role_mapper),
            "departament": relationship(
                dep_mapper,
                back_populates="_employees",
                uselist=False,
                primaryjoin="model.Departament.id == model.Employee.departament_id",
            ),
            "_history_status": relationship(
                history_status_mapper,
                collection_class=list,
            ),
            "_availible_statuses": relationship(
                status_mapper,
                secondary=availible_statuses,
                secondaryjoin="and_(model.Employee.role_id == model.AvailibleStatus.role_id, model.Employee.status_id == model.AvailibleStatus.status_id)",
                primaryjoin="model.AvailibleStatus.status_id == model.Status.id",
                collection_class=set,
                viewonly=True,
            ),
        },
    )
    # mapper_registry.metadata.drop_all(bind, checkfirst=False)
    mapper_registry.metadata.create_all(bind)
    return True
