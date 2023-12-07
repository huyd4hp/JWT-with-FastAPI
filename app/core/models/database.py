from sqlalchemy import Column, Integer, String, Enum, ForeignKey
import sqlalchemy
from sqlalchemy.orm import relationship, DeclarativeBase
import enum
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.exc import SQLAlchemyError


class Base(DeclarativeBase):
    pass


class RoleEnum(enum.Enum):
    Manager = "Manager"
    Staff = "Staff"
    Customer = "Customer"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(256))
    email = Column(
        String(50),
        unique=True,
    )
    role = Column(
        Enum(RoleEnum),
        default="Customer",
    )

    def json(self):
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "role": self.role,
        }


load_dotenv()
DATABASE_CONFIG = {
    "USER": os.getenv("MYSQL_USER"),
    "PASSWORD": os.getenv("MYSQL_PASSWORD"),
    "HOST": os.getenv("MYSQL_HOST"),
    "PORT": os.getenv("MYSQL_PORT"),
    "DATABASE": os.getenv("MYSQL_DATABASE"),
}

USER = DATABASE_CONFIG["USER"]
PASSWORD = DATABASE_CONFIG["PASSWORD"]
HOST = DATABASE_CONFIG["HOST"]
PORT = DATABASE_CONFIG["PORT"]
DATABASE = DATABASE_CONFIG["DATABASE"]

engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")


def initialDatabase():
    try:
        engine.connect()
        print("DATABASE is running")
        lstTable = sqlalchemy.inspect(engine).get_table_names()
        if len(lstTable) == 0:
            Base.metadata.create_all(engine)
    except SQLAlchemyError as error:
        raise (error)
