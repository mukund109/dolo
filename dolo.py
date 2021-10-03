import flask
from io import BytesIO
from flask import session, g
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache, wraps
import base64
from matplotlib import pyplot as plt

print("Creating state dictionary")
# `state` is a dictionary that stores widget states for different client sessions
# session -> widget id -> state
# It also stores cached functions
# function_name -> function(+cache)
# It's not thread safe
state = defaultdict(dict)

# Widgets are stateful components
# they need to have an attribute that stores state
# (there's no restriction on its type as long as its json serializable and allows for checking equality using `==`)
# and a key (str) so that they're uniquely identifiable
class Widget:
    @property
    def type_name(self):
        return self.__class__.__name__

    def __init__(self):
        if not flask.has_app_context():
            # if the script is being run outside of a flask context
            # just return default state
            return self.state

        assert "id" in session
        sess_id = session["id"]

        if "components" not in g:
            # new request, repopulate list of components
            g.components = list()

        # restore widget state
        if self.key in state[sess_id].keys():
            self.state = state[sess_id][self.key]
        else:
            # if new widget, initialize state with default value
            state[sess_id][self.key] = self.state

        # display this on the app
        g.components.append(self)

        return self.state


@dataclass
class Markup:
    html: str

    def __post_init__(self):
        if not flask.has_app_context():
            # if not flask context, do nothing
            return None

        if "components" not in g:
            # new request, repopulate list of components
            g.components = list()

        g.components.append(self)

        return None


@dataclass
class Button(Widget):
    state: bool
    description: str

    def __post_init__(self):
        self.key = str(hash(self.description))
        super().__init__()


@dataclass
class Dropdown(Widget):
    state: str
    choices: set
    description: str

    def __post_init__(self):
        self.key = str(hash(self.description + "".join(self.choices)))
        super().__init__()


@dataclass
class Filter(Widget):
    state: str
    filters: set
    description: str
    color: str

    def __post_init__(self):
        self.key = str(hash(self.description + "".join(self.filters)))
        self.theme = {
            "green": "label-success",
            "red": "label-error",
            "yellow": "label-warning",
            "blue": "label-primary",
        }[self.color]
        super().__init__()


def write(markup):
    return Markup(markup)


def table(df, display_index=True, striped=True):
    classes = ["table"]
    if striped:
        classes.append("table-striped")
    return Markup(
        df.to_html(classes=classes, index=display_index, justify="unset", border=0)
    )


def button(description):
    return Button(state=False, description=description).state


def dropdown(choices, default_choice, description):
    assert default_choice in choices
    assert len(choices) >= 1
    return Dropdown(default_choice, choices, description).state


def filter(filters, active, description, color="green"):
    assert color in ["red", "yellow", "green", "blue"]
    assert active in filters
    assert len(filters) >= 1
    return Filter(active, filters, description, color).state


def cache(func):
    func_id = func.__name__

    if func_id in state:
        return state[func_id]

    # This cache persists across different requests AND sessions, and refreshes of the session
    # It doesn't persist across different instances of the app
    # Since the cached values are tied to `wrapper`, if `wrapper` changes the cached values also disappear
    @wraps(func)
    @lru_cache(maxsize=None)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    state[func_id] = wrapper
    return wrapper


def plot(figure):
    tmpfile = BytesIO()
    figure.savefig(tmpfile, format="png")
    encoded = base64.b64encode(tmpfile.getvalue()).decode("utf-8")
    print(encoded)
    plt.close()
    return Markup(f'<img src="data:image/png;base64, {encoded}">')


print("Dolo is loaded")
