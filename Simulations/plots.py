import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import simulate
import plots


def moving_average(a, window_size=3) :
    ret = np.cumsum(a, dtype=float)
    ret[window_size:] = ret[window_size:] - ret[:-window_size]
    return ret[window_size - 1:] / window_size


def error_against_comp_ratio(ax, eta, cr, alg_name, normalized=False):
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
        d = {"$\eta$": eta, f"A = {alg_name}": cr}
        df = pd.DataFrame(data=d)
        df_cleaned = df.groupby('$\eta$').mean().reset_index()
        if ax:
            df_cleaned.plot(x='$\eta$', y=f"A = {alg_name}", ax=ax)
        else:
            ax = df_cleaned.plot(x='$\eta$', y=f"A = {alg_name}")

    return ax


def plot_ftp(ax, k, phi, length, data_model, num_rep=1000, normalized=False, alpha=0.7, beta=0.2, all_combinations=False):

    if data_model == "DataIterative":
        eta, cr = simulate.simulate_ftp(k, phi, length, num_rep=num_rep, normalized=normalized, alpha=alpha, beta=beta,
                                        all_combinations=all_combinations)
    else:
        eta, cr = simulate.simulate_alg_unif("FtP", k, phi, length, num_rep=num_rep, normalized=normalized, alpha=alpha, beta=beta, all_combinations=all_combinations)

    ax = plots.error_against_comp_ratio(ax, eta, cr, "FtP", normalized=normalized)

    if not normalized:
        upper_bound = np.max(eta)
        x = range(int(np.floor(upper_bound + 1)))
        y = [(phi ** (err / 2)) for err in x]
        plt.plot(x, y, label="Competitive Ratio")
        plt.legend()

    plt.yscale("log")

    if normalized:
        plt.savefig(f"Plots/FtP_k{k}_{data_model}_alpha{alpha}_beta{beta}_length{length}_repetitions{num_rep}_normalized_error.png")
    else:
        plt.savefig(f"../Plots/FtP_k{k}_{data_model}_alpha{alpha}_beta{beta}_length{length}_repetitions{num_rep}.png")


def plot_combined(ax, k, phi, length, alg0_name, alg1_name, l, comb_type="start", data_model="DataIterative", num_rep=1000, normalized=False, alpha=0.7, beta=0.2, all_combinations=False):

    eta, cr = simulate.simulate_combined_alg(k, phi, length, alg0_name, alg1_name, l, comb_type, data_model,
                                             num_rep, normalized, alpha, beta, all_combinations)

    ax = plots.error_against_comp_ratio(ax, eta, cr, f"{alg0_name}_{l}", normalized=normalized)

    # if not normalized:
    #     upper_bound = np.max(eta)
    #     x = range(int(np.floor(upper_bound + 1)))
    #     y = [(phi ** (err / 2)) for err in x]
    #     plt.plot(x, y, label="Competitive Ratio")
    #     plt.legend()

    return ax

    # plt.yscale("log")
    #
    # if normalized:
    #     plt.savefig(f"Plots/Combined_{alg0_name}_{alg1_name}_lambda{l}_k{k}_{data_model}_alpha{alpha}_beta{beta}_length{length}_repetitions{num_rep}_normalized_error.png")
    # else:
    #     plt.savefig(f"../Plots/Combined_{alg0_name}_{alg1_name}_lambda{l}_k{k}_{data_model}_alpha{alpha}_beta{beta}_length{length}_repetitions{num_rep}.png")



# def plot_algo(k, phi, length, algo, num_rep=1000, normalized=False):
#
#     eta, cr = simulate.simulate_algo(k, phi, length, algo, num_rep=num_rep, normalized=normalized)
#
#     algo_name = "A"
#
#     plots.error_against_comp_ratio(ax, eta, cr, algo_name, normalized=normalized)
#
#     if not normalized:
#         max_error = np.max(eta)
#         x = range(int(np.floor(max_error + 1)))
#         y = [(phi ** (err / 2)) for err in x]
#         plt.plot(x, y, label="Competitive Ratio")
#         plt.legend()
#
#     plt.yscale("log")
#
#     if normalized:
#         plt.savefig(f"Plots/{algo_name}_k{k}_length{length}_repetitions{num_rep}_normalized_error.png")
#     else:
#         plt.savefig(f"../Plots/{algo_name}_k{k}_length{length}_repetitions{num_rep}.png")