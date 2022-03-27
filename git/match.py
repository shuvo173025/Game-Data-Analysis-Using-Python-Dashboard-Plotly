from dash import Dash, dcc, html, Input, Output, State, dash_table
from collections import OrderedDict
from app import app
import pandas as pd
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv('datasets/BBL Ball-by-Ball 2011-2019.csv')

#### All bowler name
def get_match_id():
    match_id_list = df['id'].unique()
    return match_id_list


def heading_1(match_id):
    ndf = df[['id', 'inning', 'batting_team', 'bowling_team']]
    a = int(match_id)
    for i, y in enumerate(ndf['id']):
        if y == a:
            b = ndf['inning'][i]
            if b == 1:
                batting_team = ndf['batting_team'][i]
                bowling_team = ndf['bowling_team'][i]
                info = 'Match ID - ' + str(a)
                info_2 = str(batting_team) + ' - VS - ' + str(bowling_team)
                info_3 = 'In This Match ' + str(batting_team) + ' batting first.'
                break

    return info, info_2, info_3





#### building new dataframe for indubidual match and aslo individual innings
def getting_match_details(match_id,value):
    new_dict = {}
    key = 0
    z = value
    x = int(match_id)

    for i, y in enumerate(df['id']):
        inning = df['inning'][i]
        if x == y and z == inning:
            id = df['id'][i]
            inning = df['inning'][i]
            batsman = df['batsman'][i]
            non_striker = df['non_striker'][i]
            bowler = df['bowler'][i]
            batsman_runs = df['batsman_runs'][i]
            extra_runs = df['extra_runs'][i]
            total_runs = df['total_runs'][i]
            is_wicket = df['is_wicket'][i]
            dismissal_kind = df['dismissal_kind'][i]
            player_dismissed = df['player_dismissed'][i]
            fielder = df['fielder'][i]
            extras_type = df['extras_type'][i]
            batting_team = df['batting_team'][i]
            bowling_team = df['bowling_team'][i]
            temp_dict = {'id': id,'inning':inning, 'batsman': batsman, 'non_striker': non_striker,
                         'bowler': bowler, 'batsman_runs': batsman_runs, 'extra_runs': extra_runs,
                         'total_runs': total_runs,
                         'is_wicket': is_wicket, 'dismissal_kind': dismissal_kind, 'player_dismissed': player_dismissed,
                         'fielder': fielder, 'extras_type': extras_type, 'batting_team': batting_team,
                         'bowling_team': bowling_team}
            temp_dict_2 = {key: temp_dict}
            key = key + 1
            new_dict.update(temp_dict_2)

    new_data_set = pd.DataFrame(new_dict).transpose()
    return new_data_set



#### 1st Inning Batting Score Board
def performance_according_different_team_callback():
    data = pd.DataFrame(OrderedDict([
        ('Name', ['DT Christian', 'AW Robinson', 'PJ Forrest', 'CD Hartley', 'ND Buchanan', 'BB McCullum', 'ML Hayden', 'JR Hopes', 'CA Lynn']),
        ('Wicket && Ball', ['c SPD Smithb:MA Starc', 'lbw b:SPD Smith', 'c SPD Smithb:MA Starc', 'Not Out', 'c B Leeb:JR Hazlewood', 'c MA Starcb:SCG MacGill', ' b:SCG MacGill', 'c MJ Lumbb:DJ Bravo', 'c MC Henriquesb:JR Hazlewood']),
        ('Run', [32, 22, 16, 7, 1, 5, 29, 18, 2]),
        ('Ball', [22, 12, 14, 4, 5, 12, 28, 20, 3])
    ]))

    column = ['Name', 'Wicket && Ball', 'Run', 'Ball']
    return  data, column


#### 2nd Inning Batting Score Board
def performance_according_different_team_callback_3():
    data = pd.DataFrame(OrderedDict([
        ('Name', ['BJ Haddin', 'NJ Maddinson', 'SPD Smith', 'MC Henriques', 'MJ Lumb']),
        ('Wicket && Ball',  [' c ML Hayden  b: DT Christian', '   b: AC McDermott', 'Not Out', 'Not Out', ' c BB McCullum  b: JR Hopes']),
        ('Run', [76, 28, 11, 5, 18]),
        ('Ball', [59, 32, 7, 2, 12])
    ]))

    column = ['Name', 'Wicket && Ball', 'Run', 'Ball']
    return  data, column


#### 1st Inning bowling Score Board
def performance_according_different_team_callback_2():
    data = pd.DataFrame(OrderedDict([
        ('Name', ['SPD Smith', 'DJ Bravo', 'SCG MacGill', 'MA Starc', 'B Lee', 'JR Hazlewood']),
        ('Total Over',[2.0, 2.0, 4.0, 4.0, 4.0, 4.0]),
        ('Dot Ball', [2, 3, 14, 14, 15, 10]),
        ('Wicket', [1, 1, 2, 2, 0, 2]),
        ('Total Run', [27, 20, 21, 28, 19, 24]),
        ('Economy', [13.5, 10.0, 5.25, 7.0, 4.75, 6.0])
    ]))

    column = ['Name', 'Total Over', 'Dot Ball', 'Wicket','Total Run','Economy']
    return  data, column


