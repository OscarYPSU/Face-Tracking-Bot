# postresSQL 
import psycopg2
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

def checkUser(username, password):
    query = "SELECT * FROM Users WHERE username = %s AND password = %s"
    with getConn() as conn:
        cur = conn.cursor()
        cur.execute(query, (username, password))
        
        if cur.fetchone():
            return True
        return False

def checkUsername(username):
    query = "SELECT * FROM Users WHERE username = %s"
    with getConn() as conn:
        cur = conn.cursor()
        cur.execute(query, (username,))
        if cur.fetchone():
            return True 
        return False

def registerUser(username, password):
    print("registering user")
    query = "INSERT INTO Users (username, password) VALUES (%s, %s)"
    
    with getConn() as conn:
        cur = conn.cursor()
        cur.execute(query, (username, password))
        conn.commit() # saves the execution


    
    
