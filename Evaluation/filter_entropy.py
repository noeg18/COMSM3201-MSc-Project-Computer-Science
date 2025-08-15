"""this script filters entropy results so only solutions with 100% test coverage
 are included in correlation computation"""

import sys

if len(sys.argv) < 4:
    print("Missing correctness, entropy or output file.")
    sys.exit(1)

correct_file = sys.argv[1]
entropy_file = sys.argv[2]
output_file = sys.argv[3]

def extract_id(line):
    #Extract the number from solution_X
    first_part = line.split()[0]  
    number = first_part.replace(".csv", "").split("_")[1]
    return int(number)

# Get valid IDs from correctcoverage.txt
with open(correct_file, "r") as f:
    valid_ids = {extract_id(line) for line in f}

# Filter sorted_entropy.txt
with open(entropy_file, "r") as f:
    filtered_lines = [
        line for line in f
        if extract_id(line) in valid_ids
    ]

# Save results
with open(output_file, "w") as f:
    f.writelines(filtered_lines)

print(f"Filtered entropy saved as {output_file}")