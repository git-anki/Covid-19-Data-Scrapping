#Selenium:  Selenium is a web testing library. It is used to automate browser activities.
#BeautifulSoup: Beautiful Soup is a Python package for parsing HTML and XML documents. It creates parse trees that is helpful to extract the data easily.
#Pandas: Pandas is a library used for data manipulation and analysis. It is used to extract the data and store it in the desired format. 


#importing libraries

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


print ("Library Imported Successfully \n-----------------------------\n")

#To configure webdriver which is a selenium method to use Chrome browser, we have to set the path to chromedriver
driver = webdriver.Chrome(r"C:\Users\USER\Downloads\chromedriver_win32\chromedriver.exe")
print("Driver Configured Successfully \n-----------------------------\n")



#opening a webpage
driver.get("https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data/India_medical_cases_by_state_and_union_territory")

#Selenium stores the source HTML in the driver's page_source
html = driver.page_source

#parsing the page using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

#taking out table
tag = soup.table

#Important Note: 
# 1. the above tag needs to be converted into string for Pandas
# 2. pd.read_html returns you a list with one element and that element is the pandas dataframe, i.e.
# 3. Remove Header and first rows
dfs = pd.read_html(str(tag), header=0, skiprows=1) #generate a list of dataframe

#converting into dataframe 
df_conver = dfs[0] 

#removing extra columns, it returns null, modify dataframe
df_conver.drop(df_conver.iloc[:,5:9], axis=1, inplace = True)

#selecting only required rows, doesnot modify
df = df_conver.iloc[1:35]

#setting state name as index
df = df.set_index('State/Union Territory').rename_axis(index=None, columns='State/Union Territory')

#correcting column name and data
df = df.rename({"Cases[a]": "Cases"}, axis=1)
df.loc["Assam"]["Cases"] = 90740
df.loc['Kerala', 'Deaths'] = 223

#converting data into integer type

df['Cases'] = df['Cases'].map(int)
df['Deaths'] = df['Deaths'].map(int)
df['Recoveries']= df['Recoveries'].map(int)
df['Active'] = df['Active'].map(int)

print(df.head(5))

#printing bar chart
sns.set_style('ticks')
plt.figure(figsize = (25,15))
plt.barh(df.index,df["Cases"].map(int),align = 'center', color = 'lightblue', edgecolor = 'blue')
plt.xlabel('No. of Confirmed cases', fontsize = 18)
plt.ylabel('States/UT', fontsize = 18)
plt.gca().invert_yaxis()
plt.xticks(fontsize = 10)
plt.yticks(fontsize = 10)
plt.title('Total Confirmed Cases Statewise', fontsize = 18)
for index, value in enumerate(df['Cases']):
    plt.text(value, index, str(value), fontsize = 9)
plt.show()
