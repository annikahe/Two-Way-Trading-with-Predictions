import algorithms as alg
import matplotlib.pyplot as plt
from matplotlib import cm
import plots
import simulate
import pandas as pd
import numpy as np

from matplotlib.ticker import MaxNLocator


k = np.inf
phi = 10
length = 10  # length of the input sequence
normalized = False
num_rep = 1000
alpha = 0.1
beta = 0.45
# alpha = [0.7, 0.1, 0.1]
# beta=[0.2, 0.45, 0.1]
all_combinations = False
data_model = "DataIterative"
alg0_name = "ftp"
alg1_name = "opt"
lambda_list = [0, 0.25, 0.5, 0.75, 1]
comb_type = "start"

df = simulate.simulate_combined_alg_mult(k, phi, length, alg0_name, alg1_name, lambda_list, comb_type,
                                         data_model, num_rep, normalized, alpha, beta, all_combinations)

print(df)

cmap = cm.get_cmap('plasma_r')
ax = df.plot(grid=True, colormap=cmap, use_index=True)

xlim = ax.get_xlim()
if xlim[1] > 16:
    ax.set_xlim(0, 16)
    xlim = ax.get_xlim()
x = range(int(xlim[1]) + 1)
y = [(phi ** (err / 2)) for err in x]
plt.plot(x, y, label="Competitive Ratio of FtP", color="k")
plt.legend()

plt.yscale("log")
ax.set_xlabel("$\eta$")
ax.set_ylabel("$return(OFF) / return(FtP_{\lambda}^{ONL})$")
plt.setp(ax.lines, linewidth=1)
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
# ax.set_ylim(1, 10**3)

plt.savefig(f"../Plots/Combined-{alg0_name}-{alg1_name}-{comb_type}-k_{k}-{data_model}-alpha_{alpha}-beta_{beta}-length_{length}-repetitions_{num_rep}.pdf")

plt.show()



