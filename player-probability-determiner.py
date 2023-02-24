# player-probability-determiner.py
# determine the probability that a player will perform an action

import reader # input data
import numpy # mean, median
import scipy
from scipy import stats # calculate mode
from tabulate import tabulate # display output
import isolator # isolate player game data which exludes headers and monthly averages
import re # split result data into score data
import determiner # determine consistent streak

from datetime import datetime # convert date str to date so we can see if games 1 day apart and how many games apart
from datetime import timedelta

import pandas as pd # see when was prev game

# main settings
read_all_seasons = False
find_matchups = True

# input: game log
# player name
# date, opponent, result, min, fg, fg%, 3pt, 3p%, ft, ft%, reb, ast, blk, stl, pf, to, pts

data_type = 'Player Data'
player_name = 'Ja Morant'
# count no. times player hit over line
pts_line = 1
r_line = 3
a_line = 1

#print("\n===" + player_name + "===\n")
#row1 = ['Tue 2/7','vs OKC','L 133-130', '34','13-20','65.0','4-6','66.7','8-10','80.0','7','3','0','3','3','4','38']

#all_player_game_logs = []
#all_player_game_logs_dict = {}
#all_player_season_logs_dict = {}


player_names = ['Julius Randle', 'Jalen Brunson', 'RJ Barrett', 'Demar Derozan', 'Paolo Banchero', 'Zach Lavine', 'Franz Wagner', 'Nikola Vucevic', 'Wendell Carter Jr', 'Ayo Dosunmu', 'Markelle Fultz', 'Patrick Williams', 'Brandon Ingram', 'Shai Gilgeous Alexander', 'CJ Mccollum', 'Josh Giddey', 'Trey Murphy III', 'Jalen Williams', 'Herbert Jones', 'Anthony Edwards', 'Luka Doncic', 'Rudy Gobert', 'Kyrie Irving', 'Mike Conley', 'Jaden Mcdaniels', 'Jordan Poole', 'Klay Thompson', 'Draymond Green', 'Kevon Looney','Gary Harris'] #['Bojan Bogdanovic', 'Jaden Ivey', 'Killian Hayes', 'Pascal Siakam', 'Fred Vanvleet', 'Gary Trent Jr', 'Scottie Barnes', 'Isaiah Stewart', 'Jalen Duren', 'Chris Boucher'] #['Ja Morant', 'Desmond Bane', 'Jaren Jackson Jr', 'Dillon Brooks', 'Jayson Tatum', 'Derrick White', 'Robert Williams', 'Malcolm Brogdon', 'Al Horford', 'Xavier Tillman', 'Brandon Clarke']
pts_lines = [25,25,19,23,19,24,16,19,15,9,14,11,31,18,13,28,33,14,25,11,11,26,26,9,7,10] #[22, 16, 13, 25, 22, 20, 17, 12, 11, 10] #[28, 21, 16, 13, 33, 18, 10, 15, 9, 8, 10]
r_lines = [10,4,5,5,7,5,2,12,8,2,4,5,2,5,2,8,2,2,2,6,9,11,4,3,4,2,2,8,9,2] #[4, 4, 3, 7, 4, 3, 7, 9, 10, 6] #[7, 5, 7, 3, 9, 5, 10, 5, 6, 7, 6]
a_lines = [2,6,2,5,2,4,2,2,3,2,6,2,2,6,2,6,2,3,2,2,7,2,6,6,2,5,3,7,2,2] #[3, 6, 7, 6, 7, 2, 5, 2, 2, 2] #[8, 4, 2, 2, 6, 6, 2, 4, 3, 2, 2]
threes_lines = [3,1,1,1,1,3,2,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,1,1,1,5,1,1,2]
b_lines = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
s_lines = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
to_lines = [3,1,1,1,3,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1]

data_type = "Game Lines"
todays_games_date = '2/23/23'
todays_games_date_obj = datetime.strptime(todays_games_date, '%m/%d/%y')
input_type = '2_23' # date as mth_day
projected_lines = reader.extract_data(data_type, input_type, header=True)
if input_type == '': # for testing we make input type blank ''
#projected_lines = reader.read_projected_lines(date)
    projected_lines = [['Name', 'PTS', 'REB', 'AST', '3PT', 'BLK', 'STL', 'TO','LOC','OPP'], ['Giannis Antetokounmpo', '34', '13', '6', '1', '1', '1', '1', 'Home', 'ATL']]
print("projected_lines: " + str(projected_lines))

projected_lines_dict = {}
player_lines_dict = {}
header_row = projected_lines[0]
for player_lines in projected_lines[1:]:
    player_name = player_lines[0]
    projected_lines_dict[player_name] = dict(zip(header_row[1:],player_lines[1:]))
print("projected_lines_dict: " + str(projected_lines_dict))

