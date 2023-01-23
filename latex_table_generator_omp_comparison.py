import styles
from data_loader import load_omp_results_from_file
from styles import default_comparison_precision, omp_results_file

def get_execution_times_latex_table(results):
    data_rows = ""
    for algorithm_key in results.keys():
        times = list(results[algorithm_key][default_comparison_precision].values())
        row = "\t" + algorithm_key
        row += (20 - len(row)) * " "
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
                  "\\caption{Tiempos de ejecución (en segundos) de los algoritmos y librerías con " \
                  + str(default_comparison_precision) + \
                  " decimales de precisión, utilizando el paradigma de programación con OpenMP.}\n" \
                  "\\label{table:ex-omp-comparison}\n" \
                  "\\begin{tabular}{| c | c | c | c | c | c | c | c |}\n" \
                  "\\hline\n" \
                  "\t\\multirow{2}{*}{\\textbf{Algoritmo}} & \multicolumn{7}{ | c | }{\\textbf{Número de hebras}} \\\\\n" \
                  "\t\\cline{2-8} & \\textbf{1} & \\textbf{2} & \\textbf{4} & \\textbf{8} & \\textbf{12} & \\textbf{16} & \\textbf{20} \\\\\n" \
                  "\t\\hline\n" \
                  + data_rows + \
                  "\\end{tabular}\n" \
                  "\\end{center}\n" \
                  "\\end{table}\n"
    return latex_table


def get_speed_ups_latex_table(results):
    data_rows = ""
    for algorithm_key in results.keys():
        times = list(results[algorithm_key][default_comparison_precision].values())
        speed_ups = [times[0] / times[i] for i in range(len(times))]
        row = "\t" + algorithm_key
        row += (20 - len(row)) * " "
        for speed_up in speed_ups:
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
                  " decimales de precisión, utilizando el paradigma de programación con OpenMP.}\n" \
                  "\\label{table:su-omp-comparison}\n" \
                  "\\begin{tabular}{| c | c | c | c | c | c | c | c |}\n" \
                  "\\hline\n" \
                  "\t\\multirow{2}{*}{\\textbf{Algoritmo}} & \multicolumn{7}{ | c | }{\\textbf{Número de hebras}} \\\\\n" \
                  "\t\\cline{2-8} & \\textbf{1} & \\textbf{2} & \\textbf{4} & \\textbf{8} & \\textbf{12} & \\textbf{16} & \\textbf{20} \\\\\n" \
                  "\t\\hline\n" \
                  + data_rows + \
                  "\\end{tabular}\n" \
                  "\\end{center}\n" \
                  "\\end{table}\n"
    return latex_table


if __name__ == '__main__':
    # Set file and path to store the plots
    results_path = omp_results_file
    path_to_save = styles.path_to_save_tables

    data = load_omp_results_from_file(results_path)

    file = open(path_to_save + "ex-omp-comparison.tex", "w")
    file.write(get_execution_times_latex_table(data))
    file.close()

    file = open(path_to_save + "su-omp-comparison.tex", "w")
    file.write(get_speed_ups_latex_table(data))
    file.close()
