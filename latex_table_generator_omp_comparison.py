

def get_execution_times_latex_table(results):
    data_rows = ""
    for algorithm_key in results.keys():
        times = list(results[algorithm_key][default_precision].values())
        row = "\t" + algorithm_key
        # Add blank spaces
        row += (20 - len(row)) * " "
        for time in times:
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
                  " decimales de precisión y utilizando el paradigma de programación con OpenMP.}\n" \
                  "\\label{table:omp-comparison}\n" \
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
    results_path = 'results/omp/results-2022-12.csv'
    path_to_save = 'tables/omp/'
    default_precision = 200000

    data = load_results_from_file()

    file = open(path_to_save + "ex-comparison.tex", "w")
    file.write(get_latex_table(data))
    file.close()

