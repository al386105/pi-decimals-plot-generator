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
            # We can discard the thread distribution because the result is of a single thread
            thread_distribution = algorithm_tag.split('-')[-1]
            algorithm_tag = algorithm_tag[:-(len(thread_distribution) + 1)]
            precision_used = split_line[3]
            generate_iteration_times_plot(algorithm_tag, iteration_times, precision_used)
            iteration_times.clear()
        else:
            iteration_times.append(float(line) * 1000)  # In millis


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
    text = f"Media: {round(statistics.mean(iteration_times), 2)} ms\n" \
           f"Mediana: {round(statistics.median(iteration_times), 2)} ms\n" \
           f"Max: {round(max(iteration_times), 2)} ms\n" \
           f"Min: {round(min(iteration_times), 2)} ms\n" \
           f"Iteraciones: {len(iteration_times)}"
    plt.text(0.75, 0.5, text, ha='left', va='center', transform=ax.transAxes, fontdict=styles.font_text,
             bbox=dict(boxstyle="square", fc="w", ec="0.5", alpha=0.5))

    # Save figure and close
    plt.savefig(f"{styles.path_to_save_plots}it-{algorithm_name.lower()}.png")
    plt.close()


if __name__ == '__main__':
    # Set file and path to store the plots
    results_path = 'results/omp-iterations-2022-12.csv'

    load_iteration_times_from_file()
