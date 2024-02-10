import abc
from typing import TypeVar

from src.employee.domain.model import Employee

T = TypeVar("T")


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, model):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, model: T, model_id: int) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    def get_employee_by_tg_id(self, tg_id: int) -> Employee:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, model):
        self.session.add(model)

    def get(self, model, model_id):
        return self.session.query(model).filter_by(id=model_id).one()

    def get_employee_by_tg_id(self, tg_id):
        return self.session.query(Employee).filter_by(tg_id=tg_id).one()
