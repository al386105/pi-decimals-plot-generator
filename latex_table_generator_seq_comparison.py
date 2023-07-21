import styles
from data_loader import load_omp_results_from_file
from styles import default_comparison_precision, omp_results_file, omp_algorithms_included

def get_execution_times_latex_table(results):
    data_rows = ""
    for algorithm_key in results.keys():
        if algorithm_key in omp_algorithms_included:
            times = [results[algorithm_key][precision][1] for precision in results[algorithm_key].keys()]
            row = "\t \\textbf{" + algorithm_key + "}"
            row += (20 - len(row)) * " "
            for time in times:
                string_time = " & \multicolumn{1}{c|}{" + str(round(time, 2)) + "}"
                string_time = string_time.replace('.', ',')
                string_time += (12 - len(string_time)) * " "
                row += string_time
            row += "\\\\ \n\t\\hline \n"
            data_rows += row

    latex_table = "\\begin{table}[H]\n" \
                  "\\begin{center}\n" \
                  "\\large\n" \
                  "\\caption{Tiempos de ejecución (en segundos) de los algoritmos y librerías" \
                  " con diferentes valores de precisión, utilizando el paradigma de programación secuencial}\n" \
                  "\\label{table:ex-seq-comparison}\n" \
                  "\\begin{tabular}{|c|ccc|}\n" \
                  "\\hline\n" \
                  "\t\\cellcolor{Grey} & \\multicolumn{3}{c|}{\\cellcolor{Grey}\\textbf{Precisión}} \\\\\n" \
                  "\t\\cline{2-4} \n" \
                  "\t\\multirow{-2}{*}{\\cellcolor{Grey}\\textbf{Algoritmo}} & \\multicolumn{1}{c|}{\\textbf{50000}} & \\multicolumn{1}{c|}{\\textbf{100000}} & \\multicolumn{1}{c|}{\\textbf{200000}} \\\\\n " \
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
    
    file = open(path_to_save + "ex-seq-comparison.tex", "w")
    file.write(get_execution_times_latex_table(data))
    file.close()