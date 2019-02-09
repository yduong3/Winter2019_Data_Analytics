import os
import csv

csvpath = os.path.join("..", "PyBank", "budget_data.csv")

with open(csvpath, newline="") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")

    csv_header = next(csvfile)
    
    total_months = []
    total_revenue = []
    monthly_revenue_change = []

    for row in csvreader:

        total_months.append(row[0])
        total_revenue.append(int(row[1]))

    for x in range(len(total_revenue)-1):
        monthly_revenue_change.append(total_revenue[x+1]-total_revenue[x])

    max_increase_value = max(monthly_revenue_change)
    max_decrease_value = min(monthly_revenue_change)

    max_increase_month = monthly_revenue_change.index(max(monthly_revenue_change)) + 1
    max_decrease_month = monthly_revenue_change.index(min(monthly_revenue_change)) + 1 

print("Financial Analysis")
print("----------------------------")
print(f"Total Months: {len(total_months)}")
print(f"Total: ${sum(total_revenue)}")
print(f"Average Change: ${round(sum(monthly_revenue_change)/len(monthly_revenue_change),2}")
print(f"Greatest Increase in Profits: {total_months[max_increase_month]} (${(str(max_increase_value))})")
print(f"Greatest Decrease in Profits: {total_months[max_decrease_month]} (${(str(max_decrease_value))})")
