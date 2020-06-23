"""
    - Web Scraper for escportslivescore.com csgo results:
    - Creates a table based on the last x months of professional results
    - Saves table as 'csgo_data.csv'
        - Row format: [ <home_team : String> <away_team : String> <home_score : Int> <away_score : Int> <days_since : Int> <home_win : Bool(0,1)>]
"""

# Imports
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import datetime as dt
import time

# User Variables
start_date = dt.date(2020, 5, 19)
days_back = 365

"""
Methods for scraping specific elements
"""
def get_home_teams(soup):
    home_team_dump = soup.find_all("div", class_="team-home")
    home_vec = np.empty((0,0))
    for i in range(len(home_team_dump)):
        try:
            home_vec = np.append(home_vec, home_team_dump[i].div.a.img["title"])
        except:
            pass
    return home_vec

def get_away_teams(soup):
    away_team_dump = soup.find_all("div", class_="team-away")
    away_vec = np.empty((0,0))
    for i in range(len(away_team_dump)):
        try:
            away_vec = np.append(away_vec, away_team_dump[i].div.a.img["title"])
        except:
            pass
    return away_vec

def get_home_scores(soup):
    home_score_dump = soup.find_all("span", class_="home-runningscore")
    home_score_vec = np.empty((0,0))
    for i in range(len(home_score_dump)):
        try:
            home_score_vec = np.append(home_score_vec, int(home_score_dump[i].text))
        except:
            pass
    return home_score_vec

def get_away_scores(soup):
    away_score_dump = soup.find_all("span", class_="away-runningscore")
    away_score_vec = np.empty((0,0))
    for i in range(len(away_score_dump)):
        try:
            away_score_vec = np.append(away_score_vec, int(away_score_dump[i].text))
        except:
            pass
    return away_score_vec

def create_days_since(n, cur_date, start_date):
    days_since_vec = np.empty((0,0))
    value = (start_date - cur_date).days
    for _ in range(n):
        days_since_vec = np.append(days_since_vec, value)
    return days_since_vec

def get_home_win(home_score_vec, away_score_vec):
    home_win_vec = np.empty((0,0))
    for i in range(len(home_score_vec)):
        if(home_score_vec[i] >= away_score_vec[i]):
            value = 1
        else:
            value = 0
        home_win_vec = np.append(home_win_vec, value)
    return home_win_vec

def get_away_win(home_score_vec, away_score_vec):
    away_win_vec = np.empty((0,0))
    for i in range(len(home_score_vec)):
        if(home_score_vec[i] <= away_score_vec[i]):
            value = 1
        else:
            value = 0
        away_win_vec = np.append(away_win_vec, value)
    return away_win_vec

"""
Main function: Iterates through dates and and extracts new rows for date
"""
def main():

    df = pd.DataFrame(columns=['home_team', 'away_team', 'home_score', 'away_score', 'days_since', 'home_win'])

    for i in range(days_back):
        print(i)
        time.sleep(0.5)
        
        try:
            cur_date = start_date - dt.timedelta(days=i)
            url = "http://esportlivescore.com/d_{}-{:02d}-{:02d}_g_csgo.html".format(cur_date.year, cur_date.month, cur_date.day)

            page = requests.get(url)
            soup = BeautifulSoup(page.text)
            
            home_teams = get_home_teams(soup)
            away_teams = get_away_teams(soup)
            home_scores = get_home_scores(soup)
            away_scores = get_away_scores(soup)
            days_since = create_days_since(len(home_teams), cur_date, start_date)
            home_win = get_home_win(home_scores, away_scores)
            away_win = get_away_win(home_scores, away_scores)

            try:
                new_rows1 = np.stack((home_teams, away_teams, home_scores, away_scores, days_since, home_win))
                new_rows2 = np.stack((away_teams, home_teams, away_scores, home_scores, days_since, away_win))
                total_rows = np.concatenate((new_rows1, new_rows2), axis=1)
                total_rows = total_rows.T
                
                new_df_rows = pd.DataFrame(total_rows, columns=['home_team', 'away_team', 'home_score', 'away_score', 'days_since', 'home_win'])
                df = df.append(new_df_rows, ignore_index=True)
            except:
                pass
        except:
            pass

    df.to_csv('csgo_data.csv')

    return 0

main()