import os
import csv

csvpath = os.path.join("..", "PyPoll", "election_data.csv")

with open(csvpath, newline="") as csvfile:
    csvreader = csv.Dictreader(csvfile, delimiter=",")

    csv_header = next(csvfile)

    total_votes = 0
    winner_votes = 0
    total_candidates = 0
    greatest_votes = ["", 0]
    candidate_options = []
    candidate_votes = {}

    for row in reader:
        total_votes = total_votes + 1
        total_candidates = row["Candidate"]        

        if row["Candidate"] not in candidate_options:
            
            candidate_options.append(row["Candidate"])

            candidate_votes[row["Candidate"]] = 1
            
        else:
            candidate_votes[row["Candidate"]] = candidate_votes[row["Candidate"]] + 1

    print("Election Results")
    print("-------------------------")
    print(f"Total Votes + {str(votes)}")
    print("-------------------------")

    for candidate in candidate_votes:
        print(candidate + " " + str(round(((candidate_votes[candidate]/total_votes)*100))) + "%" + " (" + str(candidate_votes[candidate]) + ")") 
        candidate_results = (candidate + " " + str(round(((candidate_votes[candidate]/votes)*100))) + "%" + " (" + str(candidate_votes[candidate]) + ")") 
    
candidate_votes

winner = sorted(candidate_votes.items(), key=itemgetter(1), reverse=True)

#results
print("-------------------------")
print(f"Winner: + {str(winner[0]}"))
print("-------------------------")

output_path = os.path.join("..", "PyPoll", "main.txt")

with open(output_path, 'w') as txtfile:
    
    txtfile.write("Financial Analysis")
    txtfile.write("\n")
    txtfile.write("----------------------------")
    txtfile.write("\n")
    txtfile.write(f"Total Months: {len(total_months)}")
    txtfile.write("\n")
    txtfile.write(f"Total: ${sum(total_revenue)}")
    txtfile.write("\n")
    txtfile.write(f"Average Change: ${round(sum(monthly_revenue_change)/len(monthly_revenue_change),2)}")
    txtfile.write("\n")
    txtfile.write(f"Greatest Increase in Profits: {total_months[max_increase_month]} (${(str(max_increase_value))})")
    txtfile.write("\n")
    txtfile.write(f"Greatest Decrease in Profits: {total_months[max_decrease_month]} (${(str(max_decrease_value))})")