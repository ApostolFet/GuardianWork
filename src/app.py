from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


from src import settings
from src.employee.domain import model
from src.employee.adapters import orm

load_dotenv()

db_engine = create_engine(settings.get_db_uri())
orm.mapper_registry.metadata.create_all(bind=db_engine)
get_session = sessionmaker(bind=db_engine)
orm.start_mappers()


def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


session = get_session()
dep = model.Departament("Офис")
session.add(dep)
role = model.Role("Програмист")
session.add(role)

start_status = model.Status("start", is_working=False)
emp = model.Employee("Maxim", "Ageev", 123456, role, dep, start_status)
session.add(emp)

work = model.Status("work", is_working=True)
session.add(work)
end_status = model.Status("end", is_working=True)
session.add(end_status)

emp._availible_statuses = set([start_status, work, end_status])

availible_statuses = emp.get_available_statuses()

for status in availible_statuses:
    emp.status = status
    assert status == emp.status
assert len(availible_statuses) == len(emp._history_status)
session.commit()
