import pickle
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import MaxNLocator

with open(f'Instances/Combined-ftp-opt-start-k_inf-DataIterative-alpha_0.1-beta_0.45-length_10-repetitions_1000.pkl', 'rb') as inp:
    inst_obj = pickle.load(inp)
    print(inst_obj.df)

    cmap = cm.get_cmap('plasma_r')
    ax = inst_obj.df.plot(grid=True, colormap=cmap, use_index=True)

    xlim = ax.get_xlim()
    if xlim[1] > 16:
        ax.set_xlim(0, 16)
        xlim = ax.get_xlim()
    x = range(int(xlim[1]) + 1)
    y = [(inst_obj.phi ** (err / 2)) for err in x]
    plt.plot(x, y, label="Competitive Ratio of FtP", color="k")
    plt.legend()

    plt.yscale("log")
    ax.set_xlabel("$\eta$")
    ax.set_ylabel("$return(OFF) / return(FtP_{\lambda}^{ONL})$")
    plt.setp(ax.lines, linewidth=1)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    # ax.set_ylim(1, 10**3)

    # plt.savefig(f"Plots/Combined-{alg0_name}-{alg1_name}-{comb_type}-k_{k}-{data_model}-alpha_{alpha}-beta_{beta}-length_{length}-repetitions_{num_rep}.pdf")

    plt.show()