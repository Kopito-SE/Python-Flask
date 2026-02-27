from flask import Flask, render_template, request,redirect, url_for,session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"
users = {}


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Username and pasword are required!") 
            return redirect(url_for("register"))
        
        hashed_password = generate_password_hash(password)
        users[username] = hashed_password
        flash("Registration successful!")
        return redirect(url_for("login"))
    return render_template("register.html")
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            flash("Username and password are required!")
            return redirect(url_for("login"))

        if username in users and check_password_hash(users[username], password):
            session['user'] = username 
            flash("Login successful!")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials!")
            return redirect(url_for("login"))
    return render_template("login.html")
    
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("Please login first to access content!")
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session['user'])
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out!")
    return redirect(url_for("login"))
if __name__ == "__main__":
    app.run(debug=True)