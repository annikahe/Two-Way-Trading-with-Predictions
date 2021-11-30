class FtPComparisonObject:
    def __init__(self, df, k, phi, length, alg0_name, alg1_name, lambda_list, comb_type,
                 data_model, num_rep, normalized, alpha, beta, all_combinations):
        self.df = df
        self.k = k
        self.phi = phi
        self.length = length
        self.alg0_name = alg0_name
        self.alg1_name = alg1_name
        self.lambda_list = lambda_list
        self.comb_type = comb_type
        self.data_model = data_model
        self.num_rep = num_rep
        self.normalized = normalized
        self.alpha = alpha
        self.beta = beta
        self.all_combinations = all_combinations