from sqlalchemy import Column, Integer, String
from app.dbConfig.mysqlConfig import Base
import uuid

class Employee(Base):
    __tablename__ = "employee"

    employee_id = Column(String(50), primary_key=True, index=True, default= lambda: str(uuid.uuid4()))
    employee_name = Column(String(100), index=True)
    employee_email = Column(String(100), unique=True, index=True)