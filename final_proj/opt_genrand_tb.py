# opt_genrand_tb.py

import random
from logic_opt_tool import QuineMcCluskey, measure_optimization_time, display_expression

def generate_random_minterms_and_dont_cares(num_vars):
    total_minterms = 2 ** num_vars
    num_minterms = random.randint(1, total_minterms // 2)
    minterms = random.sample(range(total_minterms), num_minterms)
    remaining_terms = set(range(total_minterms)) - set(minterms)
    num_dont_cares = random.randint(0, len(remaining_terms) // 2)
    dont_cares = random.sample(remaining_terms, num_dont_cares)
    return sorted(minterms), sorted(dont_cares)

def run_generation_test():
    print("Random Minterms and Don't-Cares Generation")
    print("=========================================\n")
    for num_vars in range(2, 7): # 2 to 5 variables
        print(f"Number of Variables: {num_vars}")
        minterms, dont_cares = generate_random_minterms_and_dont_cares(num_vars)
        result = measure_optimization_time(QuineMcCluskey, num_vars, minterms, dont_cares)
        optimized_expression = display_expression(result['optimized'], num_vars)
        print(f"  Minterms: {minterms}")
        print(f"  Don't-Cares: {dont_cares}")
        print(f"  Total Optimization Time: {result['total_time']:.6f} seconds")
        print(f"  Minimized Boolean Expression: {optimized_expression}\n")

if __name__ == "__main__":
    run_generation_test()
