if __name__ == '__main__':
    import Simulations.simulate as simulate
    from ftp_comparison_object import FtPComparisonObject
    import Simulations.pickle_helpers as ph

    import numpy as np
    import pandas as pd
    from decimal import *

    exchange_rates_all = pd.read_csv(r'../../Data/euro-daily-hist_1999_2021.csv')

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

    obj = FtPComparisonObject(df, k, phi, length, alg0_name, alg1_name, lambda_list, comb_type,
                              data_model, num_rep, normalized, alpha, beta, all_combinations)

    ph.save_object(obj, f"Instances/Euro_USD-{alg0_name}-{alg1_name}-{comb_type}-k_{k}-{data_model}-alpha_{alpha}-beta_{beta}-length_{length}-repetitions_{num_rep}.pkl")

