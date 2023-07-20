import styles
from data_loader import load_hyb_results_from_file


def get_execution_time_latex_table(algorithm_tag, results):
    data_rows = ""
    for precision_key in results.keys():
        procs = results[precision_key]
        row = "\t \\textbf{" + str(precision_key) + "}"
        row += (8 - len(row)) * " "
        for procs_key in procs.keys():
            if procs_key in procs_to_show:
                times = list(results[precision_key][procs_key].values())
                for time in times:
                    string_time = " & \\multicolumn{1}{c|}{" + str(round(time, 2)) + "}"
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
                  " utilizando el paradigma de programación híbrido}\n" \
                  "\\label{" \
                  f"table:ex-hyb-{algorithm_tag.lower()}" \
                  "}\n" \
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
    

def get_speed_up_latex_table(algorithm_tag, results):
    data_rows = ""
    for precision_key in results.keys():
        procs = results[precision_key]
        row = "\t \\textbf{" + str(precision_key) + "}"
        row += (8 - len(row)) * " "
        seq_time = results[precision_key][1][1]
        for procs_key in procs.keys():
            if procs_key in procs_to_show:
                times = list(results[precision_key][procs_key].values())
                speed_ups = [seq_time / times[i] for i in range(len(times))]
                for speed_up in speed_ups:
                    string_su = " & \\multicolumn{1}{c|}{" + str(round(speed_up, 2)) + "}"
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
                  " utilizando el paradigma de programación híbrido}\n" \
                  "\\label{" \
                  f"table:su-hyb-{algorithm_tag.lower()}" \
                  "}\n" \
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

    data = load_hyb_results_from_file(results_path)
    procs_to_show = [1, 4, 8, 12, 16]

    for algorithm in data.keys():
        file = open(path_to_save + f"ex-hyb-{algorithm.lower()}.tex", "w")
        file.write(get_execution_time_latex_table(algorithm, data[algorithm]))
        file.close()
        file = open(path_to_save + f"su-hyb-{algorithm.lower()}.tex", "w")
        file.write(get_speed_up_latex_table(algorithm, data[algorithm]))
        file.close()
