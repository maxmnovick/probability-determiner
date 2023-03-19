# generator.py
# generate data structures so we can reference info to make decisions
# and generate decisions based on data structures

import re
from datetime import datetime # convert date str to date so we can see if games 1 day apart and how many games apart

import determiner # determine regular season games, etc

import numpy # mean, median
from scipy import stats # calculate mode

import reader # read game log from file if needed

from tabulate import tabulate # display output

# we use all_players_stats_dicts = {player name:{stat name:{}}}
# to reference stats 
# all_player_season_logs_dict = {player name:{year:{condition:{stat:[]}}}}
# projected_lines_dict = {player name:{stat:value,..,loc:val,opp:val}}
# use projected lines input param to get opponenet
# use today game date to get day and break conditions
def generate_all_players_stats_dicts(all_player_season_logs_dict, projected_lines_dict, todays_games_date_obj):
    print('\n===Generate All Players Stats Dicts===\n')
    all_players_stats_dicts = {}

    for player_name, player_season_logs in all_player_season_logs_dict.items():
    #for player_idx in range(len(all_player_game_logs)):

        print('\n===' + player_name.title() + '===\n')

        season_year = 2023

        # get no. games played this season
        current_season_log = player_season_logs[0]
        current_reg_season_log = determiner.determine_regular_season_games(current_season_log)
        num_games_played = len(current_reg_season_log.index) # see performance at this point in previous seasons

        # for game_idx, row in current_season_log.iterrows():
                    
        #     if re.search('\\*',current_season_log.loc[game_idx, 'OPP']): # all star stats not included in regular season stats
        #         #print("game excluded")
        #         continue
            
        #     if current_season_log.loc[game_idx, 'Type'] == 'Regular':
        #         num_games_played += 1


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
            all_pts_dicts = { 'all':{}, 'home':{}, 'away':{} } # 'opp eg okc':{}, 'day of week eg tue':{}
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
                #print("player_game_log:\n" + str(player_game_log))
                # we pulled game log from internet

                opponent = projected_lines_dict[player_name]['OPP'].lower() # collect data against opponent to see previous matchups
                
                # first loop thru all regular season games, then thru subset of games such as home/away
                # or just append to subset array predefined such as all_home_pts = []
                next_game_date_obj = datetime.today() # need to see if back to back games 1 day apart

                reg_season_game_log = determiner.determine_regular_season_games(player_game_log)

                total_season_games = len(reg_season_game_log.index) # so we can get game num from game idx
                
                for game_idx, row in reg_season_game_log.iterrows():
                    
                    #game = player_game_log[game_idx, row]
                    #print("game:\n" + str(game))
                    #print("player_game_log.loc[game_idx, 'Type']: " + player_game_log.loc[game_idx, 'Type'])  

                    # === Collect Stats for Current Game ===

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


                    # === Add Stats to Dict ===

                    # now that we have game stats add them to dict by condition

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
                    # only add key for current opp bc we dont need to see all opps here
                    # look for irregular abbrevs like NO and NY
                    # opponent in form 'gsw' but game log in form 'gs'
                    game_log_team_abbrev = re.sub('vs|@','',player_game_log.loc[game_idx, 'OPP'].lower()) # eg 'gs'
                    #print('game_log_team_abbrev: ' + game_log_team_abbrev)
                    opp_abbrev = opponent # default if regular
                    #print('opp_abbrev: ' + opp_abbrev)

                    irregular_abbrevs = {'nop':'no', 'nyk':'ny', 'sas': 'sa', 'gsw':'gs' } # for these match the first 3 letters of team name instead
                    if opp_abbrev in irregular_abbrevs.keys():
                        #print("irregular abbrev: " + team_abbrev)
                        opp_abbrev = irregular_abbrevs[opp_abbrev]

                    if opp_abbrev == game_log_team_abbrev:
                        #print('opp_abbrev == game_log_team_abbrev')
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

                    # if current loop is most recent game (idx 0) then today's game is the next game, if current season
                    # if last game of prev season then next game after idx 0 (bc from recent to distant) is next season game 1
                    if game_idx == 0: # see how many days after prev game is date of today's projected lines
                        # already defined or passed todays_games_date_obj
                        # todays_games_date_obj = datetime.strptime(todays_games_date, '%m/%d/%y')
                        # print("todays_games_date_obj: " + str(todays_games_date_obj))
                        current_year = 2023
                        if season_year == current_year: # current year
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

                    

                    


                    # add keys for each day of the week so we can see performance by day of week
                    # only add key for current dow bc we dont need to see all dows here
                    
                    game_dow = player_game_log.loc[game_idx, 'Date'].lower().split()[0].lower() # 'wed 2/15'[0]='wed'
                    current_dow = todays_games_date_obj.strftime('%a').lower()
                    #print('current_dow: ' + str(current_dow))
                    if current_dow == game_dow:
                        #print("found same game day of week: " + game_dow)
                        for stat_idx in range(len(all_stats_dicts.values())):
                            stat_dict = list(all_stats_dicts.values())[stat_idx]
                            stat = game_stats[stat_idx]
                            if not game_dow in stat_dict.keys():
                                stat_dict[game_dow] = {}
                            stat_dict[game_dow][game_idx] = stat
                        #print("stat_dict: " + str(stat_dict))


                    # Career/All Seasons Stats
                    # if we find a game played on the same day/mth previous seasons, add a key for this/today's day/mth
                    #today_date_data = todays_games_date.split('/')
                    today_mth_day = str(todays_games_date_obj.month) + '/' + str(todays_games_date_obj.day) #today_date_data[0] + '/' + today_date_data[1]
                    if init_game_date_string == today_mth_day:
                        #print("found same game day/mth in previous season")
                        for stat_idx in range(len(all_seasons_stats_dicts.values())):
                            stat_dict = list(all_seasons_stats_dicts.values())[stat_idx]
                            stat = game_stats[stat_idx]
                            if not game_date_string in stat_dict.keys():
                                stat_dict[game_date_string] = {}
                                stat_dict[game_date_string][game_idx] = [stat] # we cant use game idx as key bc it gets replaced instead of adding vals
                            else:
                                if game_idx in stat_dict[game_date_string].keys():
                                    stat_dict[game_date_string][game_idx].append(stat)
                                else:
                                    stat_dict[game_date_string][game_idx] = [stat]
                        #print("all_seasons_stats_dicts: " + str(all_seasons_stats_dicts))
                    # add key for the current game number for this season and add games played from previous seasons (1 per season)
                    game_num = total_season_games - game_idx # bc going from recent to past
                    if game_num == num_games_played:
                        #print("found same game num in previous season")
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
                        #print("all_seasons_stats_dicts: " + str(all_seasons_stats_dicts))


                    # after all keys are set, set next game as current game for next loop
                    next_game_date_obj = game_date_obj # next game bc we loop from most to least recent

            else:
                # if getting data from file, may not have game log from internet source
                # data_type = "Game Log"
                # player_season_log = reader.read_season_log_from_file(data_type, player_name, 'tsv')
                print('Warning: No game log for player: ' + player_name)

            # at this point we have fully populated all stats dicts for this player's season
            # add all stats for this player's season to all players stats dicts
            if player_name not in all_players_stats_dicts.keys():
                all_players_stats_dicts[player_name] = {}
            
            all_players_stats_dicts[player_name][season_year] = all_stats_dicts
            print('all_players_stats_dicts: ' + str(all_players_stats_dicts))
            season_year -= 1

        
                
    print('all_players_stats_dicts: ' + str(all_players_stats_dicts))
    return all_players_stats_dicts

