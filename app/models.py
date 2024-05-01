from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, create_engine
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    accounts = relationship("Account", back_populates="user")

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    balance = Column(Float, default=0.0)
    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    amount = Column(Float)
    account = relationship("Account", back_populates="transactions")


# def create_database():
#     engine = create_engine('sqlite:///./financial_exchange.db', echo=True)
#     Base.metadata.create_all(engine)

# if __name__ == "__main__":
#     create_database()

# from sqlalchemy.orm import sessionmaker

# def populate_data():
#     engine = create_engine('sqlite:///./financial_exchange.db', echo=True)
#     Session = sessionmaker(bind=engine)
#     session = Session()

#     # Creating sample users
#     user1 = User(username='john_doe', hashed_password='hashedpassword123', is_admin=False)
#     user2 = User(username='admin_user', hashed_password='secureadminpass', is_admin=True)
#     session.add_all([user1, user2])

#     # Commit to save the new users
#     session.commit()

#     # Creating accounts linked to the users
#     account1 = Account(user_id=user1.id, balance=1000.0)
#     account2 = Account(user_id=user2.id, balance=5000.0)
#     session.add_all([account1, account2])

#     # Commit accounts
#     session.commit()

#     # Creating transactions
#     transaction1 = Transaction(account_id=account1.id, amount=150.0)
#     transaction2 = Transaction(account_id=account2.id, amount=-200.0)
#     session.add_all([transaction1, transaction2])

#     # Final commit
#     session.commit()
#     session.close()

# if __name__ == "__main__":
#     create_database()
#     populate_data()
