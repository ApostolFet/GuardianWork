import abc

from src.employee.domain import model


class AbstractEmployeeRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, employee: model.Employee):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, tg_id: int) -> model.Employee:
        raise NotImplementedError


class AbstractDepartamentRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, departament: model.Departament):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, manager_id: int) -> list[model.Departament]:
        raise NotImplementedError


class SqlAlchemyEmployeeRepository(AbstractEmployeeRepository):
    def __init__(self, session):
        self.session = session

    def add(self, employee):
        self.session.add(employee)

    def get(self, tg_id):
        return self.session.query(model.Employee).filter_by(tg_id=tg_id).one()


class SqlAlchemyDepartamentRepository(AbstractDepartamentRepository):
    def __init__(self, session):
        self.session = session

    def add(self, departament):
        self.session.add(departament)

    def get(self, manager_id):
        return (
            self.session.query(model.Departament).filter_by(manager_id=manager_id).all()
        )
