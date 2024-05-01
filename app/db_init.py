# from sqlalchemy.orm import Session

# def populate_data(session: Session):
#     # Create some users
#     user1 = User(username='john_doe', hashed_password='hashedpassword1234', is_admin=False)
#     user2 = User(username='admin_user', hashed_password='secureadminpass', is_admin=True)

#     # Add users to the session
#     session.add(user1)
#     session.add(user2)

#     # Commit to save the new users
#     session.commit()

#     # Create accounts linked to users
#     account1 = Account(user_id=user1.id, balance=1000.0)
#     account2 = Account(user_id=user2.id, balance=5000.0)

#     # Add accounts
#     session.add(account1)
#     session.add(account2)

#     # Commit accounts
#     session.commit()

#     # Create transactions
#     transaction1 = Transaction(account_id=account1.id, amount=150.0)
#     transaction2 = Transaction(account_id=account2.id, amount=-200.0)

#     # Add transactions
#     session.add(transaction1)
#     session.add(transaction2)

#     # Final commit
#     session.commit()

# # Example usage
# if __name__ == "__main__":
#     db_url = 'sqlite:///./financial_exchange.db'
#     engine = create_engine(db_url, echo=True)
#     SessionLocal = sessionmaker(bind=engine)
#     with SessionLocal() as session:
#         populate_data(session)
