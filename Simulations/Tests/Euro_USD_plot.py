import matplotlib.pyplot as plt
import pickle

with open(f'Instances/Euro_USD-ftp-opt-start-k_inf-DataIterative-alpha_0.1-beta_0.45-length_10-repetitions_1000.pkl', 'rb') as inp:
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
        plt.savefig(f"Plots/EUR-USD-Combined_{inst.alg0_name}_{inst.alg1_name}_k{inst.k}_{inst.data_model}_alpha{inst.alpha}_beta{inst.beta}_length{inst.length}_repetitions{inst.num_rep}_normalized_error.pdf")
    else:
        plt.savefig(f"../Plots/EUR-USD-Combined_{inst.alg0_name}_{inst.alg1_name}_k{inst.k}_{inst.data_model}_alpha{inst.alpha}_beta{inst.beta}_length{inst.length}_repetitions{inst.num_rep}.pdf")


    plt.show()