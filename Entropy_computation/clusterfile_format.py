# this script changes cluster files ready for entropy script to parse
import os
import csv
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

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            with open(txt_path, 'w', encoding='utf-8') as txtfile:
                count = 1
                for row in reader:
                    cluster = row['cluster']
                    response_code = f"R{count}"
                    txtfile.write(f"{response_code} {cluster}\n")
                    count += 1

print("All files successfully changed.")
