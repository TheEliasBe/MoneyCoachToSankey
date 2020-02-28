import plotly.graph_objects as go
import numpy as np
import pandas as pd
import sys

try:
    source_file = sys.argv[1]
    data = pd.read_csv(source_file, delimiter=',', header=0)
except:
    raise FileNotFoundError()

# change dtype to float
data['Amount'] = data['Amount'].astype('float')

# extract currency
if data["Currency"][0] == "EUR":
    currency = "€"
elif data["Currency"][0] == "USD":
    currency = "$"
else:
    currency = "₿"

incomes = data[data['Type'] == 'Income']
expenses = data[data['Type'] == 'Expense']

# create array with income types and sum per type
income_types = incomes['Category'].unique()
income_type_sum = []
for it in income_types:
    income_per_type = incomes[incomes['Category'] == it]
    income_type_sum.append(round(income_per_type['Amount'].sum(), 2))

# create array with expense types and sum per type
expense_types = expenses['Category'].unique()
expense_type_sum = []
for et in expense_types:
    expense_per_type = expenses[expenses['Category'] == et]
    expense_type_sum.append(round(expense_per_type['Amount'].sum(), 2))

# compute amount saved during period
savings = round(sum(income_type_sum) - sum(expense_type_sum), 2)

# number of expense/income categories
income_num = len(income_types)
expense_num = len(expense_types)
budget_index = len(income_types)

all_labels = np.concatenate((income_types, ["Budget"], expense_types, ["Savings"]), axis=0).tolist() # create a list of all labels
source_index = np.concatenate((np.linspace(0,income_num,income_num+1,dtype=int), [budget_index]*(expense_num+2)), axis=0).tolist()
target_index = [budget_index]*(income_num+1) + (np.linspace(income_num+1, income_num+expense_num+1, expense_num+1, dtype=int).tolist())
value = income_type_sum + [0] + expense_type_sum + [savings]

print(len(all_labels), len(source_index), len(target_index))
for i in range(len(all_labels)):
    print(source_index[i], all_labels[source_index[i]])
    print(target_index[i], all_labels[target_index[i]])
    print(value[i])

fig = go.Figure(data=[go.Sankey(
    valuesuffix = currency,
    node = dict(
    pad = 15,
    thickness = 20,
    line = dict(color = "black", width = 0.5),
    label = np.asarray(all_labels),
    color = "blue"
    ),
    link = dict(
    source = source_index, # indices correspond to labels, eg A1, A2, A2, B1, ...
    target = target_index,
    value = value
  ))])

fig.update_layout(title_text="My Budget<br><i>github.com/TheEliasBe</i>", font_size=10)
fig.show()