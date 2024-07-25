import pandas as pd
from plotnine import (
    ggplot, geom_point, geom_line, aes, scale_color_manual,
    scale_shape_manual, position_jitter, labs, theme_classic,
    element_text, theme,geom_boxplot,scale_fill_manual,coord_flip,scale_x_date,scale_size_manual,ggsave,
)
import math
import numpy as np
#from scipy import stats 
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from matplotlib import pyplot as plt


df = pd.read_excel('/home/projects/zeevid/samuelsh/wheat_microbiome/data/plants_data.xlsx')
df = df.iloc[:, list(range(7)) + [11]+ [12]]
#df.dropna(subset=['date_samp'], inplace=True)

#pots to delete:
deleted_pots = df[df['order_in_greenhouse'].isin([165,139,141, 184,99])].index #these are pots that will not be included in the analysis- detailes in the excel
df=df.drop(deleted_pots)

df['date_samp'] = pd.to_datetime(df['date_samp'])
df['S'] =df['S'].astype(str)
df['Fert'] = df['Fert'].astype(str)

#which type of soil to consider:
df = df.loc[df['Soil'] == 'Loess']
#df = df.loc[df['Soil'] == 'Red']

group_and_type_by_species = {
    '65': ('landrace', 'aestivum'),
    '252': ('landrace', 'aestivum'),
    '69': ('landrace', 'aestivum'),
    '66': ('landrace', 'aestivum'),
    '9': ('landrace', 'durum'),
    '726': ('landrace', 'durum'),
    '42': ('landrace', 'durum'),
    '13': ('landrace', 'durum'),
    'Bar nir': ('Mod', 'aestivum'),
    'Gadish': ('Mod', 'aestivum'),
    'C9': ('Mod', 'durum'),
    'Zavitan': ('wild', 'wild'),
}

df['group'], df['type'] = zip(*df['S'].map(lambda s: group_and_type_by_species.get(s)))
df['group_type'] = df['group'] + '_' + df['type']

species_order = ['65', '252', '69', '66', '9', '726', '42', '13', 'Bar nir', 'Gadish', 'C9', 'Zavitan']
df['S'] = pd.Categorical(df['S'], categories=species_order, ordered=True)
df.sort_values(by='S', inplace=True)

palette = {
    'landrace_aestivum': '#003366',  # Dark blue
    'landrace_durum': '#ADD8E6',     # Light blue
    'Mod_aestivum': '#CC0000',       # Dark red
    'Mod_durum': '#FFA07A',          # Light red (salmon)
    'wild_wild': 'green'
}

markers = {
    'F+': 'o', 
    'F-': '^'
}

planting_day = pd.to_datetime('2023-11-23')
df['days_since_planting'] = (df['date_samp'] - planting_day).dt.days
fert_size_mapping = {'F+': 1, 'F-': 0.3}
df['Fert'] = pd.Categorical(df['Fert'], categories=['F+', 'F-'])

#flowering time:::

flower_df = df.copy()

dot_counts = flower_df.groupby(['S', 'date_samp']).size().reset_index(name='count')
flower_df = flower_df.merge(dot_counts, on=['S', 'date_samp'], how='left')
date_limits = ['2024-02-01', '2024-04-21']

date_limits = [pd.to_datetime(date) for date in date_limits]

p = (
    ggplot(flower_df, aes(x='date_samp', y='S', color='group_type', shape='Fert'))
    + geom_point(size=3, alpha=0.7, position=position_jitter(width=1,height=0.1))
    + geom_line(aes(group='S', color='group_type', size='np.maximum(count, 1)'), alpha=0.2)
    + scale_color_manual(values=palette)
    + scale_shape_manual(values=markers)
    + labs(title='Flowering Time- Loess Soil', x='Date', y='Species')
    + theme_classic()
    + theme(
        axis_text_x=element_text(size=12),
        axis_text_y=element_text(size=12),
        legend_title=element_text(size=12),
        legend_text=element_text(size=12)
    )
    + scale_x_date(date_labels='%d-%m', date_breaks='1 month', limits=date_limits)
)
ggsave(p, filename = '/home/projects/zeevid/samuelsh/wheat_microbiome/results/plants_metadata/flowering_time_by_lines_loess.pdf')

print(p)


