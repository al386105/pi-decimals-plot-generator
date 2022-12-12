from data_loader import load_mpi_results_from_file


def get_execution_time_latex_table(algorithm_tag, results):
    data_rows = ""
    for precision_key in results.keys():
        times = list(results[precision_key].values())
        row = "\t" + str(precision_key)
        row += (8 - len(row)) * " "
        for i, time in enumerate(times):
            if i * 10 not in procs_to_show:
                continue
            string_time = f"& {round(time, 2)}"
            string_time.replace('.', ',')
            string_time += (12 - len(string_time)) * " "
            row += string_time
        row += "\\\\ \n\t\\hline \n"
        data_rows += row

    latex_table = "\\begin{table}[H]\n" \
                  "\\begin{center}\n" \
                  "\\large\n" \
                  "\\caption{Tiempos de ejecución (en segundos) del algoritmo " \
                  + algorithm_tag + \
                  " utilizando el paradigma de programación con MPI.}\n" \
                  "\\label{" \
                  f"table:ex-mpi-{algorithm_tag.lower()}" \
                  "}\n" \
                  "\\begin{tabular}{| c | c | c | c | c | c | c | c |}\n" \
                  "\\hline\n" \
                  "\t\\multirow{2}{*}{\\textbf{Precisión}} & \multicolumn{7}{ | c | }{\\textbf{Número de procesos}} \\\\\n" \
                  "\t\\cline{2-8} & \\textbf{1} & \\textbf{10} & \\textbf{40} & \\textbf{80} & \\textbf{120} & \\textbf{160} & \\textbf{200} \\\\\n" \
                  "\t\\hline\n" \
                  + data_rows + \
                  "\\end{tabular}\n" \
                  "\\end{center}\n" \
                  "\\end{table}\n"
    return latex_table


def get_speed_up_latex_table(algorithm_tag, results):
    data_rows = ""
    for precision_key in results.keys():
        times = list(results[precision_key].values())
        speed_ups = [times[0] / times[i] for i in range(len(times))]
        row = "\t" + str(precision_key)
        row += (8 - len(row)) * " "
        for i, speed_up in enumerate(speed_ups):
            if i * 10 not in procs_to_show:
                continue
            string_su = f"& {round(speed_up, 2)}"
            string_su.replace('.', ',')
            string_su += (10 - len(string_su)) * " "
            row += string_su
        row += "\\\\ \n\t\\hline \n"
        data_rows += row

    latex_table = "\\begin{table}[H]\n" \
                  "\\begin{center}\n" \
                  "\\large\n" \
                  "\\caption{Escalabilidad del algoritmo " \
                  + algorithm_tag + \
                  " utilizando el paradigma de programación con MPI.}\n" \
                  "\\label{" \
                  f"table:su-mpi-{algorithm_tag.lower()}" \
                  "}\n" \
                  "\\begin{tabular}{| c | c | c | c | c | c | c | c |}\n" \
                  "\\hline\n" \
                  "\t\\multirow{2}{*}{\\textbf{Precisión}} & \multicolumn{7}{ | c | }{\\textbf{Número de procesos}} \\\\\n" \
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
    procs_to_show = [0, 10, 40, 80, 120, 160, 200]  # 0 means 1 proc

    data = load_mpi_results_from_file(results_path)

    for algorithm in data.keys():
        file = open(path_to_save + f"ex-mpi-{algorithm.lower()}.tex", "w")
        file.write(get_execution_time_latex_table(algorithm, data[algorithm]))
        file.close()
        file = open(path_to_save + f"su-mpi-{algorithm.lower()}.tex", "w")
        file.write(get_speed_up_latex_table(algorithm, data[algorithm]))
        file.close()