import sys

if len(sys.argv) < 3:
    print("Error missing input or output file")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, "r") as f:
    lines = f.readlines()

# Parse lines and sort by number after "solution_"
sorted_lines = sorted(
    lines,
    key=lambda x: int(x.split()[0].split("_")[1])
)

# Save to a new file
with open(output_file, "w") as f:
    f.writelines(sorted_lines)

print(f"Sorted file saved as {output_file}")