# all players stats dicts = { player: year: stat name: condition: game idx: stat val }
def generate_all_players_records_dicts(all_players_stats_dicts, projected_lines_dict):
    print('\n===Generate All Players Records Dicts===\n')
    all_records_dicts = {}

    # player_stat_dict = { year: .. }
    for player_name, player_stat_dict in all_players_stats_dicts.items():
    #for player_idx in range(len(all_player_game_logs)):

        print('\n===' + player_name.title() + '===\n')

        #season_year = 2023

        # player_season_stat_dict = { stat name: .. }
        for season_year, player_season_stat_dict in player_stat_dict.items():

            print("\n===Year " + str(season_year) + "===\n")
            #player_game_log = player_season_logs[0] #start with current season. all_player_game_logs[player_idx]
            #player_name = player_names[player_idx] # player names must be aligned with player game logs

            # all_pts_dicts = {'all':{idx:val,..},..}
            all_pts_dicts = player_season_stat_dict['pts']
            all_rebs_dicts = player_season_stat_dict['reb']
            all_asts_dicts = player_season_stat_dict['ast']
            all_threes_made_dicts = player_season_stat_dict['3pm']
            all_bs_dicts = player_season_stat_dict['blk']
            all_ss_dicts = player_season_stat_dict['stl']
            all_tos_dicts = player_season_stat_dict['to']
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
                #print("all_pts_dicts: " + str(all_pts_dicts))
                # all_pts_dicts = {'all':{1:20}}
                # key=condition, val={idx:stat}

                
                #compute stats from data
                # key represents set of conditions of interest eg home/away
                for conditions in all_pts_dicts.keys(): # all stats dicts have same keys so we use first 1 as reference

                    # reset for each set of conditions

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
                    
                    over_threes_line = '3PM ' + str(player_projected_lines['3PT']) + "+"
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


                    prob_pts_table = [prob_pts_row]
                    prob_rebs_table = [prob_rebs_row]
                    prob_asts_table = [prob_asts_row]
                    prob_threes_table = [prob_threes_row]
                    prob_blks_table = [prob_blks_row]
                    prob_stls_table = [prob_stls_row]
                    prob_tos_table = [prob_tos_row]
                    
                    all_prob_stat_tables = [prob_pts_table, prob_rebs_table, prob_asts_table, prob_threes_table, prob_blks_table, prob_stls_table, prob_tos_table]

                    all_prob_stat_rows = [prob_pts_row,prob_rebs_row,prob_asts_row,prob_threes_row,prob_blks_row,prob_stls_row,prob_tos_row]

                    # stats counts should include all stats
                    # so we save in dict for reference
                    for stat_idx in range(len(stats_counts)):
                        stat_counts = stats_counts[stat_idx]
                        prob_row = all_prob_stat_rows[stat_idx]#[0] # only needed first element bc previously formatted for table display
                        # if blk, stl, or to look for 2+
                        # for all, check to see if 1+ or not worth predicting bc too risky
                        #stat_line = prob_table[0].split
                        stat_line = int(prob_row[0].split()[1][:-1]) # [pts 16+, 1/1, 2/2, ..] -> 16
                        #print('stat_line: ' + str(stat_line))
                        if stat_line < 2: # may need to change for 3 pointers if really strong likelihood to get 1
                            continue



                        # save player stats in dict for reference
                        # save for all stats, not just streaks
                        # at first there will not be this player name in the dict so we add it
                        stat_name = prob_row[0].split()[0].lower() # [pts 16+, 1/1, 2/2, ..] -> pts
                        streak = prob_row[1:] # [pts 16+, 1/1, 2/2, ..] -> [1/1,2/2,...]

                        if not player_name in all_records_dicts.keys():
                            all_records_dicts[player_name] = {} # init bc player name key not in dict so if we attempt to set its val it is error

                            player_records_dicts = all_records_dicts[player_name] # {player name: { condition: { year: { stat: [1/1,2/2,...],.. },.. },.. },.. }

                            player_records_dicts[conditions] = {}
                            player_all_records_dicts = player_records_dicts[conditions]
                            
                            player_all_records_dicts[season_year] = { stat_name: streak }

                        else: # player already in list

                            player_records_dicts = all_records_dicts[player_name]
                            if conditions in player_records_dicts.keys():
                                #print("conditions " + conditions + " in streak tables")
                                player_all_records_dicts = player_records_dicts[conditions]
                                if season_year in player_all_records_dicts.keys():
                                    player_all_records_dicts[season_year][stat_name] = streak
                                else:
                                    player_all_records_dicts[season_year] = { stat_name: streak }

                                #player_streak_tables[conditions].append(prob_table) # append all stats for given key
                            else:
                                #print("conditions " + conditions + " not in streak tables")
                                player_records_dicts[conditions] = {}
                                player_all_records_dicts = player_records_dicts[conditions]
                                player_all_records_dicts[season_year] = { stat_name: streak }

                    # given how many of recent games we care about
                    # later we will take subsection of games with certain settings like home/away
                    # first we get all stats and then we can analyze subsections of stats
                    # eg last 10 games

            season_year -= 1
                
    print('all_records_dicts: ' + str(all_records_dicts))
    return all_records_dicts


