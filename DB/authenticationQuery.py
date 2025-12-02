# postresSQL 
import DB.connectionPool as connectionPool
import bcrypt
import DB.userDataQuery as userDataDB

def login(username, password):
    query = "SELECT * FROM public.\"Users\" WHERE username = %s"
    
    with connectionPool.getConn() as conn:
        cur = conn.cursor()
        cur.execute(query, (username,))
        dataFetched = cur.fetchone()
        if dataFetched:
            storedPassword = dataFetched[2]
            if bcrypt.checkpw(password.encode("utf-8"), storedPassword.encode("utf-8")):
                return True
        return False

def checkUsername(username):
    query = "SELECT * FROM public.\"Users\" WHERE username = %s"
    with connectionPool.getConn() as conn:
        cur = conn.cursor()
        cur.execute(query, (username,))
        if cur.fetchone():
            return True 
        return False

# return True if registered, False otherwise
def register(username, password):
    # Checks if username already exists or not
    if checkUsername(username):
        return False
    else:
        print("registering user")
        query = "INSERT INTO public.\"Users\" (username, password) VALUES (%s, %s) RETURNING id;" # Returning ID returns the created row ID to cursor to be fetched for creating user data 
        
        #encrypts the password first using bcrypt
        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        hashedPasswordString = hashedPassword.decode("utf-8")
        
        with connectionPool.getConn() as conn:
            cur = conn.cursor()
            cur.execute(query, (username, hashedPasswordString))
            userID = cur.fetchone()[0]
            
            # Log
            print(f"Creating user ID: {userID}\n")
            
            conn.commit() # saves the execution
        
        # creates user data in another table
        userDataDB.createUserData(userID, username)

        return True


