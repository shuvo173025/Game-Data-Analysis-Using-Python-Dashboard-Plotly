from dash import Dash, dcc, html, Input, Output, State, dash_table
from collections import OrderedDict
from app import app
import pandas as pd
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv('datasets/BBL Ball-by-Ball 2011-2019.csv')

#### All batsmans name
def get_batsman_name():
    batsman_name_list = df['batsman'].unique()
    return batsman_name_list

#### how many match played and for which  team
def how_many_matches_player_palyed(value):
    match_list = []
    team_list = []
    info_2 = ""
    info_4 = ""
    ndf = df[['id', 'batsman', 'non_striker', 'bowler','batting_team']]
    x = value
    for i, y in enumerate(ndf['batsman']):
        if x == y:
            z = ndf['id'][i]
            a = ndf['batting_team'][i]
            if z not in match_list:
                match_list.append(z)
                team_list.append(a)

    for i, y in enumerate(ndf['non_striker']):
        if x == y:
            z = ndf['id'][i]
            a = ndf['batting_team'][i]
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
            info_4 = info_4 + str(str(cc[i])+" matches for "+str(bb[i]+ ' , '))
        else:
            info_4 = info_4 + str(str(cc[i]) + " matches for " + str(bb[i] + '.'))

    return (len(match_list),info+info_2+info_3+info_4,match_list)


#### season total run,ball,average,strike rate
def players_season_indibidual_total_run(player_name):
    ndf = df[['batsman', 'batsman_runs']]
    x = player_name
    total_run = 0
    counter = 0
    for i, y in enumerate(ndf['batsman']):
        if x == y:
            total_run = total_run + ndf['batsman_runs'][i]
            counter = counter + 1

    try:
        strike_rate = (total_run / counter) * 100
    except ZeroDivisionError:
        strike_rate = 0
    strike_rate = round(strike_rate, 1)
    average_counter = total_run / how_many_matches_player_palyed(player_name)[0]
    t = {'Total Run': total_run, 'Total Ball Faced': counter, 'Strike Rate': strike_rate, 'Average': average_counter}

    aa = list(t.keys())
    bb = list(t.values())
    return [aa,bb]



#### season total wicket loss and type of wicket loss
def player_dismissial_total_time_and_type(player_name):
    ndf = df[["dismissal_kind","player_dismissed"]]
    x = player_name
    lbw = caught = run_out = bowled = stumped = hit_wicket = 0
    for i,y in enumerate(ndf['player_dismissed']):
        if x == y:
            if ndf['dismissal_kind'][i] == 'lbw':
                lbw = lbw + 1

            if ndf['dismissal_kind'][i] == 'caught':
                caught = caught + 1

            if ndf['dismissal_kind'][i] == 'run out':
                run_out = run_out + 1

            if ndf['dismissal_kind'][i] == 'bowled':
                bowled = bowled + 1

            if ndf['dismissal_kind'][i] == "stumped":
                stumped = stumped + 1

            if ndf['dismissal_kind'][i] == 'hit wicket':
                hit_wicket = hit_wicket + 1

    total_out_times = lbw + caught + run_out + bowled + stumped
    player_total_dismissal_time_and_kind = {'Caught':caught,'LBW':lbw,'Run Out':run_out,'Bowled':bowled,'Stumped':stumped,'Hit Wicket':hit_wicket}

    aa = list(player_total_dismissal_time_and_kind.keys())
    bb = list(player_total_dismissal_time_and_kind.values())
    return [total_out_times,aa, bb]


#### season total run types
def season_baoundaries_and_singels_count(player_name):
    players_season_total_run_kind = {}
    ndf = df[['batsman', 'batsman_runs', 'bowler']]
    x = player_name
    count_0 = count_1 = count_2 = count_3 = count_4 = count_6 = 0
    for i, y in enumerate(ndf['batsman']):
        if x == y:
            if ndf['batsman_runs'][i] == 0:
                count_0 = count_0 + 1

            if ndf['batsman_runs'][i] == 1:
                count_1 = count_1 + 1

            if ndf['batsman_runs'][i] == 2:
                count_2 = count_2 + 1

            if ndf['batsman_runs'][i] == 3:
                count_3 = count_3 + 1

            if ndf['batsman_runs'][i] == 4:
                count_4 = count_4 + 1

            if ndf['batsman_runs'][i] == 6:
                count_6 = count_6 + 1

    players_season_total_run_kind = {'0s': count_0, '1s': count_1, '2s': count_2, '3s': count_3, '4s': count_4,
                                     '6s': count_6}
    aa = list(players_season_total_run_kind.keys())
    bb = list(players_season_total_run_kind.values())
    return aa, bb



