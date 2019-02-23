# -*- coding: utf-8 -*-
"""NYCCrime1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19NR4J0Kh0RzQ-ZOWvz0v4cypnVA5tr8T

Its big chunk of dataset so i am only taking the sub-dataset duration of 5 year(12- 16)

Load the data set
"""

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
# %matplotlib inline
plt.style.use('seaborn')
import seaborn as sns
#df=pd.read_csv('Chicago_Crimes_.csv')
df=pd.read_csv('Chicago_Crimes_.csv')

df.head(2)

"""Checking the data set"""

df.columns

df.shape

"""I am removing the un-usable feature those i will not use, so that it will seedup processing of the dataset."""

df.drop(['Unnamed: 0','ID','Case Number','Updated On','Latitude','Longitude', 'Location','IUCR'],axis=1,inplace=True)
df.columns

df.dtypes

"""Check for the missing value"""

df.isna().sum()

"""first converting the date feature in to date format and use it as index value

### Let's understand the crime over the time-period
"""

df.Date = pd.to_datetime(df.Date, format='%m/%d/%Y %I:%M:%S %p')
df.index = pd.DatetimeIndex(df.Date)
plt.figure(figsize=(9,5))
df.resample('M').size().plot(legend=False)
plt.title('Number of crimes over the years')
plt.xlabel('Years')
plt.ylabel('Number of crimes')
plt.show()

"""## Fixed Kind of pattern over time-stamp

**Comment**

From above graph we can see a fix kind-of pattern over a year duration also crime count is decrease over the duraiton form 12 to 2017 and  can see crime is at max during the mid of the year.

The crime is decraseing over time.

### Let's look crime over time (with rolling the days)
"""

plt.figure(figsize=(10,5))
df.resample('D').size().rolling(365).sum().plot()
plt.title('sum of all crimes from 20012 - 2017')
plt.ylabel('Number of crimes')
plt.xlabel('Days')
plt.show()

"""**Comment**

From above rolling sum graph we can conclude that crime rate is decrease from 2013 to 2016 and 2016-2017 have around equal crime.

### **Let's understand categories of crime and its differnt prespective**

Unique feature checking for process data
"""

df.nunique()

"""### ** Let's check most common categories of crime**"""

plt.figure(figsize=(8,10))
df['Primary Type'].value_counts().sort_values(ascending=True).plot(kind='barh')
plt.title('Number of crimes by type')
plt.ylabel('Crime Type')
plt.xlabel('Number of crimes')
plt.show()

"""**Comment**

Theft , Battery, Narcotics are most popular kind of crime.

## **Crime statistics by location**
"""

plt.figure(figsize=(8,4))
df['Location Description'].value_counts().head(8).plot(kind='barh')
plt.ylabel('Crime Loc.')
plt.xlabel('Number of crimes')
plt.show()

"""**Comment-**

most crime are happened at **street, Resindence or can say at private places. **

**Better understand type of crime with location form heat map visulization**
"""

crime_area = pd.DataFrame(df.groupby(['Primary Type', 'Location Description']).size().sort_values(ascending=False).rename('Cnt').reset_index())
#topk = df.groupby(['Primary Type', 'Location Description']).size().reset_index(name='counts').groupby('Primary Type').apply(lambda x: x.sort_values('counts',ascending=False).head(3))
d;lfpivotdf = crime_area.pivot(index='Primary Type', columns='Location Description', values='Cnt')
plt.figure(figsize=(21,7))
sns.heatmap(pivotdf)

"""**Comment**

We can see for Location  like Street and Sidewalk. It makes sense that Theft, Narcotics, Motor Vehicle theft and Battery mostly happened in the streets.

At Residence we see Theft, Burglary, Deceptive Practise and Criminal Damage which are expected. But we also see Assault and Battery.

**Understand the crime by month duration**
"""

from datetime import datetime
df['month']=df.index.month
crime = pd.DataFrame(df.groupby(['month','Year']).size().sort_values(ascending=False).rename('Cnt').reset_index())
print(crime.head())
crime['month']=crime['month'].astype(str)
crime1 = crime.pivot_table(values='Cnt',index='month',columns='Year')
sns.heatmap(crime1)

