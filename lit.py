import pandas as pd
import random
import dolo

dolo.write(
    """
<div>Hello World!</div>
"""
)

button = dolo.button("Click Me!")

if button:
    dolo.write("SUCCESS! BUTTON HAS BEEN PRESSED!")
else:
    dolo.write("Button hasn't been pressed")

# if not condition:
another_button = dolo.button("Click Them!")

if another_button:
    dolo.write("YET ANOTHER SUCCESSFUL BUTTON PRESS")

df = pd.DataFrame({"col1": [2, 3, 4], "col2": [5, 6, 7]})

dolo.table(df)

a = str(random.randint(0, 10))
dolo.write(a)
