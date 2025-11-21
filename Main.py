from flask import Flask, render_template, jsonify
from PetLogic import pet
from PetLogic import petFood
import threading
import pdb
from flask_login import LoginManager, UserMixin as User

# Configures Flask app and login manager
loginManager = LoginManager()
app = Flask(__name__)
app.secret_key = "ndoiasdjaoisdj"
loginManager.init_app(app)



pet = pet.Pet()



#set  up threadiung for pet logic
petLogicThread = threading.Thread(target=pet.runPet)
# Optional: make it a daemon thread so it stops when the main program exits
petLogicThread.daemon = True

# starts the flask app
def webStart():
    app.run()
    
# user fall back for login
@loginManager.user_loader
def loadUser(userID):
    return User.get(userID)
    


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

if __name__ == "__main__":
    petLogicThread.start()
    webStart()
    