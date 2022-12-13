from data_loader import load_omp_results_from_file
import matplotlib.pyplot as plt
import numpy as np
import styles


def generate_algorithm_plots(results):
    # For each algorithm, generate the times plot and the speed_up plot
    for algorithm_key in results.keys():
        exec_times = dict()  # exec_times = { precision : list_ex_times }
        speed_ups = dict()   # speed_ups  = { precision : list_speed_ups }
        threads_used = list(results[algorithm_key][50000].keys())

        # For each precision, prepare the list of ex_times and compute the speed_ups
        for precision_key in results[algorithm_key].keys():
            exec_times[precision_key] = list(results[algorithm_key][precision_key].values())
            precision_speed_ups = [exec_times[precision_key][0] / exec_times[precision_key][i] for i in range(len(exec_times[precision_key]))]
            speed_ups[precision_key] = precision_speed_ups

        # Generate execution times plot and speed up plots
        generate_execution_times_plot(algorithm_key, threads_used, exec_times)
        generate_speed_up_plot(algorithm_key, threads_used, speed_ups)


def generate_speed_up_plot(algorithm_name, threads_used, speed_ups):
    # Set the figure within the subplot
    fig, ax = plt.subplots(figsize=(9, 6))

    # Draw the speed-up values for each precision
    i = 0
    for precision in speed_ups.keys():
        ax.plot(threads_used, speed_ups[precision], color=styles.color_lines[i], marker=styles.marker_styles[i],
                linestyle='solid', linewidth=1.5, markersize=5, label=f"prec. {precision}")
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
        plt.title(f"Escalabilidad del algoritmo {algorithm_name}", fontdict=styles.font_title)

    # Show legend
    plt.legend(loc='upper left')

    # Save figure and close
    plt.savefig(f"{path_to_save}su-{algorithm_name.lower()}.png")
    plt.close()


def generate_execution_times_plot(algorithm_name, threads_used, execution_times):
    # Set the figure within the subplot
    fig, ax = plt.subplots(figsize=(9, 6))

    # Draw the execution times for each precision
    i = 0
    for precision in execution_times.keys():
        ax.plot(threads_used, execution_times[precision], color=styles.color_lines[i], marker=styles.marker_styles[i],
                linestyle='solid', linewidth=1.5, markersize=5, label=f"prec. {precision}")
        i += 1

    # Set axis limits and steps
    plt.xticks(np.arange(0, max(threads_used) + 1, 2))
    ax.set_xlim([0, max(threads_used) + 1])
    plt.grid(axis='y')

    # Set tittles:
    plt.xlabel('Número de hebras ', fontdict=styles.font_subtitle)
    plt.ylabel('Tiempo de ejecución (s)', fontdict=styles.font_subtitle)
    if styles.show_plots_title:
        plt.title(f"Tiempos de ejecución del algoritmo {algorithm_name}", fontdict=styles.font_title)

    # Set logarithmic scale on y
    plt.yscale('log')

    # Show legend
    plt.legend(loc='upper right')

    # plt.show()
    plt.savefig(f"{path_to_save}ex-{algorithm_name.lower()}.png")
    plt.close()


if __name__ == '__main__':
    # Set file and path to store the plots
    results_path = 'results/omp/results-2022-12.csv'
    path_to_save = 'plots/omp/'

    data = load_omp_results_from_file(results_path)
    generate_algorithm_plots(data)
