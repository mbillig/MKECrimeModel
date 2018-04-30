
# coding: utf-8

# In[84]:


import pandas
import numpy
import scipy
import pickle
import matplotlib.pyplot as plt


# In[22]:


crimeDF = pickle.load( open( "df.pickle", "rb" ))
districtDF = pandas.read_csv("./data/PolicePDFs/DistrictData.csv")
policeDF = districtDF.loc[districtDF['Type'] == "Police"]

policeDF.head()


# In[30]:


crimeCounts = pandas.DataFrame(crimeDF['Police District'].value_counts())
print(districtDF.columns)
print(crimeCounts.columns)
crimeCounts.loc[1, 'Police District']


# In[31]:


#pandas.merge(policeDF, crimeCounts, how='left', on=['District', 'Police District'])
for index, row in policeDF.iterrows():
    district = row['District']
    policeDF.loc[index, 'CrimeCount'] = crimeCounts.loc[district, 'Police District']


# In[32]:


policeDF


# In[78]:


plt.subplot(3,2,1)
plt.scatter(policeDF['Parks'], policeDF['CrimeCount'])
plt.ylabel('Crime Count 2011-2016')
plt.xlabel('Parks')
 
plt.subplot(3,2,2)
plt.scatter(policeDF['Faith Orgs'], policeDF['CrimeCount'])
plt.ylabel('Crime Count 2011-2016')
plt.xlabel('Faith Organizations')
 
plt.subplot(3,2,3)
plt.scatter(policeDF['Liquor Licenses'], policeDF['CrimeCount'])
plt.ylabel('Crime Count 2011-2016')
plt.xlabel('Liquor Licenses')
 
plt.subplot(3,2,4)
plt.scatter(policeDF['18 to 24'], policeDF['CrimeCount'])
plt.ylabel('Crime Count 2011-2016')
plt.xlabel('Population between 18 and 24')

plt.subplot(3,2,5)
plt.scatter(policeDF['Total Familes'], policeDF['CrimeCount'])
plt.ylabel('Crime Count 2011-2016')
plt.xlabel('Total Families')

plt.subplot(3,2,6)
plt.scatter(policeDF['Population'], policeDF['CrimeCount'])
plt.ylabel('Crime Count 2011-2016')
plt.xlabel('Population')

plt.subplots_adjust(top=1.5, bottom=0.01, left=0.10, right=0.95, hspace=0.65, wspace=0.65)
plt.show()


# In[62]:


policeNorm = policeDF
policeNorm['PopDensity'] = policeNorm['Population']/policeNorm['Area sqmi']
policeNorm['Percent 18 to 24'] = policeNorm['18 to 24']/policeNorm['Population']
policeNorm['Percent Families'] = policeNorm['Total Familes']/policeNorm['Population']
policeNorm['Liquor per sqmi'] = policeNorm['Liquor Licenses']/policeNorm['Area sqmi']
policeNorm['Faith Orgs per sqmi'] = policeNorm['Faith Orgs']/policeNorm['Area sqmi']
policeNorm['Parks per sqmi'] = policeNorm['Parks']/policeNorm['Area sqmi']
policeNorm['Crime per sqmi'] = policeNorm['CrimeCount']/policeNorm['Area sqmi']

policeNorm


# In[81]:


plt.subplot(3,2,1)
plt.scatter(policeNorm['Parks per sqmi'], policeNorm['Crime per sqmi'])
plt.ylabel('Crime Count per sq. mile')
plt.xlabel('Parks per sq. mile')
 
plt.subplot(3,2,2)
plt.scatter(policeNorm['Faith Orgs per sqmi'], policeNorm['Crime per sqmi'])
plt.ylabel('Crime Count per sq. mile')
plt.xlabel('Faith Orgs per sq. mile')
 
plt.subplot(3,2,3)
plt.scatter(policeNorm['Liquor per sqmi'], policeNorm['Crime per sqmi'])
plt.ylabel('Crime Count per sq. mile')
plt.xlabel('Liquor Licenses per sq. mile')
 
plt.subplot(3,2,4)
plt.scatter(policeNorm['Percent 18 to 24'], policeNorm['Crime per sqmi'])
plt.ylabel('Crime Count per sq. mile')
plt.xlabel('Percent Population between 18 and 24')

plt.subplot(3,2,5)
plt.scatter(policeNorm['Percent Families'], policeNorm['Crime per sqmi'])
plt.ylabel('Crime Count per sq. mile')
plt.xlabel('Total Families / Population')

plt.subplot(3,2,6)
plt.scatter(policeNorm['PopDensity'], policeNorm['Crime per sqmi'])
plt.ylabel('Crime Count per sq. mile')
plt.xlabel('Population Density')

plt.subplots_adjust(top=1.5, bottom=0.01, left=0.10, right=0.95, hspace=0.65, wspace=0.65)
plt.show()


# In[99]:


plt.subplot(211)
plt.bar(policeDF['District'], policeDF["Population"])
plt.xlabel("Police District")
plt.ylabel("Population")
plt.subplot(212)
plt.bar(policeDF['District'], policeDF["Area sqmi"])
plt.xlabel("Police District")
plt.ylabel("Area (sq miles)")
plt.subplots_adjust(top=1.5, bottom=0.01, left=0.10, right=0.95, hspace=0.35, wspace=0.65)

plt.show()

