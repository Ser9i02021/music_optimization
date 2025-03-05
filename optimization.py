from label_chosen_licks import select_N_lick_samples
from cost_matrix_construction import build_cost_matrix

from itertools import combinations
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpBinary



def power_set(iterable, min_size, max_size):
    """
    Returns the power set (all subsets) of the given iterable
    as a list of tuples.
    """
    s = list(iterable)  # Convert to list in case it's a set
    subsets = []
    for r in range(min_size, max_size):
        # combinations(s, r) gives all subsets of length r
        for combo in combinations(s, r):
            subsets.append(list(combo))
    return subsets



licks_list, origin_of_classified_licks = select_N_lick_samples(4) # Select 2 random licks plus inital 
                                                                  # and final dummy licks
p = build_cost_matrix(licks_list) # Build the cost matrix

#L = licks_list # Set of licks (vertices)
L = [] # Set of licks (vertices) (0, 1, ..., number_of_licks + 1) 
for i in range(len(licks_list)):
    L.append(i)


A = [] # Set of arcs (edges)
for i in range(len(L)):
    for j in range(len(L)):
        if i != j:
            A.append((L[i], L[j]))

L_prime = L.copy() # Set of licks (vertices) to be optimized, without the first and last licks (which are always dummy or regular licks)
for i in range(2):
    L_prime.remove(L[-i])

G = (L, A) # Graph G = (L, A) (may not be used)

R = [] # Set of repetition licks
for i in range (1, len(licks_list) - 1):
    if "C1" in licks_list[i][2]:
        R.append(i)

T = [] # Set of turnaround licks
for i in range (1, len(licks_list) - 1):
    if "C8" in licks_list[i][2]:
        T.append(i)

P = [] # Set of licks with pause
for i in range (1, len(licks_list) - 1):
    if ("C2" or "C3" or "C4" or "C5" or "C6" or "C7") in licks_list[i][2]:
        P.append(i)

'''
c = [] # Set of durations (in bars) for each lick
for vertex in L:
    #c.append(vertex[3]) (to be implemented)
    pass
'''

# Parameters
#p = {(i, j): ... for (i, j) in A}  # Cost values for edges
#c = {i: ... for i in L_prime}  # Cost values for nodes
b = 4  # Quantity of bars in the solo (will be setted arbitrarily)
r = 1  # Constraint (5) (must be 1)
s = 3  # Constraint (6) (must be 3)

'''
# 2 < |S| < b
S = power_set(L_prime, 3, b - 1) #  # Subsets of L_prime
'''

# Define the optimization problem
model = LpProblem("Integer_Programming_Model", LpMinimize)

# Define decision variables
x = {(i, j): LpVariable(f"x_{i}_{j}", cat=LpBinary) for (i, j) in A}
y = {i: LpVariable(f"y_{i}", cat=LpBinary) for i in L_prime}

# Objective function (1)
model += lpSum(p[i][j] * x[i, j] for (i, j) in A)

# Constraints
L_minus_n_plus_1 = L.copy()
L_minus_n_plus_1.remove(L[-1])
for i in L_prime:
    model += lpSum(x[i, j] for j in L_minus_n_plus_1 if (i, j) in A) == y[i]

L_minus_0 = L.copy()
L_minus_0.remove(L[0])
for j in L_prime:
    model += lpSum(x[i, j] for i in L_minus_0 if (i, j) in A) == y[j]

#model += lpSum(c[i] * y[i] for i in L_prime) == b  # Constraint (4)

model += lpSum(y[i] for i in R) == r  # Constraint (5) (modified from the formulation on the paper, <=,
                                      # given its constraint determined on table 3 of the paper, =1)
model += lpSum(y[i] for i in P) <= s  # Constraint (6)

# Constraint (7)
L_prime_minus_T = L_prime.copy()
for t in T:
    L_prime_minus_T.remove(t)
model += lpSum(x[0, j] for j in L_prime_minus_T) == 1
model += lpSum(x[i, len(L_prime)+1] for i in T) == 1

# Constraint (8)
for (i, j) in A:
    if i < j:
        model += x[i, j] + x[j, i] <= 1
'''
# Constraint (9) - Connectivity constraint
for subset in S:
    not_subset = L
    for subset_element in subset:
        not_subset.remove(subset_element)
    model += lpSum(x[i, j] for i in subset for j in not_subset) >= 1
'''

# Solve the model
model.solve()

# Print solution
for (i, j) in A:
    print(f"x[{i}, {j}] = {x[i, j].varValue}")

for i in L_prime:
    print(f"y[{i}] = {y[i].varValue}")