#### season performance evaluation
def performance_measure(player_name):
    ndf = df[['id', 'batsman', 'batsman_runs', 'batting_team']]
    xx = how_many_matches_player_palyed(player_name)[2]
    a = player_name
    match_data = {}
    y_value = []
    x1_values = []
    x2_values = []
    for x in xx:
        match_total_run = match_total_ball = 0
        for i, y in enumerate(ndf['id']):
            if x == y:
                z = ndf['batsman'][i]
                if z == a:
                    zz = ndf['batsman_runs'][i]
                    match_total_run = match_total_run + zz
                    match_total_ball = match_total_ball + 1
        temp_dict = {x: [match_total_run, match_total_ball]}
        match_data.update(temp_dict)
    aa = list(match_data.values())
    y_temp = list(match_data.keys())
    for temp in y_temp:
        y_value.append(str(temp))

    for zz in aa:
        x1_values.append(zz[0])
        x2_values.append(zz[1])

    return [y_value,x1_values,x2_values]

    # fin_max = max(match_data, key=match_data.get)
    # fin_max_value = match_data[fin_max]



#### individual match info
def individual_match_summary(player_name,match_id):
    match_id = int(match_id)
    key = 0
    ndf = df[['id','batsman','bowling_team','batsman_runs','is_wicket','dismissal_kind','fielder','bowler','batting_team']]
    total_run = total_4 = total_6 = total_zero = ball = 0
    for i,x in enumerate(ndf['id']):
        if x == match_id:
            z = ndf['batsman'][i]
            if z == player_name:
                aa = ndf['bowling_team'][i]
                batting_team = ndf['batting_team'][i]
                #total run
                bb = ndf['batsman_runs'][i]
                total_run = total_run + bb
                ball = ball + 1
                if bb == 0:
                    total_zero = total_zero + 1
                if bb == 4:
                    total_4 = total_4 + 1
                if bb == 6:
                    total_6 = total_6 + 1

                #### wicket check
                cc = ndf['is_wicket'][i]
                if cc == 1:
                    key = 1
                    dismissal_kind = ndf['dismissal_kind'][i]
                    bowler = ndf['bowler'][i]
                    if dismissal_kind == 'run out' or dismissal_kind == 'caught' or dismissal_kind == 'stumped':
                        fielder = ndf['fielder'][i]
    try:
        strike_rate = (total_run / ball) * 100
    except ZeroDivisionError:
        strike_rate = 0
    strike_rate = round(strike_rate, 1)
    name = str(player_name)
    if key == 0:
        wicket_bowler_info = ' not out '
    if key == 1:
        if dismissal_kind == 'run out':
            if fielder == bowler:
                wicket_bowler_info = 'run out & b '+str(bowler)
            else:
                wicket_bowler_info = ' run out-'+str(fielder)+' b-'+str(bowler)

        if dismissal_kind == 'caught':
            if fielder == bowler:
                wicket_bowler_info = ' c & b-' + str(bowler)
            else:
                wicket_bowler_info = ' c-' + str(fielder) + ' b-' + str(bowler)

        if dismissal_kind == 'stumped':
            wicket_bowler_info = ' st-'+str(fielder)+' b-'+str(bowler)

        if dismissal_kind == 'bowled':
            wicket_bowler_info = ' b-'+str(bowler)

        if dismissal_kind == 'lbw':
            wicket_bowler_info = ' lbw & b-'+str(bowler)

        if dismissal_kind == 'hit wicket':
            wicket_bowler_info = ' hit wicket & b-'+str(bowler)

    dot_ball = str(total_zero)
    fours = str(total_4)
    sixs = str(total_6)
    match_total_run = str(total_run)
    match_total_ball = str(ball)
    match_strike_rate = str(strike_rate)
    first_line = "In this match \'" + str(player_name) + '\' plays for \'' + str(batting_team) + '\' againest \'' + str(aa)+'\''
    second_line = ['Name','','Dot Ball','Fours','Sixs','Total Run','Ball','Strike Rate']
    third_line = [name,wicket_bowler_info,dot_ball,fours,sixs,match_total_run,match_total_ball,match_strike_rate]

    return first_line, second_line, third_line


