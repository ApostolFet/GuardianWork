from fastapi import FastAPI

from sqlalchemy import create_engine


from src.employee.entrypoints.api_app import employee_router

from src.settings import get_db_uri
from src.employee.adapters import orm


db_engine = create_engine(get_db_uri())
orm.mapper_registry.metadata.create_all(bind=db_engine)
orm.start_mappers()


app = FastAPI(title="GuardianWork", version="0.1.0")

app.include_router(employee_router)
