from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dash():
    return render_template("dashboard.html")


app.run(debug=True)
