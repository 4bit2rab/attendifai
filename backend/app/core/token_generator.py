from jose import jwt
from fastapi import Header, HTTPException

SECRET_KEY = "hackathon-secret"
ALGORITHM = "HS256"

def create_employee_token(employee_id: int):

    to_encode = {"employee_id": employee_id}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt







 
 

 