
## IMPORTS
import pandas as pd
from IPython.display import display
import requests
from bs4 import BeautifulSoup
import re


## PREPPING TABLES
# Extract drivers and their constructors from Wikipedia
url = r'https://en.wikipedia.org/wiki/2022_Formula_One_World_Championship'
wiki_table = pd.read_html(url)[0]
wiki_table = wiki_table.drop(columns=['Entrant', 'Chassis', 'Power unit'], axis=1)
wiki_table = wiki_table[0:]
wiki_table.columns = ['Constructor', 'Number', 'Driver']
wiki_table = wiki_table.drop(columns=['Number'], axis=1)
wiki_table.drop(wiki_table.tail(1).index,inplace=True)
wiki_table['Driver'] = wiki_table['Driver'].apply(lambda x : re.findall(r"[\w']+\s[\w']+",x)[0])
wiki_table['Constructor'] = wiki_table['Constructor'].apply(lambda x : re.findall(r"([\w']+\s[\w']+|[\w']+)",x)[0])

# Get pricing table
url = r'https://www.f1fantasytracker.com/prices.html'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
tag = 'table'
attributes = {'id':'driverTable'}
table_soup = soup.find(tag,attributes)
#print(table_soup)
price_table = pd.read_html(str(table_soup))[0]
price_table['Driver'] = price_table['Driver'].apply(lambda x : re.findall(r"[\w']+\s[\w']+",x)[0])

# Combine tables
df = pd.merge(wiki_table, price_table, on ='Driver', how ="left")
#display(df)

## CHOOSING BEST TEAM
# Making team
total_budget = 100
team_size = 6

best_team = []