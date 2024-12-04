import time
import itertools
from collections import defaultdict

class QuineMcCluskey:
    def __init__(self, num_vars, minterms, dont_cares=[]):
        self.num_vars = num_vars
        self.minterms = minterms
        self.dont_cares = dont_cares
        self.terms = sorted(set(self.minterms + self.dont_cares))
        self.prime_implicants = set()
        self.minterm_to_pi = defaultdict(set)
        self.petrick_time = 0
        self.qm_time = 0

    # convert number to binary string with leading zeros
    def get_binary(self, num):
        return format(num, f'0{self.num_vars}b')

    # group minterms and implicants by number of ones
    def group_terms(self, terms):
        grouped_terms = defaultdict(set)

        for term in terms:
            binary = self.get_binary(term)
            ones = binary.count('1')
            grouped_terms[ones].add(binary)

        return grouped_terms

    # combine two groups of terms with one bit difference
    def combine_terms(self, group1, group2):
        combined = set()
        marked = set()

        for term1 in group1:
            for term2 in group2:
                diff = sum(a != b for a, b in zip(term1, term2))
                if diff == 1:
                    combined_term = ''.join([a if a == b else '-' for a, b in zip(term1, term2)])
                    combined.add(combined_term)
                    marked.add(term1)
                    marked.add(term2)
        
        return combined, marked

    # find prime implicants using QM method
    def find_prime_implicants(self):
        grouped_terms = self.group_terms(self.terms)
        next_grouped_terms = defaultdict(set)
        marked = set()
        
        while True:
            next_grouped_terms = defaultdict(set)
            new_marked = set()
            keys = sorted(grouped_terms.keys())
            
            for i in range(len(keys) - 1):
                group1 = grouped_terms[keys[i]]
                group2 = grouped_terms[keys[i + 1]]
                combined_terms, current_marked = self.combine_terms(group1, group2)
                next_grouped_terms[keys[i]].update(combined_terms)
                new_marked.update(current_marked)
            
            # Collect unmarked terms as prime implicants
            for group in grouped_terms.values():
                for term in group:
                    if term not in marked:
                        self.prime_implicants.add(term)
            
            if not next_grouped_terms:
                break
            
            grouped_terms = next_grouped_terms
            marked.update(new_marked)
    
    # get minterms covered by a prime implicant ( - to 0 or 1)
    def get_minterms_covered(self, pi):
        indices = [i for i, bit in enumerate(pi) if bit == '-']
        num_dashes = len(indices)
        minterms = set()
        
        for replacements in itertools.product('01', repeat=num_dashes):
            term = list(pi)
            
            for idx, bit in zip(indices, replacements):
                term[idx] = bit
            
            minterm = int(''.join(term), 2)
            
            if minterm in self.minterms:
                minterms.add(minterm)
        
        return minterms

    # create a chart of minterms covered by PIs
    def create_pi_chart(self):
        for pi in self.prime_implicants:
            minterms = self.get_minterms_covered(pi)
            
            for m in minterms:
                self.minterm_to_pi[m].add(pi)

    # get EPIs by selecting PIs covering only one minterm
    def select_essential_pis(self):
        essential_pis = set()
        
        while True:
            essential_found = False
            
            for m, pis in list(self.minterm_to_pi.items()):
                if len(pis) == 1:
                    pi = next(iter(pis))
                    essential_pis.add(pi)
                    self.remove_pi(pi)
                    essential_found = True
            
            if not essential_found:
                break
        
        return essential_pis

    # remove a PI and its covered minterms from chart
    def remove_pi(self, pi):
        minterms = self.get_minterms_covered(pi)
        
        for m in minterms:
            if m in self.minterm_to_pi:
                del self.minterm_to_pi[m]

    # optimize input boolean expression
    def optimize(self):
        start_qm = time.perf_counter()
        self.find_prime_implicants()
        self.create_pi_chart()
        essential_pis = self.select_essential_pis()
        end_qm = time.perf_counter()
        self.qm_time = end_qm - start_qm

        if self.minterm_to_pi:
            start_petrick = time.perf_counter()
            petrick = PetricksMethod(self.minterm_to_pi)
            minimal_pis = petrick.get_minimal_pis()
            end_petrick = time.perf_counter()
            self.petrick_time = end_petrick - start_petrick
            return essential_pis.union(minimal_pis)
        else:
            return essential_pis

class PetricksMethod:
    def __init__(self, minterm_to_pi):
        self.minterm_to_pi = minterm_to_pi

    # creates boolean expression representing all combinations of PIs that cover remaining minterms
    def get_minimal_pis(self):
        P = []
        
        for m in self.minterm_to_pi:
            P.append(set(self.minterm_to_pi[m]))
        
        solutions = self.reduce_petrick(P)
        min_len = min(len(s) for s in solutions)
        minimal_solutions = [s for s in solutions if len(s) == min_len]
        
        return set(minimal_solutions[0])

    # reduce boolean expression using Petrick's method
    def reduce_petrick(self, P):
        products = [set([pi]) for pi in P[0]]
        
        for pis in P[1:]:
            new_products = []
            
            for prod in products:
                for pi in pis:
                    new_prod = prod | {pi}
                    new_products.append(new_prod)
            
            products = self.remove_redundant(new_products)
        
        return products

    # remove redundant products
    def remove_redundant(self, products):
        unique_products = []
        
        for p in products:
            if not any(p > other_p for other_p in products if p != other_p):
                unique_products.append(p)
        
        return unique_products

# measurement functions #

# measure optimization time for alg
def measure_optimization_time(algorithm_class, num_vars, minterms, dont_cares=[]):
    optimizer = algorithm_class(num_vars, minterms, dont_cares)
    optimized = optimizer.optimize()
    total_time = optimizer.qm_time + optimizer.petrick_time
    
    return {
        'total_time': total_time,
        'qm_time': optimizer.qm_time,
        'petrick_time': optimizer.petrick_time,
        'optimized': optimized
    }

# display minimized boolean expression
def display_expression(prime_implicants, num_vars):
    var_letters = [chr(65 + i) for i in range(num_vars)]
    expressions = []
    
    for pi in prime_implicants:
        term = ""
        
        for i, val in enumerate(pi):
            if val == '-':
                continue
            elif val == '0':
                term += var_letters[i] + "'"
            elif val == '1':
                term += var_letters[i]
        
        expressions.append(term or '1')
    
    minimized_expression = ' + '.join(expressions)
    
    return minimized_expression
