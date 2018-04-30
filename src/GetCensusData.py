
# coding: utf-8

# In[2]:


import os
import requests
import pandas as pd
import numpy as np
from tabula import read_pdf
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select


# In[2]:


# https://itmdapps.milwaukee.gov/publicApplication_SR/censusTractfm.jsp

opts = Options()
# opts.set_headless()
# assert opts.headless  # operating in headless mode
path = r"C:/Users/marie/Documents/_AdvancedDataScience/MKECrimeModel/geckodriver.exe"

browser = Firefox(executable_path=path, options=opts)
browser.get('https://itmdapps.milwaukee.gov/publicApplication_SR/censusTractfm.jsp')


# In[3]:


# get and save all needed pdfs of census tract data
dropdown = browser.find_element_by_name('CensusTracts')
censusTracts = [x.get_attribute("value") for x in dropdown.find_elements_by_tag_name("option")]
for tract in censusTracts:
    url = "https://itmdapps.milwaukee.gov/publicApplication_SR/CensusTractServlet?CensusTracts=%s&fromDate=01%%2F01%%2F2005&toDate=01%%2F01%%2F2016&submit=Submit" % (tract)
    r = requests.get(url, allow_redirects=True)
    fileName = './data/CensusTracts/tract%s.pdf' % (tract)
    open(fileName, 'wb').write(r.content)
    print(fileName)
    
#search_form = browser.find_element_by_id('search_form_input_homepage')
#search_form = browser.find_element_by_name('CensusTracts')    
    
#dropdown = Select(browser.find_element_by_name('CensusTracts'))
#dropdown.select_by_value('201')

#fromDateBox = browser.find_element_by_name('fromDate')
#fromDateBox.send_keys('01/01/2005')
#toDateBox = browser.find_element_by_name('toDate')
#toDateBox.send_keys('01/01/2016')

#submitButton = browser.find_element_by_name('submit')
#submitButton.click()

#results = browser.find_elements_by_class_name('result')
#print(results)

#browser.close()
#quit()
#censusTracts


# In[73]:


# Not the cleanest, but I just ran this 3 times for census, police and aldermanic districts

#df = pd.DataFrame(columns=dfCols)
dfCols = ['District', 'Type', 'Population', 'Area sqmi', 'Under 5', '5 to 17', '18 to 24', '25 to 44', '45 to 64', 'Over 65', 'Male', 'Female', 'Total Families', 'Avg Residential Value', 'Liquor Licenses', 'Faith Orgs', 'Parks', 'Total A Offenses', 'Assault Offenses', 'Arson', 'Burglary', 'Criminal Damages', 'Locked Vehicle', 'Robbery', 'Sex Offense', 'Theft', 'Vehicle Theft', 'Homicide']

#pathToPDFs = '../data/CensusTracts/'
#pathToPDFs = '../data/PolicePDFs/'
pathToPDFs = '../data/Aldermanic/'
pdfLists = os.listdir(pathToPDFs)
for pdf in pdfLists:
    print(pdf)
    demoDF = read_pdf(pathToPDFs + pdf, pages='1-3')
    crimeDF = read_pdf(pathToPDFs + pdf, pages=4)
    
    #district = pdf.replace('tract', '').replace('.pdf', '')
    #distType = 'CensusTract'
    #district = pdf.replace('PoliceDistrict', '').replace('.pdf', '')
    #distType = 'PoliceDistrict'
    district = int(pdf.replace('AldermanicDistrict', '').replace('.pdf', ''))
    distType = 'AldermanicDistrict'
    
    
    population = int(demoDF.loc[demoDF['Unnamed: 0'] == 'Total Population', demoDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    area = float(demoDF.loc[demoDF['Unnamed: 0'] == 'Area (Square miles)', demoDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    under5 = int(demoDF.loc[demoDF['Unnamed: 0'] == 'Under 5 years', demoDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    between5and17 = int(demoDF.loc[demoDF['Unnamed: 0'] == '5 to 17 years', demoDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    between18and24 = int(demoDF.loc[demoDF['Unnamed: 0'] == '18 to 24 years', demoDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    between25and44 = int(demoDF.loc[demoDF['Unnamed: 0'] == '25 to 44 years', demoDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    between45and64 = int(demoDF.loc[demoDF['Unnamed: 0'] == '45 to 64 years', demoDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    over65 = int(demoDF.loc[demoDF['Unnamed: 0'] == '65 years and over', demoDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    male = int(demoDF.loc[demoDF['Unnamed: 0'] == 'Male', demoDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    female = int(demoDF.loc[demoDF['Unnamed: 0'] == 'Female', demoDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    families = int(demoDF.loc[demoDF['Unnamed: 0'] == 'Total families', demoDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    residentialValue = float(demoDF.loc[demoDF['Unnamed: 0'] == 'Average Assessed Residential Value (current)', demoDF.columns[1]].values[0].split(' ')[0].replace(',', '').replace('$', ''))
    liquorLicenses = int(demoDF.loc[demoDF['Unnamed: 0'] == 'Total Liquor Licenses', demoDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    faithOrgs = int(demoDF.loc[demoDF['Unnamed: 0'] == 'Faith Based Organizations', demoDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    parks = int(demoDF.loc[demoDF['Unnamed: 0'] == 'Parks', demoDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    
    totalAOffenses = int(crimeDF.loc[crimeDF['Unnamed: 0'] == 'Total Summary WIBR for specific group A offenses', crimeDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    assault = int(crimeDF.loc[crimeDF['Unnamed: 0'] == 'Assault Offenses', crimeDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    arson = int(crimeDF.loc[crimeDF['Unnamed: 0'] == 'Arson', crimeDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    burglary = int(crimeDF.loc[crimeDF['Unnamed: 0'] == 'Burglary', crimeDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    criminalDamages = int(crimeDF.loc[crimeDF['Unnamed: 0'] == 'Criminal Damage', crimeDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    lockedVehicle = int(crimeDF.loc[crimeDF['Unnamed: 0'] == 'Locked Vehicle', crimeDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    robbery = int(crimeDF.loc[crimeDF['Unnamed: 0'] == 'Robbery', crimeDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    sexOffense = int(crimeDF.loc[crimeDF['Unnamed: 0'] == 'Sex Offense', crimeDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    theft = int(crimeDF.loc[crimeDF['Unnamed: 0'] == 'Theft', crimeDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    vehicleTheft = int(crimeDF.loc[crimeDF['Unnamed: 0'] == 'Vehicle Theft', crimeDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    homicide = int(crimeDF.loc[crimeDF['Unnamed: 0'] == 'Homicide', crimeDF.columns[1]].values[0].split(' ')[0].replace(',', ''))
    
    row = pd.DataFrame([[district, distType, population, area,                         under5, between5and17, between18and24, between25and44, between45and64, over65,                         male, female, families,                         residentialValue, liquorLicenses, faithOrgs, parks,                         totalAOffenses, assault, arson, burglary, criminalDamages,                         lockedVehicle, robbery, sexOffense, theft, vehicleTheft, homicide]], 
                       columns = dfCols)
    df = df.append(row)


# In[75]:


df.to_csv('../data/CensusPoliceAldermanicData.csv', index=False)

