from re import S
import numpy as np


def calc_inter_values(Xs, n_inter=10):
    xs = np.array([])
    for i in range(len(Xs) - 1):
        xs = np.append(xs, np.linspace(Xs[i], Xs[i+1], n_inter))
    return xs


def calc_interpolation(arrays, n_inter=10):
    out = []
    for Xs in arrays:
        out.append(calc_inter_values(Xs, n_inter))
    return out    


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
    # ind_right = np.searchsorted(cdf, target_values, side='right')
        
    # import matplotlib.pyplot as plt
    # fig, ax = plt.subplots()
    # ax.scatter(np.linspace(0, len(cdf), len(cdf)), cdf)
    # ax.scatter(np.linspace(0, len(cdf), len(cdf))[ind], cdf[ind], marker="x")
    # # for tv, x in zip(target_values, np.linspace(0, len(cdf), len(cdf))[ind]):
    # for tv in target_values:
    #     ax.plot([0,len(cdf)], [tv, tv], color="gray")
    #     # ax.scatter(np.linspace(0, len(cdf), len(cdf))[ind], target_values, marker="x")    

    if use_secret:
        ind1 = ind[1:]
        ind0 = np.clip(ind1 - 1, 0, ind[-1])

        t0 = target_values[1:] - cdf[ind0]
        t1 = cdf[ind1] - target_values[1:]
        t = t0 / (t0 + t1)

        def secret(x):
            x0 = x[ind0]
            x1 = x[ind1]
            xt = (1-t) * x0 + t * x1
            return np.append(x[0], xt)

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
