#writer.py
# display data

import re # see if string contains stat and player of interest to display
import numpy # mean, median to display over time

def display_game_data(all_valid_streaks_list):
    print("\n===Game Data===\n")
    # all_player_pre_dicts = [{'prediction':val,'overall record':[],..},{},..]
    # get headers
    # header_row = ['Prediction']
    # for pre_dict in all_player_pre_dicts.values():
    #     for key in pre_dict:
    #         header_row.append(key.title())
    #     break
    # game_data = [header_row]

    # print("all_player_pre_dicts: " + str(all_player_pre_dicts))
    # for prediction, pre_dict in all_player_pre_dicts.items():
    #     prediction_row = [prediction]
    #     for val in pre_dict.values():
    #         prediction_row.append(val)
    #     game_data.append(prediction_row)



    # get headers
    header_row = []
    header_string = '' # separate by semicolons and delimit in spreadsheet
    if len(all_valid_streaks_list) > 0:
        streak1 = all_valid_streaks_list[0]
        for key in streak1.keys():
            header_row.append(key.title())
            header_string += key.title() + ";"

        game_data = [header_row]
        game_data_strings = []
        for streak in all_valid_streaks_list:
            streak_row = []
            streak_string = ''
            for val in streak.values():
                streak_row.append(val)
                streak_string += str(val) + ";"
            game_data.append(streak_row)
            game_data_strings.append(streak_string)
    else:
        print('Warning: no valid streaks!')


    #print(tabulate(game_data))

    print("Export")
    print(header_string)
    for game_data in game_data_strings:
        print(game_data)



