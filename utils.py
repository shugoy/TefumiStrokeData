from re import S
import numpy as np


def calc_inter_values(Xs, Ys, Ps, n_inter=10):
    xs = np.array([])
    ys = np.array([])
    ps = np.array([])
    for i in range(len(Xs) - 1):
        xs = np.append(xs, np.linspace(Xs[i], Xs[i+1], n_inter))
        ys = np.append(ys, np.linspace(Ys[i], Ys[i+1], n_inter))
        ps = np.append(ps, np.linspace(Ps[i], Ps[i+1], n_inter))

    return xs, ys, ps


def calc_dists(Xs, Ys):
    dists = []
    for i in range(len(Xs)):
        if i == 0:
            dist = 0
        else:
            dist_x = Xs[i-1] - Xs[i]
            dist_y = Ys[i-1] - Ys[i]
            dist = np.sqrt(dist_x**2 + dist_y**2)
        dists.append(dist)
    dists = np.array(dists)
    return dists


def uniform_stroke(Xs, Ys, Ps, n_points_per_length=10, use_secret=True):
    dists = calc_dists(Xs, Ys)

    cdf = np.cumsum(dists)  # 累積和
    total_length = cdf[-1]

    target_values = np.linspace(0, total_length, int(total_length * n_points_per_length)+2)
    ind = np.searchsorted(cdf, target_values, side='left')

    if use_secret:
        ind_l = ind#[:-1]
        ind_r = np.clip(ind + 1, 0, ind[-1])

        tl = np.abs(cdf[ind_l] - target_values)
        tr = np.abs(cdf[ind_r] - target_values)
        t = tl / (tl + tr)

        def secret(x):
            xl = x[ind_l]
            xr = x[ind_r]    
            return (1-t) * xl + t * xr

        return secret(Xs), secret(Ys), secret(Ps), (ind, cdf)
    else:
        return Xs[ind], Ys[ind], Ps[ind], (ind, cdf)


def calc_density(Xs, Ys, Ps, n_points_per_length=10, ):
    Xs_, Ys_, Ps_, (ind, cdf) = uniform_stroke(Xs, Ys, Ps, n_points_per_length=n_points_per_length)
    
    densities = []
    for i, idx in enumerate(ind):
        if i == 0:
            densities += [ind[i+1] - ind[i]]
        elif i == len(ind) - 1:
            densities += [ind[i] - ind[i-1]]
        else:
            i_start = ind[i-1]
            i_end = ind[i+1]
            n_points = i_end - i_start
            densities += [n_points]
    
    Ds = np.asarray(densities)    
    Ds = (Ds - np.median(Ds)) / (Ds.max() - Ds.min()) + 0.5
    return Xs_, Ys_, Ps_, Ds
