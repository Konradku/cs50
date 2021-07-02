import sys, csv

if (len(sys.argv) != 3):
    print("Usage: python dna.py data.csv sequence.txt")
    sys.exit(1)

data = []
with open(sys.argv[1], "r") as data_file:
    data_reader = csv.DictReader(data_file)
    for row in data_reader:
        data.append(row)

with open(sys.argv[2], "r") as seq_file:
    seq_reader = csv.reader(seq_file)
    sequence = ''.join(next(seq_reader)[0])

max_counts = []
for i in range(1, len(data_reader.fieldnames)):
    STR = data_reader.fieldnames[i]
    max_counts.append(0)
    for j in range(len(sequence)):
        STR_count = 0
        if sequence[j:(j+len(STR))] == STR:
            k = 0
            while sequence[(j+k):(j+k+len(STR))] == STR:
                STR_count += 1
                k += len(STR)
            if STR_count > max_counts[i-1]:
                max_counts[i-1] = STR_count

for i in range(len(data)):
    matches = 0
    for j in range((len(max_counts))):
        if int(max_counts[j]) == int(data[i][data_reader.fieldnames[j+1]]):
            matches += 1
    if matches == len(max_counts):
        print(data[i]["name"])
        exit(0)
print("No match")