#### 2nd Inning bowling Score Board
def performance_according_different_team_callback_4():
    data = pd.DataFrame(OrderedDict([
        ('Name', ['DT Christian', 'CA Lynn', 'JR Hopes', 'AC McDermott', 'NM Hauritz', 'ND Buchanan']),
        ('Total Over',[4.0, 3.0, 3.4, 3.0, 3.0, 2.0]),
        ('Dot Ball', [12, 6, 6, 7, 7, 3]),
        ('Wicket', [1, 0, 1, 1, 0, 0]),
        ('Total Run', [20, 14, 29, 33, 23, 21]),
        ('Economy', [5.0, 4.67, 8.53, 11.0, 7.67, 10.5])
    ]))

    column = ['Name', 'Total Over', 'Dot Ball', 'Wicket','Total Run','Economy']
    return  data, column



#### batting score total(run,over,wicket)
def innings_batting_summary(ndf,value):
    x = value
    run = ball = wicket = 0
    for i,y in enumerate(ndf['inning']):
        if x == y:
            run = run + ndf['total_runs'][i]
            b = ndf['extras_type'][i]
            if b != 'noballs' and b != 'wides':
                ball = ball + 1
            wicket = wicket + ndf['is_wicket'][i]
    temp_over = int(ball / 6)
    temp_over_2 = ((ball % 6) / 10)
    over = round((temp_over + temp_over_2), 1)
    total = [run,over,wicket]
    return total


#### bowling score total(extra run and type)
def first_inning_bowling_summary(ndf,value):
    x = value
    total_extra = total_noballs = total_byes = total_wides = total_lagbyes = 0
    for i,y in enumerate(ndf['inning']):
        if x == y:
            b = ndf['extras_type'][i]
            if b == 'legbyes':
                total_lagbyes = total_lagbyes + ndf['extra_runs'][i]
            if b == 'wides':
                total_wides = total_wides + ndf['extra_runs'][i]
            if b == 'byes':
                total_byes = total_byes + ndf['extra_runs'][i]
            if b == 'noballs':
                total_noballs = total_noballs + ndf['extra_runs'][i]

    total_extra = total_lagbyes + total_wides + total_byes + total_noballs
    info = 'Total Extra = '+str(total_extra)+'(LB'+str(total_lagbyes)+', W'+str(total_wides)+', B'+str(total_byes)+', NB'+str(total_noballs)+')'
    return info




#### 1st Inning Batting Score Board
def first_innings_batting_details(ndf):
    name_list = []
    wicket_list = []
    run_list = []
    ball_list = []
    unique_batsman_first_innings = ndf['batsman'].unique()
    total_inings_run = total_inings_over = total_inings_wicket = 0
    for x in unique_batsman_first_innings:
        xyz = 'Not Out'
        total_ball = total_run = 0
        for i,y in enumerate(ndf['batsman']):
            run = ndf['total_runs'][i]
            if x == y:
                #### koy ball khelce
                b = ndf['extras_type'][i]
                if b != 'noballs' and b != 'wides':
                    total_ball = total_ball + 1

                #### koy run nice
                c = ndf['batsman_runs'][i]
                total_run = total_run + c

                #### ki out hoice k out korce
                #### k out korce bowler and filder
                d = ndf['player_dismissed'][i]
                if d == x:
                    e = ndf['dismissal_kind'][i]
                    bowler_name = ndf['bowler'][i]
                    if e == 'run out':
                        g = ndf['fielder'][i]
                        xyz = '(run out) '+ str(g)
                    if e == 'caught':
                        g = ndf['fielder'][i]
                        xyz = ' c '+ str(g)
                    if e == 'lbw':
                        xyz = ' lbw '
                    if e == 'bowled':
                        xyz = ' '
                    if e == 'caught and bowled':
                        xyz = 'C & '
                    if e == 'stumped':
                        g = ndf['fielder'][i]
                        xyz = ' st ' + str(g)
                    if e == 'hit wicket':
                        xyz = '(hit wicket) '

        name_list.append(x)
        if xyz == 'Not Out':
            wicket_list.append(xyz)
        if xyz != 'Not Out':
            wicket = str(str(xyz)+'  b: '+str(bowler_name))
            wicket_list.append(wicket)
        run_list.append(total_run)
        ball_list.append(total_ball)
        summary = innings_batting_summary(ndf,1)
    match_summary = [summary[0],summary[2]]
    info = "Total = "+str(summary[0])+' / '+str(summary[2])+'    '+str(summary[1])+'(over)'
    return name_list, wicket_list, run_list, ball_list, match_summary,info





