from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

username = "root"
password = ""

dbURL = f"mysql+pymysql://{username}:{password}@localhost:3306/attendifai_db"
engine = create_engine(dbURL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