#### individual match info graph callback
def individual_match_info_graph_callback():
    data = [{'Name': 'Shakib Al Hasan', 'Wicket and Bowler info': ' c SNJ OKeefe b JR Hazlewood', 'Dot Ball': 8,
             'Fours': 3, 'Sixs': 2, 'Total Run': 46, 'Total Ball': 30, 'Strike Rate': 153.3}]

    column =['Name', 'Wicket and Bowler info', 'Dot Ball', 'Fours', 'Sixs',
           'Total Run', 'Total Ball', 'Strike Rate']
    return data, column




#### player performance accourding to team callback
def performance_according_different_team_callback():
    data = pd.DataFrame(OrderedDict([
        ('Team Name', ['Sydney Sixers', 'Brisbane Heat', 'Melbourne Stars', 'Sydney Thunder', 'Melbourne Renegades', 'Adelaide Strikers', 'Perth Scorchers', 'Hobart Hurricanes']),
        ('Total Match', [1, 1, 2, 0, 0, 1, 0, 1]),
        ('Total Run', [46, 2, 3, 0, 0, 22, 0, 14]),
        ('Ball Faced', [30, 3, 13, 0, 0, 16, 0, 12]),
        ('Strike Rate', [153.3, 66.7, 23.1, 0, 0, 137.5, 0, 116.7]),
        ('Wicket loss', [1, 1, 2, 0, 0, 1, 0, 1] )
    ]))

    # data = pd.DataFrame(
    #     OrderedDict([(name, col_data * 8) for (name, col_data) in data_1.items()])
    # )

    column = ['Team Name', 'Total Match', 'Total Run', 'Ball Faced','Strike Rate','Wicket loss']
    return  data, column


#### Evaluating batsmans performance accourding innings
def batsman_innings_wise_performance(batsman_name):
    ndf = df[['id','batsman','inning','is_wicket','batsman_runs','extras_type']]
    first_innings_match_count = []
    second_innings_match_count = []
    x = batsman_name
    first_innings_total_ball = first_innings_total_run = first_innings_total_out = 0
    second_innings_total_ball = second_innings_total_run = second_innings_total_out = 0
    for i,y in enumerate(ndf['batsman']):
        if x == y:
            a = ndf['inning'][i]
            #### first innings ar data storing
            if a == 1:
                z = ndf['id'][i]
                if z not in first_innings_match_count:
                    first_innings_match_count.append(z)
                b = ndf['extras_type'][i]
                if b != 'noballs' and b != 'wides':
                    first_innings_total_ball = first_innings_total_ball + 1
                c = ndf['batsman_runs'][i]
                first_innings_total_run = first_innings_total_run + c
                d = ndf['is_wicket'][i]
                first_innings_total_out = first_innings_total_out + d

            #### second innings ar data storing
            if a == 2:
                zz = ndf['id'][i]
                if zz not in second_innings_match_count:
                    second_innings_match_count.append(zz)
                e = ndf['extras_type'][i]
                if e != 'noballs' and e != 'wides':
                    second_innings_total_ball = second_innings_total_ball + 1
                f = ndf['batsman_runs'][i]
                second_innings_total_run = second_innings_total_run + f
                g = ndf['is_wicket'][i]
                second_innings_total_out = second_innings_total_out + g

    try:
        first_innings_strike_rate = (first_innings_total_run / first_innings_total_ball) * 100
    except ZeroDivisionError:
        first_innings_strike_rate = 0
    first_innings_strike_rate = round(first_innings_strike_rate, 1)

    try:
        second_innings_strike_rate = (second_innings_total_run / second_innings_total_ball) * 100
    except ZeroDivisionError:
        second_innings_strike_rate = 0
    second_innings_strike_rate = round(second_innings_strike_rate, 1)

    first_innings_performance = {'Total Match':len(first_innings_match_count),'Total Run':first_innings_total_run,'Total Ball':first_innings_total_ball,'Total Out':first_innings_total_out,'Strike Rate':first_innings_strike_rate}
    second_innings_performance = {'Total Match':len(second_innings_match_count),'Total Run':second_innings_total_run,'Total Ball':second_innings_total_ball,'Total Out':second_innings_total_out,'Strike Rate':second_innings_strike_rate}

    first_innings_key = list(first_innings_performance.keys())
    first_innings_value = list(first_innings_performance.values())
    second_innings_value = list(second_innings_performance.values())

    return first_innings_key, first_innings_value, second_innings_value





