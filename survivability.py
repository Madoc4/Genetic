import matplotlib.pyplot as plt

species_data = {}
survival_rates = {}

with open('species_history.txt', 'r') as f:
    lines = f.readlines()

current_generation = None

for line in lines:
    if line.startswith('Generation'):
        current_generation = int(line.split()[1].strip(':'))
    elif line.startswith('Species with starting size'):
        parts = line.split('.')
        starting_size = float(parts[0].split(' ')[4])
        reason = parts[-1].split('.')[0].strip()

        if starting_size not in species_data:
            species_data[starting_size] = {'Survived': 0, 'Died': 0}

        if reason != '':
            species_data[starting_size]['Died'] += 1
        else:
            species_data[starting_size]['Survived'] += 1

for size, data in species_data.items():
    total_species = data['Survived'] + data['Died']
    if data['Survived'] == 0:
        survival_rate = 0
    else:
        survival_rate = data['Survived'] / total_species if total_species > 0 else 0
    survival_rates[size] = survival_rate

sizes = list(survival_rates.keys())
survival_rates_values = list(survival_rates.values())

plt.bar(sizes, survival_rates_values, color='blue')
plt.xlabel('Starting Size')
plt.ylabel('Survival Rate')
plt.title('Survival Rate by Starting Size')
plt.show()
