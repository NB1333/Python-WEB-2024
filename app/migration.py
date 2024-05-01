import sqlite3
from sqlalchemy.orm import sessionmaker
from models import User, Account, Transaction
from database import engine

# Connect to SQLite
sqlite_connection = sqlite3.connect('./financial_exchange.db')
sqlite_cursor = sqlite_connection.cursor()

# Fetch data
sqlite_cursor.execute("SELECT * FROM users")
users_data = sqlite_cursor.fetchall()

sqlite_cursor.execute("SELECT * FROM accounts")
accounts_data = sqlite_cursor.fetchall()

sqlite_cursor.execute("SELECT * FROM transactions")
transactions_data = sqlite_cursor.fetchall()

# Set up a session for PostgreSQL
PostgreSQL_Session = sessionmaker(bind=engine)
db_session = PostgreSQL_Session()

# Migrate Users
for user in users_data:
    # Assuming User model has attributes id, username, hashed_password, and is_admin
    new_user = User(id=user[0], username=user[1], hashed_password=user[2], is_admin=user[3])
    db_session.add(new_user)

# Migrate Accounts
for account in accounts_data:
    # Assuming Account model has attributes id, user_id, balance
    new_account = Account(id=account[0], user_id=account[1], balance=account[2])
    db_session.add(new_account)

# Migrate Transactions
for transaction in transactions_data:
    # Assuming Transaction model has attributes id, account_id, amount
    new_transaction = Transaction(id=transaction[0], account_id=transaction[1], amount=transaction[2])
    db_session.add(new_transaction)

db_session.commit()

# Close sessions and connections to clean up
db_session.close()
sqlite_cursor.close()
sqlite_connection.close()
