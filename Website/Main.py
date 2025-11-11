from flask import Flask, render_template, jsonify
from PetLogic import logic
import threading
import pdb

#Starts flask application which allows integration of html data to python data and vice versa
app = Flask(__name__)

pet = logic.Pet()
#set  up threadiung for pet logic
petLogicThread = threading.Thread(target=pet.runPet)
# Optional: make it a daemon thread so it stops when the main program exits
petLogicThread.daemon = True

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
    pet.sleep()
    return jsonify({"message":"pet is asleep"})

if __name__ == "__main__":
    petLogicThread.start()
    webStart()
    