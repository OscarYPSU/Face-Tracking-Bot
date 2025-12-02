# postresSQL 
from psycopg2.pool import ThreadedConnectionPool

connPool = ThreadedConnectionPool(
    minconn=5,
    maxconn=20,
    host="localhost",
    port = "1234",
    dbname="digital pet",
    user="postgres",
    password="Oscarsgyang123"
)


from contextlib import contextmanager
@contextmanager
def getConn():
    conn = connPool.getconn()
    try:
        yield conn
    finally:
        connPool.putconn(conn)