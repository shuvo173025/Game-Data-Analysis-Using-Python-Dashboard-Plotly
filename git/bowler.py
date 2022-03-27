from dash import Dash, dcc, html, Input, Output, State, dash_table
from collections import OrderedDict
from app import app
import pandas as pd
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv('datasets/BBL Ball-by-Ball 2011-2019.csv')

#### All bowler name
def get_bowler_name():
    bowler_name_list = df['bowler'].unique()
    return bowler_name_list

### how many match played and for which  tea
def how_many_matches_player_palyed(value):
    match_list = []
    team_list = []
    info_2 = ""
    info_4 = ""
    ndf = df[['id', 'batsman', 'non_striker','batting_team', 'bowler','bowling_team']]
    x = value
    for i, y in enumerate(ndf['bowler']):
        if x == y:
            z = ndf['id'][i]
            a = ndf['bowling_team'][i]
            if z not in match_list:
                match_list.append(z)
                team_list.append(a)

    info = str(str(value) + " played a total of " + str(len(match_list)) + " matches, according to the database.")

    aa = dict(Counter(team_list))
    bb = list(dict(Counter(team_list)).keys())
    cc = list(dict(Counter(team_list)).values())
    info_3 = str(' He played ')
    if len(aa) > 1:
        info_2 = str(" As we said before, this dataset contains data from 2011–19, so in different years, " + str(
            x) + " played for " + str(len(aa)) + " different teams.")
        info_3 = str(str(x) + ' played ')

    for i in range(len(aa)):
        if i < (len(aa)-1):
            info_4 = info_4 + str(str(cc[i])+" matches for the "+str(bb[i]+ ' , '))
        else:
            info_4 = info_4 + str(str(cc[i]) + " matches for the " + str(bb[i] + '.'))

    return len(match_list),info+info_2+info_3+info_4,match_list


#### bowler season total given run , wicket taken, economy
def bowler_season_individual_over_run_economy_wicket(bowler_name):
    ndf = df[['ball', 'total_runs', 'is_wicket', 'bowler', 'extras_type', 'dismissal_kind', 'fielder']]
    ball = total_run = total_wicket = 0
    x = bowler_name
    for i, y in enumerate(ndf['bowler']):
        if x == y:
            #### total ball
            a = ndf['extras_type'][i]
            if a != 'noballs' and a != 'wides':
                ball = ball + 1

            #### total run
            b = ndf['total_runs'][i]
            total_run = total_run + b

            c = ndf['is_wicket'][i]
            d = ndf['dismissal_kind'][i]
            if d == 'run out':
                e = ndf['fielder'][i]
                if e == bowler_name:
                    total_wicket = total_wicket + c
            if d != 'run out':
                total_wicket = total_wicket + c
    temp_over = int(ball / 6)
    temp_over_2 = ((ball % 6) / 10)
    over = round((temp_over + temp_over_2), 1)

    try:
        economy = round((total_run / over), 2)
    except ZeroDivisionError:
        economy = 0.00
    aa = ['Total Overs', 'Total Runs', 'Total Wickets', 'Economy']
    bb = [over, total_run, total_wicket, economy]
    return [aa, bb]


