from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


# dbURL = "mysql+pymysql://root:India%402023@localhost:3306/attendifai_db"
dbURL = "mysql+pymysql://root:bs1234@localhost:3306/attendifai_db"
engine = create_engine(dbURL)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()