import algorithms as alg
import offline as off
import predictions as pred
import copy

import numpy as np


class History():
    def __init__(self, algo, exchange_rates):
        self.alg = copy.deepcopy(algo)
        self.exchange_rates = exchange_rates
        self.states = []
        self.payoffs = []
        self.xs = []
        self.errors = []
        opt_pred = pred.opt_off(self.exchange_rates)
        self.opt_off = alg.FtP(opt_pred)

    def update_states(self):
        self.states.append(self.alg.state)

    def update_payoffs(self):
        self.payoffs.append(self.alg.payoff)

    def update_xs(self):
        self.xs.append(self.alg.x)

    def update_errors(self, opt_off):
        self.errors.append(off.get_error_in_step(self.alg, opt_off))

    def run_step(self, exchange_rate):
        self.alg.run(exchange_rate)
        self.update_payoffs()
        self.update_xs()
        self.update_states()

    def run_full(self):
        for e in self.exchange_rates:
            self.run_step(e)
            self.opt_off.run(e)
            self.update_errors(self.opt_off)

    def get_total_error(self):
        return np.sum(self.errors)

    def get_return(self):
        return self.alg.payoff

    def get_comp_ratio(self):
        return self.opt_off.payoff / self.alg.payoff

    def get_normalized_error(self):
        return self.get_total_error() / self.opt_off.payoff

    def get_results_str(self):
        return f"return = {self.get_return()}, off return = {self.opt_off.payoff}, competitive ratio = {self.get_comp_ratio()}, eta = {self.get_total_error()}"