#### season total wicket taken and type of wickets
def season_total_bowler_wicket_and_kind(bowler_name):
    ndf = df[['bowler', 'is_wicket', 'dismissal_kind', 'fielder']]
    x = bowler_name
    total_wicket = 0
    total_caught = total_lbw = total_bowled = total_run_out = total_caught_and_bowled = total_stumped = total_hit_wicket = 0
    for i, y in enumerate(ndf['bowler']):
        if x == y:
            a = ndf['is_wicket'][i]
            if a == 1:
                total_wicket = total_wicket + 1
                b = ndf['dismissal_kind'][i]
                if b == 'caught':
                    total_caught = total_caught + 1
                if b == 'caught and bowled':
                    total_caught_and_bowled = total_caught_and_bowled + 1
                if b == 'lbw':
                    total_lbw = total_lbw + 1
                if b == 'bowled':
                    total_bowled = total_bowled + 1
                if b == 'stumped':
                    total_stumped = total_stumped + 1
                if b == 'hit wicket':
                    total_hit_wicket = total_hit_wicket + 1
                if b == 'run out':
                    c = ndf['fielder'][i]
                    if c == x:
                        total_run_out = total_run_out + 1
    run_out_other = (
            total_wicket - (total_lbw + total_caught + total_bowled + total_run_out + total_caught_and_bowled+total_stumped+total_hit_wicket))
    total_wicket_kind = {'LBW': total_lbw, 'Caught By Other': total_caught, 'Bowled': total_bowled,
                         'Run Out And Balled': total_run_out,
                         'Caught And Balled': total_caught_and_bowled, "Stumped": total_stumped,
                         'Hit Wicket': total_hit_wicket, "Run Out by Other": run_out_other}

    info = str(x) + ' got total ' + str(total_wicket) + ' wicket in this season - '
    total_wicket_kind_key = list(total_wicket_kind.keys())
    total_wicket_kind_value = list(total_wicket_kind.values())

    return info, total_wicket_kind_key, total_wicket_kind_value



#### bowler season total given run and run type
def bowler_total_run_type(bowler_name):
    ndf = df[['bowler','batsman_runs']]
    x = bowler_name
    count_0 = count_1 = count_2 = count_3 = count_4 = count_6 = total_run = 0
    for i,y in enumerate(ndf['bowler']):
        if x == y:
            a = ndf['batsman_runs'][i]
            if a == 0:
                count_0 = count_0 + 1
                total_run = total_run + 0
            if a == 1:
                count_1 = count_1 + 1
                total_run = total_run + 1
            if a == 2:
                count_2 = count_2 + 1
                total_run = total_run + 2
            if a == 3:
                count_3 = count_3 + 1
                total_run = total_run + 3
            if a == 4:
                count_4 = count_4 + 1
                total_run = total_run + 4
            if a == 6:
                count_6 = count_6 + 1
                total_run = total_run + 6
    season_total_run_kind = {'Os':count_0,'1s':count_1,'2s':count_2,'3s':count_3,'4s':count_4,'6s':count_6}

    season_total_run_kind_key = list(season_total_run_kind.keys())
    season_total_run_kind_value = list(season_total_run_kind.values())
    info = str(x)+' given total '+str(total_run)+' runs. No extra run(wides,noballs,etc) are added here.'

    return info, season_total_run_kind_key, season_total_run_kind_value




#### season total only extra run and type
def season_total_bowler_extra_run_and_type(bowler_name):
    ndf = df[['bowler','extra_runs','extras_type']]
    x = bowler_name
    total_extra_run = 0
    total_lagbyes = total_wides = total_byes = total_noballs = 0
    for i,y in enumerate(ndf['bowler']):
        if x == y:
            total_extra_run = total_extra_run + ndf['extra_runs'][i]
            a = ndf['extras_type'][i]
            if a == 'legbyes':
                total_lagbyes = total_lagbyes + 1
            if a == 'wides':
                total_wides = total_wides + 1
            if a == 'byes':
                total_byes = total_byes + 1
            if a == 'noballs':
                total_noballs = total_noballs + 1

    extra_run_type = {'Legbyes':total_lagbyes,'Wides':total_wides,'Byes':total_byes,'No balls':total_noballs}
    extra_run_type_key = list(extra_run_type.keys())
    extra_run_type_value = list(extra_run_type.values())
    info = str(x)+ ' give total '+str(total_extra_run)+ " extra run . run type -"
    return info,extra_run_type_key,extra_run_type_value


