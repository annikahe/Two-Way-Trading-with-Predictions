import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import simulate
import plots


def moving_average(a, window_size=3) :
    ret = np.cumsum(a, dtype=float)
    ret[window_size:] = ret[window_size:] - ret[:-window_size]
    return ret[window_size - 1:] / window_size


def error_against_comp_ratio(eta, cr, alg_name, normalized=False):
    if normalized:
        d = {"$\eta / return(OFF)$": eta, f"return(OFF) / return({alg_name})": cr}
        df = pd.DataFrame(data=d)
        df_sorted = df.sort_values('$\eta / return(OFF)$')
        e = df_sorted["$\eta / return(OFF)$"].values.tolist()
        r = df_sorted[f"return(OFF) / return({alg_name})"].values.tolist()
        for i in range(2):
            e = moving_average(e, 100)
            r = moving_average(r, 100)
        # df_cleaned = df_sorted.groupby('$\eta / return(OFF)$').mean().reset_index()
        plt.plot(e, r, label='$\eta / return(OFF)$')
    else:
        d = {"$\eta$": eta, f"return(OFF) / return({alg_name})": cr}
        df = pd.DataFrame(data=d)
        df_cleaned = df.groupby('$\eta$').mean().reset_index()
        df_cleaned.plot(x='$\eta$', y=f'return(OFF) / return({alg_name})')


def plot_FtP(phi, length, data_model, num_rep=1000, normalized=False, alpha=0.7, beta=0.2, all_combinations=False):

    if data_model == "DataIterative":
        eta, cr = simulate.simulate_FtP(phi, length, num_rep=num_rep, normalized=normalized, alpha=alpha, beta=beta,
                                        all_combinations=all_combinations)
    else:
        eta, cr = simulate.simulate_FtP_unif(phi, length, num_rep=num_rep, normalized=normalized, alpha=alpha, beta=beta, all_combinations=all_combinations)

    plots.error_against_comp_ratio(eta, cr, "FtP", normalized=normalized)

    if not normalized:
        upper_bound = np.max(eta)
        x = range(int(np.floor(upper_bound + 1)))
        y = [(phi ** (err / 2)) for err in x]
        plt.plot(x, y, label="Competitive Ratio")
        plt.legend()

    plt.yscale("log")

    if normalized:
        plt.savefig(f"Plots/FtP_{data_model}_alpha{alpha}_beta{beta}_length{length}_repetitions{num_rep}_normalized_error.png")
    else:
        plt.savefig(f"../Plots/FtP_{data_model}_alpha{alpha}_beta{beta}_length{length}_repetitions{num_rep}.png")


def plot_algo(phi, length, algo, num_rep=1000, normalized=False):

    eta, cr = simulate.simulate_algo(phi, length, algo, num_rep=num_rep, normalized=normalized)

    algo_name = "A"

    plots.error_against_comp_ratio(eta, cr, algo_name, normalized=normalized)

    if not normalized:
        max_error = np.max(eta)
        x = range(int(np.floor(max_error + 1)))
        y = [(phi ** (err / 2)) for err in x]
        plt.plot(x, y, label="Competitive Ratio")
        plt.legend()

    plt.yscale("log")

    if normalized:
        plt.savefig(f"Plots/{algo_name}_length{length}_repetitions{num_rep}_normalized_error.png")
    else:
        plt.savefig(f"../Plots/{algo_name}_length{length}_repetitions{num_rep}.png")