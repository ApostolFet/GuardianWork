import abc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from src import settings
from src.employee.adapters import repository


class AbstractEmployeesUnitOfWork(abc.ABC):
    employees: repository.AbstractEmployeeRepository

    def __enter__(self) -> "AbstractEmployeesUnitOfWork":
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class AbstractDepartamentUnitOfWork(abc.ABC):
    departaments: repository.AbstractDepartamentRepository

    def __enter__(self) -> "AbstractDepartamentUnitOfWork":
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        settings.get_db_uri(),
        isolation_level="REPEATABLE READ",
    )
)


class SqlAlchemyEmployeeUnitOfWork(AbstractEmployeesUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()  # type: Session
        self.employees = repository.SqlAlchemyEmployeeRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class SqlAlchemyDepartamentUnitOfWork(AbstractDepartamentUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()  # type: Session
        self.departaments = repository.SqlAlchemyDepartamentRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
