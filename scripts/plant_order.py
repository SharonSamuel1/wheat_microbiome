import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_excel('/Users/srwnlhmy/Github/wheat_microbiome/data/plant_order_11.23.xlsx')
df=df.iloc[:,0:4]

#df=df.iloc[:,0:3]
#Make dure there are 4 repetitions of each:
#df2 = df.iloc[:,0:3].groupby(df.columns.tolist(), as_index=False).size()

# Assign colors to soil types and fertilizers
soil_colors = {'Loess':'#D2B48C' , 'Red': '#A0522D'}
fertilizer_colors = {'F+': '#008000', 'F-': '#929591'}

fig, axs = plt.subplots(48, 4, figsize=(20, 80))

# Create a plot for each row
for i, (index, row) in enumerate(df.iterrows()):
    ax = axs[i % 48, row['Replicate']-1]

    ax.pie([1], colors=[soil_colors[row['Soil']]], radius=1.5, wedgeprops=dict(edgecolor='w'))
    ax.pie([1], colors=[fertilizer_colors[row['Fertilizer']]], radius=1.2, wedgeprops=dict(edgecolor='w'))
    ax.text(0, 0.3, row['Species'], ha='center', va='center', fontsize=15)
    ax.text(0, 0, row['Replicate'], ha='right', va='top', fontsize=15)
    
# Set aspect ratio to be equal
ax.axis('equal')

ax.set_xticks([])
ax.set_yticks([])

plt.savefig('/Users/srwnlhmy/Desktop/plant_order.pdf')
print("a")
# Display the pie plot
plt.show()