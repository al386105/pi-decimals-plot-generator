import styles
from styles import mpi_algorithms_excluded, default_comparison_precision
from data_loader import load_mpi_results_from_file


def get_execution_times_latex_table(results):
    data_rows = ""
    for algorithm_key in results.keys():
        if algorithm_key not in mpi_algorithms_excluded:
            times = list(results[algorithm_key][default_comparison_precision].values())
            row = "\t" + algorithm_key
            row += (24 - len(row)) * " "
            for i, time in enumerate(times):
                if i * 10 in procs_to_show:
                    string_time = f"& {round(time, 2)}"
                    string_time = string_time.replace('.', ',')
                    string_time += (12 - len(string_time)) * " "
                    row += string_time
            row += "\\\\ \n\t\\hline \n"
            data_rows += row

    latex_table = "\\begin{table}[H]\n" \
                  "\\begin{center}\n" \
                  "\\large\n" \
                  "\\caption{Tiempos de ejecución (en segundos) de los algoritmos y librerías con " \
                  + "{:,}".format(default_comparison_precision).replace(",", ".") + \
                  " decimales de precisión, utilizando el paradigma de programación con MPI}\n" \
                  "\\label{table:ex-mpi-comparison}\n" \
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


def get_speed_ups_latex_table(results):
    data_rows = ""
    for algorithm_key in results.keys():
        if algorithm_key not in mpi_algorithms_excluded:
            times = list(results[algorithm_key][default_comparison_precision].values())
            speed_ups = [times[0] / times[i] for i in range(len(times))]
            row = "\t" + algorithm_key
            row += (24 - len(row)) * " "
            for i, speed_up in enumerate(speed_ups):
                if i * 10 in procs_to_show:
                    string_su = f"& {round(speed_up, 2)}"
                    string_su = string_su.replace('.', ',')
                    string_su += (12 - len(string_su)) * " "
                    row += string_su
            row += "\\\\ \n\t\\hline \n"
            data_rows += row

    latex_table = "\\begin{table}[H]\n" \
                  "\\begin{center}\n" \
                  "\\large\n" \
                  "\\caption{Escalabilidad de los algoritmos y librerías con " \
                  + str(default_comparison_precision) + \
                  " decimales de precisión, utilizando el paradigma de programación con MPI}\n" \
                  "\\label{table:su-mpi-comparison}\n" \
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
    results_path = styles.mpi_results_file
    path_to_save = styles.path_to_save_tables
    procs_to_show = [0, 10, 40, 80, 120, 160, 200]  # 0 means 1 proc

    data = load_mpi_results_from_file(results_path)

    file = open(path_to_save + "ex-mpi-comparison.tex", "w")
    file.write(get_execution_times_latex_table(data))
    file.close()

    file = open(path_to_save + "su-mpi-comparison.tex", "w")
    file.write(get_speed_ups_latex_table(data))
    file.close()
