from dash import Dash, dcc, html, Input, Output, State
from app import app
import pandas as pd
import plotly.graph_objects as go


df = pd.read_csv('datasets/BBL Ball-by-Ball 2011-2019.csv')

##### how many player we have in this Data set
def player_list():
    temp = []
    for x in df['batsman']:
        temp.append(x)
    for y in df['bowler']:
        temp.append(y)
    for z in df['non_striker']:
        temp.append(z)

    global All_player_list
    All_player_list = pd.Series(temp).unique()
    x = str("Here, in this dataset, we have '"+str(len(All_player_list))+"' individual players' information, and of those '"+str(len(All_player_list)))+"'"
    return x



#### how many batsman and bowlar we have in this Dataset
def batsman_and_bowler_unique_list():
    batsman_list = df['batsman'].unique()
    bowler_list = df['bowler'].unique()
    list_of_batsman_and_bowler = [len(batsman_list),len(bowler_list)]
    y = str(" there are '"+str(list_of_batsman_and_bowler[0])+"' players who have their batting information and '"
            +str(list_of_batsman_and_bowler[1])+"' players who have their bowling information.")
    return y




#### how many matches played
#### How many team we have
#### team list
def total_match_team_and_name():
    ndf = df['id'].unique()
    ndf_2 = df['batting_team'].unique()
    a = str("A total of "+str(len(ndf))+" matches were played this season. A total of "+str(len(ndf_2)+1)+" teams were palyed. The team list - ")
    c = str(ndf_2)
    x = a + c
    return x



#### season total run and run types
def season_total_batsman_run_and_types():
    ndf = df['batsman_runs']
    total_zero = total_one = total_tow = total_three = total_four = total_six = 0
    total_run = 0
    for y in ndf:
        total_run = total_run + y
        if y == 0:
            total_zero = total_zero + 1
        if y == 1:
            total_one = total_one + 1
        if y == 2:
            total_tow = total_tow + 1
        if y == 3:
            total_three = total_three + 1
        if y == 4:
            total_four = total_four + 1
        if y == 6:
            total_six = total_six + 1
    season_run_type = ['0s','1s','2s','3s','4s','6s']
    season_run_value = [total_zero,total_one,total_tow,total_three,total_four,total_six]
    total_run_type_and_value = [season_run_type,season_run_value]
    x = "Total "+str(total_run)+ " runs taken in this season: The pie chart of run types - "
    return x,total_run_type_and_value




#### season total extra run and types
def season_total_extra_run_and_type():
    ndf = df[['extra_runs','extras_type']]
    total_extra_run = total_lagbyes = total_wides = total_byes = total_noballs = 0
    for i,y in enumerate(ndf['extras_type']):
        if y == 'legbyes':
            total_lagbyes = total_lagbyes + ndf['extra_runs'][i]
        if y == 'wides':
            total_wides = total_wides + ndf['extra_runs'][i]
        if y == 'byes':
            total_byes = total_byes + ndf['extra_runs'][i]
        if y == 'noballs':
            total_noballs = total_noballs + ndf['extra_runs'][i]
    total_extra_run_and_type_dict = {'Lagbyes':total_lagbyes,'Wides':total_wides,'Byes':total_byes,'Noballs':total_noballs}
    total_extra_run = total_lagbyes + total_wides + total_byes + total_noballs

    a = list(total_extra_run_and_type_dict.keys())
    b = list(total_extra_run_and_type_dict.values())
    x = str('Total '+str(total_extra_run)+' extra runs were given in this season. Pie chart for extra run types --')
    return x,a,b




#### season total wicket and types
def season_total_wicket_and_type():
    ndf = df[['is_wicket','dismissal_kind']]
    total_wicket = 0
    caught = lbw = bowled = run_out = stumped = hit_wicket = 0

    for i,y in enumerate(ndf['is_wicket']):
        if y == 1:
            total_wicket = total_wicket + 1
            a = ndf['dismissal_kind'][i]
            if a == 'caught':
                caught = caught + 1
            if a == "run out":
                run_out = run_out + 1
            if a == "stumped":
                stumped = stumped + 1
            if a == 'bowled':
                bowled = bowled + 1
            if a == 'hit wicket':
                hit_wicket = hit_wicket + 1
            if a == 'lbw':
                lbw = lbw + 1

    wicket_type = ['Caught','Run Out','Stumped','Bowled','Hit Wicket','LBW']
    wicket_value = [caught,run_out,stumped,bowled,hit_wicket,lbw]
    x = str('Total '+str(total_wicket)+' wickets were taken in this season. Pie chart for wickets types --')
    return x,wicket_type,wicket_value
