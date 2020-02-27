import plotly.graph_objects as go
import numpy as np
from numpy import genfromtxt
import pandas as pd

data = pd.read_csv("MoneyCoach.csv", delimiter=';', header=0)
data['Amount'] = data['Amount'].apply(lambda x : x.replace('.','').replace(',','.'))
data['Amount'] = data['Amount'].astype('float')
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

all_labels = np.concatenate((income_types, ["Budget"], expense_types, ["Savings"]), axis=0).tolist()
source_index = np.concatenate((np.linspace(0,5,6,dtype=int), [6]*(len(expense_types)+2)), axis=0).tolist()
target_index = [6]*len(income_types) + [6] + (np.linspace(len(income_types)+1, len(income_types)+len(expense_types)+1, len(expense_types)+1, dtype=int).tolist())
value = income_type_sum + [0] + expense_type_sum + [savings]

print(len(all_labels), len(source_index), len(target_index))
for i in range(len(all_labels)):
    print(source_index[i], all_labels[source_index[i]])
    print(target_index[i], all_labels[target_index[i]])
    print(value[i])

fig = go.Figure(data=[go.Sankey(
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

fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
fig.show()