
# coding: utf-8

# In[194]:


import os
import json
import numpy
import pandas
import ast
import re
import datetime
import pickle
import difflib


# In[36]:


f = open("data/CrimeData/2011_01_assault_clustered.js", "r") 


# In[37]:


lines = f.readlines()
f.close()

nHeaderLines = 3
nFooterLines = 3
records = len(lines) - nHeaderLines - nFooterLines


# In[132]:


def parseLine(jsLine, crimeSet):
    cleanLine = jsLine.replace(" },\n", "")
    cleanLine = cleanLine.replace(" \"type\": \"Feature\", \"properties\": { \"Unnamed: 0\": ", "")
    cleanLine = cleanLine.split(",", 1)
    cleanLine = "{" + cleanLine[1]
    cleanLine = cleanLine.split(", \"geometry")
    cleanLine = cleanLine[0]
    cleanLine = re.sub("\"Offense 2\".*Location\"", "\"Location\"", cleanLine)
    #print(cleanLine)

    try:
        dictLine = ast.literal_eval(cleanLine)
        dictLine["DateTime"] = datetime.datetime.strptime(dictLine["Date"] + " " + dictLine["Time"], "%m\/%d\/%Y %I:%M %p")
        dictLine["CrimeSet"] = crimeSet
        return dictLine
    except ValueError:
        print("ERROR converting string")
        print(cleanLine)
        return "ERROR"


# In[134]:


df = pandas.DataFrame()
path = "./data/CrimeData/"
allFiles = os.listdir(path)
nBadRecords = 0

for fileName in allFiles:
    print(fileName)
    f = open(path + fileName, "r") 
    lines = f.readlines()
    f.close()

    nHeaderLines = 3
    nFooterLines = 3
    crimeSet = fileName.split("_")[2]
    nRecords = len(lines) - nHeaderLines - nFooterLines
    print(nRecords)
    records = lines[nHeaderLines + 1:nHeaderLines + nRecords]
    iLine = nHeaderLines + 1
    for record in records:
        dictRecord = parseLine(record, crimeSet)
        if(dictRecord != "ERROR"):
            if(len(df.columns) == 0):
                df = pandas.DataFrame(dictRecord)
            else:
                df = df.append(dictRecord, ignore_index=True) 
        else:
            print("Error on line " + str(iLine))
            nBadRecords += 1;
        iLine += 1


# In[139]:


df.head()
pickleFile = open("df.pickle", "wb")
pickle.dump(df, pickleFile)
pickleFile.close()


# In[243]:


df = pickle.load( open( "df.pickle", "rb" ))


# In[245]:


df = df.drop(['Address,'], axis=1)
df.head()


# In[146]:


## Get aldermanic districts
mprop = pandas.read_csv("./data/Mprop.csv")
mprop.columns


# In[192]:


mprop["HOUSE_NR_SFX"] = mprop["HOUSE_NR_SFX"].fillna('')
mprop.loc[mprop["HOUSE_NR_SFX"].str.isalnum(), "HOUSE_NR_SFX"] = "-" + mprop["HOUSE_NR_SFX"]

mprop["FULL_ADDRESS"] = mprop["HOUSE_NR_LO"].map(str) + mprop["HOUSE_NR_SFX"] + " " + mprop["SDIR"] + " " + mprop["STREET"] + " " + mprop["STTYPE"]
mprop.head()

print(mprop['FULL_ADDRESS'].isnull().sum())
mprop['FULL_ADDRESS'] = mprop['FULL_ADDRESS'].fillna('')
print(mprop['FULL_ADDRESS'].isnull().sum())


# In[246]:


#df = df.drop(["Adermanic_District"], axis=1)
df["Aldermanic_District"] = numpy.nan
df.head()
totalFound = 0
totalFuzzy = 0
totalNotFound = 0
maxIndex = 0


# In[342]:


#maxIndex = 58035
totalNotFound = 1


# In[344]:



for index, row in df.iterrows():
    if index > maxIndex:
        if(index % 100 == 0 and index != 0):
            print("INDEX: " + str(index))
            print("found: " + str(totalFound))
            print("fuzzy: " + str(totalFuzzy))
            print("not found: " + str(totalNotFound))
            print("Null dists: " + str(df["Aldermanic_District"].isnull().sum()))
            pickleFile = open("alder.pickle", "wb")
            pickle.dump(df, pickleFile)
            pickleFile.close()

        if pandas.isnull(row['Address']):
            print('Address is null')
            df.loc[index, 'Aldermanic_District'] = numpy.nan
            totalNotFound += 1

        else:
            rootAddr = row['Address'].split(" #")[0];
            found = mprop['FULL_ADDRESS'].str.contains(rootAddr).any()
            if found == True:
                totalFound += 1
                dist = mprop[mprop['FULL_ADDRESS']==rootAddr]['GEO_ALDER'].tolist()
                if len(dist) == 0:
                    dist = numpy.nan
                else:
                    dist = dist[0]
                df.loc[index, 'Aldermanic_District'] = dist
            else:
                print("    " + rootAddr)
                matches = difflib.get_close_matches(rootAddr, mprop['FULL_ADDRESS'].tolist(), 5)
                #mprop.loc[mprop["FULL_ADDRESS"] == matches, "GEO_ALDER"]
                dist = mprop[mprop["FULL_ADDRESS"].isin(matches)]["GEO_ALDER"].mode()
                #row['Aldermanic_District'] = dist[0]
                #df.iloc[index, 'Aldermanic_District'] = dist[0]
                if len(dist) == 0:
                    df.loc[index, 'Aldermanic_District'] = numpy.nan
                else:
                    df.loc[index, 'Aldermanic_District'] = dist[0]
                totalFuzzy += 1
        maxIndex = index


# In[228]:


a = "7061 N TEUTONIA AV #206"
poss = mprop['FULL_ADDRESS'].tolist();
matches = difflib.get_close_matches(a, poss, 5)
print(matches)
dist = mprop[mprop["FULL_ADDRESS"].isin(matches)]["GEO_ALDER"].mode()
dist[0]


# In[335]:


print(pandas.isnull(row['Address']))
print(pandas.isnull(rootAddr))


# In[346]:


print(maxIndex)
print(len(df))
print(df["Aldermanic_District"].isnull().sum())
pickleFile = open("alderFULL.pickle", "wb")
pickle.dump(df, pickleFile)
pickleFile.close()