p = (
    ggplot(flower_df, aes(x='group_type', y='days_since_planting', fill='group_type',color='Fert')) #changes from "group"
    + geom_boxplot(aes(size='Fert'),alpha=0.5)
    #+ scale_fill_manual(values=['red','#0072B2','green'])
    + scale_fill_manual(values=palette) 
    + scale_color_manual(values=['black', 'black'])  
    + theme_classic()
    + labs(title='Days Since Planting by Groups- Loess Soil', x='Group', y='Days Since Planting')
    + theme(
        axis_text_x=element_text(size=12),
        axis_text_y=element_text(size=12),
        legend_title=element_text(size=12),
        legend_text=element_text(size=12)
    )
    +  scale_size_manual(values=fert_size_mapping)
    +theme(axis_text_x = element_text(angle = 15))
)
ggsave(p, filename = '/home/projects/zeevid/samuelsh/wheat_microbiome/results/plants_metadata/days_since_planting_by_groups_loess.pdf')

print(p)

#transformation
flower_df['log_days_since_planting'] = np.log(flower_df['days_since_planting'])

p = (
    ggplot(flower_df, aes(x='group_type', y='log_days_since_planting', fill='group_type',color='Fert')) #changes from "group"
    + geom_boxplot(aes(size='Fert'),alpha=0.5)
    #+ scale_fill_manual(values=['red','#0072B2','green'])
    + scale_fill_manual(values=palette) 
    + scale_color_manual(values=['black', 'black'])  
    + theme_classic()
    + labs(title='Days Since Planting by Groups- Loess Soil', x='Group', y='Days Since Planting')
    + theme(
        axis_text_x=element_text(size=12),
        axis_text_y=element_text(size=12),
        legend_title=element_text(size=12),
        legend_text=element_text(size=12)
    )
    +  scale_size_manual(values=fert_size_mapping)
    +theme(axis_text_x = element_text(angle = 15))
)
ggsave(p, filename = '/home/projects/zeevid/samuelsh/wheat_microbiome/results/plants_metadata/days_since_planting_by_groups_trans_loess.pdf')

print(p)


#for stat tests with R
#df.to_csv("'/home/projects/zeevid/samuelsh/wheat_microbiome/data/Loess_for_tests.csv")- delete?


#plant weight:::
weight_df = df.copy()

#pots to delete:
weight_df = weight_df.dropna(subset=['weight_spike(mg)']) 
didnt_weight = weight_df[weight_df['weight_spike(mg)'].isin(["didn't weight"])].index #these are pots that we did not measure (started meauring only after some sampling days)
weight_df=weight_df.drop(didnt_weight)

weight_df['weight_spike(mg)'] = pd.to_numeric(weight_df['weight_spike(mg)'])

fert_size_mapping = {'F+': 1, 'F-': 0.3}
weight_df['Fert'] = pd.Categorical(weight_df['Fert'], categories=['F+', 'F-'])

#by lines:
p = (
    ggplot(weight_df, aes(x='S', y='weight_spike(mg)', fill='group_type', color='Fert'))
    + geom_boxplot(aes(size='Fert'), alpha=0.5)  
    + scale_color_manual(values=['black', 'black']) 
    + scale_fill_manual(values=palette)  
    + theme_classic()
    + labs(title='Spike Weight by Lines- Loess Soil', x='Wheat Line', y='Spike Weight (mg)')
    + theme(
        axis_text_x=element_text(size=12),
        axis_text_y=element_text(size=12),
        legend_title=element_text(size=12),
        legend_text=element_text(size=12),
    )
    + coord_flip()
    +  scale_size_manual(values=fert_size_mapping)
    + theme(figure_size=(6,6))

)
ggsave(p, filename = '/home/projects/zeevid/samuelsh/wheat_microbiome/results/plants_metadata/spike_weight_by_lines_Loess.pdf')

print(p)

#trans
weight_df['log_weight_spike'] = np.log(weight_df['weight_spike(mg)'])

