import requests
from flask import Flask, render_template, request, redirect, make_response, jsonify
import time
from models import User, db
import hashlib
import uuid

# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.

app = Flask(__name__)
db.create_all()


@app.route("/index", methods=["GET"])
@app.route("/", methods=["GET"])
def index():
    time_now = time.time()
    user_name = request.cookies.get("name")
    return render_template("index.html", trenutni_cas=time_now, name=user_name)


@app.route("/logout", methods=["POST"])
def logout():
    session_token = request.cookies.get("session_token")
    user = db.query(User).filter_by(session_token=session_token).first()

    user.session_token = ""
    db.add(user)
    db.commit()
    return redirect("index")


@app.route("/login", methods=["POST"])
def login():
    user_name = request.form.get("user_name")
    user_email = request.form.get("user_email")
    user_password = request.form.get("user_password")
    print(user_email)
    print(user_password)
    salt = "moj super skrivni string"
    user_password += salt  # user_password = user_password + salt
    hashed_password = hashlib.sha256(user_password.encode()).hexdigest()
    print(hashed_password)

    user = db.query(User).filter_by(email=user_email).first()
    test = db.query(User).all()
    print(test)
    session_token = str(uuid.uuid4())
    print(session_token)

    print(user)
    print(type(user))

    if user is None:
        user = User(name=user_name, password=hashed_password, email=user_email, session_token=session_token)
        db.add(user)
        db.commit()

    else:
        if user.password == hashed_password:
            user.session_token = session_token
            db.add(user)
            db.commit()
        else:
            return "Wrong password, please try again!"

    response = make_response(redirect("index"))
    response.set_cookie("session_token", session_token)
    return response


@app.route("/profile", methods=["GET", "POST"])
def user_profile():
    session_token = request.cookies.get("session_token")

    user1 = db.query(User).filter_by(session_token=session_token).first()

    if user1:
        # render_template(template, **kwargs)
        return render_template("user_profile.html", user=user1)
    else:
        return redirect("index")


@app.route("/edit_user", methods=["POST"])
def edit_user():
    session_token = request.cookies.get("session_token")
    user = db.query(User).filter_by(session_token=session_token).first()

    new_user_name = request.form.get("user_name")
    new_user_email = request.form.get("user_email")

    user.name = new_user_name
    user.email = new_user_email

    db.add(user)
    db.commit()

    return redirect("profile")


@app.route("/delete_profile", methods=["GET", "POST"])
def delete_profile():
    if request.method == "GET":
        return render_template("delete_profile.html")
    elif request.method == "POST":
        session_token = request.cookies.get("session_token")
        user = db.query(User).filter_by(session_token=session_token).first()

        db.delete(user)
        db.commit()

        response = make_response(redirect("index"))
        response.set_cookie("session_token", "")
        return response


@app.route("/about-me", methods=["GET", "POST"])
def about_me():
    if request.method == "GET":
        user_name = request.cookies.get("name")
        return render_template("about_me.html", name=user_name)
    elif request.method == "POST":
        user_name = request.form.get("name")
        print(user_name)
        print(request.form.get("email"))
        print(request.form.get("comment"))

        response = make_response(redirect("index"))
        response.set_cookie("name", user_name)
        return response


@app.route("/portfolio", methods=["GET"])
def portfolio():
    session_token = request.cookies.get("session_token")
    user = db.query(User).filter_by(session_token=session_token).first()
    projects = [
        {"name": "Test",
         "year": 2018},
        {"name": "Fitnes",
         "year": 2014},
        {"name": "Carpark",
         "year": 2017}
    ]
    user_name = request.cookies.get("name")
    return render_template("portfolio.html", projects=projects, name=user_name, user=user)


@app.route("/vreme", methods=["GET"])
def weather():
    url = "http://api.openweathermap.org/data/2.5/weather?q=Ljubljana&units=metric&apikey=ad5210298c8369fba090781a076f0f18"

    data = requests.get(url=url)
    print(data)
    print(data.json())
    return render_template("weather.html", weather_data=data.json())


@app.route("/api/v1/oseba")
def my_api():
    d = {"ime": "Janez",
         "priimek": "Kranjski",
         "IBAN": "SI5612341234123"}
    return jsonify(d)

if __name__ == '__main__':
    app.run(debug=True)
