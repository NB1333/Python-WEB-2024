# import psycopg
# from psycopg_pool import ConnectionPool

# # Connection URI
# DATABASE_URL = "postgresql://myuser:mypassword@localhost:5433/financial_exchange"

# # Create a connection pool
# conn_pool = ConnectionPool(DATABASE_URL)

from pymongo import MongoClient

# MongoDB connection string
MONGO_URL = "mongodb://localhost:27017"
client = MongoClient(MONGO_URL)

# Access database
db = client['financial_exchange']

sequence_collection = db.sequences  # This holds sequence counters for various document types

# Access collections
users = db.users
accounts = db.accounts
transactions = db.transactions