"""**Comment**

Mid of the Year >>June and July ( 6th , 7th and 8th) months have the **highest crime rate **over the years and can also see that crime rate is descreasing from 2012 to 2017 as color of heatmap is getting lighter.

### Let's understand different ( Top) crime type-
"""

df_theft = df[df['Primary Type'] == "THEFT"]
df_battery = df[df['Primary Type'] == "BATTERY"]

"""Bar plot to understand the sub-categories of Theft"""

df_theft['Description'].value_counts(normalize=True).plot.bar()
plt.title("Theft Types")
plt.show()

df_battery['Description'].value_counts(normalize=True).plot.bar()
plt.title("Battery Types")
plt.show()

"""**Comment**

Theft crime register most for money with small amount. 

Domestic Battery is the most common Battery practice

## **Geographic distribution of crime **

**First plot the district wise different location mentioned in dataset **
"""

df=df[df['Y Coordinate']>0]
df.plot(kind='scatter',x='X Coordinate', y='Y Coordinate', c='District')

"""**Comment**

All districts have a number of crimes associated with them

### Let's check Relative Crime rate among district
"""

plt.figure(figsize=(8,8))
sns.jointplot(x=df['X Coordinate'].values, y=df['Y Coordinate'].values, size=10, kind='hex')
plt.ylabel('Longitude', fontsize=8)
plt.xlabel('Latitude', fontsize=8)
plt.show()

"""**Comment**

We can see that North-West region of chicago has offence recorded than other area

on y axis two kind of cluster creating on N-E and S-E Areas.

**Let's understand Arrest rate**
"""

plt.figure(figsize=(12,12))
sns.lmplot(x='X Coordinate', y='Y Coordinate', size=10, hue='Primary Type', data=df, fit_reg=False)
plt.ylabel('Longitude', fontsize=12)
plt.xlabel('Latitude', fontsize=12)
plt.show()

"""**Comment**

From Geo-plot we are unable to see a specific crime location wise. different crime type are spreaded randomly.

### Arrest Percentage
"""

plt.figure(figsize=(5,4))
df.groupby(['Year','Arrest'])['Domestic'].count().unstack().plot.bar()
plt.title("Arrest Rate")
plt.show()

"""**Comment**

We can see out of total crime only around 0.28 percent arrest done others either be warned as per the severity of the crime.

over the 5 year arrest percenatage is almost constant.
"""



"""## Predictive Use Cases of the dataset

**Future Crime prediction **

**Geographically crime type division and forcasting so necessary action can be taken. **

**Minimization primary type of crime by visulizing root cause and accordingly action items**

### Future Crime Prediction

we have seen earlier a fixed kind of pattern of crime over time duration so we can use time series model further forcasting

by using ARIMA or Prophet model

**ARIMA or Prophet** >>Model work where non-linear trends are fit with yearly, weekly, and daily seasonality. these work best with time series that have strong seasonal effects and several seasons of historical data.
"""



"""We can implement above data-set with checking **seasonality, ACF and PACF value** and fit the model over the data.

Due to some time constraints and occupied by other office activity i am leaving that part.if further  predictive forcasting required please let me know.

## Thanks
"""

def create_day_series(df1):
    
    
    day_df = pd.Series(df1.groupby(['Date']).size())
    # setting Date/Time as index
    day_df.index = pd.DatetimeIndex(day_df.index)
    # Resampling to daily trips
    day_df = day_df.resample('1D').apply(np.sum)
    
    return day_df

df_day = create_day_series(df)
df_day.head()

def initial_plots(time_series, num_lag):

 
    plt.figure(1)
    plt.plot(time_series)
    plt.title('Original data across time')
    plt.figure(2)
    plot_acf(time_series, lags = num_lag)
    plt.title('Autocorrelation plot')
    plot_pacf(time_series, lags = num_lag)
    plt.title('Partial autocorrelation plot')
    
    plt.show()
    
initial_plots(day_df_2014, 45)