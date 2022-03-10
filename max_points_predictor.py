## IMPORTS
import pandas as pd
from IPython.display import display
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from itertools import chain, combinations
from tqdm import tqdm


def master_table():
    # Get driver and constructor table
    url = r'https://en.wikipedia.org/wiki/2022_Formula_One_World_Championship'
    wiki_table = pd.read_html(url)[0]
    wiki_table = wiki_table.drop(columns=['Entrant', 'Chassis', 'Power unit'], axis=1)
    wiki_table = wiki_table[0:]
    wiki_table.columns = ['Constructor', 'Number', 'Driver']
    wiki_table = wiki_table.drop(columns=['Number'], axis=1)
    wiki_table.drop(wiki_table.tail(1).index,inplace=True)
    try:
        wiki_table['Driver'] = wiki_table['Driver'].apply(lambda x : re.findall(r"[\w']+\s[\w']+",x)[0])
    except:
        pass
    wiki_table['Constructor'] = wiki_table['Constructor'].apply(lambda x : re.findall(r"([\w']+\s[\w']+|[\w']+)",x)[0])
    
    # Get pricing table
    driver = webdriver.Chrome()
    url = r'https://www.f1fantasytracker.com/prices.html'
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tag = 'table'
    attributes = {'id':'driverTable'}
    table_soup = soup.find(tag,attributes)
    price_table = pd.read_html(str(table_soup))[0]
    driver.close()

    price_table['Driver'] = price_table['Driver'].apply(lambda x : re.findall(r"[\w']+\s[\w']+",x)[0])
    price_table.rename(columns={'Season Start PriceSeason Price': 'Start Price'}, inplace=True)
    price_table['Current Price'] = price_table['Current Price'].apply(lambda x: x.replace('$','').replace('m',''))
    price_table['Start Price'] = price_table['Start Price'].apply(lambda x: x.replace('$','').replace('m',''))
    price_table['Driver'] = price_table['Driver'].replace('SAI Carlos','Carlos Sainz Jr.')
    price_table['Driver'] = price_table['Driver'].replace('Sergio Perez','Sergio Pérez')

    # Combine tables
    df = pd.merge(wiki_table, price_table, on ='Driver', how ="left")
    df['Constructor'] = df['Constructor'].replace('AlphaTauri','Alpha Tauri')
    df['Constructor'] = df['Constructor'].replace('McLaren','Mclaren')
    
    return df


def constructor_table():
    driver = webdriver.Chrome()
    url = r'https://www.f1fantasytracker.com/prices.html'
    driver.get(url)
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, 750)") 
    time.sleep(3)
    xpath_constr_tab = r'//li[@class="pill2 statPill"]'
    driver.find_element_by_xpath(xpath_constr_tab).click()
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    tag = 'table'
    attributes = {'id':'constructorTable'}
    table_soup = soup.find(tag,attributes)
    price_table = pd.read_html(str(table_soup))[0]
    driver.quit()

    price_table.rename(columns={'Season Start PriceSeason Price': 'Start Price'}, inplace=True)
    price_table['Current Price'] = price_table['Current Price'].apply(lambda x: x.replace('$','').replace('m',''))
    price_table['Start Price'] = price_table['Start Price'].apply(lambda x: x.replace('$','').replace('m',''))

    return price_table


def feature_engineering(df):
    df['Points'] = df['Points/Million']*df['Current Price']
    return df


def drivers_not_racing():
    return []

def greedy_algorithm(df, budget=100, no_drivers=5, con=1):
    best_team = []
    budget = budget
    not_racing = drivers_not_racing()
    for index, row in df.iterrows():
        if len(best_team) < no_drivers and row['Driver'] not in not_racing and budget >= float(row['Current Price']):
            best_team.append(row['Driver'])
            budget -= float(row['Current Price'])
    return best_team, budget


def dynamic_prog(df, budget=100, no_drivers=5, con=1):
    pass


def powerset(s):
    # returns list of list of every possible combination of 5 drivers
    return [i for i in combinations(s, 5)]


def all_poss_teams(df):
    driver_combos = powerset(df['Driver'].tolist())
    cons = set(df['Constructor'].tolist())
    team_combos = []
    for i in driver_combos:
        for j in cons:
            team_combos.append(list(i + (j,)))
    return team_combos


def brute_force(df, dfc, budget=100, no_drivers=5, con=1):
    best_team = []
    best_points = 0
    best_cost = 0
    combos=all_poss_teams(df)
    realistic_combos = []
    budget = budget
    not_racing = drivers_not_racing()
    # removing over-budget/incomplete teams
    for team in tqdm(combos):
        team_df = df[df.isin(team).any(axis=1)]
        driver_cost = team_df['Current Price'].sum()
        cons_cost = dfc.loc[dfc['Team'] == team[5], 'Current Price'].iloc[0]
        if (driver_cost + cons_cost) <= budget and not (set(team) & set(not_racing)):
            realistic_combos.append(team)
    # finding team with highest points/million
    for team in tqdm(realistic_combos):
        team_df = df[df.isin(team).any(axis=1)]
        driver_points = team_df['Points'].sum()
        cons_points = dfc.loc[dfc['Team'] == team[5], 'Points'].iloc[0]
        points = driver_points + cons_points
        if points > best_points:
            best_team = team
            best_points = points
            best_cost = team_df['Current Price'].sum() + dfc.loc[dfc['Team'] == team[5], 'Current Price'].iloc[0]
    return best_team, best_points, best_cost


# # df = master_table()
# # df.to_csv('driver_table.csv')
df = pd.read_csv('driver_table.csv')
dfc = pd.read_csv('constructor_table.csv')

df = feature_engineering(df)
dfc = feature_engineering(dfc)

a, b, c = brute_force(df, dfc)
print('best team is: ', a)
print('best points is: ', b)
print('cost is: ', c)