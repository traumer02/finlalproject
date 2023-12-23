from sqlalchemy import Column, DATETIME, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from config import PostgresConfig

Base = declarative_base()
username = PostgresConfig.POSTGRES_LOGIN
password = PostgresConfig.POSTGRES_PASSWORD
host = PostgresConfig.POSTGRES_HOST
port = PostgresConfig.POSTGRES_PORT
db = PostgresConfig.POSTGRES_DATABASE
engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{db}')


class DB:
    session = None

    def __init__(self):
        if DB.session:
            raise Exception("This class is a singleton!")
        else:
            Session_: Session = sessionmaker(bind=engine)
            self.session: Session = Session_()


class Model(Base):
    __tablename__ = 'nypd'

    fullname = Column(String, nullable=False, primary_key=True)
    rank = Column(String)
    precinct = Column(String)
    appearance = Column(String)
    link = Column(String)


if __name__ == "__main__":
    db = DB().session.is_active
    print(db)
