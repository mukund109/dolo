from flask import Flask, session, redirect, url_for, request
from flask import render_template
import random
import importlib
from dolo import state
import lit
import time

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

run_id = str(time.time())


@app.route("/")
def index():

    if "id" not in session:
        # first time person has opened this
        session["id"] = random.randint(1, 1000000)
        session["run_id"] = run_id

    elif "id" in session and session["run_id"] != run_id:
        # its the same person but using a different instance of the app
        session["run_id"] = run_id

        # destroy old state
        state[session["id"]] = {}

    # Session id needs to be set before reloading module
    importlib.reload(lit)

    return render_template("index.html")


@app.route("/refresh")
def refresh():
    if "id" in session:
        # initialize state dictionary
        state[session["id"]] = {}

    return redirect(url_for("index"))


@app.route("/event/<widget_id>", methods=["POST"])
def update_state(widget_id):
    data = request.get_json()

    new_state = data["widget_state"]
    # If not change in state
    if new_state == state[session["id"]][widget_id]:
        return "", 200

    # widget state has to be json serializable
    state[session["id"]][widget_id] = data["widget_state"]
    return "", 205


if app.debug:
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
