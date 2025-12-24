from fastapi import Header, HTTPException, status
from jose import jwt, JWTError

SECRET_KEY = "hackathon-secret"
ALGORITHM = "HS256"

def get_employee_id_from_token(authorization: str = Header(...)) -> int:
    """
    Expects:
    Authorization: Bearer <token>
    """
    try:
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Authorization header"
            )

        token = authorization.split(" ")[1]

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        employee_id = payload.get("employee_id")
        if employee_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="employee_id missing in token"
            )

        return employee_id  # ✅ RETURN INT ONLY

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )   