from models import Base, User, Account, Transaction
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "postgresql://myuser:mypassword@localhost:5433/financial_exchange"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

Base.metadata.create_all(engine)
