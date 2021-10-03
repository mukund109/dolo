import dolo
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

sns.set_theme()

matplotlib.use("Agg")

dolo.write("<h2>Create a dropdown</h2>")

name = dolo.dropdown(
    choices=["planets", "titanic", "iris"],
    default_choice="planets",
    description="Pick a dataset",
)

df = sns.load_dataset(name)

dolo.table(df.head(7))

dolo.write("<br><h4>Plot some figures!</h4>")

x_col = dolo.filter(filters=df.columns, active=df.columns[0], description="X-axis")
y_col = dolo.filter(
    filters=df.columns, active=df.columns[1], description="Y-axis", color="yellow"
)

fig = sns.relplot(data=df, x=x_col, y=y_col)
dolo.plot(fig)
