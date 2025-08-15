import numpy as np
from scipy import stats
import re
import sys

if len(sys.argv) < 3:
   print("Error: missing entropy or correctness file")
   sys.exit(1)

def add_values_to_array(file_path):
   list_of_values = []
   f = open(file_path, "r")
   for line in f.readlines():
      value = line.split(' ', 1)[1].strip()
      value = re.sub(r"[^0-9eE.\-]", "", value)
      list_of_values.append(float(value))
   return list_of_values

def main():
   correctness = add_values_to_array(sys.argv[1])
   entropy = add_values_to_array(sys.argv[2])
   corr, p_value = stats.pearsonr(correctness, entropy)

 
   with open("correlation.txt", "a") as f:
      f.write(f"Pearson correlation: {corr}\nP-value: {p_value}\n")

if __name__ == "__main__":
    main()
   





