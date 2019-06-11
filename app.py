import json
from flask import Flask, render_template, request, jsonify, redirect, session, abort, flash
from functools import wraps
from hashlib import sha256

# local files
from models import User
from settings import app, db


def login_required(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        print(session)
        if "user" in session:
            return function(*args, **kwargs)
        return redirect("/login")
    
    return wrap

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if not session.get("user"):
            return render_template("generic_form.html", fields=User.login_fields(), action_url="/login/")
        else:
            return redirect("/")

    elif request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user:
            print(user)
            if user.password == sha256(str(request.form["password"]).encode()).hexdigest():
                session["user"] = user.serialize()  
                return redirect("/")
            else:
                return render_template("generic_form.html", fields=User.login_fields(), action_url="/login/", errors=["Username and password do not match!"])
        return render_template("generic_form.html", fields=User.login_fields(), action_url="/login/", errors=["User does not exist!"])


@app.route("/logout/", methods=["GET"])
@login_required
def logout():
    session.pop("user", None)
    return redirect("/")



def token_required(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        print(session)
        if request.headers.get("auth_token") and request.headers["auth_token"] != "":
            user = User.query.filter_by(auth_token=request.headers["auth_token"]).first()
            if user:
                return function(*args, **kwargs)
        
        return jsonify({"message": "Token invalid"})
    
    return wrap

@app.route("/api/login/", methods=["POST"])
def api_login():
    data = json.loads(request.data)
    def data_validator(data):
        username = data.get("username") or ""
        password = data.get("password") or ""
        return locals()
    valid_data = data_validator(data)
    print(valid_data)

    user = User.query.filter_by(username=valid_data["username"]).first()

    if user:
        print(user)
        if user.password == sha256(str(valid_data["password"]).encode()).hexdigest():
            return jsonify({ "token": user.obtain_auth_token() })
        else:
            return jsonify({"message": "Username and password do not match!"})

    return jsonify({"message": "User does not exist!"})


@app.route("/api/logout/", methods=["GET"])
@token_required
def api_logout():
    user = User.query.filter_by(auth_token=request.headers["auth_token"]).first()
    user.clear_auth_token()
    return jsonify({ "message": "Logged out" })






@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html")

@app.route("/update/", methods=["POST"])
@login_required
def update():
    return jsonify({"message": "update"})


@app.route("/api/", methods=["GET"])
@token_required
def api_index():
    return jsonify({"message": "api view"})

@app.route("/api/update/", methods=["POST"])
@token_required
def api_update():
    return jsonify({"message": "api update"})



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
