import Simulations.simulate as simulate

import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
import numpy as np
from matplotlib.ticker import MaxNLocator

k = np.inf
phi = 10
length = 10  # length of the input sequence
normalized = False
num_rep = 1000

alpha = 0.1
beta = 0.1
# alpha = [0.7, 0.1, 0.1]
# beta=[0.2, 0.45, 0.1]

all_combinations = False
data_model = "DataUniform"
alg0_name = "ftp"
alg1_name = "opt"
lambda_list = [0, 0.25, 0.5, 0.75, 0.99]


eta, cr = simulate.compare_ftpl_types(k, phi, length, alg0_name, alg1_name, lambda_list, data_model, num_rep, alpha, beta, all_combinations)

column_names = [f"$\lambda = {l}$" for l in lambda_list]
df = pd.DataFrame(data=np.array(cr).transpose(), index=eta, columns=column_names)
df = df.groupby(df.index).mean()

cmap = cm.get_cmap('plasma_r')
ax = df.plot(grid=True, colormap=cmap, use_index=True)

xlim = ax.get_xlim()
if xlim[1] > 16:
    ax.set_xlim(0, 16)
    xlim = ax.get_xlim()
plt.legend()

plt.yscale("symlog")
ax.set_xlabel("$\eta$")
ax.set_ylabel("$return(OFF) / return(FtP_{\lambda}^{ONL})$")
plt.setp(ax.lines, linewidth=2)
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
# ax.set_ylim(1, 10**3)

plt.savefig(f"../Plots/Difference-Combined-{alg0_name}-{alg1_name}-Step-min-Start-k_{k}-{data_model}-alpha_{alpha}-beta_{beta}-length_{length}-repetitions_{num_rep}.pdf")


plt.show()



