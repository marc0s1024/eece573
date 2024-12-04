import random
from logic_opt_tool import QuineMcCluskey, measure_optimization_time, display_expression

# gen random minterm and don't care input
def gen_rand_input(num_vars):
    total_minterms = 2 ** num_vars
    num_minterms = random.randint(1, total_minterms // 2)
    minterms = random.sample(range(total_minterms), num_minterms)
    remaining_terms = list(set(range(total_minterms)) - set(minterms))
    num_dont_cares = random.randint(0, len(remaining_terms) // 2)
    dont_cares = random.sample(remaining_terms, num_dont_cares)
    
    return sorted(minterms), sorted(dont_cares)

# run testbench
def run_tb():
    print("--Optimization Time Testbench--\n")
    
    # issue with computation runtime at 6 variables and above
    for num_vars in range(2, 6): # 2 to 5 variables due to computational time growth
        print(f"Number of Variables: {num_vars}")
        minterms, dont_cares = gen_rand_input(num_vars)
        result = measure_optimization_time(QuineMcCluskey, num_vars, minterms, dont_cares)
        optimized_expression = display_expression(result['optimized'], num_vars)
        print(f"  Minterms: {minterms}")
        print(f"  Don't-Cares: {dont_cares}")
        print(f"  Total Optimization Time: {result['total_time']:.6f} seconds")
        print(f"  Minimized Boolean Expression: {optimized_expression}\n")

if __name__ == "__main__":
    run_tb()
