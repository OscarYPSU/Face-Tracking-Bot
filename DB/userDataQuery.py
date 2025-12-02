from DB.connectionPool import getConn

# intializes user data for their pet when they create an account
def createUserData(userID, username):
    
    # Log
    print("Creating user data\n")
    
    query = "INSERT INTO public.\"userdata\" (id, username, happiness, sleepiness,  hunger) VALUES (%s, %s, %s, %s, %s)"
    
    with getConn() as conn:
        cur = conn.cursor()
        cur.execute(query, (userID, username, 100, 0, 0))
        conn.commit()

def getAllUserPetData(username):
    
    # Log 
    print(f"fetching user pet data : {username}\n")
    
    query = "SELECT happiness, sleepiness, hunger FROM public.\"userdata\" WHERE username = %s"
    
    with getConn() as conn:
        cur = conn.cursor()
        cur.execute(query, (username,))
        
        data = cur.fetchone() # the return row of data
        happiness, sleepiness, hunger = data
        
        # Log
        print(f"Received user pet data = {data}\n")
        
        return {"happiness":happiness, "sleepiness":sleepiness, "hunger":hunger}

    return 

def updateUserPetData(username):
    return 