import predictions as pred
from history import History
import instances as inst
import algorithms as alg

def simulate(phi, length, num_rep=1000):
    eta = []
    cr = []
    for i in range(num_rep):
        for sigma in [0, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10]:
            exchange_rates = inst.exchange_rates_normal_from_last(phi, length, sigma)

            p = pred.opt_off_distorted(exchange_rates)
            alg_pred = alg.FtP(p)

            h = History(alg_pred, exchange_rates)
            h.run_full()
            eta.append(h.get_total_error())
            cr.append(h.get_comp_ratio())

    return eta, cr