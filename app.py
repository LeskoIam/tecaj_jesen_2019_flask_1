from flask import Flask, render_template
import time

# Documentation is like sex.
# When it's good, it's very good.
# When it's bad, it's better than nothing.
# When it lies to you, it may be a while before you realize something's wrong.

app = Flask(__name__)


@app.route("/index")
@app.route("/")
def index():
    time_now = time.time()
    return render_template("index.html", trenutni_cas=time_now)


@app.route("/about-me")
def about_me():
    user = "Kostanj"
    return render_template("about_me.html", user=user)


@app.route("/portfolio")
def portfolio():
    projects = [
        {"name": "Test",
         "year": 2018},
        {"name": "Fitnes",
         "year": 2014},
        {"name": "Carpark",
         "year": 2017}
    ]
    return render_template("portfolio.html", projects=projects)


if __name__ == '__main__':
    app.run(debug=True)
