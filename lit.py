import pandas as pd
import random
import dolo

dolo.write(
    """
<div>Hello World!</div>
"""
)

button = dolo.button("Click Me!")

df = pd.DataFrame({"col1": [2, 3, 4], "col2": [5, 6, 7]})

dolo.table(df)

a = str(random.randint(0, 10))
dolo.write(a)
