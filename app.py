from flask import Flask, session, redirect, url_for, request
import random
import importlib
from dolo import state
import lit
import time

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

with open("index.html", "r") as f:
    template = "".join(f.readlines())

run_id = str(time.time())


@app.route("/")
def index():

    if "id" not in session:
        # first time person has opened this
        session["id"] = random.randint(1, 1000000)
        session["run_id"] = run_id

        # initialize state dictionary
        state[session["id"]] = {"widget_state": {}, "markup": list()}

    elif "id" in session and session["run_id"] != run_id:
        # its the same person but using a different instance of the app
        session["run_id"] = run_id

        # re-initialize state dictionary
        state[session["id"]] = {"widget_state": {}, "markup": list()}

    session_id = session["id"]

    # Session id needs to be set before reloading module
    importlib.reload(lit)

    heading = f"<h1>{session_id}</h1>"
    markup = heading + "\n".join(state[session_id]["markup"])
    return template.replace("{{}}", markup)


@app.route("/refresh")
def refresh():
    if "id" in session:
        # initialize state dictionary
        state[session["id"]] = {"widget_state": {}, "markup": list()}

    return redirect(url_for("index"))


@app.route("/event/<widget_id>", methods=["POST"])
def update_state(widget_id):
    data = request.get_json()
    print(data)

    # widget state has to be json serializable
    state[session["id"]]["widget_state"][widget_id] = data["widget_state"]
    return "", 205
