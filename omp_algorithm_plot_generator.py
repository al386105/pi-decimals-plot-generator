import statistics
import matplotlib.pyplot as plt
import numpy as np


# This function returns a dictionary with the executions results median of any algorithm
#     results = {'algorithm_tag' : { precision : { threads_used : median_execution_time } } } }
#     results = {'GMP-BBP-BEL-BLC' : {50000 : {1 : 20.5, 2 : 10.8, 4 : 6.1}} }

def load_results_from_file():
    file = open(path + file_name, "r")

    results = dict()

    # Iterate the file results, each line file is an execution result and store it in a dictionary
    for line_result in file:
        split_line = line_result.split(';')
        algorithm_tag = split_line[2]
        precision_used = int(split_line[3])
        threads_used = int(split_line[5])
        decimals_computed = int(split_line[6])
        execution_time = float(split_line[7])

        # Check if the decimals computed are greater than the desired:
        if precision_used > decimals_computed:
            print("Something went wrong! It looks like some executions did not go as expected.")
            print(f"Check {algorithm_tag} algorithm")

        if algorithm_tag not in results:
            results[algorithm_tag] = dict()

        if precision_used not in results[algorithm_tag]:
            results[algorithm_tag][precision_used] = dict()

        if threads_used not in results[algorithm_tag][precision_used]:
            results[algorithm_tag][precision_used][threads_used] = []
        results[algorithm_tag][precision_used][threads_used].append(execution_time)

    # Finally, replace the execution times with the median of them in the same dictionary
    for algorithm_key in results.keys():
        for precision_key in results[algorithm_key]:
            for thread_key in results[algorithm_key][precision_key]:
                results[algorithm_key][precision_key][thread_key] = statistics.median(
                    results[algorithm_key][precision_key][thread_key])

    return results


def generate_algorithm_plots(results):
    for algorithm_key in results.keys():
        exec_times_based_on_prec = dict()
        speed_up_based_on_prec = dict()
        for precision_key in results[algorithm_key].keys():
            exec_times_based_on_prec[precision_key] = list(results[algorithm_key][precision_key].values())
            speed_ups = list()
            for i in range(len(exec_times_based_on_prec[precision_key])):
                speed_ups.append(
                    exec_times_based_on_prec[precision_key][0] / exec_times_based_on_prec[precision_key][i])
            speed_up_based_on_prec[precision_key] = speed_ups

        generate_execution_times_plot(algorithm_name=algorithm_key,
                                      threads_used=list(results[algorithm_key][50000].keys()),
                                      execution_times=exec_times_based_on_prec)
        generate_speed_up_plot(algorithm_name=algorithm_key,
                               threads_used=list(results[algorithm_key][50000].keys()),
                               speed_ups=speed_up_based_on_prec)


def generate_speed_up_plot(algorithm_name, threads_used, speed_ups, show_title=True):
    # Set the figure within the subplot
    fig, ax = plt.subplots(figsize=(9, 6))

    # Draw the speed-up values for each precision
    i = 0
    for precision in speed_ups.keys():
        ax.plot(threads_used, speed_ups[precision], color=color_lines[i], marker=marker_styles[i], linestyle='solid',
                linewidth=1.5, markersize=5, label=f"prec. {precision}")
        i += 1

    # Set axis limits and steps
    plt.xticks(np.arange(0, max(threads_used) + 1, 2))
    plt.yticks(np.arange(0, max(threads_used) + 1, 2))
    ax.set_ylim([0, max(threads_used) + 1])
    ax.set_xlim([0, max(threads_used) + 1])
    plt.grid(axis='y')

    # Set tittles:
    plt.xlabel('Número de hebras ', fontdict=font_subtitle)
    plt.ylabel('Escalabilidad ', fontdict=font_subtitle)
    plt.title(f"Escalabilidad del algoritmo {algorithm_name}", fontdict=font_title)

    # Show legend
    plt.legend(loc='upper left')

    # Save figure and close
    plt.savefig(f"{path}SU-{algorithm_name}.png")
    plt.close()


def generate_execution_times_plot(algorithm_name, threads_used, execution_times):
    # Set the figure within the subplot
    fig, ax = plt.subplots(figsize=(9, 6))

    # Draw the execution times for each precision
    i = 0
    for precision in execution_times.keys():
        ax.plot(threads_used, execution_times[precision], color=color_lines[i], marker=marker_styles[i],
                linestyle='solid', linewidth=1.5, markersize=5, label=f"prec. {precision}")
        i += 1

    # Set axis limits and steps
    plt.xticks(np.arange(0, max(threads_used) + 1, 2))
    ax.set_xlim([0, max(threads_used) + 1])
    # ax.set_ylim([execution_times[50000][-1], execution_times[200000][0]])
    plt.grid(axis='y')

    # Set tittles:
    plt.xlabel('Número de hebras ', fontdict=font_subtitle)
    plt.ylabel('Tiempo de ejecución (s)', fontdict=font_subtitle)
    plt.title(f"Tiempos de ejecución del algoritmo {algorithm_name}", fontdict=font_title)

    # Set logarithmic scale on y
    plt.yscale('log')

    # Show legend
    plt.legend(loc='upper right')

    # plt.show()
    plt.savefig(f"{path}EX-{algorithm_name}.png")
    plt.close()


if __name__ == '__main__':
    # Set file and path to store the plots
    path = 'results/omp-2022-12/'
    file_name = 'results-pi-decimals-2022-12.csv'

    # Define the styles
    color_lines = ['#5383EC', '#D85040', '#F2BF41']
    marker_styles = ['o', '^', 's']
    font_title = {'family': 'serif', 'color': 'black', 'weight': 'bold', 'size': 12}
    font_subtitle = {'family': 'serif', 'color': 'black', 'weight': 'normal', 'size': 11}
    font_text = {'family': 'serif', 'color': 'black', 'weight': 'normal', 'size': 11}

    data = load_results_from_file()
    generate_algorithm_plots(data)
