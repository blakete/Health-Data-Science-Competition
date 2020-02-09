# Health-Data-Science-Competition
U of SC National Big Health Data Science Competition code to classify patient chemical exposure based on their symptoms.

## Basic Top-N Sweep Algorithm (achieves ~99% accuracy, top 3 conference accuracy)

- Calculated symptom difference for each patient between all chemicals
  - Kept & sorted top-15 closest chemical symptom differences (ascending order)
- Counted number of top-1 estimated chemical exposure per patient
- Created top-n most likely chemicals
  -Only >= 5% frequency included 
- If patient predicted chemical exposure in top-n
  - Kept the same
- If patients predicted chemical exposure not in top-n:
  - Checked ascending top-15 closest for chemical in top-n
    - If no chemical in the top-n most probable, patient symptoms are an outlier and the original chemical prediction is kept

TODO add group member algorithms
TODO add neural network implementation
TODO add R analysis scripts
