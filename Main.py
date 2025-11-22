from flask import Flask, render_template, jsonify, redirect, url_for
from PetLogic import pet
from PetLogic import petFood
import threading
import pdb

# for redis as login session for flask
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_session import Session
import redis

# import db query functions
from DB import mainQuery as db


# Configures Flask app and login manager
loginManager = LoginManager()
app = Flask(__name__)
app.secret_key = "SuperSecretKey"
loginManager.init_app(app)

# Configure Redis session
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.Redis(host='localhost', port=6379, db=0)
Session(app) # applies the change to Flask app from above


# set up for pet logic

pet = pet.Pet()
#set  up threadiung for pet logic
petLogicThread = threading.Thread(target=pet.runPet)
# Optional: make it a daemon thread so it stops when the main program exits
petLogicThread.daemon = True

# starts the flask app
def webStart():
    app.run()
    
@app.route('/')
def startPage():
    return render_template('home.html')

@app.route('/hunger', methods=["GET"])
def getHunger():
    data = {"hunger": pet.getHunger()} # gets data
    return jsonify(data)

@app.route("/hunger", methods=["POST"])
def addHunger():
    pet.feed()
    return jsonify({"message":"Pet Fed!"})

@app.route('/happiness', methods=["GET"])
def getHappiness():
    data = {"happiness": pet.getHappiness()} # gets data
    return jsonify(data)

@app.route('/happiness', methods=["POST"])
def play():
    pet.play()
    return jsonify({"message":"pet is played with!"})

@app.route('/sleepiness', methods=["GET"])
def getSleepiness():
    data = {"sleepiness":pet.getSleep()}
    return jsonify(data)

@app.route("/sleepiness", methods=["PUT"])
def sleep():
    pet.ToggleSleep()
    return jsonify({"message":"pet is asleep"})

class User(UserMixin):
    def __init__(self, user):
        self.id = user

@loginManager.user_loader()
def loadUser(user):
    if db.checkUser(user):
        return User(user)

@app.route("/login", methods=["POST", "GET"])
def login():
    return redirect(url_for("homepage"))   

if __name__ == "__main__":
    petLogicThread.start()
    webStart()
    