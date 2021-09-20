import flask
from flask import session, g
from collections import defaultdict
import functools

print("creating state")
state = defaultdict(dict)


def mark(func):
    @functools.wraps(func)
    def store_markup(*args, **kwargs):
        if not flask.has_app_context():
            # if not flask context, do nothing
            return

        assert "id" in session
        sess_id = session["id"]

        if "flag" not in g:

            # new request, flush the markup
            state[sess_id]["markup"] = list()

            # set flag, the value doesn't matter
            g.flag = 0

        res, markup = func(*args, **kwargs)
        state[sess_id]["markup"].append(markup)

        return res

    return store_markup


def widget(func):
    @functools.wraps(func)
    def store_markup_and_state(*args, **kwargs):
        if not flask.has_app_context():
            # if not flask context, do nothing
            return

        assert "id" in session
        sess_id = session["id"]

        if "flag" not in g:

            # new request, flush the markup
            state[sess_id]["markup"] = list()

            # set flag, the value doesn't matter
            g.flag = 0

        res, markup, key = func(*args, **kwargs)

        # if new widget, initialize state with default value
        if key not in state[sess_id]["widget_state"].keys():
            state[sess_id]["widget_state"][key] = res

        state[sess_id]["markup"].append(markup)

        return state[sess_id]["widget_state"][key]

    return store_markup_and_state


# widgets
# define their keys
# corresponding html element should have that as id


@mark
def write(markup):
    return None, markup


@mark
def table(df):
    return None, df.to_html()


@widget
def button(message):
    key = str(hash(message))
    # probably need to do some escaping
    markup = f'<button id="{key}" type="button">{message}</button>'

    # returns default_value, markup
    return False, markup, key


# difference between markup and widgets
# widget store state across requests, per session
# they also need to be uniquely identifiable

# =request context=
#   access correct button ID
#   access correct button state by ID
#   create button markup
#   set return value

# =POST update=
#   =Session context=
#       update button state by ID