player_names = isolator.isolate_data_field("name",projected_lines)
pts_lines = isolator.isolate_data_field("pts",projected_lines)
r_lines = isolator.isolate_data_field("reb",projected_lines)
a_lines = isolator.isolate_data_field("ast",projected_lines)
threes_lines = isolator.isolate_data_field("3",projected_lines)
#print("threes_lines: " + str(threes_lines))
b_lines = isolator.isolate_data_field("blk",projected_lines)
#print("b_lines: " + str(b_lines))
s_lines = isolator.isolate_data_field("stl",projected_lines)
to_lines = isolator.isolate_data_field("to",projected_lines)
locations = isolator.isolate_data_field("loc",projected_lines) # home/away
opponents = isolator.isolate_data_field("opp",projected_lines) # format OKC



# get all player season logs
all_player_season_logs_dict = reader.read_all_players_season_logs(player_names)


# for p_name in player_names:

#     # player_season_logs = reader.read_player_season_logs(p_name) # list of game logs for each season played by p_name
#     # all_player_season_logs_dict[p_name] = player_season_logs


#     player_game_log = reader.read_player_season_log(p_name) # construct player url from name

#     all_player_game_logs.append(player_game_log) # could continue to process in this loop or save all player game logs to process in next loop

#     #all_player_game_logs_dict[p_name] = player_game_log


print("\n===All Players===\n")

#player_game_log = all_player_game_logs[0] # init
# player game log from espn, for 1 season or all seasons

all_streak_tables = { } # { 'player name': { 'all': {year:[streaks],...}, 'home':{year:streak}, 'away':{year:streak} } }


