import random

# Configuration for the test data
num_companies = 12
num_investors = 80
company_size_range = (1, 2)
num_preferences = 5

# Generate company names and sizes
def generate_companies(num_companies, size_range):
    companies = {}
    for i in range(1, num_companies + 1):
        companies[f"Company_{i}"] = random.randint(*size_range)
    return companies

# Generate investors and their preferences
def generate_investors(num_investors, num_companies, num_preferences):
    investors = {}
    for i in range(1, num_investors + 1):
        preferences = random.sample(range(1, num_companies + 1), num_preferences)
        investors[f"Investor_{i}"] = [f"Company_{pref}" for pref in preferences]
    return investors


def write_test_data_to_file(file_path, companies, investors):
    with open(file_path, 'w') as file:
        # Write companies and sizes
        for company, size in companies.items():
            file.write(f"{company},{size}\n")
        file.write("\n")  

        # Write investors and their preferences
        for investor, preferences in investors.items():
            file.write(f"{investor},{','.join(preferences)}\n")


def generate_test_data(file_path, num_companies, num_investors, company_size_range, num_preferences):
    companies = generate_companies(num_companies, company_size_range)
    investors = generate_investors(num_investors, num_companies, num_preferences)
    write_test_data_to_file(file_path, companies, investors)

# Generate the test input file
test_input_file = 'input.txt'
generate_test_data(test_input_file, num_companies, num_investors, company_size_range, num_preferences)
print(f"Generated big test input in {test_input_file}")
