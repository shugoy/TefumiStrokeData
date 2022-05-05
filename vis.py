import os, sys
import numpy as np
import json
import gzip
import argparse

import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.widgets import Slider, Button

import utils

def drawChar(
        data, char_, ax, 
        method="density", 
        radius=100, 
        alpha=1, 
        n_sample=30, 
        n_interpolate=10, 
        radius_by_pressure=True,
        cmap="jet"):
    
    ax.cla()
    a = data.get(char_)
    if a is None:
        print('Not exist:', char_)
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
        Ps_med = np.median(Ps)
        
        if method == "density":
            Xs, Ys, Ps, Ds = utils.calc_density(Xs, Ys, Ps, n_sample)
            Xs, Ys, Ps, Ds = utils.calc_interpolation([Xs, Ys, Ps, Ds], n_interpolate)  ## 点の間を補間
            Ps = (Ps - Ps_med) + 0.5
            ax.scatter(
                Xs, -Ys, s=radius*Ps if radius_by_pressure else radius, 
                c=Ds, cmap=cmap, norm=Normalize(0,1), alpha=alpha, linewidths=0)
        elif method == "pressure_uniform":
            Xs, Ys, Ps, _ = utils.uniform_stroke(Xs, Ys, Ps, n_sample)  ## 等間隔にサンプル
            Xs, Ys, Ps = utils.calc_interpolation([Xs, Ys, Ps], n_interpolate)  ## 点の間を補間
            Ps = (Ps - Ps_med) + 0.5
            ax.scatter(
                Xs, -Ys, s=radius*Ps if radius_by_pressure else radius, 
                c=Ps, cmap=cmap, norm=Normalize(0,1), alpha=alpha, linewidths=0)
        elif method == "pressure_raw":
            Ps = (Ps - Ps_med) + 0.5
            ax.scatter(
                Xs, -Ys, s=radius*Ps if radius_by_pressure else radius, 
                c=Ps, cmap=cmap, norm=Normalize(0,1), alpha=alpha, linewidths=0)
        else:
            raise NotImplementedError(method)


def compareChars(data, text, opt):
    fig, axes = plt.subplots(1, 3, figsize=(4*3, 4))
    
    drawChar(data, text[0], axes[0], "pressure_raw", opt.radius, opt.alpha, opt.n_sample, opt.n_interpolate, opt.radius_by_pressure, opt.colormap)
    drawChar(data, text[0], axes[1], "pressure_uniform", opt.radius, opt.alpha, opt.n_sample, opt.n_interpolate, opt.radius_by_pressure, opt.colormap)
    drawChar(data, text[0], axes[2], "density", opt.radius, opt.alpha, opt.n_sample, opt.n_interpolate, opt.radius_by_pressure, opt.colormap)
        
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", type=str, default="美")
    parser.add_argument("--method", type=str, default="density", help="[density/pressure_raw/pressure_uniform]")
    parser.add_argument("--radius", type=int, default=100)
    parser.add_argument("--alpha", type=float, default=1)
    parser.add_argument("--n_sample", type=int, default=30)
    parser.add_argument("--n_interpolate", type=int, default=10)
    parser.add_argument("--radius_by_pressure", action="store_true")
    parser.add_argument("--colormap", type=str, default="jet")
    
    opts = parser.parse_args()

    with gzip.open("data.json.gz", "rt") as f:
        data = json.load(f)

    compareChars(data, opts.text, opts)

