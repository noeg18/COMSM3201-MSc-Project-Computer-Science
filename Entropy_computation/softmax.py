import os
import csv
import numpy as np
from scipy.special import softmax
import sys

if len(sys.argv) < 3 or not os.path.exists(sys.argv[1]):
    print("Error: missing input or output folder.")
    sys.exit(1)
input_folder = sys.argv[1]
output_folder = sys.argv[2]

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        csv_path = os.path.join(input_folder, filename)
        txt_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.txt')

        # collect all probs from the 'cluster' column
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = list(csv.DictReader(csvfile)) 
            cluster_values = np.array([float(row['cluster']) for row in reader])
            softmax_probs = softmax(cluster_values)

        # write softmax result
        with open(txt_path, 'w', encoding='utf-8') as txtfile:
            for i, prob in enumerate(softmax_probs):
                response_code = f"R{i+1}"
                txtfile.write(f"{response_code} {prob:.6f}\n")

print("All probabilities calculated and written to files.")
