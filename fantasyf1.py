#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 19 13:03:13 2021

@author: harrietcrisp
"""

#exporting data from website
from scipy.optimize import linprog
from pulp import *
import requests
import pandas as pd
import csv

budget = 100
driver = ["ALO", "BOT", "GAS", "GIO", "HAM", "LAT", "LEC", "MAZ", "MSC", "NOR", "OCO", "PER", "RAI", "RIC", "RUS", "SAI", "STR", "TSU", "VER", "VET"]
team = ['Mercedes', 'Red Bull Racing Honda', 'Ferrari', 'McLaren Mercedes', 'Aston Martin Mercedes', 'Alpine Renault', 'AlphaTauri Honda', 'Alfa Romeo Racing Ferrari', 'Williams Mercedes', 'Haas Ferrari']
drivers = {"ALO":0, "BOT":0, "GAS":0, "GIO":0, "HAM":0, "LAT":0, "LEC":0, "MAZ":0, "MSC":0, "NOR":0, "OCO":0, "PER":0, "RAI":0, "RIC":0, "RUS":0, "SAI":0, "STR":0, "TSU":0, "VER":0, "VET":0}
teams = {'Mercedes':0, 'Red Bull Racing Honda':0, 'Ferrari':0, 'McLaren Mercedes':0, 'Aston Martin Mercedes':0, 'Alpine Renault':0, 'AlphaTauri Honda':0, 'Alfa Romeo Racing Ferrari':0, 'Williams Mercedes':0, 'Haas Ferrari':0}
driver_prices = {"ALO":14.8, "BOT":23, "GAS":11.8, "GIO":8, "HAM":33.1, "LAT":6.4, "LEC":17.8, "MAZ":5.3, "MSC":5.8, "NOR":13.9, "OCO":10.4, "PER":18.6, "RAI":9.3, "RIC":15.9, "RUS":6.2, "SAI":14.6, "STR":13.3, "TSU":8.4, "VER":25.6, "VET":15.1}
team_prices = {'Mercedes':37.3, 'Red Bull Racing Honda':26.4, 'Ferrari':19, 'McLaren Mercedes':18.6, 'Aston Martin Mercedes':16.4, 'Alpine Renault':15.3, 'AlphaTauri Honda':12.6, 'Alfa Romeo Racing Ferrari':9.2, 'Williams Mercedes':6.3, 'Haas Ferrari':6.1}

url1 = 'https://www.formula1.com/en/results.html/2021/races/1070/france/practice-1.html'
url2 = 'https://www.formula1.com/en/results.html/2021/races/1070/france/practice-2.html'
url3 = 'https://www.formula1.com/en/results.html/2021/races/1070/france/practice-3.html'


pd.read_html(requests.get(url1).content)[-1].to_csv('practice1.csv')
pd.read_html(requests.get(url2).content)[-1].to_csv('practice2.csv')
pd.read_html(requests.get(url3).content)[-1].to_csv('practice3.csv')

with open('practice1.csv', newline='') as File:  
    next(File)
    reader = csv.reader(File)
    for row in reader:
        if row[4][-3:] in drivers:
            drivers[row[4][-3:]] += int(row[2])
            teams[row[5]] += int(row[2])
            
with open('practice2.csv', newline='') as File:  
    next(File)
    reader = csv.reader(File)
    for row in reader:
        if row[4][-3:] in drivers:
            drivers[row[4][-3:]] += int(row[2])
            teams[row[5]] += int(row[2])

with open('practice3.csv', newline='') as File:  
    next(File)
    reader = csv.reader(File)
    for row in reader:
        if row[4][-3:] in drivers:
            drivers[row[4][-3:]] += int(row[2])       
            teams[row[5]] += int(row[2])

print(dict(sorted(drivers.items(), key=lambda item: item[1])))
print(dict(sorted(teams.items(), key=lambda item: item[1])))


prob = LpProblem("Fantasy", LpMinimize)

prob += lpSum([drivers[i]+drivers[j]+drivers[k]+drivers[l]+drivers[m]+teams[n] for i in driver for j in driver for k in driver for l in driver for m in driver for n in team])


for i in driver:
    for j in driver:
        j!=i
        for k in driver:
            k!=j
            k!=i
            for l in driver:
                l!=k
                l!=j
                l!=i
                for m in driver:
                    m!=l
                    m!=k
                    m!=j
                    m!=i
                    
                    for n in team:
    
                        prob += lpSum(drivers[i]+drivers[j]+drivers[k]+drivers[l]+drivers[m]+teams[n] for i in driver for j in driver for k in driver for l in driver for m in driver for n in team)<= budget

prob.solve()


opt_team = [driver[i],driver[j],driver[k],driver[l],driver[m],team[n]]
total_score = drivers[driver[i]]+drivers[driver[j]]+drivers[driver[k]]+drivers[driver[l]]+drivers[driver[m]]+teams[team[n]]
total_price = driver_prices[driver[i]]+driver_prices[driver[j]]+driver_prices[driver[k]]+driver_prices[driver[l]]+driver_prices[driver[m]]+team_prices[team[n]]


print('Optimal team is {}, {}, {}, {}, {} and {}. Total score: {}, total price: {}'.format(driver[i],driver[j],driver[k],driver[l],driver[m],team[n],total_score,total_price))

