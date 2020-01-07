from flask import Flask, render_template, request, redirect, make_response
import time

# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.

app = Flask(__name__)


@app.route("/index", methods=["GET"])
@app.route("/", methods=["GET"])
def index():
    time_now = time.time()
    user_name = request.cookies.get("name")
    return render_template("index.html", trenutni_cas=time_now, name=user_name)


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
    projects = [
        {"name": "Test",
         "year": 2018},
        {"name": "Fitnes",
         "year": 2014},
        {"name": "Carpark",
         "year": 2017}
    ]
    user_name = request.cookies.get("name")
    return render_template("portfolio.html", projects=projects, name=user_name)


if __name__ == '__main__':
    app.run(debug=True)