for player_name, player_season_logs in all_player_season_logs_dict.items():
#for player_idx in range(len(all_player_game_logs)):

    season_year = 2023

    # get no. games played this season
    num_games_played = 0 # see performance at this point in previous seasons
    current_season_log = player_season_logs[0]
    for game_idx, row in current_season_log.iterrows():
                
        if re.search('\\*',current_season_log.loc[game_idx, 'OPP']): # all star stats not included in regular season stats
            #print("game excluded")
            continue
        
        if current_season_log.loc[game_idx, 'Type'] == 'Regular':
            num_games_played += 1


    all_seasons_pts_dicts = {}
    all_seasons_rebs_dicts = {}
    all_seasons_asts_dicts = {}
    all_seasons_winning_scores_dicts = {}
    all_seasons_losing_scores_dicts = {}
    all_seasons_minutes_dicts = {}
    all_seasons_fgms_dicts = {}
    all_seasons_fgas_dicts = {}
    all_seasons_fg_rates_dicts = {}
    all_seasons_threes_made_dicts = {}
    all_seasons_threes_attempts_dicts = {}
    all_seasons_threes_rates_dicts = {}
    all_seasons_ftms_dicts = {}
    all_seasons_ftas_dicts = {}
    all_seasons_ft_rates_dicts = {}
    all_seasons_bs_dicts = {}
    all_seasons_ss_dicts = {}
    all_seasons_fs_dicts = {}
    all_seasons_tos_dicts = {}

    all_seasons_stats_dicts = {'pts':all_seasons_pts_dicts, 'reb':all_seasons_rebs_dicts, 'ast':all_seasons_asts_dicts, 'w score':all_seasons_winning_scores_dicts, 'l score':all_seasons_losing_scores_dicts, 'min':all_seasons_minutes_dicts, 'fgm':all_seasons_fgms_dicts, 'fga':all_seasons_fgas_dicts, 'fg%':all_seasons_fg_rates_dicts, '3pm':all_seasons_threes_made_dicts, '3pa':all_seasons_threes_attempts_dicts, '3p%':all_seasons_threes_rates_dicts, 'ftm':all_seasons_ftms_dicts, 'fta':all_seasons_ftas_dicts, 'ft%':all_seasons_ft_rates_dicts, 'blk':all_seasons_bs_dicts, 'stl':all_seasons_ss_dicts, 'pf':all_seasons_fs_dicts, 'to':all_seasons_tos_dicts} # loop through to add all new stats with 1 fcn

    for player_game_log in player_season_logs:

        print("\n===Year " + str(season_year) + "===\n")
        #player_game_log = player_season_logs[0] #start with current season. all_player_game_logs[player_idx]
        #player_name = player_names[player_idx] # player names must be aligned with player game logs

        # all_pts_dicts = {'all':{idx:val,..},..}
        all_pts_dicts = { 'all':{}, 'home':{}, 'away':{} }
        all_rebs_dicts = { 'all':{}, 'home':{}, 'away':{} }
        all_asts_dicts = { 'all':{}, 'home':{}, 'away':{} }
        all_winning_scores_dicts = { 'all':{}, 'home':{}, 'away':{} }
        all_losing_scores_dicts = { 'all':{}, 'home':{}, 'away':{} }
        all_minutes_dicts = { 'all':{}, 'home':{}, 'away':{} }
        all_fgms_dicts = { 'all':{}, 'home':{}, 'away':{} }
        all_fgas_dicts = { 'all':{}, 'home':{}, 'away':{} }
        all_fg_rates_dicts = { 'all':{}, 'home':{}, 'away':{} }
        all_threes_made_dicts = { 'all':{}, 'home':{}, 'away':{} }
        all_threes_attempts_dicts = { 'all':{}, 'home':{}, 'away':{} }
        all_threes_rates_dicts = { 'all':{}, 'home':{}, 'away':{} }
        all_ftms_dicts = { 'all':{}, 'home':{}, 'away':{} }
        all_ftas_dicts = { 'all':{}, 'home':{}, 'away':{} }
        all_ft_rates_dicts = { 'all':{}, 'home':{}, 'away':{} }
        all_bs_dicts = { 'all':{}, 'home':{}, 'away':{} }
        all_ss_dicts = { 'all':{}, 'home':{}, 'away':{} }
        all_fs_dicts = { 'all':{}, 'home':{}, 'away':{} }
        all_tos_dicts = { 'all':{}, 'home':{}, 'away':{} }

        all_stats_dicts = {'pts':all_pts_dicts, 'reb':all_rebs_dicts, 'ast':all_asts_dicts, 'w score':all_winning_scores_dicts, 'l score':all_losing_scores_dicts, 'min':all_minutes_dicts, 'fgm':all_fgms_dicts, 'fga':all_fgas_dicts, 'fg%':all_fg_rates_dicts, '3pm':all_threes_made_dicts, '3pa':all_threes_attempts_dicts, '3p%':all_threes_rates_dicts, 'ftm':all_ftms_dicts, 'fta':all_ftas_dicts, 'ft%':all_ft_rates_dicts, 'blk':all_bs_dicts, 'stl':all_ss_dicts, 'pf':all_fs_dicts, 'to':all_tos_dicts} # loop through to add all new stats with 1 fcn


        # if getting data from player game logs read from internet
        # for game log for particular given season/year
        # for season in all seasons
        if len(player_game_log) > 0:
            #season_year = '23'
            print("player_game_log:\n" + str(player_game_log))
            # we pulled game log from internet

            opponent = projected_lines_dict[player_name]['OPP'].lower() # collect data against opponent to see previous matchups
            
            # first loop thru all regular season games, then thru subset of games such as home/away
            # or just append to subset array predefined such as all_home_pts = []
            next_game_date_obj = datetime.today() # need to see if back to back games 1 day apart

            reg_season_games = determiner.determine_regular_season_games(player_game_log)

            total_season_games = 0 # so we can get game num from game idx
            for game_idx, row in player_game_log.iterrows():
                
                #game = player_game_log[game_idx, row]
                #print("game:\n" + str(game))
                #print("player_game_log.loc[game_idx, 'Type']: " + player_game_log.loc[game_idx, 'Type'])

                if re.search('\\*',player_game_log.loc[game_idx, 'OPP']): # all star stats not included in regular season stats
                    #print("game excluded")
                    continue
                
                if player_game_log.loc[game_idx, 'Type'] == 'Regular':
                    #print("Current Game Num: " + str(game_idx))
                    total_season_games += 1
            
            for game_idx, row in player_game_log.iterrows():
                
                #game = player_game_log[game_idx, row]
                #print("game:\n" + str(game))
                #print("player_game_log.loc[game_idx, 'Type']: " + player_game_log.loc[game_idx, 'Type'])

                if re.search('\\*',player_game_log.loc[game_idx, 'OPP']): # all star stats not included in regular season stats
                    #print("game excluded")
                    continue
                
                if player_game_log.loc[game_idx, 'Type'] == 'Regular':
                    #print("Current Game Num: " + str(game_idx))

                    
                    

                    pts = int(player_game_log.loc[game_idx, 'PTS'])
                    rebs = int(player_game_log.loc[game_idx, 'REB'])
                    asts = int(player_game_log.loc[game_idx, 'AST'])

                    results = player_game_log.loc[game_idx, 'Result']
                    #print("results: " + results)
                    results = re.sub('[a-zA-Z]', '', results)
                    # remove #OT from result string
                    results = re.split("\\s+", results)[0]
                    #print("results_data: " + str(results_data))
                    score_data = results.split('-')
                    #print("score_data: " + str(score_data))
                    winning_score = int(score_data[0])
                    losing_score = int(score_data[1])

                    minutes = int(player_game_log.loc[game_idx, 'MIN'])

                    fgs = player_game_log.loc[game_idx, 'FG']
                    fg_data = fgs.split('-')
                    fgm = int(fg_data[0])
                    fga = int(fg_data[1])
                    fg_rate = round(float(player_game_log.loc[game_idx, 'FG%']), 1)

                    #threes = game[three_idx]
                    #threes_data = threes.split('-')
                    #print("threes_data: " + str(threes_data))
                    threes_made = int(player_game_log.loc[game_idx, '3PT_SA'])
                    threes_attempts = int(player_game_log.loc[game_idx, '3PT_A'])
                    three_rate = round(float(player_game_log.loc[game_idx, '3P%']), 1)

                    fts = player_game_log.loc[game_idx, 'FT']
                    ft_data = fts.split('-')
                    ftm = int(ft_data[0])
                    fta = int(ft_data[1])
                    ft_rate = round(float(player_game_log.loc[game_idx, 'FT%']), 1)

                    bs = int(player_game_log.loc[game_idx, 'BLK'])
                    ss = int(player_game_log.loc[game_idx, 'STL'])
                    fs = int(player_game_log.loc[game_idx, 'PF'])
                    tos = int(player_game_log.loc[game_idx, 'TO'])

                    game_stats = [pts,rebs,asts,winning_score,losing_score,minutes,fgm,fga,fg_rate,threes_made,threes_attempts,three_rate,ftm,fta,ft_rate,bs,ss,fs,tos] # make list to loop through so we can add all stats to dicts with 1 fcn

                    # now that we have game stats add them to dict

                    for stat_idx in range(len(all_stats_dicts.values())):
                        stat_dict = list(all_stats_dicts.values())[stat_idx]
                        stat = game_stats[stat_idx]
                        stat_dict['all'][game_idx] = stat

                    if re.search('vs',player_game_log.loc[game_idx, 'OPP']):

                        for stat_idx in range(len(all_stats_dicts.values())):
                            stat_dict = list(all_stats_dicts.values())[stat_idx]
                            stat = game_stats[stat_idx]
                            stat_dict['home'][game_idx] = stat

                        
                    else: # if not home then away
                        for stat_idx in range(len(all_stats_dicts.values())):
                            stat_dict = list(all_stats_dicts.values())[stat_idx]
                            stat = game_stats[stat_idx]
                            stat_dict['away'][game_idx] = stat

                        

                    # matchup against opponent
                    if re.search(opponent,player_game_log.loc[game_idx, 'OPP'].lower()):

                        for stat_idx in range(len(all_stats_dicts.values())):
                            stat_dict = list(all_stats_dicts.values())[stat_idx]
                            stat = game_stats[stat_idx]
                            if not opponent in stat_dict.keys():
                                stat_dict[opponent] = {}
                            stat_dict[opponent][game_idx] = stat

                        


                    # see if this game is 1st or 2nd night of back to back bc we want to see if pattern for those conditions
                    init_game_date_string = player_game_log.loc[game_idx, 'Date'].lower().split()[1] # 'wed 2/15'[1]='2/15'
                    game_mth = init_game_date_string.split('/')[0]
                    final_season_year = str(season_year)
                    if int(game_mth) in range(10,13):
                        final_season_year = str(season_year - 1)
                    game_date_string = init_game_date_string + "/" + final_season_year
                    #print("game_date_string: " + str(game_date_string))
                    game_date_obj = datetime.strptime(game_date_string, '%m/%d/%Y')
                    #print("game_date_obj: " + str(game_date_obj))

                    # if current loop is most recent game (idx 0) then today's game is the next game
                    if game_idx == 0: # see how many days after prev game is date of today's projected lines
                        # already defined or passed todays_games_date_obj
                        # todays_games_date_obj = datetime.strptime(todays_games_date, '%m/%d/%y')
                        # print("todays_games_date_obj: " + str(todays_games_date_obj))
                        if season_year == 2023:
                            next_game_date_obj = todays_games_date_obj # today's game is the next game relative to the previous game
                        else:
                            next_game_date_obj = game_date_obj # should be 0 unless we want to get date of next season game
                    #print("next_game_date_obj: " + str(next_game_date_obj))
                    # no need to get next game date like this bc we can see last loop
                    # else: # if not most recent game then we can see the following game in the game log at prev idx
                    #     next_game_date_string = player_game_log.loc[game_idx-1, 'Date'].lower().split()[1] + "/" + season_year
                    #     print("next_game_date_string: " + str(next_game_date_string))
                    #     next_game_date_obj = datetime.strptime(next_game_date_string, '%m/%d/%y')
                    #     print("next_game_date_obj: " + str(next_game_date_obj))

                    days_before_next_game_int = (next_game_date_obj - game_date_obj).days
                    days_before_next_game = str(days_before_next_game_int) + ' before'
                    #print("days_before_next_game: " + days_before_next_game)

                    for stat_idx in range(len(all_stats_dicts.values())):
                        stat_dict = list(all_stats_dicts.values())[stat_idx]
                        stat = game_stats[stat_idx]
                        if not days_before_next_game in stat_dict.keys():
                            stat_dict[days_before_next_game] = {}
                        stat_dict[days_before_next_game][game_idx] = stat

                    init_prev_game_date_string = ''
                    if len(player_game_log.index) > game_idx+1:
                        init_prev_game_date_string = player_game_log.loc[game_idx+1, 'Date'].lower().split()[1]
                    
                        prev_game_mth = init_prev_game_date_string.split('/')[0]
                        final_season_year = str(season_year)
                        if int(prev_game_mth) in range(10,13):
                            final_season_year = str(season_year - 1)
                        prev_game_date_string = init_prev_game_date_string + "/" + final_season_year
                        #print("prev_game_date_string: " + str(prev_game_date_string))
                        prev_game_date_obj = datetime.strptime(prev_game_date_string, '%m/%d/%Y')
                        #print("prev_game_date_obj: " + str(prev_game_date_obj))

                        days_after_prev_game_int = (game_date_obj - prev_game_date_obj).days
                        days_after_prev_game = str(days_after_prev_game_int) + ' after'
                        #print("days_after_prev_game: " + days_after_prev_game)

                        for stat_idx in range(len(all_stats_dicts.values())):
                            stat_dict = list(all_stats_dicts.values())[stat_idx]
                            stat = game_stats[stat_idx]
                            if not days_after_prev_game in stat_dict.keys():
                                stat_dict[days_after_prev_game] = {}
                            stat_dict[days_after_prev_game][game_idx] = stat

                    

                    next_game_date_obj = game_date_obj # next game bc we loop from most to least recent


                    # if we find a game played on the same day/mth previous seasons, add a key for this/today's day/mth
                    today_date_data = todays_games_date.split('/')
                    today_day_mth = today_date_data[0] + '/' + today_date_data[1]
                    if init_game_date_string == today_day_mth:
                        print("found same game day/mth in previous season")
                        for stat_idx in range(len(all_seasons_stats_dicts.values())):
                            stat_dict = list(all_seasons_stats_dicts.values())[stat_idx]
                            stat = game_stats[stat_idx]
                            if not game_date_string in stat_dict.keys():
                                stat_dict[game_date_string] = {}
                                stat_dict[game_date_string][game_idx] = [stat] # we cant use game idx as key bc it gets replaced instead of adding vals
                            else:
                                stat_dict[game_date_string][game_idx].append(stat)
                        print("all_seasons_stats_dicts: " + str(all_seasons_stats_dicts))
                    # add key for the current game number for this season and add games played from previous seasons (1 per season)
                    game_num = total_season_games - game_idx # bc going from recent to past
                    if game_num == num_games_played:
                        print("found same game num in previous season")
                        for stat_idx in range(len(all_seasons_stats_dicts.values())):
                            stat_dict = list(all_seasons_stats_dicts.values())[stat_idx]
                            stat = game_stats[stat_idx]
                            if not num_games_played in stat_dict.keys():
                                stat_dict[num_games_played] = {}
                                stat_dict[num_games_played][game_idx] = [stat] # we cant use game idx as key bc it gets replaced instead of adding vals
                            else:
                                if game_idx in stat_dict[num_games_played].keys():
                                    stat_dict[num_games_played][game_idx].append(stat)
                                else:
                                    stat_dict[num_games_played][game_idx] = [stat]
                        print("all_seasons_stats_dicts: " + str(all_seasons_stats_dicts))
                        

        else:
            # if getting data from file
            player_season_log = reader.read_season_log_from_file(data_type, player_name, 'tsv')


        # no matter how we read data, we should have filled all_pts list
        if len(all_pts_dicts['all'].keys()) > 0:
            # no matter how we get data, 
            # next we compute relevant results

            # first for all then for subsets like home/away
            # all_pts_dict = { 'all':[] }
            # all_pts_means_dict = { 'all':0, 'home':0, 'away':0 }
            # all_pts_medians_dict = { 'all':0, 'home':0, 'away':0 }
            # all_pts_modes_dict = { 'all':0, 'home':0, 'away':0 }
            # all_pts_min_dict = { 'all':0, 'home':0, 'away':0 }
            # all_pts_max_dict = { 'all':0, 'home':0, 'away':0 }

            all_stats_counts_dict = { 'all': [], 'home': [], 'away': [] }

            # at this point we have added all keys to dict eg all_pts_dict = {'1of2':[],'2of2':[]}
            #print("all_pts_dict: " + str(all_pts_dict))
            print("all_pts_dicts: " + str(all_pts_dicts))
            # all_pts_dicts = {'all':{1:20}}
            # key=condition, val={idx:stat}

            
            #compute stats from data
            # key represents set of conditions of interest eg home/away
            for conditions in all_pts_dicts.keys(): # all stats dicts have same keys so we use first 1 as reference

                # reset for each set of conditions
                header_row = ['Output']
                stat_means = ['Mean'] #{pts:'',reb...}
                stat_medians = ['Median']
                stat_modes = ['Mode']
                stat_mins = ['Min']
                stat_maxes = ['Max']

                for stat_key, stat_dict in all_stats_dicts.items(): # stat key eg pts

                    header_row.append(stat_key.upper())

                    stat_vals = list(stat_dict[conditions].values())
                    #print("stat_vals: " + str(stat_vals))

                    stat_mean = round(numpy.mean(stat_vals), 1)
                    stat_median = int(numpy.median(stat_vals))
                    stat_mode = stats.mode(stat_vals, keepdims=False)[0]
                    stat_min = numpy.min(stat_vals)
                    stat_max = numpy.max(stat_vals)

                    stat_means.append(stat_mean)
                    stat_medians.append(stat_median)
                    stat_modes.append(stat_mode)
                    stat_mins.append(stat_min)
                    stat_maxes.append(stat_max)

                output_table = [header_row, stat_means, stat_medians, stat_modes, stat_mins, stat_maxes]

                output_title = str(conditions).title() + ", " + str(season_year)
                if re.search('before',conditions):
                    output_title = re.sub('Before','days before next game', output_title).title()
                elif re.search('after',conditions):
                    output_title = re.sub('After','days after previous game', output_title).title()
                
                print("\n===" + player_name + " Average and Range===\n")
                print(output_title)
                print(tabulate(output_table))



                # for same set of conditions, count streaks for stats
                min_line_hits = 7
                game_sample = 10
                current_line_hits = 10 # player reached 0+ stats in all 10/10 games. current hits is for current level of points line

                pts_count = 0
                r_count = 0
                a_count = 0

                threes_count = 0
                b_count = 0
                s_count = 0
                to_count = 0

                all_pts_counts = []
                all_rebs_counts = []
                all_asts_counts = []

                all_threes_counts = []
                all_blks_counts = []
                all_stls_counts = []
                all_tos_counts = []

                # prob = 1.0
                # while(prob > 0.7):
                #if set_sample_size = True: # if we set a sample size only consider those settings. else take all games
                #while(current_line_hits > min_line_hits) # min line hits is considered good odds. increase current line hits count out of 10
                    # if count after 10 games is greater than min line hits then check next level up
                for game_idx in range(len(all_pts_dicts[conditions].values())):
                    pts = list(all_pts_dicts[conditions].values())[game_idx]
                    rebs = list(all_rebs_dicts[conditions].values())[game_idx]
                    asts = list(all_asts_dicts[conditions].values())[game_idx]

                    threes = list(all_threes_made_dicts[conditions].values())[game_idx]
                    blks = list(all_bs_dicts[conditions].values())[game_idx]
                    stls = list(all_ss_dicts[conditions].values())[game_idx]
                    tos = list(all_tos_dicts[conditions].values())[game_idx]

                    player_projected_lines = projected_lines_dict[player_name]
                    if pts >= int(player_projected_lines['PTS']):
                        pts_count += 1
                    if rebs >= int(player_projected_lines['REB']):
                        r_count += 1
                    if asts >= int(player_projected_lines['AST']):
                        a_count += 1

                    if threes >= int(player_projected_lines['3PT']):
                        threes_count += 1
                    if blks >= int(player_projected_lines['BLK']):
                        b_count += 1
                    if stls >= int(player_projected_lines['STL']):
                        s_count += 1
                    if tos >= int(player_projected_lines['TO']):
                        to_count += 1

                    all_pts_counts.append(pts_count)
                    all_rebs_counts.append(r_count)
                    all_asts_counts.append(a_count)

                    all_threes_counts.append(threes_count)
                    all_blks_counts.append(b_count)
                    all_stls_counts.append(s_count)
                    all_tos_counts.append(to_count)

                # make stats counts to find consistent streaks
                all_stats_counts_dict[conditions] = [ all_pts_counts, all_rebs_counts, all_asts_counts, all_threes_counts, all_blks_counts, all_stls_counts, all_tos_counts ]

                stats_counts = [ all_pts_counts, all_rebs_counts, all_asts_counts, all_threes_counts, all_blks_counts, all_stls_counts, all_tos_counts ]

                header_row = ['Games']
                over_pts_line = 'PTS ' + str(player_projected_lines['PTS']) + "+"
                over_rebs_line = 'REB ' + str(player_projected_lines['REB']) + "+"
                over_asts_line = 'AST ' + str(player_projected_lines['AST']) + "+"
                
                over_threes_line = '3P ' + str(player_projected_lines['3PT']) + "+"
                over_blks_line = 'BLK ' + str(player_projected_lines['BLK']) + "+"
                over_stls_line = 'STL ' + str(player_projected_lines['STL']) + "+"
                over_tos_line = 'TO ' + str(player_projected_lines['TO']) + "+"
                
                prob_pts_row = [over_pts_line]
                prob_rebs_row = [over_rebs_line]
                prob_asts_row = [over_asts_line]

                prob_threes_row = [over_threes_line]
                prob_blks_row = [over_blks_line]
                prob_stls_row = [over_stls_line]
                prob_tos_row = [over_tos_line]

                

                for game_idx in range(len(all_pts_dicts[conditions].values())):
                    p_count = all_pts_counts[game_idx]
                    r_count = all_rebs_counts[game_idx]
                    a_count = all_asts_counts[game_idx]

                    threes_count = all_threes_counts[game_idx]
                    b_count = all_blks_counts[game_idx]
                    s_count = all_stls_counts[game_idx]
                    to_count = all_tos_counts[game_idx]

                    current_total = str(game_idx + 1)
                    current_total_games = current_total# + ' Games'
                    header_row.append(current_total_games)

                    prob_over_pts_line = str(p_count) + "/" + current_total
                    prob_pts_row.append(prob_over_pts_line)
                    
                    prob_over_rebs_line = str(r_count) + "/" + current_total
                    prob_rebs_row.append(prob_over_rebs_line)
                    prob_over_asts_line = str(a_count) + "/" + current_total
                    prob_asts_row.append(prob_over_asts_line)

                    prob_over_threes_line = str(threes_count) + "/" + current_total
                    prob_threes_row.append(prob_over_threes_line)
                    prob_over_blks_line = str(b_count) + "/" + current_total
                    prob_blks_row.append(prob_over_blks_line)
                    prob_over_stls_line = str(s_count) + "/" + current_total
                    prob_stls_row.append(prob_over_stls_line)
                    prob_over_tos_line = str(to_count) + "/" + current_total
                    prob_tos_row.append(prob_over_tos_line)

                game_num_header = 'Games Ago'
                game_num_row = [game_num_header]
                game_day_header = 'DoW'
                game_day_row = [game_day_header]
                game_date_header = 'Date'
                game_date_row = [game_date_header]

                for game_num in all_pts_dicts[conditions].keys():
                    #game_num = all_pts_dicts[key]
                    game_num_row.append(game_num)
                    game_day_date = player_game_log.loc[game_num,'Date']
                    game_day = game_day_date.split()[0]
                    game_day_row.append(game_day)
                    game_date = game_day_date.split()[1]
                    game_date_row.append(game_date)
                

                #total = str(len(all_pts))
                #probability_over_line = str(count) + "/" + total
                #total_games = total + " Games"
                #header_row = ['Points', total_games]
                #print(probability_over_line)

                #prob_row = [over_line, probability_over_line]

                print("\n===" + player_name + " Probabilities===\n")

                game_num_table = [game_num_row, game_day_row, game_date_row]
                print(tabulate(game_num_table))

                prob_pts_table = [prob_pts_row]
                print(tabulate(prob_pts_table))

                prob_rebs_table = [prob_rebs_row]
                print(tabulate(prob_rebs_table))

                prob_asts_table = [prob_asts_row]
                print(tabulate(prob_asts_table))

                prob_threes_table = [prob_threes_row]
                print(tabulate(prob_threes_table))

                prob_blks_table = [prob_blks_row]
                print(tabulate(prob_blks_table))

                prob_stls_table = [prob_stls_row]
                print(tabulate(prob_stls_table))

                prob_tos_table = [prob_tos_row]
                print(tabulate(prob_tos_table))


                all_prob_stat_tables = [prob_pts_table, prob_rebs_table, prob_asts_table, prob_threes_table, prob_blks_table, prob_stls_table, prob_tos_table]

                for stat_idx in range(len(stats_counts)):
                    stat_counts = stats_counts[stat_idx]
                    prob_table = all_prob_stat_tables[stat_idx][0] # only need first element bc previously formatted for table display
                    if determiner.determine_consistent_streak(stat_counts):
                        # { 'player name': { 'all': {year:[streaks],...}, 'home':{year:streak}, 'away':{year:streak} } }
                        if player_name in all_streak_tables.keys():
                            print(player_name + " in streak tables")

                            player_streak_tables = all_streak_tables[player_name]
                            if conditions in player_streak_tables.keys():
                                print("conditions " + conditions + " in streak tables")
                                player_all_season_streaks = player_streak_tables[conditions]
                                if season_year in player_all_season_streaks.keys():
                                    player_all_season_streaks[season_year].append(prob_table)
                                else:
                                    player_all_season_streaks[season_year] = [prob_table]

                                #player_streak_tables[conditions].append(prob_table) # append all stats for given key
                            else:
                                print("conditions " + conditions + " not in streak tables")
                                player_streak_tables[conditions] = {}
                                player_all_season_streaks = player_streak_tables[conditions]
                                player_all_season_streaks[season_year] = [prob_table]

                                #player_streak_tables[conditions] = [prob_table]
                        else:
                            print(player_name + " not in streak tables")

                            all_streak_tables[player_name] = {}
                            player_streak_tables = all_streak_tables[player_name]

                            #player_streak_tables[conditions] = [prob_table] # v1

                            # v2
                            player_streak_tables[conditions] = {} #[prob_table]

                            player_all_season_streaks = player_streak_tables[conditions]
                            player_all_season_streaks[season_year] = [prob_table]

                        print("player_all_season_streaks: " + str(player_all_season_streaks))
                        print("player_streak_tables: " + str(player_streak_tables))

                            

                        # if key in player_streak_tables.keys():
                        #     player_streak_tables[key].append(prob_table) # append all stats for given key
                        # else:
                        #     player_streak_tables[key] = [prob_table]

                # given how many of recent games we care about
                # later we will take subsection of games with certain settings like home/away
                # first we get all stats and then we can analyze subsections of stats
                # eg last 10 games

        season_year -= 1
            
    

