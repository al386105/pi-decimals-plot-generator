import statistics


def load_omp_results_from_file(results_path):
    """
        Load the OpenMP execution times from the file indicated in the results_path param
        Return a 'results' dictionary with the executions median of any algorithm
        results = {'algorithm_tag' : { precision : { threads_used : median_execution_time } } }
    """
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
            for thread_key in results[algorithm_key][precision_key]:
                results[algorithm_key][precision_key][thread_key] = statistics.median(
                    results[algorithm_key][precision_key][thread_key])

    return results


def load_mpi_results_from_file(results_path):
    """
        Load the MPI execution times from the file indicated in the results_path param
        Return a 'results' dictionary with the executions median of any algorithm
        results = {'algorithm_tag' : { procs_used : median_execution_time } }
    """

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

        # If we are sure that the line is a mpi result, we can discard the thread distribution way
        thread_distribution = algorithm_tag.split('-')[-1]
        algorithm_tag = algorithm_tag[:-(len(thread_distribution) + 1)]

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
                results[algorithm_key][precision_key][procs_key] = \
                    statistics.median(results[algorithm_key][precision_key][procs_key])

    return results
