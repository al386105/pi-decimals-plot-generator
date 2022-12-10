import statistics
from tabulate import tabulate


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
        procs_used = int(split_line[5])
        threads_used = int(split_line[6])
        decimals_computed = int(split_line[7])
        execution_time = float(split_line[8])

        # Check if the decimals computed are greater than the desired:
        if precision_used > decimals_computed:
            print("Something went wrong! It looks like some executions did not go as expected.")
            print(f"Check {algorithm_tag} algorithm")
            exit(-1)

        if threads_used > 1:
            print("Something went wrong! It looks like some executions use more than one thread (hybrid) ")
            exit(-1)

        if algorithm_tag not in results:
            results[algorithm_tag] = dict()

        if precision_used not in results[algorithm_tag]:
            results[algorithm_tag][precision_used] = dict()

        if procs_used not in results[algorithm_tag][precision_used]:
            results[algorithm_tag][precision_used][procs_used] = []

        results[algorithm_tag][precision_used][procs_used].append(execution_time)

    # Finally, replace the execution times with the median of them in the same dictionary
    for algorithm_key in results.keys():
        for precision_key in results[algorithm_key]:
            for procs_key in results[algorithm_key][precision_key]:
                median_rounded = str(round(statistics.median(results[algorithm_key][precision_key][procs_key]), 2))
                results[algorithm_key][precision_key][procs_key] = median_rounded.replace('.', ',')

    return results


if __name__ == '__main__':
    # Set file and path to store the plots
    results_path = 'results/mpi/results-2022-12.csv'
    path_to_save = 'tables/mpi/'
    default_precision = 200000

    data = load_results_from_file()

    table_data = []
    for algorithm in data.keys():
        if len(table_data) == 0:
            first_row = ["Algorithm"]
            first_row += list(data[algorithm][default_precision].keys())
            table_data.append(first_row)
        algorithm_row = [algorithm]
        algorithm_row += list(data[algorithm][default_precision].values())
        table_data.append(algorithm_row)

    file = open(path_to_save + "EX-COMPARISON.tex", "w")
    file.write(tabulate(table_data, tablefmt='latex_longtable'))
