from sqlalchemy import Column, Integer, String
from app.dbConfig.mysqlConfig import Base

class EmployeeToken(Base):
    __tablename__ = "employee_token"

    token = Column(String(255), primary_key=True, index=True)
    employee_id = Column(String(50), index=True)
    created_at = Column(String(100))