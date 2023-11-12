import pulp
from collections import defaultdict
# Read companies and investors preferences from file
def read_input(file_path):
    companies = {}
    investors = {}
    with open(file_path, 'r') as file:
        company_section = True
        for line in file:
            if line.strip() == "":
                company_section = False
                continue

            if company_section:
                name, size = line.strip().split(',')
                companies[name] = int(size)
            else:
                parts = line.strip().split(',')
                investors[parts[0]] = parts[1:]

    return companies, investors

def calculate_min_table_size(companies, investors, num_investors): 
    min_table_size = max(num_investors // len(companies), min(companies.values()))
    max_table_size = num_investors

    while min_table_size < max_table_size:
        mid_size = (min_table_size + max_table_size) // 2
        table_sizes = {company: mid_size for company in companies}
        if seating_lp(companies, investors, num_investors, table_sizes, True):
            max_table_size = mid_size
        else:
            min_table_size = mid_size + 1

    return {company: min_table_size for company in companies}


def seating_lp(companies, investors, num_investors, table_sizes, check_feasibility=False):
    prob = pulp.LpProblem("OptimalSeating", pulp.LpMaximize)

    x = pulp.LpVariable.dicts("seat", 
                              ((i, j, k) for i in investors 
                                            for j in companies 
                                            for k in range(1, 4)),
                              cat='Binary')

    preferences = {i: {c: (5 - rank if c in choices else 0) for rank, choices in enumerate(investors[i]) for c in companies} for i in investors}
    preference_weights = {1: 15, 2: 10, 3: 8, 4: 6, 5: 4}
    prob += pulp.lpSum([preference_weights[preferences[i][j]] * x[(i, j, k)] 
                        if (j, k) in preferences[i] else 0 
                        for i in investors for j in companies for k in range(1, 4)])
    for i in investors:
        for k1 in range(1, 4):
            prob += pulp.lpSum([x[(i, j, k1)] for j in companies]) == 1
            for k2 in range(k1 + 1, 4):
                for j in companies:
                    prob += x[(i, j, k1)] + x[(i, j, k2)] <= 1

    for j in companies:
        for k in range(1, 4):
            prob += pulp.lpSum([x[(i, j, k)] for i in investors]) <= table_sizes[j]
            if not check_feasibility:
                
                prob += pulp.lpSum([x[(i, j, k)] for i in investors]) >= (table_sizes[j]) * 0.6


    for i in investors:
        prob += pulp.lpSum([preferences[i][j] * x[(i, j, k)] for j in companies for k in range(1, 4)]) >= 1

    prob.solve()

    if check_feasibility:
        return prob.status == pulp.LpStatusOptimal

    if prob.status != pulp.LpStatusOptimal:
        print("No feasible solution found. Status:", pulp.LpStatus[prob.status])
        return None

    results = defaultdict(lambda: defaultdict(list))
    for i in investors:
        for j in companies:
            for k in range(1, 4):
                if pulp.value(x[(i, j, k)]) == 1:
                    results[k][j].append(i)

    return results

# Write output - rounds in sorted order
def write_output(results, table_sizes, file_path):
    with open(file_path, 'w') as file:
        file.write(f"Minimum Table Size: {next(iter(table_sizes.values()))}\n\n")
        for round_number in sorted(results):  # sort the round numbers
            company_to_investors = results[round_number]
            file.write(f"Round {round_number}:\n")
            for company, investor_list in company_to_investors.items():
                file.write(f"{company} (Table Size: {table_sizes[company]}): {' '.join(investor_list)}\n")
            file.write("\n")



def seat(input_file_path, output_file_path):
    companies, investors = read_input(input_file_path)
    num_investors = len(investors)
    table_sizes = calculate_min_table_size(companies, investors, num_investors)
    results = seating_lp(companies, investors, num_investors, table_sizes)
    if results:
        write_output(results, table_sizes, output_file_path)


