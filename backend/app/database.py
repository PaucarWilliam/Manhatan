from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./pizzeria.db"

#Conexión librería SQL y BD
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

#Sesión de BD
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

#Tablas heredan esto y serán administradas por ORM
class Base(DeclarativeBase):
    pass
