from data_loader import load_omp_results_from_file


def get_execution_time_latex_table(algorithm_tag, results):
    data_rows = ""
    for precision_key in results.keys():
        times = list(results[precision_key].values())
        row = "\t" + str(precision_key)
        row += (8 - len(row)) * " "
        for time in times:
            string_time = f"& {round(time, 2)}"
            string_time = string_time.replace('.', ',')
            string_time += (12 - len(string_time)) * " "
            row += string_time
        row += "\\\\ \n\t\\hline \n"
        data_rows += row

    latex_table = "\\begin{table}[H]\n" \
                  "\\begin{center}\n" \
                  "\\large\n" \
                  "\\caption{Tiempos de ejecución (en segundos) del algoritmo " \
                  + algorithm_tag + \
                  " utilizando el paradigma de programación con OpenMP.}\n" \
                  "\\label{" \
                  f"table:ex-omp-{algorithm_tag.lower()}" \
                  "}\n" \
                  "\\begin{tabular}{| c | c | c | c | c | c | c | c |}\n" \
                  "\\hline\n" \
                  "\t\\multirow{2}{*}{\\textbf{Precisión}} & \multicolumn{7}{ | c | }{\\textbf{Número de hebras}} \\\\\n" \
                  "\t\\cline{2-8} & \\textbf{1} & \\textbf{2} & \\textbf{4} & \\textbf{8} & \\textbf{12} & \\textbf{16} & \\textbf{20} \\\\\n" \
                  "\t\\hline\n" \
                  + data_rows.replace('.', ',') + \
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
        for speed_up in speed_ups:
            string_su = f"& {round(speed_up, 2)}"
            string_su = string_su.replace('.', ',')
            string_su += (10 - len(string_su)) * " "
            row += string_su
        row += "\\\\ \n\t\\hline \n"
        data_rows += row

    latex_table = "\\begin{table}[H]\n" \
                  "\\begin{center}\n" \
                  "\\large\n" \
                  "\\caption{Escalabilidad del algoritmo " \
                  + algorithm_tag + \
                  " utilizando el paradigma de programación con OpenMP.}\n" \
                  "\\label{" \
                  f"table:su-omp-{algorithm_tag.lower()}" \
                  "}\n" \
                  "\\begin{tabular}{| c | c | c | c | c | c | c | c |}\n" \
                  "\\hline\n" \
                  "\t\\multirow{2}{*}{\\textbf{Precisión}} & \multicolumn{7}{ | c | }{\\textbf{Número de hebras}} \\\\\n" \
                  "\t\\cline{2-8} & \\textbf{1} & \\textbf{2} & \\textbf{4} & \\textbf{8} & \\textbf{12} & \\textbf{16} & \\textbf{20} \\\\\n" \
                  "\t\\hline\n" \
                  + data_rows.replace('.', ',') + \
                  "\\end{tabular}\n" \
                  "\\end{center}\n" \
                  "\\end{table}\n"
    return latex_table


if __name__ == '__main__':
    # Set file and path to store the plots
    results_path = 'results/omp-2022-12.csv'
    path_to_save = 'tables/'

    data = load_omp_results_from_file(results_path)

    for algorithm in data.keys():
        file = open(path_to_save + f"ex-omp-{algorithm.lower()}.tex", "w")
        file.write(get_execution_time_latex_table(algorithm, data[algorithm]))
        file.close()
        file = open(path_to_save + f"su-omp-{algorithm.lower()}.tex", "w")
        file.write(get_speed_up_latex_table(algorithm, data[algorithm]))
        file.close()
