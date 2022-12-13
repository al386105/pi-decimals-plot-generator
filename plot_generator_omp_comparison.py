from data_loader import load_omp_results_from_file
import matplotlib.pyplot as plt
import numpy as np
import styles


def generate_comparison_speed_up_plot(threads_used, speed_ups):
    # Set the figure within the subplot
    fig, ax = plt.subplots(figsize=(9, 6))

    # Draw the speed-up values for each precision
    i = 0
    for algorithm in speed_ups.keys():
        ax.plot(threads_used, speed_ups[algorithm], color=styles.color_lines[i], marker=styles.marker_styles[i], linestyle='solid',
                linewidth=1.5, markersize=5, label=algorithm)
        i += 1

    # Set axis limits and steps
    plt.xticks(np.arange(0, max(threads_used) + 1, 2))
    plt.yticks(np.arange(0, max(threads_used) + 1, 2))
    ax.set_ylim([0, max(threads_used) + 1])
    ax.set_xlim([0, max(threads_used) + 1])
    plt.grid(axis='y')

    # Set tittles:
    plt.xlabel('Número de hebras', fontdict=styles.font_subtitle)
    plt.ylabel('Escalabilidad ', fontdict=styles.font_subtitle)
    if styles.show_plots_title:
        plt.title("Comparación de la escalabilidad de los algoritmos \n con el paradigma de OpenMP", fontdict=styles.font_title)

    # Show legend
    plt.legend(loc='upper left')

    # Save figure and close
    plt.savefig(f"{path_to_save}su-comparison.png")
    plt.close()


def generate_comparison_execution_times_plot(threads_used, execution_times):
    # Set the figure within the subplot
    fig, ax = plt.subplots(figsize=(9, 6))

    # Draw the execution times for each precision
    i = 0
    for algorithm in execution_times.keys():
        ax.plot(threads_used, execution_times[algorithm], color=styles.color_lines[i], marker=styles.marker_styles[i],
                linestyle='solid', linewidth=1.5, markersize=5, label=algorithm)
        i += 1

    # Set axis limits and steps
    plt.xticks(np.arange(0, max(threads_used) + 1, 2))
    ax.set_xlim([0, max(threads_used) + 1])
    plt.grid(axis='y')

    # Set tittles:
    plt.xlabel('Número de hebras', fontdict=styles.font_subtitle)
    plt.ylabel('Tiempo de ejecución (s)', fontdict=styles.font_subtitle)
    if styles.show_plots_title:
        plt.title("Comparación de los tiempos de ejecución de los algoritmos \n con el paradigma de OpenMP", fontdict=styles.font_title)

    # Set logarithmic scale on y
    plt.yscale('log')

    # Show legend
    plt.legend(loc='upper right')

    # plt.show()
    plt.savefig(f"{path_to_save}ex-comparison.png")
    plt.close()


if __name__ == '__main__':
    # Set file and path to store the plots
    results_path = 'results/omp/results-2022-12.csv'
    path_to_save = 'plots/omp/'

    data = load_omp_results_from_file(results_path)

    # Generate the times plot and the speed_up plot
    exec_times = dict()  # exec_times = { algorithm_tag : list_ex_times }
    speed_ups = dict()   # speed_ups  = { algorithm_tag : list_speed_ups }
    threads_used = list()

    for algorithm_key in data.keys():
        exec_times[algorithm_key] = list(data[algorithm_key][styles.default_comparison_precision].values())
        threads_used = list(data[algorithm_key][styles.default_comparison_precision].keys())
        algorithm_speed_ups = [exec_times[algorithm_key][0] / exec_times[algorithm_key][i] for i in range(len(exec_times[algorithm_key]))]
        speed_ups[algorithm_key] = algorithm_speed_ups

    # Generate execution times plot and speed up plots
    generate_comparison_execution_times_plot(threads_used, exec_times)
    generate_comparison_speed_up_plot(threads_used, speed_ups)