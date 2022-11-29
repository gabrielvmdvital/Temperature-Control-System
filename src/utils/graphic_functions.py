import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import random

def plot_line(df: pd.DataFrame, enviroment_id: str,  timesleep: int, title: str = "versus Time") -> None:
    df["time, s"] = np.arange(df.shape[0])
    x = df["time, s"].apply(lambda x: x+timesleep*0.2)
    y_t = df[f"Temperature_{enviroment_id}"]
    y_p = df[f"Potency_{enviroment_id}"].apply(lambda x: x*1200 if x*1200 <= 1200 else 1200)
    y_Tinterpolate = make_interp_spline(x, y_t)
    y_Pinterpolate = make_interp_spline(x, y_p)
    X = np.linspace(x.min(), x.max(), 500)
    Y_t = y_Tinterpolate(X)
    Y_p = y_Pinterpolate(X)

    plt.figure(figsize=(12, 4))
    plt.subplot(121)
    plt.plot(X, Y_p)
    plt.title(f"Potency {title} in {enviroment_id}")
    plt.xlabel("Time, s")
    plt.ylabel("Potency, BTU/milhão")
    
    plt.subplot(122)
    plt.plot(X, Y_t)
    plt.title(f"Temperature {title} in {enviroment_id}")
    plt.xlabel("Time, s")
    plt.ylabel("Temperature, °C")
    plt.show()



if __name__ == "__main__":
    x = np.arange(30)
    y_t = np.array([random.randint(15, 28) for _ in range(30)])
    y_p = np.array([random.randint(0, 1200) for _ in range(30)])
    y_Tinterpolate = make_interp_spline(x, y_t)
    y_Pinterpolate = make_interp_spline(x, y_p)
    X = np.linspace(x.min(), x.max(), 500)
    #Y_t = y_Tinterpolate(X)
    #Y_p = y_Pinterpolate(X)

    plt.figure(figsize=(12, 4))
    plt.subplot(121)
    plt.plot(x, y_p)
    plt.title(f"Potency versus Time")
    plt.ylabel("BTU")
    plt.xlabel("s")
    
    plt.subplot(122)
    plt.plot(x, y_t)
    plt.title(f"Temperature versus Time")
    plt.ylabel("°C")
    plt.xlabel("s")

    plt.show()