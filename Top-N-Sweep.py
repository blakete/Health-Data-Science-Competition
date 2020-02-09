import pickle
import heapq
import numpy as np
from numpy import genfromtxt
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)


# count the top chemical frequencies
filename = "/Users/blakeedwards/Documents/Data-Science-Competition/Edwards-Health-Data-Science-Competition/Ranked_Data/final_rank2.pkl"
with open(filename, "rb") as file:
    patient_closest_chemical_matches = pickle.load(file)

chem_freqs = np.zeros(311)

for i in range(len(patient_closest_chemical_matches)):
    patient_chem_ranked = patient_closest_chemical_matches[i]
    chem_freqs[int(patient_chem_ranked[0][0])] += 1

# chems = np.arange(1, 312, 1)
# plt.bar(chems, chem_freqs, color='g')
# plt.show()
# print(chems)
# print(chem_freqs)
# chems = PriorityQueue()
# for chem in chem_freqs:
#     chems.push(chem, chem)
#
# while not chems.isEmpty():
#     print(chems.pop())

cuttoff = 0.05
freq_cuttoff = len(patient_closest_chemical_matches)*cuttoff
significant_chemicals = []
# print(f"significant chemicals: {significant_chemicals}")
for i in range(len(chem_freqs)):
    if chem_freqs[i] > freq_cuttoff:
        significant_chemicals.append(i)

# print(f"most significant chemicals: {significant_chemicals}")
patient_exposure_diagnosis = []
for i in range(len(patient_closest_chemical_matches)):
    if patient_closest_chemical_matches[i][0][0] in significant_chemicals:
        patient_exposure_diagnosis.append(patient_closest_chemical_matches[i][0][0])
    else:
        wasSet = False
        for chem in patient_closest_chemical_matches[i]:
            if chem[0] in significant_chemicals:
                patient_exposure_diagnosis.append(chem[0])
                wasSet = True
                break
        if not wasSet:
            patient_exposure_diagnosis.append(patient_closest_chemical_matches[i][0][0])

# print(patient_exposure_diagnosis)
with open('Generated Data/predictions2.csv', 'w') as filehandle:
    for diagnosis in patient_exposure_diagnosis:
        filehandle.write('%s\n' % diagnosis)

chem_freqs = np.zeros(311)

for i in range(len(patient_exposure_diagnosis)):
    chem_freqs[int(patient_exposure_diagnosis[i])] += 1

chems = PriorityQueue()
for i in range(len(chem_freqs)):
    chems.push((i, chem_freqs[i]), chem_freqs[i])

top_chems = []
while not chems.isEmpty():
    top_chems.insert(0, chems.pop())

print(f"Ranking of chemicals by frequency : {top_chems}")
print(f"Ranking of chemicals by percentage: {[(x[0], x[1]/len(patient_closest_chemical_matches) * 100) for x in top_chems]}")
print(f"Top chemicals: {top_chems[:len(significant_chemicals)]}")

import matplotlib.pyplot as plt
chems = np.arange(1, 312, 1)
plt.bar(chems, chem_freqs, color='b', width=5)
plt.show()

# calculate difference between top chemicals
chemicalFile = "/Users/blakeedwards/Documents/Data-Science-Competition/Edwards-Health-Data-Science-Competition/Chemicals.csv"
print("Importing data from csv files...")
chemical_data = genfromtxt(chemicalFile, delimiter=',')

def calculate_symptom_difference(chem_symptoms, patient_symptoms):
    diff = 0
    for i in range(len(chem_symptoms)):
        if chem_symptoms[i] != patient_symptoms[i]:
            diff += 1
    return diff

# iterate all of the chemicals
print("Calculating differences...")
chem_diffs = []
for i in range(len(significant_chemicals)):
    curr_diffs = []
    for j in range(len(significant_chemicals)):
        chem1 = chemical_data[significant_chemicals[i]]
        chem2 = chemical_data[significant_chemicals[j]]
        curr_diffs.append(calculate_symptom_difference(chem1, chem2))
    chem_diffs.append(curr_diffs)

chem_array = np.array(chem_diffs)
chem_array = chem_array.astype(int)
ax = sns.heatmap(chem_array, cmap="binary")
plt.show()
print(chem_array)
print(f"Top chemicals: {significant_chemicals}")