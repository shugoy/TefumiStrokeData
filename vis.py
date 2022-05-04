import os, sys
import numpy as np
import json
import gzip

import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.widgets import Slider, Button

import utils

def drawChar(data, name, ax, method="density", radius=100, alpha=1, n_sample=30, n_interpolate=10, radius_by_pressure=True):
    ax.cla()

    a = data.get(name)
    if a is None:
        print('Not exist:', name)
        return
    x_strokes = a["x"]
    y_strokes = a["y"]
    p_strokes = a["pressure"]
    
    for Xs, Ys, Ps in zip(x_strokes, y_strokes, p_strokes):
        if len(Xs) == 0:
            continue
        
        Xs = np.asarray(Xs)
        Ys = np.asarray(Ys)
        Ps = np.asarray(Ps)
        median = np.median(Ps)
        
        if method == "density":
            Xs, Ys, Ps = utils.calc_inter_values(Xs, Ys, Ps, n_interpolate)  ## 点の間を補間
            Xs, Ys, Ps, Ds = utils.calc_density(Xs, Ys, Ps, n_sample)
            Ps = (Ps - median) + 0.5
            D_md = np.median(Ds)
            ax.scatter(
                Xs, -Ys, s=radius*Ps if radius_by_pressure else radius, 
                c=Ds, cmap='jet', norm=Normalize(0,1), alpha=alpha, linewidths=0)
        elif method == "pressure_uniform":
            Xs, Ys, Ps = utils.calc_inter_values(Xs, Ys, Ps, n_interpolate)  ## 点の間を補間
            Xs, Ys, Ps, _ = utils.uniform_stroke(Xs, Ys, Ps, n_sample)  ## 等間隔にサンプル
            Ps = (Ps - median) + 0.5
            ax.scatter(
                Xs, -Ys, s=radius*Ps if radius_by_pressure else radius, 
                c=Ps, cmap='jet', norm=Normalize(0,1), alpha=alpha, linewidths=0)
        elif method == "pressure_raw":
            Ps = (Ps - median) + 0.5
            ax.scatter(
                Xs, -Ys, s=radius*Ps if radius_by_pressure else radius, 
                c=Ps, cmap='jet', norm=Normalize(0,1), alpha=alpha, linewidths=0)
    
    # ax.axis('off')
    

def drawChars(data, text):
    fig, axes = plt.subplots(1,len(text), figsize=(len(text)*4, 4))
    
    drawChar(data, text[0], axes, "pressure_raw")
        
    plt.show()


if __name__ == '__main__':
    with gzip.open("data.json.gz", "rt") as f:
        data = json.load(f)

    drawChars(data, sys.argv[1])

