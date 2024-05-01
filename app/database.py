import psycopg
from psycopg_pool import ConnectionPool

# Connection URI
DATABASE_URL = "postgresql://myuser:mypassword@localhost:5433/financial_exchange"

# Create a connection pool
conn_pool = ConnectionPool(DATABASE_URL)
