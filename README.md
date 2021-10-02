## What is `dolo`?

Dolo is something I put together over a weekend or two. Its a way to create web-based dashboards by writing a simple python script. The programming model is declarative and very similar to React. The API is pretty much a copy of [streamlit](https://streamlit.io/)'s, but feature set is smaller and implementation is simpler.

I was blown away by streamlit's design and simplicity (and [valuation](https://blog.streamlit.io/our-35-million-series-b/)) when I first used it, so decided to hack together a smaller working copy. Compared to streamlit, dolo only has a handful of components, and is more of a toy rather than a polished, production-ready thing.

## How to use
* Call `dolo.write` to render markup
* `dolo.button(...)` creates a button and returns the state of the button (True or False)
* `dolo.dropdown(...)` creates a dropdown and returns the selected option as a string
* `dolo.filter(...)` creates a filter and returns the active filter as a string
* You can cache the outputs of expensive functions using the `dolo.cache` decorator

## How it works
* The output of the script is used to generate the markup
* For every incoming request dolo re-runs the script with the updated component state and re-renders the webpage based on the script's output.
* The state is stored in a python dictionary.
* All rendering is done server-side, which means even a button press refreshes the entire page. This is different from streamlit which is more of an SPA and changes are streamed over a websocket.

## Bugs / Possible Bugs

* state dictionary isn't thread-safe
* UI breaks if a state update happens while the page is refreshing
* using `matplotlib.plt` [isn't recommended](https://matplotlib.org/stable/gallery/user_interfaces/web_application_server_sgskip.html) in a multi-threaded environment
