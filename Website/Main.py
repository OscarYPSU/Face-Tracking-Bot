from flask import Flask, render_template, jsonify
from PetLogic import logic
import threading

#Starts flask application which allows integration of html data to python data and vice versa
app = Flask(__name__)
    
#set  up threadiung for pet logic
petLogicThread = threading.Thread(target=logic.runPet)
# Optional: make it a daemon thread so it stops when the main program exits
petLogicThread.daemon = True

def webStart():
    app.run()
    

@app.route('/')
def startPage():
    return render_template('home.html')

@app.route('/getHunger')
def getHunger():
    data = {"hunger": logic.getHunger()} # gets data
    
    return jsonify(data)

if __name__ == "__main__":
    petLogicThread.start()
    webStart()
    