import styles
from styles import mpi_algorithms_excluded, default_comparison_precision
from data_loader import load_hyb_results_from_file


def get_execution_times_latex_table(results):
    data_rows = ""
    for algorithm_key in results.keys():
        if algorithm_key not in mpi_algorithms_excluded:
            procs = results[algorithm_key][default_comparison_precision]
            times = []
            for procs_key in procs.keys():
                if procs_key in procs_to_show:
                    times.extend(list(results[algorithm_key][default_comparison_precision][procs_key].values()))      
            row = "\t \\textbf{" + str(algorithm_key) + "}"
            row += (24 - len(row)) * " "
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
                  "\\caption{Tiempos de ejecución (en segundos) de los algoritmos y librerías con " \
                  + "{:,}".format(default_comparison_precision).replace(",", ".") + \
                  " decimales de precisión, utilizando el paradigma de programación híbrido}\n" \
                  "\\label{table:ex-hyb-comparison}\n" \
                  "\\begin{tabular}{|c|cccccc|}\n" \
                  "\t\\hline\n" \
                  "\t\\cellcolor{Grey} & \multicolumn{6}{c|}{\cellcolor{Grey}\\textbf{Número de procesos}} \\\\\n" \
                  "\t\\cline{2-7} \n" \
                  "\t\\cellcolor{Grey} & \\multicolumn{2}{c|}{\\textbf{1}}  & \\multicolumn{1}{c|}{\\textbf{4}} & \\multicolumn{1}{c|}{\\textbf{8}} & \\multicolumn{1}{c|}{\\textbf{12}} & \\textbf{16} \\\\\n" \
                  "\t\\cline{2-7} \n" \
                  "\t\\cline{2-7} \n" \
                  "\t\\cellcolor{Grey} & \\multicolumn{6}{c|}{\\cellcolor{Grey}{\\textbf{Número de hebras por proceso}}} \\\\ \n" \
                  "\t\\cline{2-7} \n" \
                  "\t\\multirow{-4}{*}{\\cellcolor{Grey}{\\textbf{Precisión}}} & \\multicolumn{1}{c|}{\\textbf{1}} & \\multicolumn{1}{c|}{\\textbf{10}} & \\multicolumn{1}{c|}{\\textbf{10}} & \\multicolumn{1}{c|}{\\textbf{10}} & \\multicolumn{1}{c|}{\\textbf{10}} & \\textbf{10} \\\\ \n" \
                  "\t\\hline \n" \
                  + data_rows + \
                  "\\end{tabular}\n" \
                  "\\end{center}\n" \
                  "\\end{table}\n"
    return latex_table


def get_speed_ups_latex_table(results):
    data_rows = ""
    for algorithm_key in results.keys():
        if algorithm_key not in mpi_algorithms_excluded:
            procs = results[algorithm_key][default_comparison_precision]
            times = []
            for procs_key in procs.keys():
                if procs_key in procs_to_show:
                    times.extend(list(results[algorithm_key][default_comparison_precision][procs_key].values())) 
            speed_ups = [times[0] / times[i] for i in range(len(times))]     
            row = "\t \\textbf{" + str(algorithm_key) + "}"
            row += (24 - len(row)) * " "
            for speed_up in speed_ups:
                string_su = " & \multicolumn{1}{c|}{" + str(round(speed_up, 2)) + "}"
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
                  " decimales de precisión, utilizando el paradigma de programación híbrido}\n" \
                  "\\label{table:su-hyb-comparison}\n" \
                  "\\begin{tabular}{|c|cccccc|}\n" \
                  "\t\\hline\n" \
                  "\t\\cellcolor{Grey} & \multicolumn{6}{c|}{\cellcolor{Grey}\\textbf{Número de procesos}} \\\\\n" \
                  "\t\\cline{2-7} \n" \
                  "\t\\cellcolor{Grey} & \\multicolumn{2}{c|}{\\textbf{1}}  & \\multicolumn{1}{c|}{\\textbf{4}} & \\multicolumn{1}{c|}{\\textbf{8}} & \\multicolumn{1}{c|}{\\textbf{12}} & \\textbf{16} \\\\\n" \
                  "\t\\cline{2-7} \n" \
                  "\t\\cline{2-7} \n" \
                  "\t\\cellcolor{Grey} & \\multicolumn{6}{c|}{\\cellcolor{Grey}{\\textbf{Número de hebras por proceso}}} \\\\ \n" \
                  "\t\\cline{2-7} \n" \
                  "\t\\multirow{-4}{*}{\\cellcolor{Grey}{\\textbf{Precisión}}} & \\multicolumn{1}{c|}{\\textbf{1}} & \\multicolumn{1}{c|}{\\textbf{10}} & \\multicolumn{1}{c|}{\\textbf{10}} & \\multicolumn{1}{c|}{\\textbf{10}} & \\multicolumn{1}{c|}{\\textbf{10}} & \\textbf{10} \\\\ \n" \
                  "\t\\hline \n" \
                  + data_rows + \
                  "\\end{tabular}\n" \
                  "\\end{center}\n" \
                  "\\end{table}\n"
    return latex_table


if __name__ == '__main__':
    # Set file and path to store the plots
    results_path = styles.hyb_results_file
    path_to_save = styles.path_to_save_tables
    procs_to_show = [1, 4, 8, 12, 16]

    data = load_hyb_results_from_file(results_path)

    file = open(path_to_save + "ex-hyb-comparison.tex", "w")
    file.write(get_execution_times_latex_table(data))
    file.close()

    file = open(path_to_save + "su-hyb-comparison.tex", "w")
    file.write(get_speed_ups_latex_table(data))
    file.close()
