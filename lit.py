import pandas as pd
import random
import dolo

dolo.write(
    """
<h2>The App of the Gods</h2>
"""
)

button = dolo.button("Click Me!")

if button:
    dolo.write("SUCCESS! BUTTON HAS BEEN PRESSED!")
else:
    dolo.write("Button hasn't been pressed")

another_button = dolo.button("Don't Click!")

if another_button:
    dolo.write("YET ANOTHER SUCCESSFUL BUTTON PRESS")

df = pd.DataFrame(
    {
        "Movies": [
            "Real Housewives Of Shawshank",
            "Avengers: Ek Prem Katha",
            "Harry Singh and the Sorcerer's Dupatta",
        ],
        "Genre": ["Crime, Situational Comedy", "Romance, Thanos", "Magical Romance"],
        "Directors": ["Anurag Kashyap", "Akshay Kumar", "James Cameron"],
    }
)

dolo.table(df, display_index=False, striped=True)

choice = dolo.dropdown(
    ["Yolo", "Dolo", "Streamlit", "Shiny"], "Dolo", "Pick the best data app framework"
)

dolo.write("Active choice: " + choice)

a = str(random.randint(0, 10))
dolo.write(a)