def display_stat_plot(all_valid_streaks_list, all_players_stats_dicts, stat_of_interest, player_of_interest):
    print('\n===Plot Stats===\n')
    #Three lines to make our compiler able to draw:
    import matplotlib.pyplot as plt

    #display player stat values so we can see plot
    #columns: game num, stat val, over average record
    #print('all_players_stats_dicts: ' + str(all_players_stats_dicts))
    for valid_streak in all_valid_streaks_list:

        
        
        if re.search(stat_of_interest, valid_streak['prediction'].lower()) and re.search(player_of_interest, valid_streak['prediction'].lower()):

            print('valid_streak: ' + str(valid_streak))
            player_name = ' '.join(valid_streak['prediction'].split()[:-2]).lower() # anthony davis 12+ pts
            print("player_name from prediction: " + player_name)

            stat_name = valid_streak['prediction'].split()[-1].lower()
            condition = 'all'
            season_year = 2023
            stat_vals_dict = all_players_stats_dicts[player_name][season_year][stat_name][condition]
            print('stat_vals_dict: ' + str(stat_vals_dict))

            game_nums = list(stat_vals_dict.keys())
            #print('game_nums: ' + str(game_nums))
            stat_vals = list(stat_vals_dict.values())
            stat_vals.reverse()
            print('stat_vals: ' + str(stat_vals))

            stat_line = int(valid_streak['prediction'].split()[-2][:-1])
            print('stat_line: ' + str(stat_line))

            plot_stat_line = [stat_line] * len(game_nums)
            print('plot_stat_line: ' + str(plot_stat_line))

            # x = np.array(game_nums)
            # y = np.array(stat_vals)

            plt.plot(game_nums, stat_vals, label = "Stat Vals") # reverse bc input from recent to distant but we plot left to right
            plt.plot(game_nums, plot_stat_line,  label = "Stat Line")

            # also plot avg over time to compare trend of avg
            # bc just seeing season avg is barely useful almost useless unless we see either avg in last few games (and multiple subset) or we can simply see if avg is increasing or decreasing
            # the avg for the first game must be based on previous seasons
            # but for now arbitrary number
            #init_mean_stat_val
            prev_stat_vals = []
            mean_stat_vals = [] # how mean changes over time
            past_ten_stat_vals = []
            past_ten_mean_stat_vals = [] # mean over last 10 games to get more recent relevant picture
            past_three_stat_vals = []
            past_three_mean_stat_vals = []
            for stat_val_idx in range(len(stat_vals)):
                stat_val = stat_vals[stat_val_idx]
                #print('prev_stat_vals: ' + str(prev_stat_vals))
                #print('past_ten_stat_vals: ' + str(past_ten_stat_vals))
                # compute avg of this and previous vals
                if stat_val_idx == 0:
                    mean_stat_val = stat_val
                    past_ten_mean_stat_val = stat_val
                    past_three_mean_stat_val = stat_val

                else:
                    mean_stat_val = round(numpy.mean(prev_stat_vals), 1)
                    #print('mean_stat_val: ' + str(mean_stat_val))
                    past_ten_mean_stat_val = round(numpy.mean(past_ten_stat_vals), 1)
                    #print('past_ten_mean_stat_val: ' + str(past_ten_mean_stat_val))
                    past_three_mean_stat_val = round(numpy.mean(past_three_stat_vals), 1)
                    #print('past_three_mean_stat_val: ' + str(past_three_mean_stat_val))

                mean_stat_vals.append(mean_stat_val)
                past_ten_mean_stat_vals.append(past_ten_mean_stat_val)
                past_three_mean_stat_vals.append(past_three_mean_stat_val)

                prev_stat_vals.append(stat_val)

                if stat_val_idx < 10: # add vals to list until we reach 10 bc we only want past 10 games
                    past_ten_stat_vals.append(stat_val)
                else: # replace in list instead of adding
                    past_ten_stat_vals.pop(0)
                    past_ten_stat_vals.append(stat_val)
                if stat_val_idx < 3: # add vals to list until we reach 10 bc we only want past 10 games
                    past_three_stat_vals.append(stat_val)
                else: # replace in list instead of adding
                    past_three_stat_vals.pop(0)
                    past_three_stat_vals.append(stat_val)
                

            #print('mean_stat_vals: ' + str(mean_stat_vals))
            #print('past_ten_mean_stat_vals: ' + str(past_ten_mean_stat_vals))
            #print('past_three_mean_stat_vals: ' + str(past_three_mean_stat_vals))

            plt.plot(game_nums, mean_stat_vals,  label = "Overall Mean")
            plt.plot(game_nums, past_ten_mean_stat_vals,  label = "Past 10 Mean")
            plt.plot(game_nums, past_three_mean_stat_vals,  label = "Past 3 Mean")


            plt.title(player_name.title() + " " + stat_name.upper() + " over Time")
            plt.xlabel("Game Num")
            plt.ylabel(stat_name.upper())

            plt.legend()
            plt.show()

            # display table so we can export to files and view graphs in spreadsheet

            #Two  lines to make our compiler able to draw:
            # plt.savefig(sys.stdout.buffer)
            # sys.stdout.flush()


def display_all_players_records_dicts(all_players_records_dicts, all_player_season_logs_dict):
    print('\n===Display All Players Records Dicts===\n')

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
                print("all_pts_dicts: " + str(all_pts_dicts))
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

                    # display game info for reference based on game idx
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

                    print("\n===" + player_name.title() + " Probabilities===\n")

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

            season_year -= 1

# player_outcomes = {player: stat name: outcome dict}
def display_player_outcomes(player_outcomes):

    print("\n===Player Outcomes===\n")


    # convert player outcomes dict into list
    player_outcomes_list = []
    for stat_outcome_dict in player_outcomes.values():

        for outcome_dict in stat_outcome_dict.values():

            player_outcomes_list.append(outcome_dict)

    # get headers
    header_row = []
    header_string = '' # separate by semicolons and delimit in spreadsheet
    if len(player_outcomes_list) > 0:
        outcome1 = player_outcomes_list[0]
        for key in outcome1.keys():
            header_row.append(key.title())
            header_string += key.title() + ";"

        game_data = [header_row]
        game_data_strings = []
        for outcome in player_outcomes_list:
            outcome_row = []
            outcome_string = ''
            for val in outcome.values():
                outcome_row.append(val)
                outcome_string += str(val) + ";"
            game_data.append(outcome_row)
            game_data_strings.append(outcome_string)
    else:
        print('Warning: no valid streaks!')


    #print(tabulate(game_data))

    print("Export")
    print(header_string)
    for game_data in game_data_strings:
        print(game_data)

    print("\n===End Player Outcomes===\n")