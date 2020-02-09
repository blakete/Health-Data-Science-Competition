import pandas as pd
import pickle
import heapq
from numpy import genfromtxt
import numpy as np

saved_filename = "Ranked_Data/final_rank.pkl"

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


def calculate_symptom_difference(chem_symptoms, patient_symptoms):
    diff = 0
    for i in range(len(chem_symptoms)):
        if chem_symptoms[i] != patient_symptoms[i]:
            diff += 1
    return diff

# import data
dataFile = "/Users/blakeedwards/Documents/Data-Science-Competition/Edwards-Health-Data-Science-Competition/CaseCompetitionPatientData.csv"
chemicalFile = "/Users/blakeedwards/Documents/Data-Science-Competition/Edwards-Health-Data-Science-Competition/Chemicals.csv"

print("Importing data from csv files...")
chemical_data = genfromtxt(chemicalFile, delimiter=',')
patient_data = genfromtxt(dataFile, delimiter=',')

# iterate all patients
print("Finding best chemical matches for all patients...")
patient_closest_chemical_matches = []
for p in range(len(patient_data)+1):
    current_patient_symptoms = patient_data[p]
    # calculate best chemical match for the current patient
    bestChem = [0]
    bestChemDiff = calculate_symptom_difference(chemical_data[0], current_patient_symptoms)
    # iterate all chemicals
    chem_diff_queue = PriorityQueue()
    for c in range(len(chemical_data)-1):
        curr_chemical_diff = calculate_symptom_difference(chemical_data[c+1], current_patient_symptoms)
        chem_diff_queue.push((c, curr_chemical_diff), curr_chemical_diff)
    ranked_chem_diffs = []
    for i in range(50):
        ranked_chem_diffs.append(chem_diff_queue.pop())
    patient_closest_chemical_matches.append(ranked_chem_diffs)
    if (p+1) % 1000 == 0:
        print(f"Patient #{p+1}: {ranked_chem_diffs}")
        with open(saved_filename, 'wb') as filehandler:
            pickle.dump(patient_closest_chemical_matches, filehandler)





# df_patient = pd.read_csv(dataFile, header=None)
# df_chemical = pd.read_csv(chemicalFile, header=None)
# # iterate all patients
# patient_closest_chemical_matches = []
# for p in range(df_patient.shape[0]):
#     current_patient_symptoms = list(df_patient.iloc[p, :])
#     # calculate best chemical match for the current patient
#     bestChem = 0
#     bestChemDiff = calculate_symptom_difference(list(df_chemical.iloc[0, :]), current_patient_symptoms)
#     # iterate all chemicals
#     for c in range(df_chemical.shape[0]-1):
#         current_chemical_symptoms = list(df_chemical.iloc[c+1, :])
#         curr_chemical_diff = calculate_symptom_difference(current_chemical_symptoms, current_patient_symptoms)
#         if curr_chemical_diff < bestChemDiff:
#             bestChemDiff = curr_chemical_diff
#             bestChem = c
#     best_match = (bestChem, bestChemDiff)
#     patient_closest_chemical_matches.append(best_match)
#     print(f"Patient #{p}: {best_match}")
#     filehandler = open(saved_filename, 'w')
#     pickle.dump(patient_closest_chemical_matches, filehandler)