#### 2nd Inning Batting Score Board
def second_innings_batting_details(ndf):
    name_list = []
    wicket_list = []
    run_list = []
    ball_list = []
    unique_batsman_first_innings = ndf['batsman'].unique()
    total_inings_run = total_inings_over = total_inings_wicket = 0
    for x in unique_batsman_first_innings:
        xyz = 'Not Out'
        total_ball = total_run = 0
        for i,y in enumerate(ndf['batsman']):
            run = ndf['total_runs'][i]
            if x == y:
                #### koy ball khelce
                b = ndf['extras_type'][i]
                if b != 'noballs' and b != 'wides':
                    total_ball = total_ball + 1

                #### koy run nice
                c = ndf['batsman_runs'][i]
                total_run = total_run + c

                #### ki out hoice k out korce
                #### k out korce bowler and filder
                d = ndf['player_dismissed'][i]
                if d == x:
                    e = ndf['dismissal_kind'][i]
                    bowler_name = ndf['bowler'][i]
                    if e == 'run out':
                        g = ndf['fielder'][i]
                        xyz = '(run out) '+ str(g)
                    if e == 'caught':
                        g = ndf['fielder'][i]
                        xyz = ' c '+ str(g)
                    if e == 'lbw':
                        xyz = ' lbw '
                    if e == 'bowled':
                        xyz = ' '
                    if e == 'caught and bowled':
                        xyz = 'C & '
                    if e == 'stumped':
                        g = ndf['fielder'][i]
                        xyz = ' st ' + str(g)
                    if e == 'hit wicket':
                        xyz = '(hit wicket) '
        name_list.append(x)
        if xyz == 'Not Out':
            wicket_list.append(xyz)
        if xyz != 'Not Out':
            wicket = str(str(xyz)+'  b: '+str(bowler_name))
            wicket_list.append(wicket)
        run_list.append(total_run)
        ball_list.append(total_ball)
        summary = innings_batting_summary(ndf,2)
    match_summary = [summary[0],summary[2]]
    info = "Total = "+str(summary[0])+' / '+str(summary[2])+'    '+str(summary[1])+'(over)'
    return name_list, wicket_list, run_list, ball_list, match_summary,info









#### 1st Inning bowling Score Board
def first_innings_bowling_details(ndf):
    name_list = []
    wicket_list = []
    run_list = []
    over_list = []
    Dot_ball = []
    economy_list = []
    unique_bowler_first_innings = ndf['bowler'].unique()

    for x in unique_bowler_first_innings:
        ball = dot_ball = run = wicket = 0
        for i,y in enumerate(ndf['bowler']):
            if x == y:
                #### total ball
                b = ndf['extras_type'][i]
                if b != 'noballs' and b != 'wides':
                    ball = ball + 1
                    #### total dot ball
                    c = ndf['total_runs'][i]
                    if c == 0:
                        dot_ball = dot_ball + 1

                #### total run
                run = run + ndf['total_runs'][i]
                d = ndf['is_wicket'][i]
                if d == 1:
                    e = ndf['dismissal_kind'][i]
                    if e == 'run out':
                        f = ndf['fielder'][i]
                        if f == x:
                            wicket = wicket + 1
                    else:
                        wicket = wicket + 1

        temp_over = int(ball / 6)
        temp_over_2 = ((ball % 6) / 10)
        over = round((temp_over + temp_over_2), 1)
        economy = round((run / over), 2)
        name_list.append(x)
        over_list.append(over)
        Dot_ball.append(dot_ball)
        wicket_list.append(wicket)
        run_list.append(run)
        economy_list.append(economy)
    summary = first_inning_bowling_summary(ndf, 1)
    return name_list,over_list,Dot_ball,wicket_list,run_list,economy_list,summary


#### 2nd Inning bowling Score Board
def second_innings_bowling_details(ndf):
    name_list = []
    wicket_list = []
    run_list = []
    over_list = []
    Dot_ball = []
    economy_list = []
    unique_bowler_first_innings = ndf['bowler'].unique()

    for x in unique_bowler_first_innings:
        ball = dot_ball = run = wicket = 0
        for i,y in enumerate(ndf['bowler']):
            if x == y:
                #### total ball
                b = ndf['extras_type'][i]
                if b != 'noballs' and b != 'wides':
                    ball = ball + 1
                    #### total dot ball
                    c = ndf['total_runs'][i]
                    if c == 0:
                        dot_ball = dot_ball + 1

                #### total run
                run = run + ndf['total_runs'][i]
                d = ndf['is_wicket'][i]
                if d == 1:
                    e = ndf['dismissal_kind'][i]
                    if e == 'run out':
                        f = ndf['fielder'][i]
                        if f == x:
                            wicket = wicket + 1
                    else:
                        wicket = wicket + 1

        temp_over = int(ball / 6)
        temp_over_2 = ((ball % 6) / 10)
        over = round((temp_over + temp_over_2), 1)
        economy = round((run / over), 2)
        name_list.append(x)
        over_list.append(over)
        Dot_ball.append(dot_ball)
        wicket_list.append(wicket)
        run_list.append(run)
        economy_list.append(economy)
    summary = first_inning_bowling_summary(ndf, 2)
    return name_list,over_list,Dot_ball,wicket_list,run_list,economy_list,summary
