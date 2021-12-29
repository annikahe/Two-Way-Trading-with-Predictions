import algorithms as alg
import offline as off
import predictions as pred


def alg_return(algo, exchange_rates):
    for e in exchange_rates:
        algo.run(e)

    return algo.payoff


def run_algo_and_compare_to_off(algo, exchange_rates):
    off_pred = pred.opt_off(exchange_rates)
    opt_off = alg.FtP(off_pred)

    error = 0
    for e in exchange_rates:
        algo.run(e)
        opt_off.run(e)
        error += off.get_error_in_step(algo, opt_off)


