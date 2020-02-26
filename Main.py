import plotly.graph_objects as go
import numpy as np
from numpy import genfromtxt
import pandas as pd

data = pd.read_csv("MoneyCoach.csv", delimiter=';', header=0)
data['Amount'] = data['Amount'].apply(lambda x : x.replace('.','').replace(',','.'))
print(data['Amount'])
data['Amount'] = data['Amount'].astype('float')
incomes = data[data['Type'] == 'Income']
expenses = data[data['Type'] == 'Expense']
income_types = incomes['Category'].unique()
income_type_sum = []

for it in income_types:
    income_per_type = incomes[incomes['Category'] == it]
    print(income_per_type['Amount'])
    income_type_sum.append(income_per_type['Amount'].sum())

print(income_type_sum)
print(income_types)

all_labels = income_types + ['Budget']

fig = go.Figure(data=[go.Sankey(
    node = dict(
    pad = 15,
    thickness = 20,
    line = dict(color = "black", width = 0.5),
    label = np.asarray(income_types),
    color = "blue"
    ),
    link = dict(
    source = [0,1,2,3,4], # indices correspond to labels, eg A1, A2, A2, B1, ...
    target = [5,5,5,5,5],
    value = np.asarray(income_type_sum)
  ))])

fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
fig.show()