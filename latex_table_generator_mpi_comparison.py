from styles import mpi_algorithms_excluded
from data_loader import load_mpi_results_from_file


def get_execution_times_latex_table(results):
    data_rows = ""
    for algorithm_key in results.keys():
        if algorithm_key not in mpi_algorithms_excluded:
            times = list(results[algorithm_key][default_precision].values())
            row = "\t" + algorithm_key
            row += (24 - len(row)) * " "
            for i, time in enumerate(times):
                if i * 10 not in procs_to_show:
                    continue
                string_time = f"& {time}"
                string_time += (12 - len(string_time)) * " "
                row += string_time
            row += "\\\\ \n\t\\hline \n"
            data_rows += row

    latex_table = "\\begin{table}[H]\n" \
                  "\\begin{center}\n" \
                  "\\large\n" \
                  "\\caption{Tiempos de ejecución (en segundos) de los algoritmos y librerías con " \
                  + str(default_precision) + \
                  " decimales de precisión y utilizando el paradigma de programación con MPI.}\n" \
                  "\\label{table:mpi-comparison}\n" \
                  "\\begin{tabular}{| c | c | c | c | c | c | c | c |}\n" \
                  "\\hline\n" \
                  "\t\\multirow{2}{*}{\\textbf{Algoritmo}} & \multicolumn{7}{ | c | }{\\textbf{Número de procesos}} \\\\\n" \
                  "\t\\cline{2-8} & \\textbf{1} & \\textbf{10} & \\textbf{40} & \\textbf{80} & \\textbf{120} & \\textbf{160} & \\textbf{200} \\\\\n" \
                  "\t\\hline\n" \
                  + data_rows + \
                  "\\end{tabular}\n" \
                  "\\end{center}\n" \
                  "\\end{table}\n"
    return latex_table


if __name__ == '__main__':
    # Set file and path to store the plots
    results_path = 'results/mpi/results-2022-12.csv'
    path_to_save = 'tables/mpi/'
    default_precision = 200000
    procs_to_show = [0, 10, 40, 80, 120, 160, 200]  # 0 means 1 proc

    data = load_mpi_results_from_file(results_path)

    file = open(path_to_save + "ex-comparison.tex", "w")
    file.write(get_execution_times_latex_table(data))
    file.close()
