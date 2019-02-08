import os
import csv

csvpath = os.path.join("..", "PyBank", "budget_data.csv")

with open(csvpath, newline="") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")

    csv_header = next(csvfile)

    print("Financial Analysis")
    print("----------------------------")
    
    total_months = []
    total_profit = []
    monthly_profit_change = []

    for row in csvreader:

        total_months.append(row[0])
        total_profit.apend(row[1])

    for x in range(len(total_profit)-1):
        






