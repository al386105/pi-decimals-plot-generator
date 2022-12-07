import matplotlib.pyplot as plt
import styles


def load_iteration_times_from_file():
    file = open(path + file_name, "r")

    iteration_times = []
    for line in file:
        split_line = line.split(';')
        if len(split_line) > 1:
            algorithm_tag = split_line[2]
            generate_iteration_times_plot(algorithm_tag, iteration_times)
            iteration_times.clear()
        else:
            iteration_times.append(float(line))


def generate_iteration_times_plot(algorithm_name, iteration_times):
    # Set the figure within the subplot
    fig, ax = plt.subplots(figsize=(9, 6))

    ax.plot(iteration_times)

    # Set tittles:
    plt.xlabel('Iteración', fontdict=styles.FONT_SUBTITLE)
    plt.ylabel('Tiempo (s)', fontdict=styles.FONT_SUBTITLE)
    plt.title(f"Coste de las iteraciones del algoritmo {algorithm_name}", fontdict=styles.FONT_TITLE)

    # Save figure and close
    plt.savefig(f"{path}IT-{algorithm_name}.png")
    plt.close()


if __name__ == '__main__':
    # Set file and path to store the plots
    path = 'results/iterations-2022-12/'
    file_name = 'omp-iterations.csv'

    load_iteration_times_from_file()
