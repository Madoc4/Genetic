import matplotlib.pyplot as plt

with open('species_history.txt', 'r') as f:
    lines = f.readlines()

generations = {}

for line in lines:
    if line.startswith('Total generations: '):
        g = int(line.split(' ')[2].strip())
        for i in range(1, g+1):
            generations[i] = 0
    if line.startswith('Species with starting size'):
        birth = int(line.split(' ')[10].replace('.',''))
        death = int(line.split(' ')[12])
        for i in range(birth, death+1):
            generations[i] += 1

plt.scatter(generations.keys(), generations.values(), color='blue')
plt.xlabel('Generation')
plt.ylabel('Number of Species')
plt.title('Population by Generation')
plt.show()
