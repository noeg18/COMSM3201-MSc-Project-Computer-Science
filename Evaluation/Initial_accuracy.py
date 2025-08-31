# this script counts the proportion of correct (i.e >= 66.67) solutions
import sys

if len(sys.argv) < 2:
   print("Error: missing input file")
   sys.exit(1)

filename = sys.argv[1]
correctcount = 0
totalcount = 0
with open(filename, 'r') as file:
    for line in file:
        words = line.strip().split()
        if len(words) < 2:
            continue  
        correctness = float(words[1].replace('%', ''))
        totalcount += 1 
        if correctness > 66:
            correctcount += 1

percentage = (correctcount / totalcount) * 100
print(correctcount)
print(totalcount)
print(f"Correctness: {percentage}")