#### #### season performance evaluation
def performance_measure(player_name):
    ndf = df[['id', 'batsman', 'batsman_runs', 'batting_team','bowler','total_runs','is_wicket','extras_type']]
    xx = how_many_matches_player_palyed(player_name)[2]
    a = player_name
    match_data = {}
    y_value = []
    x1_values = []
    x2_values = []
    x3_values = []
    for x in xx:
        match_total_run = match_total_wicket = ball = 0
        for i, y in enumerate(ndf['id']):
            if x == y:
                z = ndf['bowler'][i]
                if z == a:
                    zz = ndf['total_runs'][i]
                    match_total_run = match_total_run + zz
                    bb = ndf['extras_type'][i]
                    if bb != 'noballs' and bb != 'wides':
                        ball = ball + 1
                    cc = ndf['is_wicket'][i]
                    if cc == 1:
                        match_total_wicket = match_total_wicket + 1
        temp_over = int(ball / 6)
        temp_over_2 = ((ball % 6) / 10)
        over = round((temp_over + temp_over_2), 1)
        temp_dict = {x: [match_total_run, over,match_total_wicket]}
        match_data.update(temp_dict)
    aa = list(match_data.values())
    y_temp = list(match_data.keys())
    for temp in y_temp:
        y_value.append(str(temp))

    for zz in aa:
        x1_values.append(zz[0])
        x2_values.append(zz[1])
        x3_values.append(zz[2])

    return y_value,x1_values,x2_values,x3_values


#### individual match info graph callback
def individual_match_info_graph_callback():
    data = [{'Name': 'Shakib Al Hasan', 'Wicket and Bowler info': ' c SNJ OKeefe b JR Hazlewood', 'Dot Ball': 8,
             'Fours': 3, 'Sixs': 2, 'Total Run': 46, 'Total Ball': 30, 'Strike Rate': 153.3}]

    column =['Name', 'Wicket and Bowler info', 'Dot Ball', 'Fours', 'Sixs',
           'Total Run', 'Total Ball', 'Strike Rate']
    return data, column




#### single match summary
def bowler_performance_againest_individual_team_match_id(bowler_name,match_id):
    ndf = df[['id','over','ball','bowler','total_runs','is_wicket','batting_team','extras_type','bowling_team']]
    bowler_performance_dict = {}

    z = bowler_name
    x = int(match_id)
    ball = total_run = total_wicket = dot = 0
    for i,y in enumerate(ndf['bowler']):
        if z == y and x == ndf['id'][i]:
            bowling_team = ndf['bowling_team'][i]
            batting_team = ndf['batting_team'][i]

            a = ndf['extras_type'][i]
            if a != 'noballs' and a != 'wides':
                ball = ball + 1
            b = ndf['total_runs'][i]
            total_run = total_run + b
            if b == 0:
                dot = dot + 1

            c = ndf['is_wicket'][i]
            total_wicket = total_wicket + c
        temp_over = int(ball / 6)
        temp_over_2 = ((ball % 6) / 10)
        over = round((temp_over + temp_over_2), 1)

        try:
            economy = round((total_run / over), 2)
        except ZeroDivisionError:
            economy = 0.00

    first_line = str("In this match " + str(z) + ' playes for ' + str(bowling_team) + ' againest ' + str(batting_team))
    second_line = ['Name','Total Run', 'Over', 'Wicket', 'Dot Ball', 'Economy']
    third_line = [z, total_run, over, total_wicket, dot,economy ]

    return first_line,second_line,third_line



#### individual match info graph callback
def individual_match_info_graph_callback():
    data = [{'Name': 'Shakib Al Hasan', 'Total Run': 10, 'Total Over': 1.0,
             'Wicket': 0, 'Dot Ball': 2, 'Economy': 10.0}]

    column =['Name', 'Total Run', 'Total Over', 'Wicket', 'Dot Ball', 'Economy']
    return data, column




