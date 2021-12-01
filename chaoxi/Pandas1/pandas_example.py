import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def craw_bar():
    df2 = pd.DataFrame(np.random.rand(10, 4), columns=['a', 'b', 'c', 'd'])
    df2.plot.bar()
    plt.show()

def craw_line():
    ts = pd.Series(np.random.randn(1000), index=pd.date_range("1/1/2000", periods=1000))
    ts = ts.cumsum()
    ts.plot()
    plt.show()

def craw_line1():
    ts = pd.Series(np.random.randn(1000), index=pd.date_range("1/1/2000", periods=1000))
    df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list("ABCD"))
    df = df.cumsum()
    df.plot()
    plt.show()


def craw_bar():
    ts = pd.Series(np.random.randn(1000), index=pd.date_range("1/1/2000", periods=1000))
    df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list("ABCD"))
    plt.figure()
    df.iloc[5].plot(kind="bar")
    plt.show()

def craw_bar1():
    df2 = pd.DataFrame(np.random.rand(10, 4), columns=["a", "b", "c", "d"])
    df2.plot.bar()
    plt.show()

def craw_bar2():
    df2 = pd.DataFrame(np.random.rand(10, 4), columns=["a", "b", "c", "d"])
    df2.plot.bar(stacked=True)
    plt.show()

def craw_bar3():
    df2 = pd.DataFrame(np.random.rand(10, 4), columns=["a", "b", "c", "d"])
    df2.plot.barh(stacked=True)
    plt.show()

if __name__ == '__main__':
    craw_bar3()
