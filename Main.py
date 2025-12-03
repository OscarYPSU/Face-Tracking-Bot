from flask import Flask, render_template, jsonify, redirect, url_for, request
from PetLogic import pet
from PetLogic import petFood
import threading
import pdb

# for redis as login session for flask
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_session import Session
import redis

# import db query functions
from DB import authenticationQuery as authy, userDataQuery as DB


# Configures Flask app and login manager
loginManager = LoginManager()
app = Flask(__name__)
app.secret_key = "SuperSecretKey"
loginManager.init_app(app)
loginManager.login_view = "login"

# Configure Redis session
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.Redis(host='localhost', port=6379, db=0)
Session(app) # applies the change to Flask app from above

# Placeholder for user pet data
userPet = None

# starts the flask app
def webStart():
    app.run()

@app.route("/")
@login_required
def startup():
    return render_template('home.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/hunger', methods=["GET"])
def getHunger():
    data = {"hunger": current_user.userPet.getHunger()} # gets data
    return jsonify(data)

@app.route("/hunger", methods=["POST"])
def addHunger():
    current_user.userPet.feed()
    return jsonify({"message":"Pet Fed!"})

@app.route('/happiness', methods=["GET"])
def getHappiness():
    data = {"happiness": current_user.userPet.getHappiness()} # gets data
    return jsonify(data)

@app.route('/happiness', methods=["POST"])
def play():
    pecurrent_user.userPett.play()
    return jsonify({"message":"pet is played with!"})

@app.route('/sleepiness', methods=["GET"])
def getSleepiness():
    data = {"sleepiness":current_user.userPet.getSleep()}
    return jsonify(data)

@app.route("/sleepiness", methods=["PUT"])
def sleep():
    current_user.userPet.ToggleSleep()
    return jsonify({"message":"pet is asleep"})

# Flask friendly User class to store user data for server side cache
class User(UserMixin):
    def __init__(self, user):
        self.id = user
        self.user = user
        self.userPet = userPetDict[user]

# creates a Flask friendly User class for signed in User to be accessed for session management
@loginManager.user_loader
def loadUser(user):
    if authy.checkUsername(user):
        return User(user)

# login route, takes in username and password
@app.route("/login", methods=["POST", "GET"])
def login():
    global userPet
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        print("authenicating user for login\n")
        if authy.login(username, password):
            print("authentication success\n")
            user = User(username)
            login_user(user)  # stores user ID in session (Redis)
            return redirect(url_for("home"))
        else:
            print("authentication not sucess, user sent to register page\n")
            return redirect(url_for("register"))
    return render_template("login.html")

# Registers new user with username and password into postgreSQL 
@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if authy.register(username, password):
            return redirect(url_for("login"))
        else:
            return redirect(url_for("register"))

    return render_template("register.html")


# Deletes User server side session key
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

# for keeping track of individual user threads
userThread = {}
userPetDict = {}

def startThread():
    print("starting pet thread for user\n")
    
    # gets all username exisiting in DB
    datas = DB.getAllUsername()
    
    for row in datas:
        # set up for pet logic
        userPet = pet.Pet(row[0])
        petLogicThread = threading.Thread(target=userPet.runPet)
        # Optional: make it a daemon thread so it stops when the main program exits
        petLogicThread.daemon = True
        # Starts the pet mechanics in the background in a multhread
        petLogicThread.start()
        
        # stores data for record keeping
        userThread[row[0]] = petLogicThread
        userPetDict[row[0]] = userPet


if __name__ == "__main__":
    # starts thread for user pet mechanics
    startThread()
    
    webStart()

    logout()

    