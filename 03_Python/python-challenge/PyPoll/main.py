import os
import csv

csvpath = os.path.join("..", "PyPoll", "election_data.csv")

poll = {}
total_votes = 0

with open(csvpath, newline="") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")

    csv_header = next(csvfile)
    
    for row in csvreader:
        total_votes = total_votes + 1
        
        if row[2] in poll.keys():
            poll[row[2]] = poll[row[2]] + 1
        else:
            poll[row[2]] = 1
 
candidates = []
candidate_votes = []

for key, value in poll.items():
    candidates.append(key)
    candidate_votes.append(value)

vote_percent = []
for votes in candidate_votes:
    vote_percent.append(round(votes/total_votes*100, 1))

candidate_data = list(zip(candidates, candidate_votes, vote_percent))

winner_list = []

for name in candidate_data:
    if max(candidate_votes) == name[1]:
        winner_list.append(name[0])

winner = winner_list[0]

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
    for entry in candidate_data:
        txtfile.write(entry[0] + ": " + str(entry[2]) +'%  (' + str(entry[1]) + ')\n')
    txtfile.write("------------------------")
    txtfile.write("\n")
    txtfile.write(f"Winner: {winner}")
    txtfile.write("\n")
    txtfile.write("-------------------------")

with open(output_file, 'r') as readfile:
    print(readfile.read())