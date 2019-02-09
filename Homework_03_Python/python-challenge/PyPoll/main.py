import os
import csv

csvpath = os.path.join("..", "PyPoll", "election_data.csv")

poll = {}

total_votes = 0

with open(csvpath, newline="") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")

    csv_header = next(csvfile)
    
    for row in csvreader:
        total_votes += 1
        
        if row[2] in poll.keys():
            poll[row[2]] = poll[row[2]] + 1
        else:
            poll[row[2]] = 1
 
candidates = []
num_votes = []

for key, value in poll.items():
    candidates.append(key)
    num_votes.append(value)

vote_percent = []
for n in num_votes:
    vote_percent.append(round(n/total_votes*100, 1))

clean_data = list(zip(candidates, num_votes, vote_percent))

winner_list = []

for name in clean_data:
    if max(num_votes) == name[1]:
        winner_list.append(name[0])

winner = winner_list[0]

if len(winner_list) > 1:
    for w in range(1, len(winner_list)):
        winner = winner + ", " + winner_list[w]

output_file = os.path.join("..", "PyPoll", "main.txt")

with open(output_file, 'w') as txtfile:
    txtfile.write("Election Results")
    txtfile.write("\n")
    txtfile.write("-------------------------")
    txtfile.write("\n")
    txtfile.write(f"Total Votes: {str(total_votes)}")
    txtfile.write("\n")
    txtfile.write("-------------------------")
    txtfile.write("\n")
    for entry in clean_data:
        txtfile.write(entry[0] + ": " + str(entry[2]) +'%  (' + str(entry[1]) + ')\n')
    txtfile.write("------------------------")
    txtfile.write("\n")
    txtfile.write(f"Winner: {winner}")
    txtfile.write("\n")
    txtfile.write("-------------------------")

with open(output_file, 'r') as readfile:
    print(readfile.read())