import Simulations.algorithms as alg
import Simulations.plots
import Simulations.simulate as simulate
import numpy as np

import Simulations.pickle_helpers as ph


if __name__ == '__main__':
    from ftp_comparison_object import FtPComparisonObject

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

    obj = FtPComparisonObject(df, k, phi, length, alg0_name, alg1_name, lambda_list, comb_type,
                                             data_model, num_rep, normalized, alpha, beta, all_combinations)

    ph.save_object(obj, f"Instances/Combined-{alg0_name}-{alg1_name}-{comb_type}-k_{k}-{data_model}-alpha_{alpha}-beta_{beta}-length_{length}-repetitions_{num_rep}.pkl")
