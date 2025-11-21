from flask import Flask, render_template_string, redirect, url_for, request, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_session import Session
import redis

# postresSQL 
import psycopg2


conn = psycopg2.connect(
    host="localhost",
    port = "1234",
    dbname="digital pet",
    user="postgres",
    password="Oscarsgyang123"
)

cur = conn.cursor()

def checkUser(username, password):
    query = "SELECT * FROM Users WHERE username = %s AND password = %s"
    cur.execute(query, (username, password))
    
    if cur.fetchone():
        return True
    return False

def registerUser(username, password):
    
    print("registering user")
    query = "INSERT INTO Users (username, password) VALUES (%s, %s)"
    
    cur.execute(query, (username, password))
    conn.commit() # saves the execution

app = Flask(__name__)
# Secret key for signing sessions
app.secret_key = "supersecretkey"
# Dummy user store
USERS = {"admin": "password123"}

# Configure Redis session
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.Redis(host='localhost', port=6379, db=0)

# Initialize session
Session(app)

# Dummy user store
USERS = {"admin": {"password": "password123"}}

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def loadUser(username):
    if checkUser(username):
        return User(username)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # authenticate from our mock database
        if checkUser(username, password):
            user = User(username)
            login_user(user)  # stores user ID in session (Redis)
            return redirect(url_for("dashboard"))
        
        return "Invalid username or password"

    return render_template_string("""
        <form method="POST">
            <input name="username" placeholder="Username">
            <input name="password" placeholder="Password" type="password">
            <button type="submit">Login</button>
        </form>
    """)


@app.route("/dashboard")
@login_required
def dashboard():
    return f"Welcome {current_user.id}! <br><a href='/logout'>Logout</a>"



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
    cur.close()
    conn.close()