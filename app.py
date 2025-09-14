from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import datetime
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.remember_cookie_duration = datetime.timedelta(days=365)  # keep logged in for 1 year

USERS_FILE = "users.txt"
ALERTS_FILE = "alerts.txt"

# ---------------------------
# User Class
# ---------------------------
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

# ---------------------------
# Ensure demo account exists
# ---------------------------
def ensure_demo_user():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            f.write("demo|demo123|user\n")  # create file with demo user
        return

    # Check if demo user exists
    with open(USERS_FILE, "r") as f:
        users = [line.strip().split("|")[0] for line in f if line.strip()]

    if "demo" not in users:
        with open(USERS_FILE, "a") as f:
            f.write("demo|demo123|user\n")

# Run this at startup
ensure_demo_user()

# ---------------------------
# Flask-Login user loader
# ---------------------------
@login_manager.user_loader
def load_user(user_id):
    try:
        with open(USERS_FILE, "r") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                username, password, role = line.strip().split("|")
                if str(i) == user_id:
                    return User(id=i, username=username, role=role)
    except FileNotFoundError:
        return None
    return None

# ---------------------------
# Alerts helpers
# ---------------------------
def read_alerts():
    alerts = []
    if not os.path.exists(ALERTS_FILE):
        return alerts
    with open(ALERTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 4:
                timestamp, message, status, sender = parts
                alerts.append({"timestamp": timestamp, "message": message, "status": status, "user": sender})
    return alerts

def save_alerts(alerts):
    with open(ALERTS_FILE, "w", encoding="utf-8") as f:
        for alert in alerts:
            f.write(f"{alert['timestamp']}|{alert['message']}|{alert['status']}|{alert['user']}\n")

# ---------------------------
# Routes
# ---------------------------
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    alerts = read_alerts()
    if request.method == "POST":
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = "Emergency alert sent to authorities!"
        sender = current_user.username
        alerts.append({"timestamp": timestamp, "message": message, "status": "Pending", "user": sender})
        save_alerts(alerts)
        flash("🚨 Emergency alert sent! Authorities will investigate.")
        return redirect(url_for("index"))
    # Reverse alerts to show newest first
    alerts = list(reversed(alerts))
    return render_template("index.html", alerts=alerts, user=current_user)

@app.route("/mark/<int:index>/<status>")
@login_required
def mark_alert(index, status):
    alerts = read_alerts()
    if 0 <= index < len(alerts):
        real_index = len(alerts) - 1 - index
        alerts[real_index]["status"] = status
        save_alerts(alerts)
        flash(f"Alert #{index+1} marked {status}.")
    return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            with open(USERS_FILE, "r") as f:
                for i, line in enumerate(f.readlines()):
                    u, p, role = line.strip().split("|")
                    if username == u and password == p:
                        user = User(id=i, username=u, role=role)
                        login_user(user, remember=True)
                        return redirect(url_for("index"))
        except FileNotFoundError:
            flash("Users file not found!")
            return redirect(url_for("login"))
        flash("Invalid credentials")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
