import predictions as pred
from history import History
import instances as inst
import algorithms as alg

import numpy as np
import pandas as pd
from tqdm import tqdm


def generate_alpha_beta_list(alpha, beta, all_combinations=False):
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

    return alpha_beta_list


def append_results(h, eta, cr, normalized=False):
    h.run_full()
    if normalized:
        eta.append(h.get_normalized_error())
    else:
        eta.append(h.get_total_error())
    cr.append(h.get_comp_ratio())


def simulate_ftp(k, phi, length, num_rep=1000, normalized=False, alpha=0.7, beta=0.2, all_combinations=False):
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
    alpha_beta_list = generate_alpha_beta_list(alpha, beta, all_combinations)

    eta = []
    cr = []

    for i in range(num_rep):
        for alpha, beta in alpha_beta_list:
            for sigma in [0, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100]:
                exchange_rates = inst.exchange_rates_normal_from_last(phi, length, sigma)

                p = pred.opt_off_distorted(exchange_rates, alpha, beta)
                ftp = alg.FtP(k, p)

                h = History(ftp, p, exchange_rates)
                append_results(h, eta, cr, normalized)

    return eta, cr


def simulate_combined_alg(k, phi, length, alg0_name, alg1_name, lambda_list, comb_type="start", data_model="DataIterative", num_rep=1000, normalized=False, alpha=0.7, beta=0.2, all_combinations=False):
    alpha_beta_list = generate_alpha_beta_list(alpha, beta, all_combinations)

    eta = []
    cr = [[] for l in lambda_list]

    for i in tqdm(range(num_rep)):
        for alpha, beta in alpha_beta_list:
            for sigma in [0, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100]:
                if data_model == "DataIterative":
                    exchange_rates = inst.exchange_rates_normal_from_last(phi, length, sigma)
                else:  # elif inst_type == "DataUniform":
                    exchange_rates = inst.exchange_rates_uniform(phi, length)

                p = pred.opt_off_distorted(exchange_rates, alpha, beta)
                ftp = alg.FtP(k, p)
                h_ftp = History(ftp, p, exchange_rates)
                h_ftp.run_full()
                eta.append(h_ftp.get_total_error())

                for index, l in enumerate(lambda_list):
                    if alg0_name.lower() == "ftp":
                        alg0 = alg.FtP(k, p)
                    elif alg0_name.lower() == "opt":
                        alg0 = alg.OptDeterministic(k, phi)
                    else:
                        return 1

                    if alg1_name.lower() == "ftp":
                        alg1 = alg.FtP(k, p)
                    elif alg1_name.lower() == "opt":
                        alg1 = alg.OptDeterministic(k, phi)
                    else:
                        return 1

                    if comb_type.lower() == "start":
                        alg_combined = alg.CombineRandStart(k, alg0, alg1, l)
                    else:
                        alg_combined = alg.CombineRandStep(k, alg0, alg1, l)

                    h = History(alg_combined, p, exchange_rates)
                    h.run_full()
                    cr[index].append(h.get_comp_ratio())

    print(cr)

    return eta, cr


def compare_ftpl_types(k, phi, length, alg0_name, alg1_name, lambda_list, data_model="DataIterative", num_rep=1000, alpha=0.7, beta=0.2, all_combinations=False):

    alpha_beta_list = generate_alpha_beta_list(alpha, beta, all_combinations)

    eta = []
    cr = [[] for l in lambda_list]

    for i in tqdm(range(num_rep)):
        for alpha, beta in alpha_beta_list:
            for sigma in [0, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100]:
                if data_model == "DataIterative":
                    exchange_rates = inst.exchange_rates_normal_from_last(phi, length, sigma)
                else:  # elif inst_type == "DataUniform":
                    exchange_rates = inst.exchange_rates_uniform(phi, length)

                p = pred.opt_off_distorted(exchange_rates, alpha, beta)
                ftp = alg.FtP(k, p)
                h_ftp = History(ftp, p, exchange_rates)
                h_ftp.run_full()
                eta.append(h_ftp.get_total_error())

                for index, l in enumerate(lambda_list):
                    if alg0_name.lower() == "ftp":
                        alg0_start = alg.FtP(k, p)
                        alg0_step = alg.FtP(k, p)
                    elif alg0_name.lower() == "opt":
                        alg0_start = alg.OptDeterministic(k, phi)
                        alg0_step = alg.OptDeterministic(k, phi)
                    else:
                        return 1

                    if alg1_name.lower() == "ftp":
                        alg1_start = alg.FtP(k, p)
                        alg1_step = alg.FtP(k, p)
                    elif alg1_name.lower() == "opt":
                        alg1_start = alg.OptDeterministic(k, phi)
                        alg1_step = alg.OptDeterministic(k, phi)
                    else:
                        return 1

                    alg_combined_start = alg.CombineRandStart(k, alg0_start, alg1_start, l)
                    alg_combined_step = alg.CombineRandStep(k, alg0_step, alg1_step, l)

                    h_start = History(alg_combined_start, p, exchange_rates)
                    h_start.run_full()
                    h_step = History(alg_combined_step, p, exchange_rates)
                    h_step.run_full()
                    cr[index].append(h_step.get_comp_ratio() - h_start.get_comp_ratio())

    print(cr)

    return eta, cr


def simulate_combined_alg_mult(k, phi, length, alg0_name, alg1_name, lambda_list, comb_type="start",
                      data_model="DataIterative", num_rep=1000, normalized=False, alpha=0.7, beta=0.2,
                      all_combinations=False):
        eta, cr = simulate_combined_alg(k, phi, length, alg0_name, alg1_name, lambda_list, comb_type, data_model,
                                        num_rep, normalized, alpha, beta, all_combinations)


        column_names = [f"$\lambda = {l}$" for l in lambda_list]
        df = pd.DataFrame(data=np.array(cr).transpose(), index=eta, columns=column_names)
        df_avg = df.groupby(df.index).mean()

        return df_avg


def simulate_ftp_unif(k, phi, length, num_rep=1000, normalized=False, alpha=0.7, beta=0.2, all_combinations=False):
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

    alpha_beta_list = generate_alpha_beta_list(alpha, beta, all_combinations)

    eta = []
    cr = []

    for i in range(num_rep):
        for alpha, beta in alpha_beta_list:
            exchange_rates = inst.exchange_rates_uniform(phi, length)

            p = pred.opt_off_distorted(exchange_rates, alpha, beta)
            ftp = alg.FtP(k, p)

            h = History(ftp, p, exchange_rates)
            append_results(h, eta, cr, normalized)

    return eta, cr
