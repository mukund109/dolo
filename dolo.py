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


@mark
def write(markup):
    return None, markup


@mark
def table(df):
    return None, df.to_html()


@mark
def button(message):
    # probably need to do some escaping
    markup = f'<button type="button">{message}</button>'
    return False, markup


# difference between markup and widgets
# widget store state across requests, per session
# they also need to be uniquely identifiable (by order in which they're invoked)

# =request context=
#   access correct button ID
#   access correct button state by ID
#   create button markup
#   set return value

# =POST update=
#   =Session context=
#       update button state by ID
