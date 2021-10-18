import copy

import algorithms as alg
import offline as off
import predictions as pred
import testing as test
from history import History
import pandas as pd
import matplotlib.pyplot as plt
import plots
import simulate

# exchange_rates = [1, 2, 3, 1, 4, 1, 6, 1, 1, 1, 2, 1, 6, 4, 2, 3, 1, 8]
exchange_rates = [3, 2, 1, 3, 2, 1, 1, 2, 3, 3, 3, 4, 5, 1]
phi = max(exchange_rates)

# alg1 = alg.AlgorithmRandom()
# alg2 = alg.AlgorithmRandomTrade()
#
# pred = pred.opt_off_distorted(exchange_rates)
# alg_pred = alg.FtP(pred)
# print(test.alg_return(copy.deepcopy(alg_pred), exchange_rates))
#
# h = History(alg_pred, exchange_rates)
# h.run_full()
# print(h.get_results_str())
#
# h1 = History(alg1, exchange_rates)
# h1.run_full()
# print(h1.get_results_str())
#
# h2 = History(alg2, exchange_rates)
# h2.run_full()
# print(h2.get_results_str())

# eta = []
# cr = []
# for i in range(10000):
#     p = pred.opt_off_distorted(exchange_rates)
#     alg_pred = alg.FtP(p)
#
#     h = History(alg_pred, exchange_rates)
#     h.run_full()
#     eta.append(h.get_total_error())
#     cr.append(h.get_comp_ratio())

length = 1000
eta, cr = simulate.simulate(phi, length)

plots.error_against_comp_ratio(eta, cr)
x = range(length)
y = [1/(phi**(err/2)) for err in x]
plt.plot(x, y, label="Lower bound")
plt.show()