#by lines:
p = (
    ggplot(weight_df, aes(x='S', y='log_weight_spike', fill='group_type', color='Fert'))
    + geom_boxplot(aes(size='Fert'), alpha=0.5)  
    + scale_color_manual(values=['black', 'black']) 
    + scale_fill_manual(values=palette)  
    + theme_classic()
    + labs(title='Spike Weight by Lines- Loess Soil', x='Wheat Line', y='Spike Weight (mg) (log10)')
    + theme(
        axis_text_x=element_text(size=12),
        axis_text_y=element_text(size=12),
        legend_title=element_text(size=12),
        legend_text=element_text(size=12),
    )
    + coord_flip()
    +  scale_size_manual(values=fert_size_mapping)
    + theme(figure_size=(6,6))

)
ggsave(p, filename = '/home/projects/zeevid/samuelsh/wheat_microbiome/results/plants_metadata/spike_weight_by_lines_trans_loess.pdf')

print(p)

#by groups_type:

p = (
    ggplot(weight_df, aes(x='group_type', y='weight_spike(mg)', fill='group_type',color='Fert')) #changes from "group"
    + geom_boxplot(aes(size='Fert'),alpha=0.5)
    + scale_fill_manual(values=palette) 
    + scale_color_manual(values=['black', 'black'])  
    + theme_classic()
    + labs(title='Spike Weight by Groups- Loess Soil', x='Group', y='Spike Weight (mg)')
    + theme(
        axis_text_x=element_text(size=12),
        axis_text_y=element_text(size=12),
        legend_title=element_text(size=12),
        legend_text=element_text(size=12)
    )
    +  scale_size_manual(values=fert_size_mapping)
    +theme(axis_text_x = element_text(angle = 15))
)
ggsave(p, filename = '/home/projects/zeevid/samuelsh/wheat_microbiome/results/plants_metadata/spike_weight_by_groups_loess.pdf')

print(p)

#trans

p = (
    ggplot(weight_df, aes(x='group_type', y='log_weight_spike', fill='group_type',color='Fert')) #changes from "group"
    + geom_boxplot(aes(size='Fert'),alpha=0.5)
    + scale_fill_manual(values=palette) 
    + scale_color_manual(values=['black', 'black'])  
    + theme_classic()
    + labs(title='Spike Weight by Groups- Loess Soil', x='Group', y='Spike Weight (mg) (log10)')
    + theme(
        axis_text_x=element_text(size=12),
        axis_text_y=element_text(size=12),
        legend_title=element_text(size=12),
        legend_text=element_text(size=12)
    )
    +  scale_size_manual(values=fert_size_mapping)
    +theme(axis_text_x = element_text(angle = 15))
)
ggsave(p, filename = '/home/projects/zeevid/samuelsh/wheat_microbiome/results/plants_metadata/spike_weight_by_groups_trans_loess.pdf')

print(p)

#plant height

height_df = df.copy()

p = (
    ggplot(height_df, aes(x='S', y='plant_height_(cm)', fill='group_type', color='Fert'))
    + geom_boxplot(aes(size='Fert'), alpha=0.5)  
    + scale_color_manual(values=['black', 'black']) 
    + scale_fill_manual(values=palette)  
    + theme_classic()
    + labs(title='Plant Height by Lines- Loess Soil', x='Wheat Line', y='Plant Height (cm)')
    + theme(
        axis_text_x=element_text(size=12),
        axis_text_y=element_text(size=12),
        legend_title=element_text(size=12),
        legend_text=element_text(size=12),
    )
    + coord_flip()
    +  scale_size_manual(values=fert_size_mapping)
    + theme(figure_size=(6,6))

)
ggsave(p, filename = '/home/projects/zeevid/samuelsh/wheat_microbiome/results/plants_metadata/plant_height_by_lines_loess.pdf')

print(p)

#by groups_type:

p = (
    ggplot(height_df, aes(x='group_type', y='plant_height_(cm)', fill='group_type',color='Fert')) #changes from "group"
    + geom_boxplot(aes(size='Fert'),alpha=0.5)
    + scale_fill_manual(values=palette) 
    + scale_color_manual(values=['black', 'black'])  
    + theme_classic()
    + labs(title='Plant Height by Groups- Loess Soil', x='Group', y='Plant Height (cm)')
    + theme(
        axis_text_x=element_text(size=12),
        axis_text_y=element_text(size=12),
        legend_title=element_text(size=12),
        legend_text=element_text(size=12)
    )
    +  scale_size_manual(values=fert_size_mapping)
    +theme(axis_text_x = element_text(angle = 15))
)
ggsave(p, filename = '/home/projects/zeevid/samuelsh/wheat_microbiome/results/plants_metadata/plant_height_by_groups_loess.pdf')

print(p)
