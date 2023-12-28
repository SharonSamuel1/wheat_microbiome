import pandas as pd

df = pd.read_excel('/Users/srwnlhmy/Github/wheat_microbiome/data/plant_order_11.23.xlsx')
df=df.iloc[:,0:3]

soil_coding = {'Loess':'L' , 'Red': 'R'}
fertilizer_coding = {'F+': '+', 'F-': '-'}
species=set(df=df.iloc[:,2])
species_coding = {x:species.count(x) for x in species}

df['code'] = df.apply(lambda row: f"{soil_coding.get(row['Soil'], '')}{fertilizer_coding.get(row['Fertilizer'], '')}{species_coding.get(row['Species'], '')}{row['Repetition']}", axis=1)

df.to_excel("data/plants_coded.xlsx")

print ("delete!")