if find_matchups:
    print("\n===Find Matchups===\n")
    # get matchup data before looping thru consistent streaks bc we will present matchup data alongside consistent streaks for comparison
    fantasy_pros_url = 'https://www.fantasypros.com/daily-fantasy/nba/fanduel-defense-vs-position.php' #'https://www.fantasypros.com/nba/defense-vs-position.php' #alt 2: betting_pros_url = 'https://www.bettingpros.com/nba/defense-vs-position/'
    hashtag_bball_url = 'https://hashtagbasketball.com/nba-defense-vs-position'
    swish_analytics_url = 'https://swishanalytics.com/optimus/nba/daily-fantasy-team-defensive-ranks-position'
    draft_edge_url = 'https://draftedge.com/nba-defense-vs-position/'


    # get matchup data for streaks to see if likely to continue streak
    matchup_data_sources = [fantasy_pros_url, hashtag_bball_url, swish_analytics_url] #, hashtag_bball_url, swish_analytics_url, betting_pros_url, draft_edge_url] # go thru each source so we can compare conflicts
    # first read all matchup data from internet and then loop through tables
    all_matchup_data = reader.read_all_matchup_data(matchup_data_sources)


    # display streak tables separately
    # only pull matchup data for streaks bc too much uncertainty without streak, until we get ml to analyze full pattern
    #streaks = isolator.isolate_consistent_streaks(all_stats_counts_dict)

