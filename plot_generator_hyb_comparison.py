from data_loader import load_hyb_results_from_file
import matplotlib.pyplot as plt
import numpy as np
import styles


def generate_comparison_speed_up_plot(procs_threads_used, speed_ups):
    # Set the figure within the subplot
    fig, ax = plt.subplots(figsize=(9, 6))

    # Draw the speed-up values for each precision
    i = 0
    for algorithm in speed_ups.keys():
        ax.plot(procs_threads_used, speed_ups[algorithm], color=styles.color_lines[i], marker=styles.marker_styles[i],
                linestyle='solid', linewidth=1.5, markersize=5, label=algorithm)
        i += 1

    # Set axis limits and steps
    plt.yticks(np.arange(0, 200, 10))
    plt.xticks(rotation=30)
    ax.set_ylim([0, 200])
    plt.grid(axis='y')

    # Set tittles:
    plt.xlabel('Número de procesos/hebras', fontdict=styles.font_subtitle)
    plt.ylabel('Escalabilidad ', fontdict=styles.font_subtitle)
    if styles.show_plots_title:
        plt.title("Comparación de la escalabilidad de los algoritmos \n con el paradigma híbrido", fontdict=styles.font_title)

    # Show legend
    plt.legend(loc='upper left')

    # Save figure and close
    plt.savefig(f"{styles.path_to_save_plots}su-hyb-comparison.png")
    plt.close()


def generate_comparison_execution_times_plot(procs_threads_used, execution_times):
    # Set the figure within the subplot
    fig, ax = plt.subplots(figsize=(9, 6))

    # Draw the execution times for each precision
    i = 0
    for algorithm in execution_times.keys():
        ax.plot(procs_threads_used, execution_times[algorithm], color=styles.color_lines[i], marker=styles.marker_styles[i],
                linestyle='solid', linewidth=1.5, markersize=5, label=algorithm)
        i += 1

    # Set axis limits and steps
    plt.xticks(rotation=30)
    plt.grid(axis='y')

    # Set tittles:
    plt.xlabel('Número de procesos/hebras', fontdict=styles.font_subtitle)
    plt.ylabel('Tiempo de ejecución (s)', fontdict=styles.font_subtitle)
    if styles.show_plots_title:
        plt.title("Comparación de los tiempos de ejecución de los algoritmos \n con el paradigma híbrido", fontdict=styles.font_title)

    # Set logarithmic scale on y
    plt.yscale('log')

    # Show legend
    plt.legend(loc='upper right')

    # plt.show()
    plt.savefig(f"{styles.path_to_save_plots}ex-hyb-comparison.png")
    plt.close()


if __name__ == '__main__':
    data = load_hyb_results_from_file(styles.hyb_results_file)

    # Generate the times plot and the speed_up plot
    exec_times = dict()  # exec_times = { algorithm_tag : list_ex_times }
    speed_ups = dict()   # speed_ups  = { algorithm_tag : list_speed_ups }
    procs_threads_used = []
    for algorithm_key in data.keys():
        list_ex_times = []
        procs_threads_used = []
        for procs_key in data[algorithm_key][styles.default_comparison_precision].keys():
            for threads_key in data[algorithm_key][styles.default_comparison_precision][procs_key]:
                procs_threads_used.append(f'{procs_key}/{threads_key}')
                list_ex_times.append(data[algorithm_key][styles.default_comparison_precision][procs_key][threads_key])
        exec_times[algorithm_key] = list_ex_times
        algorithm_speed_ups = [exec_times[algorithm_key][0] / exec_times[algorithm_key][i] for i in range(len(exec_times[algorithm_key]))]
        speed_ups[algorithm_key] = algorithm_speed_ups

    # Generate execution times plot and speed up plots
    generate_comparison_execution_times_plot(procs_threads_used, exec_times)
    generate_comparison_speed_up_plot(procs_threads_used, speed_ups)