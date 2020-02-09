
import pickle
from numpy import genfromtxt
import numpy as np
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from numpy import savetxt
import csv

file_output = 'Generated Data/chemical_symptoms_differences.csv'

def calculate_symptom_difference(chem_symptoms, patient_symptoms):
    diff = 0
    for i in range(len(chem_symptoms)):
        if chem_symptoms[i] != patient_symptoms[i]:
            diff += 1
    return diff

# import data
chemicalFile = "/Users/blakeedwards/Documents/Data-Science-Competition/Health-Data-Science-Competition/Chemicals.csv"
print("Importing data from csv files...")
chemical_data = genfromtxt(chemicalFile, delimiter=',')

# iterate all of the chemicals
print("Calculating differences...")
chem_diffs = []
for c1 in range(len(chemical_data)):
    curr_diffs = []
    for c2 in range(len(chemical_data)):
        chem1 = chemical_data[c1]
        chem2 = chemical_data[c2]
        curr_diffs.append(calculate_symptom_difference(chem1, chem2))
    chem_diffs.append(curr_diffs)


with open(file_output, "w") as f:
    writer = csv.writer(f)
    writer.writerows(chem_diffs)

chem_array = np.array(chem_diffs)
chem_array = chem_array.astype(int)
ax = sns.heatmap(chem_array, cmap="binary")
plt.show()