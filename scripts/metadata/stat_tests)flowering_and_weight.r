
install.packages("multcomp")

library(dplyr)
library(lubridate)
library(readxl)
library(tidyverse)
#library(Hmisc)
library(reshape2)
library(car)
library(kableExtra)
library(stargazer)

library(ggplot2)
library(ggpubr)
library(multcomp)


df=read_excel("/home/projects/zeevid/samuelsh/wheat_microbiome/data/plants_data.xlsx")

df <- df[, c(1:7, 12,13)]
df <- df[complete.cases(df$date_samp), ]

# Convert 'date_samp' column to Date type
df$date_samp <- ymd(df$date_samp)

# Define pots to delete and remove them from the DataFrame
deleted_pots <- c(165, 139, 141, 184, 99)
df <- df[!df$order_in_greenhouse %in% deleted_pots, ]

df$S <- as.factor(df$S)
df$Fert <- as.factor(df$Fert)

#pick type of soil
df <- df[df$Soil == 'Red', ]
#df <- df[df$Soil == 'Loess', ]

df$Fert <- as.character(df$Fert)

group_and_type_by_species <- list(
  '65' = c('landrace', 'aestivum'),
  '252' = c('landrace', 'aestivum'),
  '69' = c('landrace', 'aestivum'),
  '66' = c('landrace', 'aestivum'),
  '9' = c('landrace', 'durum'),
  '726' = c('landrace', 'durum'),
  '42' = c('landrace', 'durum'),
  '13' = c('landrace', 'durum'),
  'Bar nir' = c('Mod', 'aestivum'),
  'Gadish' = c('Mod', 'aestivum'),
  'C9' = c('Mod', 'durum'),
  'Zavitan' = c('wild', 'wild')
)

df$group <- unlist(lapply(df$S, function(s) group_and_type_by_species[[as.character(s)]][1]))
df$type <- unlist(lapply(df$S, function(s) group_and_type_by_species[[as.character(s)]][2]))

df$group_type <- paste(df$group, df$type, sep = '_')

df$date_samp <- as.Date(df$date_samp)

planting_day <- as.Date('2023-11-23')

df$days_since_planting <- as.numeric(df$date_samp - planting_day)


#days since planting:

df_days <- df[,c("Fert","S","days_since_planting","group_type","group")]
df_long <- reshape2::melt(df_days)

#levene
leveneTest(value~group_type*Fert,data=df_long, center=mean)

#Anova


aov.org <- aov(
  days_since_planting ~ group_type * Fert, data = df_days,
  contrasts = list(
    Fert = 'contr.sum',
    group_type = 'contr.sum'
  )
)
Anova(aov.org, type = 'III')


aov.log <- aov(
  log10(days_since_planting) ~ group_type * Fert, data = df_days,
  contrasts = list(
    Fert = 'contr.sum',
    group_type = 'contr.sum'
  )
)
Anova(aov.log, type = 'III')

aov.rnk <- aov(
  rank(days_since_planting) ~ group_type * Fert, data = df_days,
  contrasts = list(
    Fert = 'contr.sum',
    group_type = 'contr.sum'
  )
)
Anova(aov.rnk, type = 'III')

#normality
shapiro.test(aov.org$residual)
shapiro.test(aov.log$residual)
shapiro.test(aov.rnk$residual)

#Tuckey

TukeyHSD(aov.rnk)





#spike weight


df_weight <- df[,c("Fert","S","weight_spike(mg)","group","group_type")]

df_weight <- df_weight %>% filter(`weight_spike(mg)` != "didn't weight")

df_weight$`weight_spike(mg)` <- as.numeric(df_weight$`weight_spike(mg)`)

df_long <- reshape2::melt(df_weight)

colnames(df_weight) <- c("Fert","S","weight_spike","group","group_type")

#levene
leveneTest(value~group*Fert,data=df_long, center=mean)

#Anova


aov.org <- aov(
  weight_spike ~ group_type * Fert, data = df_weight,
  contrasts = list(
    Fert = 'contr.sum',
    group_type = 'contr.sum'
  )
)
Anova(aov.org, type = 'III')


aov.log <- aov(
  log10(weight_spike) ~ group_type * Fert, data = df_weight,
  contrasts = list(
    Fert = 'contr.sum',
    group_type = 'contr.sum'
  )
)
Anova(aov.log, type = 'III')

aov.rnk <- aov(
  rank(weight_spike) ~ group_type * Fert, data = df_weight,
  contrasts = list(
    Fert = 'contr.sum',
    group_type = 'contr.sum'
  )
)
Anova(aov.rnk, type = 'III')

#normality
shapiro.test(aov.org$residual)
shapiro.test(aov.log$residual)
shapiro.test(aov.rnk$residual)

#Tuckey

TukeyHSD(aov.rnk)

cor(df_weight$weight_spike
    )