#### Evaluating bowler performance accourding innings
def bowler_innings_wise_performance(bowler_name):
    ndf = df[['bowler','inning','is_wicket','total_runs','extras_type']]

    x = bowler_name
    first_innings_total_ball = first_innings_total_run = first_innings_total_wicket = 0
    second_innings_total_ball = second_innings_total_run = second_innings_total_wicket = 0
    for i,y in enumerate(ndf['bowler']):
        if x == y:
            a = ndf['inning'][i]
            #### first innings ar data storing
            if a == 1:
                b = ndf['extras_type'][i]
                if b != 'noballs' and b != 'wides':
                    first_innings_total_ball = first_innings_total_ball + 1
                c = ndf['total_runs'][i]
                first_innings_total_run = first_innings_total_run + c
                d = ndf['is_wicket'][i]
                first_innings_total_wicket = first_innings_total_wicket + d

            #### second innings ar data storing
            if a == 2:
                e = ndf['extras_type'][i]
                if e != 'noballs' and e != 'wides':
                    second_innings_total_ball = second_innings_total_ball + 1
                f = ndf['total_runs'][i]
                second_innings_total_run = second_innings_total_run + f
                g = ndf['is_wicket'][i]
                second_innings_total_wicket = second_innings_total_wicket + g

    temp_over = int(first_innings_total_ball / 6)
    temp_over_2 = ((first_innings_total_ball % 6) / 10)
    first_innings_total_over = round((temp_over + temp_over_2), 1)
    first_innings_economy = round((first_innings_total_run / first_innings_total_over),2)

    temp_over = int(second_innings_total_ball / 6)
    temp_over_2 = ((second_innings_total_ball % 6) / 10)
    second_innings_total_over = round((temp_over + temp_over_2), 1)
    second_innings_economy = round((second_innings_total_run / second_innings_total_over), 2)

    first_innings_performance = {'Total Over':first_innings_total_over,'Total Run':first_innings_total_run,'Total Wicket':first_innings_total_wicket,'Economy Rate':first_innings_economy}
    second_innings_performance = {'Total Over':second_innings_total_over,'Total Run':second_innings_total_run,'Total Wicket':second_innings_total_wicket,'Economy Rate':second_innings_economy}



    first_innings_key = list(first_innings_performance.keys())
    first_innings_value = list(first_innings_performance.values())
    second_innings_value = list(second_innings_performance.values())

    return first_innings_key,first_innings_value,second_innings_value



#### Evaluating bowler performance accourding order
def bowler_bowling_performance_order_wise(bowler_name):
    ndf = df[['over','bowler','total_runs','is_wicket','extras_type']]
    x = bowler_name
    first_order_total_run = first_order_total_wicket = middle_order_total_run = middle_order_total_wicket = last_order_total_run = last_order_total_wicket = 0
    first_order_over = middle_order_over = last_order_over = 0
    for i,y in enumerate(ndf['bowler']):
        if x == y:
            a = ndf['over'][i]
            b = ndf['extras_type'][i]
            if a < 7:
                if b != 'noballs' and b != 'wides':
                    first_order_over = first_order_over + 1

                first_order_total_run = first_order_total_run + ndf['total_runs'][i]
                first_order_total_wicket = first_order_total_wicket + ndf['is_wicket'][i]
            if a >= 7 and a < 17:
                if b != 'noballs' and b != 'wides':
                    middle_order_over = middle_order_over + 1

                middle_order_total_run = middle_order_total_run + ndf['total_runs'][i]
                middle_order_total_wicket = middle_order_total_wicket + ndf['is_wicket'][i]
            if a >= 17:
                if b != 'noballs' and b != 'wides':
                    last_order_over = last_order_over + 1

                last_order_total_run = last_order_total_run + ndf['total_runs'][i]
                last_order_total_wicket = last_order_total_wicket + ndf['is_wicket'][i]

    temp_over = int(first_order_over / 6)
    temp_over_2 = ((first_order_over % 6) / 10)
    first_order_total_over = round((temp_over + temp_over_2), 1)

    temp_over_3 = int(middle_order_over / 6)
    temp_over_4 = ((middle_order_over % 6) / 10)
    middle_order_total_over = round((temp_over_3 + temp_over_4), 1)

    temp_over_5 = int(last_order_over / 6)
    temp_over_6 = ((last_order_over % 6) / 10)
    last_order_total_over = round((temp_over_5 + temp_over_6), 1)



    order_performance_key = ['Total Over', 'Total Run', 'Total Wicket']
    first_order_performance_value = [first_order_total_over, first_order_total_run, first_order_total_wicket]
    middel_order_performance_value = [middle_order_total_over, middle_order_total_run, middle_order_total_wicket]
    last_order_performance_value = [last_order_total_over, last_order_total_run, last_order_total_wicket]

    return order_performance_key, first_order_performance_value, middel_order_performance_value, last_order_performance_value


