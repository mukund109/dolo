from flask import Flask, session
import random
import importlib
from dolo import state
import lit

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

with open("index.html", "r") as f:
    template = "".join(f.readlines())


@app.route("/")
def index():
    if "id" not in session:
        session["id"] = random.randint(1, 1000000)

    session_id = session["id"]

    # Session id needs to be set before reloading module
    importlib.reload(lit)

    heading = f"<h1>{session_id}</h1>"
    markup = heading + "\n".join(state[session_id]["markup"])
    return template.replace("{{}}", markup)
