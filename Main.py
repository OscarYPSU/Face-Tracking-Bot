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
from DB import authenticationQuery as authy


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
    data = {"hunger": userPet.getHunger()} # gets data
    return jsonify(data)

@app.route("/hunger", methods=["POST"])
def addHunger():
    pet.feed()
    return jsonify({"message":"Pet Fed!"})

@app.route('/happiness', methods=["GET"])
def getHappiness():
    data = {"happiness": userPet.getHappiness()} # gets data
    return jsonify(data)

@app.route('/happiness', methods=["POST"])
def play():
    pet.play()
    return jsonify({"message":"pet is played with!"})

@app.route('/sleepiness', methods=["GET"])
def getSleepiness():
    data = {"sleepiness":userPet.getSleep()}
    return jsonify(data)

@app.route("/sleepiness", methods=["PUT"])
def sleep():
    userPet.ToggleSleep()
    return jsonify({"message":"pet is asleep"})

# Flask friendly User class to store user data for server side cache
class User(UserMixin):
    def __init__(self, user):
        self.id = user
        self.user = user

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
            
            # set up for pet logic
            userPet = pet.Pet(username)
            #set  up threadiung for pet logic
            petLogicThread = threading.Thread(target=userPet.runPet)
            # Optional: make it a daemon thread so it stops when the main program exits
            petLogicThread.daemon = True
            # Starts the pet mechanics in the background in a multhread
            
            petLogicThread.start()
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

if __name__ == "__main__":
    webStart()
    
    
    logout()

    