#### player performance accourding to team callback
def performance_according_different_team_callback():
    data = pd.DataFrame(OrderedDict([
        ('Team Name', ['Brisbane Heat', 'Sydney Sixers', 'Sydney Thunder', 'Melbourne Stars', 'Adelaide Strikers', 'Melbourne Renegades', 'Hobart Hurricanes']),
        ('Total Match', [1, 1, 0, 2, 1, 0, 1]),
        ('Total Run', [13, 21, 0, 33, 28, 0, 33]),
        ('Total Over', [4.0, 4.0, 0.0, 5.0, 4.0, 0.0, 4.0]),
        ('Total Wicket', [5, 2, 0, 1, 0, 0, 2]),
        ('Economy', [3.25, 5.25, 0.0, 6.6, 7.0, 0.0, 8.25] )
    ]))

    column = ['Team Name', 'Total Match', 'Total Run', 'Total Over','Total Wicket','Economy']
    return  data, column


#### player performance accourding to team
def bowler_performance_againest_individual_team(bowler_name):
    ndf = df[['id','over','ball','batsman','batsman_runs','is_wicket','bowling_team','extras_type','bowler','batting_team','total_runs']]
    unique_batting_team_list = ndf['batting_team'].unique()
    batsman_performance_dict = {}

    z = bowler_name

    for x in unique_batting_team_list:
        ball = total_run = total_wicket = dot_ball = 0
        match_count = []
        for i, y in enumerate(ndf['bowler']):
            if z == y and x == ndf['batting_team'][i]:
                d = ndf['id'][i]
                if d not in match_count:
                    match_count.append(d)
                a = ndf['extras_type'][i]
                if a != 'noballs' and a != 'wides':
                    ball = ball + 1

                b = ndf['total_runs'][i]
                total_run = total_run + b
                if b == 0:
                    dot_ball = dot_ball + 1

                c = ndf['is_wicket'][i]
                total_wicket = total_wicket + c
            temp_over = int(ball / 6)
            temp_over_2 = ((ball % 6) / 10)
            over = round((temp_over + temp_over_2), 1)

            try:
                economy = round((total_run / over), 2)
            except ZeroDivisionError:
                economy = 0.00

            temp_dict = [len(match_count), total_run, over, total_wicket,dot_ball, economy]
        temp_dict_2 = {x: temp_dict}
        batsman_performance_dict.update(temp_dict_2)

    team_name = list(batsman_performance_dict.keys())
    #temp_team_name = team_name.pop(len(team_name)-1)

    team_value = list(batsman_performance_dict.values())
    #temp_team_value =team_value.pop(len(team_value)-1)
    match_data = []
    run_data = []
    over_data = []
    wicket_data = []
    dot_ball_data_data = []
    economy_data = []
    for xx in team_value:
        match_data.append(xx[0])
        run_data.append(xx[1])
        over_data.append(xx[2])
        wicket_data.append(xx[3])
        dot_ball_data_data.append(xx[4])
        economy_data.append(xx[5])

    return team_name, match_data, run_data, over_data, wicket_data,dot_ball_data_data, economy_data
