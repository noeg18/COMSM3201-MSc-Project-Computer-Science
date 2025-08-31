import numpy as np
from tpfp import tpfp
import sys

if len(sys.argv) < 3:
   print("Error: missing correctness or entropy file")
   sys.exit(1)

def get_array(file, is_percent=False):
    numbers = []
    with open(file, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(" ", 1)
                if len(parts) > 1:
                    num = float(parts[1].replace('%',''))
                    if is_percent:
                        num /= 100.0  # normalise to 0–1
                    numbers.append(num)
    return np.array(numbers)


UNCERTAINTY_THRESH = 0.28
CORRECTNESS_THRESH = 0.66

correctness = get_array(sys.argv[1], is_percent=True)
uncertainty = get_array(sys.argv[2])

predictions = np.where(uncertainty < UNCERTAINTY_THRESH, 1.0, 0.0)
ground_truth = np.where(correctness > CORRECTNESS_THRESH, 1.0, 0.0)

print(UNCERTAINTY_THRESH)
metrics = tpfp(predictions, ground_truth)
print(metrics)

