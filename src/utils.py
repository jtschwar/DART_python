import numpy as np
from os import listdir
import matplotlib.pyplot as plt

def main():
    res_path = "results/angle_range/clouds"
    labels = ["DART_fbp", "DART_sart", "DART_sirt", "FBP", "SART", "SIRT"]
    tick_labels = [10, 20, 40, 60, 100, 120, 150, 180]
    #tick_labels = np.round([(label/53418)*100 for label in tick_labels],1)

    title="Effect of angle range on cloud phantoms"
    xlabel="Angle range"
    ylabel="Mean Absolute Pixel Error"
    ylim=100
    save_name= "plots_for_report/temp.png"
    
    plot_results(res_dir=res_path, labels=labels, 
                tick_labels=tick_labels,
                title=title, xlabel=xlabel, ylabel=ylabel,
                ylim=ylim, save_name=save_name)


def plot_results(res_dir, labels=None, tick_labels=None,
                title=None, use_log=False, 
                xlabel=None, ylabel=None, ylim=50,
                save_name="plots_for_report/temp.png"):
    """ Creates a plot for experiments, given the file structure:
            - res_path/
                -- exp_0/
                    --- alg_0.npy
                    --- alg_1.npy
                --exp_1/
                    --- alg_0.npy
                    --- alg_1.npy
                ...
    """
    #check path
    if res_dir[-1] != "/":
        res_dir += "/"

    family_subdirs = sorted(listdir(res_dir))
    print("\nConsidered subdirectories:",family_subdirs)
    alg_names = sorted(listdir(res_dir+family_subdirs[0]))
    n_algs = len(sorted(listdir(res_dir+family_subdirs[0])))
    
    # define figure
    plt.figure(figsize=(8,6))
    
    counter = 0
    # iterate over each algorithm
    for i in range(n_algs):
        curr_alg_errs = []
        # iterate over each experiment
        for curr_dir in family_subdirs:
            curr_dir = res_dir + curr_dir + "/"
            dir_files = sorted(listdir(curr_dir))
            # take only files relevant to current algorithm
            for filename in dir_files:
                if alg_names[i] not in filename:
                    continue
                if '.npy' in filename:
                    curr_alg_errs.append(np.load(curr_dir+filename))

        # define values to plot
        means = np.mean(curr_alg_errs, axis=0)
        maxs = np.max(curr_alg_errs, axis=0)
        mins = np.min(curr_alg_errs, axis=0)
        if use_log:
            means = np.log(means)
            maxs = np.log(maxs)
            mins = np.log(mins)
        # debug print
        print(alg_names[i])

        # plotting styles
        if alg_names[i] == "RBF":
            alg_names[i] = "FBP"
        if "DART" in alg_names[i]:
            line = "solid"
            if "sirt" in alg_names[i]:
                line = "--"
        elif "DART" not in alg_names[i] and "SART" in alg_names[i] or "SIRT" in alg_names[i]:
            line = "dotted"
        else: line = "dashdot"
        if "FBP" in alg_names[i] or "fbp" in alg_names[i]:
            line = "dashdot"
        lab = alg_names[i] if labels == None else labels[i]
        # plot main mean trend of algorithm
        plt.plot(means, label=lab, 
                linestyle=line,
                linewidth=5)
        # fill values between min/max
        plt.fill_between(range(len(means)), mins, maxs, alpha=0.2)

        # update control params
        curr_alg_errs = []
        counter += 1

    plt.legend(fontsize=12)
    plt.title(title, fontsize=18)
    plt.xlabel(xlabel, fontsize=16)
    plt.ylabel(ylabel, fontsize=16)
    plt.xticks(ticks=range(len(means)) ,labels=tick_labels, fontsize=14)
    plt.yticks( fontsize=14)
    if ylim:
        plt.ylim([0, ylim])
    plt.margins(x=0, y=0)
    plt.savefig(save_name)

if __name__ == "__main__":
    main()