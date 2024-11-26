# opt_avgcomp_tb.py

import random
import statistics
from logic_opt_tool import QuineMcCluskey, measure_optimization_time

def generate_random_minterms_and_dont_cares(num_vars):
    total_minterms = 2 ** num_vars
    num_minterms = random.randint(1, total_minterms // 2)
    minterms = random.sample(range(total_minterms), num_minterms)
    remaining_terms = set(range(total_minterms)) - set(minterms)
    num_dont_cares = random.randint(0, len(remaining_terms) // 2)
    dont_cares = random.sample(remaining_terms, num_dont_cares)
    return sorted(minterms), sorted(dont_cares)

def run_statistics_test(iterations=5):
    print("Optimization Time Statistics")
    print("============================\n")
    for num_vars in range(2, 6): # 2 to 5 variables
        qm_times = []
        petrick_times = []
        total_times = []
        print(f"Number of Variables: {num_vars}")
        for i in range(iterations):
            minterms, dont_cares = generate_random_minterms_and_dont_cares(num_vars)
            result = measure_optimization_time(QuineMcCluskey, num_vars, minterms, dont_cares)
            qm_times.append(result['qm_time'])
            petrick_times.append(result['petrick_time'])
            total_times.append(result['total_time'])
        # Calculate statistics
        avg_qm_time = statistics.mean(qm_times)
        min_qm_time = min(qm_times)
        max_qm_time = max(qm_times)
        avg_petrick_time = statistics.mean(petrick_times)
        min_petrick_time = min(petrick_times)
        max_petrick_time = max(petrick_times)
        avg_total_time = statistics.mean(total_times)
        min_total_time = min(total_times)
        max_total_time = max(total_times)
        print(f"  QM Time (avg): {avg_qm_time:.6f} seconds")
        print(f"    Min: {min_qm_time:.6f} s, Max: {max_qm_time:.6f} s")
        print(f"  Petrick's Algorithm Time (avg): {avg_petrick_time:.6f} seconds")
        print(f"    Min: {min_petrick_time:.6f} s, Max: {max_petrick_time:.6f} s")
        print(f"  Total Optimization Time (avg): {avg_total_time:.6f} seconds")
        print(f"    Min: {min_total_time:.6f} s, Max: {max_total_time:.6f} s\n")

if __name__ == "__main__":
    run_statistics_test(iterations=10)
