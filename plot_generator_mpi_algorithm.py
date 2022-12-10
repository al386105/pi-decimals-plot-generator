import statistics
import matplotlib.pyplot as plt
import numpy as np
import styles

# This function returns a dictionary with the executions results median of any algorithm
#     results = {'algorithm_tag' : { precision : { procs_used  { median_execution_time } } }

def load_results_from_file():
    file = open(results_path, "r")

    results = dict()

    # Iterate the file results, each line file is an execution result and store it in a dictionary
    for line_result in file:
        split_line = line_result.split(';')
        algorithm_tag = split_line[2]
        precision_used = int(split_line[3])
        procs_used = int(split_line[5])
        threads_used = int(split_line[6])
        decimals_computed = int(split_line[7])
        execution_time = float(split_line[8])

        # Check if the decimals computed are greater than the desired:
        if precision_used > decimals_computed:
            print("Something went wrong! It looks like some executions did not go as expected.")
            print(f"Check {algorithm_tag} algorithm")
            exit(-1)

        if threads_used > 1:
            print("Something went wrong! It looks like some executions use more than one thread (hybrid) ")
            exit(-1)

        if algorithm_tag not in results:
            results[algorithm_tag] = dict()

        if precision_used not in results[algorithm_tag]:
            results[algorithm_tag][precision_used] = dict()

        if procs_used not in results[algorithm_tag][precision_used]:
            results[algorithm_tag][precision_used][procs_used] = []

        results[algorithm_tag][precision_used][procs_used].append(execution_time)

    # Finally, replace the execution times with the median of them in the same dictionary
    for algorithm_key in results.keys():
        for precision_key in results[algorithm_key]:
            for procs_key in results[algorithm_key][precision_key]:
                results[algorithm_key][precision_key][procs_key] = \
                    statistics.median(results[algorithm_key][precision_key][procs_key])

    return results


def generate_algorithm_plots(results):
    # For each algorithm, generate the times plot and the speed_up plot
    for algorithm_key in results.keys():
        exec_times = dict()  # exec_times = { precision : list_ex_times }
        speed_ups = dict()   # speed_ups  = { precision : list_speed_ups }
        procs_used = list(results[algorithm_key][50000].keys())

        # For each precision, prepare the list of ex_times and compute the speed_ups
        for precision_key in results[algorithm_key].keys():
            exec_times[precision_key] = list(results[algorithm_key][precision_key].values())
            precision_speed_ups = list()
            for i in range(len(exec_times[precision_key])):
                precision_speed_ups.append(exec_times[precision_key][0] / exec_times[precision_key][i])
            speed_ups[precision_key] = precision_speed_ups

        # Generate execution times plot and speed up plots
        generate_execution_times_plot(algorithm_key, procs_used, exec_times)
        generate_speed_up_plot(algorithm_key, procs_used, speed_ups)


def generate_speed_up_plot(algorithm_name, procs_used, speed_ups):
    # Set the figure within the subplot
    fig, ax = plt.subplots(figsize=(9, 6))

    # Draw the speed-up values for each precision
    i = 0
    for precision in speed_ups.keys():
        ax.plot(procs_used, speed_ups[precision], color=styles.COLOR_LINES[i], marker=styles.MARKER_STYLES[i],
                linestyle='solid', linewidth=1.5, markersize=5, label=f"prec. {precision}")
        i += 1

    # Set axis limits and steps
    plt.xticks(np.arange(0, max(procs_used) + 1, 10))
    plt.yticks(np.arange(0, max(procs_used) + 1, 10))
    ax.set_ylim([0, max(procs_used) + 1])
    ax.set_xlim([0, max(procs_used) + 1])
    plt.grid(axis='y')

    # Set tittles:
    plt.xlabel('Número de procesos', fontdict=styles.FONT_SUBTITLE)
    plt.ylabel('Escalabilidad ', fontdict=styles.FONT_SUBTITLE)
    plt.title(f"Escalabilidad del algoritmo {algorithm_name}", fontdict=styles.FONT_TITLE)

    # Show legend
    plt.legend(loc='upper left')

    # Save figure and close
    plt.savefig(f"{path_to_save}SU-{algorithm_name}.png")
    plt.close()


def generate_execution_times_plot(algorithm_name, procs_used, execution_times):
    # Set the figure within the subplot
    fig, ax = plt.subplots(figsize=(9, 6))

    # Draw the execution times for each precision
    i = 0
    for precision in execution_times.keys():
        ax.plot(procs_used, execution_times[precision], color=styles.COLOR_LINES[i], marker=styles.MARKER_STYLES[i],
                linestyle='solid', linewidth=1.5, markersize=5, label=f"prec. {precision}")
        i += 1

    # Set axis limits and steps
    plt.xticks(np.arange(0, max(procs_used) + 1, 10))
    ax.set_xlim([0, max(procs_used) + 1])
    plt.grid(axis='y')

    # Set tittles:
    plt.xlabel('Número de procesos', fontdict=styles.FONT_SUBTITLE)
    plt.ylabel('Tiempo de ejecución (s)', fontdict=styles.FONT_SUBTITLE)
    plt.title(f"Tiempos de ejecución del algoritmo {algorithm_name}", fontdict=styles.FONT_TITLE)

    # Set logarithmic scale on y
    plt.yscale('log')

    # Show legend
    plt.legend(loc='upper right')

    # plt.show()
    plt.savefig(f"{path_to_save}EX-{algorithm_name}.png")
    plt.close()


if __name__ == '__main__':
    # Set file and path to store the plots
    results_path = 'results/mpi/results-2022-12.csv'
    path_to_save = 'plots/mpi/'

    data = load_results_from_file()
    generate_algorithm_plots(data)
