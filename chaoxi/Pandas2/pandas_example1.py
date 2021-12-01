import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def draw_pie():

    series = pd.Series(3 * np.random.rand(4), index=["1", "2", "3", "4"], name="series")
    series.plot.pie(figsize=(6, 6));
    plt.show()


def draw_pie1():
    df = pd.DataFrame(
        3 * np.random.rand(4, 2), index=["a", "b", "c", "d"], columns=["x", "y"])
    df.plot.pie(subplots=True, figsize=(8, 4), legend=False)
    plt.show()

def draw_pie2():
    series = pd.Series(3 * np.random.rand(4), index=["1", "2", "3", "4"], name="series")
    series.plot.pie(
        labels=["A", "B", "C", "D"],
        colors=["r", "g", "b", "c"],
        autopct="%.2f",
        fontsize=20,
        figsize=(6, 6),)
    plt.show()

def draw_pie3():
    series = pd.Series([0.1] * 4, index=["a", "b", "c", "d"], name="series2")
    series.plot.pie(figsize=(6, 6))
    plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
def draw_pie4():

    df = pd.DataFrame(np.random.randn(1000, 4), columns=["a", "b", "c", "d"])

    scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal="kde")
    plt.show()

if __name__ == '__main__':
    draw_pie4()