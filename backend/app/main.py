from fastapi import FastAPI
from app.dbConfig.mysqlConfig import Base, engine
from app.api.employee_routes import router as employee_router
from app.api.token_routes import router as token_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(employee_router)
app.include_router(token_router)

    