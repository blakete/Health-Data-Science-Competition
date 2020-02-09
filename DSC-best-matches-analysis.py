import pickle
import heapq
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

with open("/Users/blakeedwards/Documents/Data-Science-Competition/Health-Data-Science-Competition/best_matches.pkl", "rb") as file:
    data = pickle.load(file)

best_matches = {}
best_matches_duplicates = {}
for i in range(len(data)):
    patient_best_matches, diffs = data[i]
    # if len(patient_best_matches) > 1:
    #     if patient_best_matches[0] not in best_matches_duplicates.keys():
    #         best_matches_duplicates[patient_best_matches[0]] =
    for chemical in patient_best_matches:
        if chemical not in best_matches.keys():
            best_matches[chemical] = 1
        else:
            best_matches[chemical] += 1

best_matches_chem_list = list(best_matches.keys())
best_matches_ocur_list = list(best_matches.values())
queue = PriorityQueue()
for i in range(len(best_matches_chem_list)):
    queue.push((best_matches_chem_list[i], best_matches_ocur_list[i]), best_matches_ocur_list[i])
ordered_chems = []
ordered_occurrence = []
while not queue.isEmpty():
    chem, occurrence = queue.pop()
    ordered_chems.append(chem)
    ordered_occurrence.append(occurrence)

print(ordered_chems)
print(ordered_occurrence)

plt.bar(ordered_chems, ordered_occurrence, stacked=True, color='g')
plt.show()