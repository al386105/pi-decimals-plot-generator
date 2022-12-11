import statistics
import styles
import matplotlib.pyplot as plt


def load_iteration_times_from_file():
    file = open(results_path, "r")

    iteration_times = []
    for line in file:
        split_line = line.split(';')
        if len(split_line) > 1:
            algorithm_tag = split_line[2]
            precision_used = split_line[3]
            generate_iteration_times_plot(algorithm_tag, iteration_times, precision_used)
            iteration_times.clear()
        else:
            iteration_times.append(float(line) * 1000)


def generate_iteration_times_plot(algorithm_name, iteration_times, precision_used):
    # Set the figure within the subplot
    fig, ax = plt.subplots(figsize=(9, 6))

    ax.plot(iteration_times)

    # Set tittles:
    plt.xlabel('Iteración', fontdict=styles.font_subtitle)
    plt.ylabel('Tiempo (ms)', fontdict=styles.font_subtitle)
    if styles.show_plots_title:
        plt.title(f"Coste de las iteraciones del algoritmo {algorithm_name} \n "
              f"para calcular los primeros {precision_used} decimales", fontdict=styles.font_title)

    # Print text with mean, median...
    text = f"Avg: {round(statistics.mean(iteration_times), 2)} ms\n" \
           f"Median: {round(statistics.median(iteration_times), 2)} ms\n" \
           f"Max: {round(max(iteration_times), 2)} ms\n" \
           f"Min: {round(min(iteration_times), 2)} ms\n" \
           f"Iterations: {len(iteration_times)}"
    plt.text(0.02, 0.97, text, ha='left', va='top', transform=ax.transAxes, fontdict=styles.font_text,
             bbox=dict(boxstyle="square", fc="w", ec="0.5", alpha=0.5))

    # Save figure and close
    plt.savefig(f"{path_to_save}it-{algorithm_name.lower()}.png")
    plt.close()


if __name__ == '__main__':
    # Set file and path to store the plots
    results_path = 'results/iterations/omp-iterations-2022-12-a.csv'
    path_to_save = 'plots/iterations/'

    load_iteration_times_from_file()
