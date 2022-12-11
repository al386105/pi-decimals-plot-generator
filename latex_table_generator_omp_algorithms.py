import statistics


# This function returns a dictionary with the executions results median of any algorithm
#     results = {'algorithm_tag' : { precision : { procs_used  { median_execution_time } } }

def load_results_from_file():
    file = open(results_path, "r")

    results = dict()

    # Iterate the file results, each line file is an execution result and store it in a dictionary
    for line_result in file:
        split_line = line_result.split(';')
        algorithm_tag = split_line[2]
        precision_used = int(split_line[3])
        threads_used = int(split_line[5])
        decimals_computed = int(split_line[6])
        execution_time = float(split_line[7])

        # Check if the decimals computed are greater than the desired:
        if precision_used > decimals_computed:
            print("Something went wrong! It looks like some executions did not go as expected.")
            print(f"Check {algorithm_tag} algorithm")
            exit(-1)

        if algorithm_tag not in results:
            results[algorithm_tag] = dict()

        if precision_used not in results[algorithm_tag]:
            results[algorithm_tag][precision_used] = dict()

        if threads_used not in results[algorithm_tag][precision_used]:
            results[algorithm_tag][precision_used][threads_used] = []

        results[algorithm_tag][precision_used][threads_used].append(execution_time)

    # Finally, replace the execution times with the median of them in the same dictionary
    for algorithm_key in results.keys():
        for precision_key in results[algorithm_key]:
            for threads_key in results[algorithm_key][precision_key]:
                median_rounded = str(round(statistics.median(results[algorithm_key][precision_key][threads_key]), 2))
                results[algorithm_key][precision_key][threads_key] = median_rounded.replace('.', ',')

    return results


def get_latex_table(algorithm_tag, results):
    data_rows = ""
    for precision_key in results.keys():
        times = list(results[precision_key].values())
        row = "\t" + str(precision_key)
        # Add blank spaces
        row += (8 - len(row)) * " "
        for time in times:
            string_time = f"& {time}"
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
                  f"table:omp-{algorithm_tag.lower()}" \
                  "}\n" \
                  "\\begin{tabular}{| c | c | c | c | c | c | c | c |}\n" \
                  "\\hline\n" \
                  "\t\\multirow{2}{*}{\\textbf{Precisión}} & \multicolumn{7}{ | c | }{\\textbf{Número de hebras}} \\\\\n" \
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

    data = load_results_from_file()

    for algorithm in data.keys():
        file = open(path_to_save + f"ex-{algorithm.lower()}.tex", "w")
        file.write(get_latex_table(algorithm, data[algorithm]))
        file.close()
