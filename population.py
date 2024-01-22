import matplotlib.pyplot as plt

with open('population_by_gen.txt', 'r') as f:
    lines = f.readlines()

generations = {}

for line in lines:
    g = int(line.split(' ')[1].replace(':', ''))
    num = int(line.split(' ')[-1].strip())
    generations[g] = num

print(generations)
plt.scatter(generations.keys(), generations.values(), color='blue')
plt.xlabel('Generation')
plt.ylabel('Number of Species')
plt.title('Population by Generation')
plt.show()
