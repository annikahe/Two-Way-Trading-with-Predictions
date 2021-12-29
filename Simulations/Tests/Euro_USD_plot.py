import matplotlib.pyplot as plt
import pickle

"Instances/Euro_USD-{alg0_name}-{alg1_name}-{comb_type}-k_{k}-{data_model}-alpha_{alpha}-beta_{beta}-length_{length}-repetitions_{num_rep}.pkl"

ks = [1, 2, 4, 8, 16, 32, 64, 128, 256, "inf"]

for k in ks:
    with open(f'Instances/Euro_USD-ftp-opt-step-k_{k}-DataIterative-alpha_[0.7, 0.1, 0.1]-beta_[0.2, 0.45, 0.1]-length_100-repetitions_10.pkl', 'rb') as inp:
        inst = pickle.load(inp)
        print(inst.df)

        ax = inst.df.plot()

        xlim = ax.get_xlim()
        x = range(int(xlim[1]) + 1)
        y = [(inst.phi ** (err / 2)) for err in x]
        plt.plot(x, y, label="Competitive Ratio of FtP", color="k")
        plt.legend()

        plt.yscale("log")
        ax.set_ylabel("$return(OFF) / return(A)$")
        plt.setp(ax.lines, linewidth=1)

        if inst.normalized:
            plt.savefig(f"Plots/Euro_USD-{inst.alg0_name}-{inst.alg1_name}-k_{inst.k}-{inst.data_model}-alpha_{inst.alpha}-beta_{inst.beta}-length_{inst.length}-repetitions_{inst.num_rep}-normalized_error.pdf")
        else:
            plt.savefig(f"../Plots/Euro_USD-{inst.alg0_name}-{inst.alg1_name}-k_{inst.k}-{inst.data_model}-alpha_{inst.alpha}-beta_{inst.beta}-length_{inst.length}-repetitions_{inst.num_rep}.pdf")


        plt.show()