#### Evaluating batsmans performance accourding to order
#### from 0-6 first order, from 7-15 middle order, rest last order
def performance_evaluation_order_wise(player_name):
    ndf = df[['batsman', 'over', 'batsman_runs']]
    x = player_name
    last_order_strike_rate = middle_order_strike_rate = first_order_strike_rate = last_order_ball_faced = last_order_run = middle_order_ball_faced = middle_order_run = first_order_ball_faced = first_order_run = 0
    for i, y in enumerate(ndf['batsman']):
        if x == y:
            over = (ndf['over'][i])
            run = ndf['batsman_runs'][i]
            if over < 7:
                first_order_run = first_order_run + run
                first_order_ball_faced = first_order_ball_faced + 1
            if over >= 7 and over < 17:
                middle_order_run = middle_order_run + run
                middle_order_ball_faced = middle_order_ball_faced + 1
            if over >= 17:
                last_order_run = last_order_run + run
                last_order_ball_faced = last_order_ball_faced + 1

        try:
            first_order_strike_rate = (first_order_run / first_order_ball_faced) * 100
        except ZeroDivisionError:
            first_order_strike_rate = 0
        first_order_strike_rate = round(first_order_strike_rate, 1)

        try:
            middle_order_strike_rate = (middle_order_run / middle_order_ball_faced) * 100
        except ZeroDivisionError:
            middle_order_strike_rate = 0
        middle_order_strike_rate = round(middle_order_strike_rate, 1)

        try:
            last_order_strike_rate = (last_order_run / last_order_ball_faced) * 100
        except ZeroDivisionError:
            last_order_strike_rate = 0
        last_order_strike_rate = round(last_order_strike_rate, 1)

    order_performance_key = ['Total Run', 'Total Ball', 'Strike Rate']
    first_order_performance_value = [first_order_run, first_order_ball_faced, first_order_strike_rate]
    middel_order_performance_value = [middle_order_run, middle_order_ball_faced, middle_order_strike_rate]
    last_order_performance_value = [last_order_run, last_order_ball_faced, last_order_strike_rate]

    return order_performance_key, first_order_performance_value, middel_order_performance_value, last_order_performance_value




#### player performance accourding to team
def batsman_performance_againest_individual_team(batsman_name):
    ndf = df[['id','over','ball','batsman','batsman_runs','is_wicket','bowling_team','extras_type']]
    unique_bowling_team_list = ndf['bowling_team'].unique()
    batsman_performance_dict = {}

    z = batsman_name

    for x in unique_bowling_team_list:
        ball = total_run = total_wicket = 0
        match_count = []
        for i, y in enumerate(ndf['batsman']):
            if z == y and x == ndf['bowling_team'][i]:
                d = ndf['id'][i]
                if d not in match_count:
                    match_count.append(d)
                a = ndf['extras_type'][i]
                if a != 'noballs' and a != 'wides':
                    ball = ball + 1

                b = ndf['batsman_runs'][i]
                total_run = total_run + b

                c = ndf['is_wicket'][i]
                total_wicket = total_wicket + c
            try:
                strike_rate = (total_run / ball) * 100
            except ZeroDivisionError:
                strike_rate = 0
            strike_rate = round(strike_rate, 1)
            temp_dict = [len(match_count), total_run, ball, total_wicket, strike_rate]
        temp_dict_2 = {x: temp_dict}
        batsman_performance_dict.update(temp_dict_2)

    team_name = list(batsman_performance_dict.keys())
    temp_team_name = team_name.pop(len(team_name)-1)

    team_value = list(batsman_performance_dict.values())
    temp_team_value =team_value.pop(len(team_value)-1)
    match_data = []
    run_data = []
    ball_data = []
    wicket_data = []
    strike_rate_data = []
    for xx in team_value:
        match_data.append(xx[0])
        run_data.append(xx[1])
        ball_data.append(xx[2])
        wicket_data.append(xx[3])
        strike_rate_data.append(xx[4])

    return team_name, match_data, run_data, ball_data, wicket_data, strike_rate_data
