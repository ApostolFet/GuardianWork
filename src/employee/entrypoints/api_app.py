from fastapi import APIRouter

from pydantic import BaseModel

from src.employee.service_layer.services import add_employee, add_manager_departament
from src.employee.service_layer.unit_of_work import SqlAlchemyUnitOfWork

employee_router = APIRouter(
    prefix="/employees",
    tags=["employees"],
)


class EmployeeShema(BaseModel):
    first_name: str
    last_name: str
    tg_id: int
    role_id: int
    departament_id: int


class AddManagerDepartamentShema(BaseModel):
    departament_id: int
    employee_id: int


class StatusShema(BaseModel):
    status: str


@employee_router.post("")
async def register(employee: EmployeeShema) -> int:
    employee_id = add_employee(
        employee.first_name,
        employee.last_name,
        employee.tg_id,
        employee.role_id,
        employee.departament_id,
        uow=SqlAlchemyUnitOfWork(),
    )
    return employee_id


@employee_router.post("/departament/manager")
async def register_manager_departament(data: AddManagerDepartamentShema):
    add_manager_departament(
        data.departament_id,
        data.employee_id,
        uow=SqlAlchemyUnitOfWork(),
    )
    return StatusShema(status="success")