print("\n===Consistent Streaks===\n")

injury_prone_players = ['dangelo russell', 'anthony davis', 'joel embiid']
all_player_game_dicts = {}
for p_name, p_streak_tables in all_streak_tables.items():
    print("\n===" + p_name + "===\n")

    # should we include in output if they have 9/10 overall record but 3/10 location record? depends on breaks and matchups and history pattern

    player_game_dict = {}
    all_player_game_dicts[p_name] = player_game_dict
    if p_name in injury_prone_players:
        print("\n===Warning: Injury Prone Player: " + p_name + "!===\n")
        player_game_dict['warning'] = 'Avoid: ' + p_name + ' is an Injury Prone Player!'

    #print("p_streak_tables:\n" + str(p_streak_tables))

    # we need to get schedule to get next game date to see how many days until next game
    # but we can get prev game from player game log we already have
    # todays_games_date_obj = datetime.strptime(todays_games_date, '%m/%d/%y')
    # print("todays_games_date_obj: " + str(todays_games_date_obj))

    player_season_logs = all_player_season_logs_dict[p_name]
    current_season_log = player_season_logs[0]

    #player_game_log = all_player_game_logs_dict[p_name]
    season_year = 2023
    prev_game_date_obj = determiner.determine_prev_game_date(current_season_log, season_year) # exclude all star and other special games
    # prev_game_date_string = player_game_log.loc[prev_game_idx, 'Date'].split()[1] + "/" + season_year # eg 'wed 2/15' to '2/15/23'
    # prev_game_date_obj = datetime.strptime(prev_game_date_string, '%m/%d/%y')
    days_after_prev_game = (todays_games_date_obj - prev_game_date_obj).days
    print("days_after_prev_game: " + str(days_after_prev_game))

    # p_streak_tables = { 'all': {year:[streaks],...}, 'home':{year:streak}, 'away':{year:streak} }
    for condition, streak_dicts in p_streak_tables.items():
        player_lines = projected_lines_dict[p_name]
        #print("player_lines: " + str(player_lines))

        opponent = player_lines['OPP'].lower()

       
        
        #days_before_next_game = 1
        if str(condition) == 'all' or str(condition) == player_lines['LOC'].lower() or str(condition) == opponent or str(condition) == str(days_after_prev_game) + ' after': # current conditions we are interested in
            print(str(condition).title())
            
            for year, streak_tables in streak_dicts.items():
                print('\n===' + str(year) + '===\n')
                print(tabulate(streak_tables))

            # determine matchup for opponent and stat. we need to see all position matchups to see relative ease
            # display matchup tables with consistent streaks (later look at easiest matchups for all current games, not just consistent streaks bc we may find an exploit)
            
            #print("streak_tables: " + str(streak_tables))
            if find_matchups:
                for streak in streak_tables:

                    print("\n===Matchups===\n")

                    print(streak)

                    stat = streak[0].split(' ')[0]#'pts'
                    #print("stat: " + stat)
                    #all_matchup_ratings = { 'all':{}, 'pg':{}, 'sg':{}, 'sf':{}, 'pf':{}, 'c':{} } # { 'pg': { 'values': [source1,source2,..], 'ranks': [source1,source2,..] }, 'sg': {}, ... }
                    #position_matchup_rating = { 'values':[], 'ranks':[] } # comparing results from different sources
                    current_matchup_data = determiner.determine_matchup_rating(opponent, stat, all_matchup_data) # first show matchups from easiest to hardest position for stat. 

                    #sources_results={values:[],ranks:[]}
                    
                    for pos, sources_results in current_matchup_data.items():
                        print("Position: " + pos.upper())

                        

                        matchup_table_header_row = ['Sources'] # [source1, source2, ..]
                        num_sources = len(sources_results['averages']) #len(source_vals)

                        for source_idx in range(num_sources):
                            source_num = source_idx + 1
                            source_header = 'Source ' + str(source_num)
                            matchup_table_header_row.append(source_header)

                        matchup_table = [matchup_table_header_row]
                        for result, source_vals in sources_results.items():
                            source_vals.insert(0, result.title())
                            matchup_table.append(source_vals)

                        #source_matchup_ratings={ source1: {positions:[], averages:[], ranks:[], avg_ranks:[]}, source2...}
                        avg_source_matchup_ratings = {} # so we can sort by average rank
                        source_matchup_ratings = {}


                        print(tabulate(matchup_table))

