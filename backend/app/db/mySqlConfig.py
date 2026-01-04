from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")
print(DATABASE_URL)

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")
# dbURL = "mysql+pymysql://root:India%402023@localhost:3306/attendifai_db"
engine = create_engine(DATABASE_URL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()