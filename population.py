import matplotlib.pyplot as plt

with open('species_history.txt', 'r') as f:
    lines = f.readlines()

born = {}
died = {}

