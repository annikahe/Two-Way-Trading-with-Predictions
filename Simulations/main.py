import algorithms as alg
import matplotlib.pyplot as plt
import plots
import simulate
import pandas as pd
import numpy as np


k = np.inf
phi = 100
length = 100  # length of the input sequence
normalized = False
num_rep = 1000
alpha = 1  # 0.7
beta = 0  # 0.2
# alpha = [0.7, 0.1, 0.1]
# beta=[0.2, 0.45, 0.1]
all_combinations = False
data_model = "DataIterative"

# plots.plot_ftp(k, phi, length, data_model, num_rep, normalized, alpha, beta, all_combinations)

alg0_name = "ftp"
alg1_name = "opt"
# l = 0.5
lambda_list = [0, 0.2, 0.4, 0.6, 0.8, 1]  # list(np.linspace(0, 1, 6))
comb_type = "start"

# ax = None
#
# for l in np.linspace(0, 1, 6):
#     l = round(l, 1)
#     ax = plots.plot_combined(ax, k, phi, length, alg0_name, alg1_name, l, comb_type, data_model, num_rep, normalized, alpha, beta, all_combinations)
# ax = plots.plot_combined(ax, k, phi, length, alg0_name, alg1_name, 0.7, comb_type, data_model, num_rep, normalized, alpha, beta, all_combinations)

df = simulate.simulate_combined_alg_mult(k, phi, length, alg0_name, alg1_name, lambda_list, comb_type,
                      data_model, num_rep, normalized, alpha, beta, all_combinations)

print(df)

ax = df.plot()

xlim = ax.get_xlim()
x = range(int(xlim[1]) + 1)
y = [(phi ** (err / 2)) for err in x]
plt.plot(x, y, label="Competitive Ratio")
plt.legend()

plt.yscale("log")
ax.set_ylabel("$return(OFF) / return(A)$")
plt.setp(ax.lines, linewidth=1)

if normalized:
    plt.savefig(f"Plots/Combined_{alg0_name}_{alg1_name}_k{k}_{data_model}_alpha{alpha}_beta{beta}_length{length}_repetitions{num_rep}_normalized_error.svg")
else:
    plt.savefig(f"../Plots/Combined_{alg0_name}_{alg1_name}_k{k}_{data_model}_alpha{alpha}_beta{beta}_length{length}_repetitions{num_rep}.svg")

# d = {"$\eta / return(OFF)$": [], f"return(OFF) / return({alg_name})": []}
# df = pd.DataFrame([])
#
# eta, cr = simulate.simulate_combined_alg(k, phi, length, alg0_name, alg1_name, l, comb_type, data_model,
#                                          num_rep, normalized, alpha, beta, all_combinations)


plt.show()



