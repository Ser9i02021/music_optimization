from label_chosen_licks import select_N_lick_samples
from cost_matrix_construction import build_cost_matrix

from itertools import combinations
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpBinary

from pulp import *
from collections import defaultdict



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



licks_list = select_N_lick_samples(17) # Select 15 random licks plus inital 
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


# 2 < |S| < b (or len(L_prime) (modified from the paper))
S = power_set(L_prime, 3, len(L_prime)) #  # Subsets of L_prime


# Define the optimization problem
model = LpProblem("Integer_Programming_Model", LpMinimize)

# Define decision variables
x = {(i, j): LpVariable(f"x_{i}_{j}", cat=LpBinary) for (i, j) in A}
y = {i: LpVariable(f"y_{i}", cat=LpBinary) for i in L_prime}

# Objective function (1)
model += lpSum(p[i][j] * x[i, j] for (i, j) in A)

# Constraints
# Additional constraint to make the modified formulation of (2) and (3) work
model += x[0, L[-1]] == 0

# (2)
for i in L:
    if i == 0:
        model += lpSum(x[i, j] for j in L if (i, j) in A) == 1
    elif i > 0 and i < L[-1]:
        model += lpSum(x[i, j] for j in L if (i, j) in A) == y[i]
    else:
        model += lpSum(x[i, j] for j in L if (i, j) in A) == 0


'''
L_minus_n_plus_1 = L.copy()
L_minus_n_plus_1.remove(L[-1])
L_minus_n_plus_1.remove(L[0]) # Modification to the formulation on the paper
for i in L_prime:
    model += lpSum(x[i, j] for j in L_minus_n_plus_1 if (i, j) in A) == y[i]
'''
# (3)
for j in L:
    if j == 0:
        model += lpSum(x[i, j] for i in L if (i, j) in A) == 0
    elif j > 0 and j < L[-1]:
        model += lpSum(x[i, j] for i in L if (i, j) in A) == y[j]
    else:
        model += lpSum(x[i, j] for i in L if (i, j) in A) == 1



'''
L_minus_0 = L.copy()
L_minus_0.remove(L[0])
L_minus_0.remove(L[-1]) # Modification to the formulation on the paper
for j in L_prime:
    model += lpSum(x[i, j] for i in L_minus_0 if (i, j) in A) == y[j]
'''

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

# Constraint (9) - Connectivity constraint (may be removed considering the new formulated constraints (2) and (3))
'''
for subset in S:
    #not_subset = L
    for subset_element in subset:

        model += lpSum(x[i, j] for i in subset for j in subset if (i, j) in A) >= 1
'''
'''
Z = []
for (i, j) in A:
    if x[i, j].varValue == 1:
        Z.append((i, j))

#print(Z)
edge1 = Z[0]
w = True
while w:
    for edge2 in Z:
        if edge1[1] == edge2[0]:
            Z.remove(edge1)
            edge1 = edge2
            if edge2[1] == L[-1]:
                Z.remove(edge2)
                w = False
                break


#print(Z)

# Remove all remaining cycles
Subtours = []
while len(Z) > 0:
    edge1 = Z[0]
    edge0 = Z[0]
    Subtour = [edge1]
    w = True
    while w:
        for edge2 in Z:
            if edge1[1] == edge2[0]:
                Subtour.append(edge2)
                Z.remove(edge1)
                edge1 = edge2
                if edge2[1] == edge0[0]:
                    Z.remove(edge2)
                    w = False
                    break
    Subtours.append(Subtour)

for subtour in Subtours:
    model += lpSum(x[edge[0], edge[1]] for edge in subtour) <= len(Z) - 1
'''


# Solve the model
while True:
    model.solve()
    # Every iteration, we try to find a solution. Then we check for subtours.
    # If there are no subtours, the solution is adopted, otherwise, new constraints are setted
    # to the model in order to make it avoid utlizing the subtour(s) just found in future solutions
    Z = []
    for (i, j) in A:
        if x[i, j].varValue == 1:
            Z.append((i, j))

    print(Z)
    edge1 = Z[0]
    w = True
    while w:
        for edge2 in Z:
            if edge1[1] == edge2[0]:
                Z.remove(edge1)
                edge1 = edge2
                if edge2[1] == L[-1]:
                    Z.remove(edge2)
                    w = False
                    break

    if len(Z) == 0:
        break
    print(Z)

    # Remove all remaining cycles
    Subtours = []
    while len(Z) > 0:
        edge1 = Z[0]
        edge0 = Z[0]
        Subtour = [edge1]
        w = True
        while w:
            for edge2 in Z:
                if edge1[1] == edge2[0]:
                    Subtour.append(edge2)
                    Z.remove(edge1)
                    edge1 = edge2
                    if edge2[1] == edge0[0]:
                        Z.remove(edge2)
                        w = False
                        break
        Subtours.append(Subtour)
    
    for subtour in Subtours:
        model += lpSum(x[edge[0], edge[1]] for edge in subtour) == len(subtour) - 1 # Still needs to be validated




graph_path = [] # List of the edges used in the solution (unordered)

# Print solution
for (i, j) in A:
    print(f"x[{i}, {j}] = {x[i, j].varValue}")
    if x[i, j].varValue == 1:
        graph_path.append((i, j))

edge1 = graph_path[0]
graph_path_ordered = [edge1] # List of the edges used in the solution (ordered)
while True:
    for edge2 in graph_path:
        if edge1[1] == edge2[0]:
            graph_path_ordered.append(edge2)
            edge1 = edge2
            break
    if edge1[1] == L[-1]:
        break

graph_path_vertices_ordered = [] # List of the vertices used in the solution (ordered)
for edge in graph_path_ordered:
    graph_path_vertices_ordered.append(edge[0])
graph_path_vertices_ordered.append(graph_path_ordered[-1][1])

for i in L_prime:
    print(f"y[{i}] = {y[i].varValue}")

print(graph_path_vertices_ordered)
print("Objective function value:", model.objective.value())

'''
# Visualization of chosen edge in the matrix
for i in range(len(licks_list)):
    for j in range(len(licks_list)):
        if i != j:
            if x[i, j].varValue == 1:
                print(p[i][j], end="@ ")
            else:
                print(p[i][j], end=" ")
        else:
            print(p[i][j], end=" ")
    print()
'''












# Stage 5: Post-processing
file_paths_for_the_ordered_licks_in_the_solution = []

for vertex in graph_path_vertices_ordered:
    file_paths_for_the_ordered_licks_in_the_solution.append(licks_list[vertex][-1])

print(file_paths_for_the_ordered_licks_in_the_solution)
