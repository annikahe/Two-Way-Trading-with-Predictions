import predictions as pred
from history import History
import instances as inst
import algorithms as alg


def simulate_FtP(phi, length, num_rep=1000, normalized=False, alpha=0.7, beta=0.2, all_combinations=False):
    """

    :param phi:
    :param length: int
        Length of the input sequence.
    :param num_rep: int
        Number of repetitions.
    :param normalized: boolean
        Determine whether to use normalized errors TODO
    :param alpha: float or list
    :param beta: float or list
    :param all_combinations: boolean.
        Only relevant if alpha and beta are both lists.
        Determines how the elements from alpha and beta should be combined.
        all_combinations=False: Combine elements from alpha and beta index-wise (Default)
        all_combinations=True: Create all possible pairwise combinations of elements from alpha and beta
    :return:
    """
    if isinstance(alpha, list) and isinstance(beta, list):
        if all_combinations:
            alpha_beta_list = [(a, b) for b in beta for a in alpha]
        else:
            alpha_beta_list = list(zip(alpha, beta))
    elif isinstance(alpha, list):
        alpha_beta_list = [(a, beta) for a in alpha]
    elif isinstance(beta, list):
        alpha_beta_list = [(alpha, b) for b in beta]
    else:
        alpha_beta_list = [(alpha, beta)]

    eta = []
    cr = []

    for i in range(num_rep):
        for alpha, beta in alpha_beta_list:
            for sigma in [0, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100]:
                exchange_rates = inst.exchange_rates_normal_from_last(phi, length, sigma)

                p = pred.opt_off_distorted(exchange_rates, alpha, beta)
                alg_pred = alg.FtP(p)

                h = History(alg_pred, exchange_rates)
                h.run_full()
                if normalized:
                    eta.append(h.get_normalized_error())
                else:
                    eta.append(h.get_total_error())
                cr.append(h.get_comp_ratio())

    return eta, cr



def simulate_FtP_unif(phi, length, num_rep=1000, normalized=False, alpha=0.7, beta=0.2, all_combinations=False):
    """

    :param phi:
    :param length: int
        Length of the input sequence.
    :param num_rep: int
        Number of repetitions.
    :param normalized: boolean
        Determine whether to use normalized errors TODO
    :param alpha: float or list
    :param beta: float or list
    :param all_combinations: boolean.
        Only relevant if alpha and beta are both lists.
        Determines how the elements from alpha and beta should be combined.
        all_combinations=False: Combine elements from alpha and beta index-wise (Default)
        all_combinations=True: Create all possible pairwise combinations of elements from alpha and beta
    :return:
    """
    if isinstance(alpha, list) and isinstance(beta, list):
        if all_combinations:
            alpha_beta_list = [(a, b) for b in beta for a in alpha]
        else:
            alpha_beta_list = list(zip(alpha, beta))
    elif isinstance(alpha, list):
        alpha_beta_list = [(a, beta) for a in alpha]
    elif isinstance(beta, list):
        alpha_beta_list = [(alpha, b) for b in beta]
    else:
        alpha_beta_list = [(alpha, beta)]

    eta = []
    cr = []

    for i in range(num_rep):
        for alpha, beta in alpha_beta_list:
            exchange_rates = inst.exchange_rates_uniform(phi, length)

            p = pred.opt_off_distorted(exchange_rates, alpha, beta)
            alg_pred = alg.FtP(p)

            h = History(alg_pred, exchange_rates)
            h.run_full()
            if normalized:
                eta.append(h.get_normalized_error())
            else:
                eta.append(h.get_total_error())
            cr.append(h.get_comp_ratio())

    return eta, cr


def simulate_Alg(phi, length, num_rep=1000, normalized=False):
    eta = []
    cr = []
    for i in range(num_rep):
        for sigma in [0, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100]:
            exchange_rates = inst.exchange_rates_normal_from_last(phi, length, sigma)

            p = pred.opt_off_distorted(exchange_rates)
            alg_pred = alg.FtP(p)

            h = History(alg_pred, exchange_rates)
            h.run_full()
            if normalized:
                eta.append(h.get_normalized_error())
            else:
                eta.append(h.get_total_error())
            cr.append(h.get_comp_ratio())

    return eta, cr