def generate_player_stat_dict(player_name, player_season_logs):

    print('\n===' + player_name.title() + '===\n')

    season_year = 2023

    # get no. games played this season
    current_season_log = player_season_logs[0]
    current_reg_season_log = determiner.determine_regular_season_games(current_season_log)
    num_games_played = len(current_reg_season_log.index) # see performance at this point in previous seasons

    # for game_idx, row in current_season_log.iterrows():
                
    #     if re.search('\\*',current_season_log.loc[game_idx, 'OPP']): # all star stats not included in regular season stats
    #         #print("game excluded")
    #         continue
        
    #     if current_season_log.loc[game_idx, 'Type'] == 'Regular':
    #         num_games_played += 1


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
        all_pts_dicts = { 'all':{}, 'home':{}, 'away':{} } # 'opp eg okc':{}, 'day of week eg tue':{}
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
            #print("player_game_log:\n" + str(player_game_log))
            # we pulled game log from internet

            opponent = projected_lines_dict[player_name]['OPP'].lower() # collect data against opponent to see previous matchups
            
            # first loop thru all regular season games, then thru subset of games such as home/away
            # or just append to subset array predefined such as all_home_pts = []
            next_game_date_obj = datetime.today() # need to see if back to back games 1 day apart

            reg_season_game_log = determiner.determine_regular_season_games(player_game_log)

            total_season_games = len(reg_season_game_log.index) # so we can get game num from game idx
            
            for game_idx, row in reg_season_game_log.iterrows():
                
                #game = player_game_log[game_idx, row]
                #print("game:\n" + str(game))
                #print("player_game_log.loc[game_idx, 'Type']: " + player_game_log.loc[game_idx, 'Type'])  

                # === Collect Stats for Current Game ===

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


                # === Add Stats to Dict ===

                # now that we have game stats add them to dict by condition

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
                # only add key for current opp bc we dont need to see all opps here
                # look for irregular abbrevs like NO and NY
                # opponent in form 'gsw' but game log in form 'gs'
                game_log_team_abbrev = re.sub('vs|@','',player_game_log.loc[game_idx, 'OPP'].lower()) # eg 'gs'
                #print('game_log_team_abbrev: ' + game_log_team_abbrev)
                opp_abbrev = opponent # default if regular
                #print('opp_abbrev: ' + opp_abbrev)

                irregular_abbrevs = {'nop':'no', 'nyk':'ny', 'sas': 'sa', 'gsw':'gs' } # for these match the first 3 letters of team name instead
                if opp_abbrev in irregular_abbrevs.keys():
                    #print("irregular abbrev: " + team_abbrev)
                    opp_abbrev = irregular_abbrevs[opp_abbrev]

                if opp_abbrev == game_log_team_abbrev:
                    #print('opp_abbrev == game_log_team_abbrev')
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

                # if current loop is most recent game (idx 0) then today's game is the next game, if current season
                # if last game of prev season then next game after idx 0 (bc from recent to distant) is next season game 1
                if game_idx == 0: # see how many days after prev game is date of today's projected lines
                    # already defined or passed todays_games_date_obj
                    # todays_games_date_obj = datetime.strptime(todays_games_date, '%m/%d/%y')
                    # print("todays_games_date_obj: " + str(todays_games_date_obj))
                    current_year = 2023
                    if season_year == current_year: # current year
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

                

                


                # add keys for each day of the week so we can see performance by day of week
                # only add key for current dow bc we dont need to see all dows here
                
                game_dow = player_game_log.loc[game_idx, 'Date'].lower().split()[0].lower() # 'wed 2/15'[0]='wed'
                current_dow = todays_games_date_obj.strftime('%a').lower()
                #print('current_dow: ' + str(current_dow))
                if current_dow == game_dow:
                    print("found same game day of week: " + game_dow)
                    for stat_idx in range(len(all_stats_dicts.values())):
                        stat_dict = list(all_stats_dicts.values())[stat_idx]
                        stat = game_stats[stat_idx]
                        if not game_dow in stat_dict.keys():
                            stat_dict[game_dow] = {}
                        stat_dict[game_dow][game_idx] = stat
                    print("stat_dict: " + str(stat_dict))


                # Career/All Seasons Stats
                # if we find a game played on the same day/mth previous seasons, add a key for this/today's day/mth
                #today_date_data = todays_games_date.split('/')
                today_mth_day = str(todays_games_date_obj.month) + '/' + str(todays_games_date_obj.day) #today_date_data[0] + '/' + today_date_data[1]
                if init_game_date_string == today_mth_day:
                    print("found same game day/mth in previous season")
                    for stat_idx in range(len(all_seasons_stats_dicts.values())):
                        stat_dict = list(all_seasons_stats_dicts.values())[stat_idx]
                        stat = game_stats[stat_idx]
                        if not game_date_string in stat_dict.keys():
                            stat_dict[game_date_string] = {}
                            stat_dict[game_date_string][game_idx] = [stat] # we cant use game idx as key bc it gets replaced instead of adding vals
                        else:
                            if game_idx in stat_dict[game_date_string].keys():
                                stat_dict[game_date_string][game_idx].append(stat)
                            else:
                                stat_dict[game_date_string][game_idx] = [stat]
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






                # after all keys are set, set next game as current game for next loop
                next_game_date_obj = game_date_obj # next game bc we loop from most to least recent

        else:
            # if getting data from file, may not have game log from internet source
            # data_type = "Game Log"
            # player_season_log = reader.read_season_log_from_file(data_type, player_name, 'tsv')
            print('Warning: No game log for player: ' + player_name)


        

        season_year -= 1

# prediction is really a list of features that we must assess to determine the probability of both/all outcomes
#def generate_player_prediction(player_name, player_season_logs):
def generate_player_prediction(player_name, player_season_logs):

    player_stat_dict = generate_player_stat_dict(player_name, player_season_logs)

    player_record_dict = generate_player_record_dict(player_name, player_season_logs)

    player_averages_dict = generate_player_averages_dict(player_name, player_season_logs)

    player_range_dict = generate_player_range_dict(player_name, player_season_logs)


    # todo: make fcn to classify recently broken streaks bc that recent game may be anomaly and they may revert back to streak
    # todo: to fully predict current player stats, must predict teammate and opponent stats and prioritize and align with totals

