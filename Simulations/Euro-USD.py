import simulate

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from decimal import *


exchange_rates_all = pd.read_csv(r'../Data/euro-daily-hist_1999_2021.csv')

exchange_rates_orig = pd.to_numeric(exchange_rates_all['[US dollar ]'], errors='coerce').dropna().values.tolist()

exchange_rates = exchange_rates_orig / np.min(exchange_rates_orig)

k = np.inf
phi = 100
length = 100  # length of the input sequence
normalized = False
num_rep = 1000
# alpha = 0.7
# beta = 0.2
alpha = [0.7, 0.1, 0.1]
beta=[0.2, 0.45, 0.1]
all_combinations = False
data_model = "DataIterative"
alg0_name = "ftp"
alg1_name = "opt"
lambda_list = [0, 0.25, 0.5, 0.75, 1]
comb_type = "step"

df = simulate.simulate_combined_alg_mult(k, phi, length, alg0_name, alg1_name, lambda_list, comb_type,
                                         data_model, num_rep, normalized, alpha, beta, all_combinations)

print(df)

ax = df.plot()

xlim = ax.get_xlim()
x = range(int(xlim[1]) + 1)
y = [(phi ** (err / 2)) for err in x]
plt.plot(x, y, label="Competitive Ratio of FtP", color="k")
plt.legend()

plt.yscale("log")
ax.set_ylabel("$return(OFF) / return(A)$")
plt.setp(ax.lines, linewidth=1)

if normalized:
    plt.savefig(f"Plots/EUR-USD-Combined_{alg0_name}_{alg1_name}_k{k}_{data_model}_alpha{alpha}_beta{beta}_length{length}_repetitions{num_rep}_normalized_error.pdf")
else:
    plt.savefig(f"../Plots/EUR-USD-Combined_{alg0_name}_{alg1_name}_k{k}_{data_model}_alpha{alpha}_beta{beta}_length{length}_repetitions{num_rep}.pdf")


plt.show()