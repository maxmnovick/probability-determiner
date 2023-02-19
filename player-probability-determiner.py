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

all_player_game_logs = []


player_names = ['Julius Randle', 'Jalen Brunson', 'RJ Barrett', 'Demar Derozan', 'Paolo Banchero', 'Zach Lavine', 'Franz Wagner', 'Nikola Vucevic', 'Wendell Carter Jr', 'Ayo Dosunmu', 'Markelle Fultz', 'Patrick Williams', 'Brandon Ingram', 'Shai Gilgeous Alexander', 'CJ Mccollum', 'Josh Giddey', 'Trey Murphy III', 'Jalen Williams', 'Herbert Jones', 'Anthony Edwards', 'Luka Doncic', 'Rudy Gobert', 'Kyrie Irving', 'Mike Conley', 'Jaden Mcdaniels', 'Jordan Poole', 'Klay Thompson', 'Draymond Green', 'Kevon Looney','Gary Harris'] #['Bojan Bogdanovic', 'Jaden Ivey', 'Killian Hayes', 'Pascal Siakam', 'Fred Vanvleet', 'Gary Trent Jr', 'Scottie Barnes', 'Isaiah Stewart', 'Jalen Duren', 'Chris Boucher'] #['Ja Morant', 'Desmond Bane', 'Jaren Jackson Jr', 'Dillon Brooks', 'Jayson Tatum', 'Derrick White', 'Robert Williams', 'Malcolm Brogdon', 'Al Horford', 'Xavier Tillman', 'Brandon Clarke']
pts_lines = [25,25,19,23,19,24,16,19,15,9,14,11,31,18,13,28,33,14,25,11,11,26,26,9,7,10] #[22, 16, 13, 25, 22, 20, 17, 12, 11, 10] #[28, 21, 16, 13, 33, 18, 10, 15, 9, 8, 10]
r_lines = [10,4,5,5,7,5,2,12,8,2,4,5,2,5,2,8,2,2,2,6,9,11,4,3,4,2,2,8,9,2] #[4, 4, 3, 7, 4, 3, 7, 9, 10, 6] #[7, 5, 7, 3, 9, 5, 10, 5, 6, 7, 6]
a_lines = [2,6,2,5,2,4,2,2,3,2,6,2,2,6,2,6,2,3,2,2,7,2,6,6,2,5,3,7,2,2] #[3, 6, 7, 6, 7, 2, 5, 2, 2, 2] #[8, 4, 2, 2, 6, 6, 2, 4, 3, 2, 2]
threes_lines = [3,1,1,1,1,3,2,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,1,1,1,5,1,1,2]
b_lines = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
s_lines = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
to_lines = [3,1,1,1,3,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1]

data_type = "Game Lines"
input_type = ''#'2_14' # date as mth_day
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

for p_name in player_names:

    player_game_log = reader.read_player_game_log(p_name) # player url includes year at this point

    all_player_game_logs.append(player_game_log) # could continue to process in this loop or save all player game logs to process in next loop




print("\n===All Players===\n")

player_game_log = all_player_game_logs[0]
# player game log from espn
for player_idx in range(len(all_player_game_logs)):
    player_game_log = all_player_game_logs[player_idx]
    player_name = player_names[player_idx]

    all_pts = []
    all_rebs = []
    all_asts = []

    all_winning_scores = []
    all_losing_scores = []
    all_minutes = []
    all_fgms = []
    all_fgas = []
    all_fg_rates = []
    all_threes_made = []
    all_threes_attempts = []
    all_three_rates = []
    all_ftms = []
    all_ftas = []
    all_ft_rates = []
    all_bs = []
    all_ss = []
    all_fs = []
    all_tos = []

    all_pts_dict = { 'all':[], 'home':[], 'away':[] }
    all_rebs_dict = { 'all':[], 'home':[], 'away':[] }
    all_asts_dict = { 'all':[], 'home':[], 'away':[] }
    all_winning_scores_dict = { 'all':[], 'home':[], 'away':[] }
    all_losing_scores_dict = { 'all':[], 'home':[], 'away':[] }
    all_minutes_dict = { 'all':[], 'home':[], 'away':[] }
    all_fgms_dict = { 'all':[], 'home':[], 'away':[] }
    all_fgas_dict = { 'all':[], 'home':[], 'away':[] }
    all_fg_rates_dict = { 'all':[], 'home':[], 'away':[] }
    all_threes_made_dict = { 'all':[], 'home':[], 'away':[] }
    all_threes_attempts_dict = { 'all':[], 'home':[], 'away':[] }
    all_threes_rates_dict = { 'all':[], 'home':[], 'away':[] }
    all_ftms_dict = { 'all':[], 'home':[], 'away':[] }
    all_ftas_dict = { 'all':[], 'home':[], 'away':[] }
    all_ft_rates_dict = { 'all':[], 'home':[], 'away':[] }
    all_bs_dict = { 'all':[], 'home':[], 'away':[] }
    all_ss_dict = { 'all':[], 'home':[], 'away':[] }
    all_fs_dict = { 'all':[], 'home':[], 'away':[] }
    all_tos_dict = { 'all':[], 'home':[], 'away':[] }


    if len(player_game_log) > 0:
        print("player_game_log:\n" + str(player_game_log))
        # we pulled game log from internet

        opponent = projected_lines_dict[player_name]['OPP'].lower() # collect data against opponent to see previous matchups
        
        # first loop thru all regular season games, then thru subset of games such as home/away
        # or just append to subset array predefined such as all_home_pts = []
        for game_idx, row in player_game_log.iterrows():
            
            #game = player_game_log[game_idx, row]
            #print("game:\n" + str(game))
            #print("player_game_log.loc[game_idx, 'Type']: " + player_game_log.loc[game_idx, 'Type'])

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

                all_pts.append(pts)
                all_rebs.append(rebs)
                all_asts.append(asts)

                all_winning_scores.append(winning_score)
                all_losing_scores.append(losing_score)

                all_minutes.append(minutes)
                all_fgms.append(fgm)
                all_fgas.append(fga)
                all_fg_rates.append(fg_rate)
                all_threes_made.append(threes_made)
                all_threes_attempts.append(threes_attempts)
                all_three_rates.append(three_rate)
                all_ftms.append(ftm)
                all_ftas.append(fta)
                all_ft_rates.append(ft_rate)
                all_bs.append(bs)
                all_ss.append(ss)
                all_fs.append(fs)
                all_tos.append(tos)

                all_pts_dict['all'].append(pts)
                #print("all_pts_dict: " + str(all_pts_dict))
                all_rebs_dict['all'].append(rebs)
                all_asts_dict['all'].append(asts)
                all_winning_scores_dict['all'].append(winning_score)
                all_losing_scores_dict['all'].append(losing_score)
                all_minutes_dict['all'].append(minutes)
                all_fgms_dict['all'].append(fgm)
                all_fgas_dict['all'].append(fga)
                all_fg_rates_dict['all'].append(fg_rate)
                all_threes_made_dict['all'].append(threes_made)
                all_threes_attempts_dict['all'].append(threes_attempts)
                all_threes_rates_dict['all'].append(three_rate)
                all_ftms_dict['all'].append(ftm)
                all_ftas_dict['all'].append(fta)
                all_ft_rates_dict['all'].append(ft_rate)
                all_bs_dict['all'].append(bs)
                all_ss_dict['all'].append(ss)
                all_fs_dict['all'].append(fs)
                all_tos_dict['all'].append(tos)

                if re.search('vs',player_game_log.loc[game_idx, 'OPP']):
                    all_pts_dict['home'].append(pts)
                    #print("all_pts_dict: " + str(all_pts_dict))
                    all_rebs_dict['home'].append(rebs)
                    all_asts_dict['home'].append(asts)
                    all_winning_scores_dict['home'].append(winning_score)
                    all_losing_scores_dict['home'].append(losing_score)
                    all_minutes_dict['home'].append(minutes)
                    all_fgms_dict['home'].append(fgm)
                    all_fgas_dict['home'].append(fga)
                    all_fg_rates_dict['home'].append(fg_rate)
                    all_threes_made_dict['home'].append(threes_made)
                    all_threes_attempts_dict['home'].append(threes_attempts)
                    all_threes_rates_dict['home'].append(three_rate)
                    all_ftms_dict['home'].append(ftm)
                    all_ftas_dict['home'].append(fta)
                    all_ft_rates_dict['home'].append(ft_rate)
                    all_bs_dict['home'].append(bs)
                    all_ss_dict['home'].append(ss)
                    all_fs_dict['home'].append(fs)
                    all_tos_dict['home'].append(tos)
                else: # if not home then away
                    all_pts_dict['away'].append(pts)
                    #print("all_pts_dict: " + str(all_pts_dict))
                    all_rebs_dict['away'].append(rebs)
                    all_asts_dict['away'].append(asts)
                    all_winning_scores_dict['away'].append(winning_score)
                    all_losing_scores_dict['away'].append(losing_score)
                    all_minutes_dict['away'].append(minutes)
                    all_fgms_dict['away'].append(fgm)
                    all_fgas_dict['away'].append(fga)
                    all_fg_rates_dict['away'].append(fg_rate)
                    all_threes_made_dict['away'].append(threes_made)
                    all_threes_attempts_dict['away'].append(threes_attempts)
                    all_threes_rates_dict['away'].append(three_rate)
                    all_ftms_dict['away'].append(ftm)
                    all_ftas_dict['away'].append(fta)
                    all_ft_rates_dict['away'].append(ft_rate)
                    all_bs_dict['away'].append(bs)
                    all_ss_dict['away'].append(ss)
                    all_fs_dict['away'].append(fs)
                    all_tos_dict['away'].append(tos)

                # matchup against opponent
                if re.search(opponent,player_game_log.loc[game_idx, 'OPP'].lower()):
                    if opponent in all_pts_dict.keys():
                        all_pts_dict[opponent].append(pts)
                        #print("all_pts_dict: " + str(all_pts_dict))
                        all_rebs_dict[opponent].append(rebs)
                        all_asts_dict[opponent].append(asts)
                        all_winning_scores_dict[opponent].append(winning_score)
                        all_losing_scores_dict[opponent].append(losing_score)
                        all_minutes_dict[opponent].append(minutes)
                        all_fgms_dict[opponent].append(fgm)
                        all_fgas_dict[opponent].append(fga)
                        all_fg_rates_dict[opponent].append(fg_rate)
                        all_threes_made_dict[opponent].append(threes_made)
                        all_threes_attempts_dict[opponent].append(threes_attempts)
                        all_threes_rates_dict[opponent].append(three_rate)
                        all_ftms_dict[opponent].append(ftm)
                        all_ftas_dict[opponent].append(fta)
                        all_ft_rates_dict[opponent].append(ft_rate)
                        all_bs_dict[opponent].append(bs)
                        all_ss_dict[opponent].append(ss)
                        all_fs_dict[opponent].append(fs)
                        all_tos_dict[opponent].append(tos)
                    else:
                        all_pts_dict[opponent] = [pts]
                        all_rebs_dict[opponent] = [rebs]
                        all_asts_dict[opponent] = [asts]
                        all_winning_scores_dict[opponent] = [winning_score]
                        all_losing_scores_dict[opponent] = [losing_score]
                        all_minutes_dict[opponent] = [minutes]
                        all_fgms_dict[opponent] = [fgm]
                        all_fgas_dict[opponent] = [fga]
                        all_fg_rates_dict[opponent] = [fg_rate]
                        all_threes_made_dict[opponent] = [threes_made]
                        all_threes_attempts_dict[opponent] = [threes_attempts]
                        all_threes_rates_dict[opponent] = [three_rate]
                        all_ftms_dict[opponent] = [ftm]
                        all_ftas_dict[opponent] = [fta]
                        all_ft_rates_dict[opponent] = [ft_rate]
                        all_bs_dict[opponent] = [bs]
                        all_ss_dict[opponent] = [ss]
                        all_fs_dict[opponent] = [fs]
                        all_tos_dict[opponent] = [tos]


                    

    else:
        # if getting data from file
        player_data = reader.extract_data(data_type, player_name, 'tsv')
        # first row is headers, next are games with monthly averages bt each mth

        #desired_field = 'points'
        #desired_field_idx = determiner.determine_field_idx(desired_field)
        date_idx = 0
        opp_idx = 1
        result_idx = 2
        minutes_idx = 3
        fg_idx = 4
        fg_rate_idx = 5
        three_idx = 6
        three_rate_idx = 7
        ft_idx = 8
        ft_rate_idx = 9
        r_idx = 10
        a_idx = 11
        b_idx = 12
        s_idx = 13
        f_idx = 14
        to_idx = 15
        p_idx = 16

        # isolate games from lebron data
        # exclude headers and monthly averages
        player_games_data = isolator.isolate_player_game_data(player_data, player_name)



        if len(player_games_data) > 0:
            for game in player_games_data:
                pts = int(game[p_idx])
                rebs = int(game[r_idx])
                asts = int(game[a_idx])

                results = game[result_idx]
                #print("results: " + results)
                results_data = re.split('\\s+', results)
                #print("results_data: " + str(results_data))
                score_data = results_data[1].split('-')
                #print("score_data: " + str(score_data))
                winning_score = int(score_data[0])
                losing_score = int(score_data[1])

                minutes = int(game[minutes_idx])

                fgs = game[fg_idx]
                fg_data = fgs.split('-')
                fgm = int(fg_data[0])
                fga = int(fg_data[1])
                fg_rate = round(float(game[fg_rate_idx]), 1)

                threes = game[three_idx]
                threes_data = threes.split('-')
                #print("threes_data: " + str(threes_data))
                threes_made = int(threes_data[0])
                threes_attempts = int(threes_data[1])
                three_rate = round(float(game[three_rate_idx]), 1)

                fts = game[ft_idx]
                ft_data = fts.split('-')
                ftm = int(ft_data[0])
                fta = int(ft_data[1])
                ft_rate = round(float(game[ft_rate_idx]), 1)

                bs = int(game[b_idx])
                ss = int(game[s_idx])
                fs = int(game[f_idx])
                tos = int(game[to_idx])

                all_pts.append(pts)
                all_rebs.append(rebs)
                all_asts.append(asts)

                all_winning_scores.append(winning_score)
                all_losing_scores.append(losing_score)

                all_minutes.append(minutes)
                all_fgms.append(fgm)
                all_fgas.append(fga)
                all_fg_rates.append(fg_rate)
                all_threes_made.append(threes_made)
                all_threes_attempts.append(threes_attempts)
                all_three_rates.append(three_rate)
                all_ftms.append(ftm)
                all_ftas.append(fta)
                all_ft_rates.append(ft_rate)
                all_bs.append(bs)
                all_ss.append(ss)
                all_fs.append(fs)
                all_tos.append(tos)

        else:
            print("Warning: No player games data!")


    if len(all_pts) > 0:
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
        all_streak_tables = { } # { 'player name': { 'all': [], 'home':[], 'away':[] } }

        print("all_pts_dict: " + str(all_pts_dict))
        for key in all_pts_dict.keys():
            pts_mean = round(numpy.mean(all_pts_dict[key]), 1)
            pts_median = int(numpy.median(all_pts_dict[key]))
            pts_mode = stats.mode(all_pts_dict[key], keepdims=False)[0]
            pts_min = numpy.min(all_pts_dict[key])
            pts_max = numpy.max(all_pts_dict[key])

            rebs_mean = round(numpy.mean(all_rebs_dict[key]), 1)
            rebs_median = int(numpy.median(all_rebs_dict[key]))
            rebs_mode = stats.mode(all_rebs_dict[key], keepdims=False)[0]
            rebs_min = numpy.min(all_rebs_dict[key])
            rebs_max = numpy.max(all_rebs_dict[key])

            asts_mean = round(numpy.mean(all_asts_dict[key]), 1)
            asts_median = int(numpy.median(all_asts_dict[key]))
            asts_mode = stats.mode(all_asts_dict[key], keepdims=False)[0]
            asts_min = numpy.min(all_asts_dict[key])
            asts_max = numpy.max(all_asts_dict[key])


            winning_score_mean = round(numpy.mean(all_winning_scores_dict[key]), 1)
            winning_score_median = int(numpy.median(all_winning_scores_dict[key]))
            winning_score_mode = stats.mode(all_winning_scores_dict[key], keepdims=False)[0]
            winning_score_min = int(numpy.min(all_winning_scores_dict[key]))
            winning_score_max = int(numpy.max(all_winning_scores_dict[key]))

            losing_score_mean = round(numpy.mean(all_losing_scores_dict[key]), 1)
            losing_score_median = int(numpy.median(all_losing_scores_dict[key]))
            losing_score_mode = stats.mode(all_losing_scores_dict[key], keepdims=False)[0]
            losing_score_min = int(numpy.min(all_losing_scores_dict[key]))
            losing_score_max = int(numpy.max(all_losing_scores_dict[key]))

            result_mean = str(winning_score_mean) + "-" + str(losing_score_mean)
            result_median = str(winning_score_median) + "-" + str(losing_score_median)
            result_mode = str(winning_score_mode) + "-" + str(losing_score_mode)
            result_min = str(winning_score_min) + "-" + str(losing_score_min)
            result_max = str(winning_score_max) + "-" + str(losing_score_max)


            minutes_mean = round(numpy.mean(all_minutes_dict[key]), 1)
            minutes_median = int(numpy.median(all_minutes_dict[key]))
            minutes_mode = stats.mode(all_minutes_dict[key], keepdims=False)[0]
            minutes_min = int(numpy.min(all_minutes_dict[key]))
            minutes_max = int(numpy.max(all_minutes_dict[key]))

            fgm_mean = round(numpy.mean(all_fgms_dict[key]), 1)
            fgm_median = int(numpy.median(all_fgms_dict[key]))
            fgm_mode = stats.mode(all_fgms_dict[key], keepdims=False)[0]
            fgm_min = numpy.min(all_fgms_dict[key])
            fgm_max = numpy.max(all_fgms_dict[key])

            fga_mean = round(numpy.mean(all_fgas_dict[key]), 1)
            fga_median = int(numpy.median(all_fgas_dict[key]))
            fga_mode = stats.mode(all_fgas_dict[key], keepdims=False)[0]
            fga_min = numpy.min(all_fgas_dict[key])
            fga_max = numpy.max(all_fgas_dict[key])

            fg_mean = str(fgm_mean) + "-" + str(fga_mean)
            fg_median = str(fgm_median) + "-" + str(fga_median)
            fg_mode = str(fgm_mode) + "-" + str(fga_mode)
            fg_min = str(fgm_min) + "-" + str(fga_min)
            fg_max = str(fgm_max) + "-" + str(fga_max)

            fg_rate_mean = round(numpy.mean(all_fg_rates_dict[key]), 1)
            fg_rate_median = round(float(numpy.median(all_fg_rates_dict[key])), 1)
            fg_rate_mode = stats.mode(all_fg_rates_dict[key], keepdims=False)[0]
            fg_rate_min = numpy.min(all_fg_rates_dict[key])
            fg_rate_max = numpy.max(all_fg_rates_dict[key])



            threes_made_mean = round(numpy.mean(all_threes_made_dict[key]), 1)
            threes_made_median = int(numpy.median(all_threes_made_dict[key]))
            threes_made_mode = stats.mode(all_threes_made_dict[key], keepdims=False)[0]
            threes_made_min = numpy.min(all_threes_made_dict[key])
            threes_made_max = numpy.max(all_threes_made_dict[key])

            threes_attempts_mean = round(numpy.mean(all_threes_attempts_dict[key]), 1)
            threes_attempts_median = int(numpy.median(all_threes_attempts_dict[key]))
            threes_attempts_mode = stats.mode(all_threes_attempts_dict[key], keepdims=False)[0]
            threes_attempts_min = numpy.min(all_threes_attempts_dict[key])
            threes_attempts_max = numpy.max(all_threes_attempts_dict[key])

            threes_mean = str(threes_made_mean) + "-" + str(threes_attempts_mean)
            threes_median = str(threes_made_median) + "-" + str(threes_attempts_median)
            threes_mode = str(threes_made_mode) + "-" + str(threes_attempts_mode)
            threes_min = str(threes_made_min) + "-" + str(threes_attempts_min)
            threes_max = str(threes_made_max) + "-" + str(threes_attempts_max)

            threes_rate_mean = round(numpy.mean(all_threes_rates_dict[key]), 1)
            threes_rate_median = round(float(numpy.median(all_threes_rates_dict[key])), 1)
            threes_rate_mode = stats.mode(all_threes_rates_dict[key], keepdims=False)[0]
            threes_rate_min = numpy.min(all_threes_rates_dict[key])
            threes_rate_max = numpy.max(all_threes_rates_dict[key])



            ftm_mean = round(numpy.mean(all_ftms_dict[key]), 1)
            ftm_median = int(numpy.median(all_ftms_dict[key]))
            ftm_mode = stats.mode(all_ftms_dict[key], keepdims=False)[0]
            ftm_min = numpy.min(all_ftms_dict[key])
            ftm_max = numpy.max(all_ftms_dict[key])

            fta_mean = round(numpy.mean(all_ftas_dict[key]), 1)
            fta_median = int(numpy.median(all_ftas_dict[key]))
            fta_mode = stats.mode(all_ftas_dict[key], keepdims=False)[0]
            fta_min = numpy.min(all_ftas_dict[key])
            fta_max = numpy.max(all_ftas_dict[key])

            ft_mean = str(ftm_mean) + "-" + str(fta_mean)
            ft_median = str(ftm_median) + "-" + str(fta_median)
            ft_mode = str(ftm_mode) + "-" + str(fta_mode)
            ft_min = str(ftm_min) + "-" + str(fta_min)
            ft_max = str(ftm_max) + "-" + str(fta_max)

            ft_rate_mean = round(numpy.mean(all_ft_rates_dict[key]), 1)
            ft_rate_median = round(float(numpy.median(all_ft_rates_dict[key])), 1)
            ft_rate_mode = stats.mode(all_ft_rates_dict[key], keepdims=False)[0]
            ft_rate_min = numpy.min(all_ft_rates_dict[key])
            ft_rate_max = numpy.max(all_ft_rates_dict[key])



            b_mean = round(numpy.mean(all_bs_dict[key]), 1)
            b_median = int(numpy.median(all_bs_dict[key]))
            b_mode = stats.mode(all_bs_dict[key], keepdims=False)[0]
            b_min = numpy.min(all_bs_dict[key])
            b_max = numpy.max(all_bs_dict[key])

            s_mean = round(numpy.mean(all_ss_dict[key]), 1)
            s_median = int(numpy.median(all_ss_dict[key]))
            s_mode = stats.mode(all_ss_dict[key], keepdims=False)[0]
            s_min = numpy.min(all_ss_dict[key])
            s_max = numpy.max(all_ss_dict[key])

            f_mean = round(numpy.mean(all_fs_dict[key]), 1)
            f_median = int(numpy.median(all_fs_dict[key]))
            f_mode = stats.mode(all_fs_dict[key], keepdims=False)[0]
            f_min = numpy.min(all_fs_dict[key])
            f_max = numpy.max(all_fs_dict[key])

            to_mean = round(numpy.mean(all_tos_dict[key]), 1)
            to_median = int(numpy.median(all_tos_dict[key]))
            to_mode = stats.mode(all_tos_dict[key], keepdims=False)[0]
            to_min = numpy.min(all_tos_dict[key])
            to_max = numpy.max(all_tos_dict[key])

            # p(a|b) = p(b|a)p(a)/p(b)
            # a = player does action, 
            # b = player did action in previous x/y instances, where x is no. times did action and y is no. opportunities to do action
            # eg if player was 3/3, 3/4, 4/5 then the next move he always goes 4/4, 4/5, 5/6 but this is misleading bc must account for external environmental factors

            # output: 
            # 1, 2, 3, ... 30 ... 82 (total games played)
            # 1/1, 2/2, 3/3, ..., 10/30, 30/82
            # mean, median, mode
            # get for all games, just winning games, just losing, just home/away, given opp, given set of circumstances, etc

            #header_row = ["Result"]
            #header_row.append(player_data[0][2:])

            header_row = ['Output', 'Result', 'MIN', 'FG', 'FG%', '3P', '3P%', 'FT', 'FT%', 'REB', 'AST', 'BLK', 'STL', 'PF', 'TO', 'PTS']

        
            
            #output_row = [field_name]
            mean_row = ["Mean", result_mean, minutes_mean, fg_mean, fg_rate_mean, threes_mean, threes_rate_mean, ft_mean, ft_rate_mean, rebs_mean, asts_mean, b_mean, s_mean, f_mean, to_mean, pts_mean]
            median_row = ["Median", result_median, minutes_median, fg_median, fg_rate_median, threes_median, threes_rate_median, ft_median, ft_rate_median, rebs_median, asts_median, b_median, s_median, f_median, to_median, pts_median]
            mode_row = ["Mode", result_mode, minutes_mode, fg_mode, fg_rate_mode, threes_mode, threes_rate_mode, ft_mode, ft_rate_mode, rebs_mode, asts_mode, b_mode, s_mode, f_mode, to_mode, pts_mode]
            min_row = ["Min", result_min, minutes_min, fg_min, fg_rate_min, threes_min, threes_rate_min, ft_min, ft_rate_min, rebs_min, asts_min, b_min, s_min, f_min, to_min, pts_min]
            max_row = ["Max", result_max, minutes_max, fg_max, fg_rate_max, threes_max, threes_rate_max, ft_max, ft_rate_max, rebs_max, asts_max, b_max, s_max, f_max, to_max, pts_max]
            #header_row = ["Output"] + player_data[0][2:]
            output_table = [header_row, mean_row, median_row, mode_row, min_row, max_row]
            print(str(key).title())
            print(tabulate(output_table))

            # header_row = ['Points', 'All Season']
            # mean_row = ['Mean', pts_mean]
            # median_row = ['Median', pts_median]
            # mode_row = ['Mode', pts_mode]
            # output_table = [header_row, mean_row, median_row, mode_row]

            # print("\n===" + player_name + "===\n")
            # print(tabulate(output_table))

            # given how many of recent games we care about
            # later we will take subsection of games with certain settings like home/away
            # first we get all stats and then we can analyze subsections of stats
            # eg last 10 games
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
            for game_idx in range(len(all_pts_dict[key])):
                pts = all_pts_dict[key][game_idx]
                rebs = all_rebs_dict[key][game_idx]
                asts = all_asts_dict[key][game_idx]

                threes = all_threes_made_dict[key][game_idx]
                blks = all_bs_dict[key][game_idx]
                stls = all_ss_dict[key][game_idx]
                tos = all_tos_dict[key][game_idx]

                if pts >= int(pts_lines[player_idx]):
                    pts_count += 1
                if rebs >= int(r_lines[player_idx]):
                    r_count += 1
                if asts >= int(a_lines[player_idx]):
                    a_count += 1

                if threes >= int(threes_lines[player_idx]):
                    threes_count += 1
                if blks >= int(b_lines[player_idx]):
                    b_count += 1
                if stls >= int(s_lines[player_idx]):
                    s_count += 1
                if tos >= int(to_lines[player_idx]):
                    to_count += 1

                all_pts_counts.append(pts_count)
                all_rebs_counts.append(r_count)
                all_asts_counts.append(a_count)

                all_threes_counts.append(threes_count)
                all_blks_counts.append(b_count)
                all_stls_counts.append(s_count)
                all_tos_counts.append(to_count)

            # make stats counts to find consistent streaks
            all_stats_counts_dict[key] = [ all_pts_counts, all_rebs_counts, all_asts_counts, all_threes_counts, all_blks_counts, all_stls_counts, all_tos_counts ]

            stats_counts = [ all_pts_counts, all_rebs_counts, all_asts_counts, all_threes_counts, all_blks_counts, all_stls_counts, all_tos_counts ]

            header_row = ['Games']
            over_pts_line = 'PTS ' + str(pts_lines[player_idx]) + "+"
            over_rebs_line = 'REB ' + str(r_lines[player_idx]) + "+"
            over_asts_line = 'AST ' + str(a_lines[player_idx]) + "+"
            
            over_threes_line = '3PM ' + str(threes_lines[player_idx]) + "+"
            over_blks_line = 'BLK ' + str(b_lines[player_idx]) + "+"
            over_stls_line = 'STL ' + str(s_lines[player_idx]) + "+"
            over_tos_line = 'TO ' + str(to_lines[player_idx]) + "+"
            
            prob_pts_row = [over_pts_line]
            prob_rebs_row = [over_rebs_line]
            prob_asts_row = [over_asts_line]

            prob_threes_row = [over_threes_line]
            prob_blks_row = [over_blks_line]
            prob_stls_row = [over_stls_line]
            prob_tos_row = [over_tos_line]

            for game_idx in range(len(all_pts_dict[key])):
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


            

            #total = str(len(all_pts))
            #probability_over_line = str(count) + "/" + total
            #total_games = total + " Games"
            #header_row = ['Points', total_games]
            #print(probability_over_line)

            #prob_row = [over_line, probability_over_line]

            print("\n===" + player_name + "===\n")

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
                    if player_name in all_streak_tables.keys():
                        player_streak_tables = all_streak_tables[player_name]
                        if key in player_streak_tables.keys():
                            player_streak_tables[key].append(prob_table) # append all stats for given key
                        else:
                            player_streak_tables[key] = [prob_table]
                    else:
                        all_streak_tables[player_name] = {}
                        player_streak_tables = all_streak_tables[player_name]
                        player_streak_tables[key] = [prob_table]

                    # if key in player_streak_tables.keys():
                    #     player_streak_tables[key].append(prob_table) # append all stats for given key
                    # else:
                    #     player_streak_tables[key] = [prob_table]
    

# get matchup data before looping thru consistent streaks bc we will present matchup data alongside consistent streaks for comparison
fantasy_pros_url = 'https://www.fantasypros.com/daily-fantasy/nba/fanduel-defense-vs-position.php' #'https://www.fantasypros.com/nba/defense-vs-position.php' #alt 2: betting_pros_url = 'https://www.bettingpros.com/nba/defense-vs-position/'
hashtag_bball_url = 'https://hashtagbasketball.com/nba-defense-vs-position'
swish_analytics_url = 'https://swishanalytics.com/optimus/nba/daily-fantasy-team-defensive-ranks-position'
draft_edge_url = 'https://draftedge.com/nba-defense-vs-position/'


# get matchup data for streaks to see if likely to continue streak
matchup_data_sources = [hashtag_bball_url] #, hashtag_bball_url, swish_analytics_url, betting_pros_url, draft_edge_url] # go thru each source so we can compare conflicts
# first read all matchup data from internet and then loop through tables
all_matchup_data = reader.read_all_matchup_data(matchup_data_sources)


# display streak tables separately
#streaks = isolator.isolate_consistent_streaks(all_stats_counts_dict)
print("\n===Consistent Streaks===\n")
for p_name, p_streak_tables in all_streak_tables.items():
    print("\n===" + p_name + "===\n")
    for key, streak_tables in p_streak_tables.items():
        player_lines = projected_lines_dict[p_name]
        #print("player_lines: " + str(player_lines))

        opponent = player_lines['OPP'].lower()

        if str(key) == 'all' or str(key) == player_lines['LOC'].lower() or str(key) == opponent: # current conditions we are interested in
            print(str(key).title())
            
            print(tabulate(streak_tables))

            # determine matchup for opponent and stat. we need to see all position matchups to see relative ease
            # display matchup tables with consistent streaks (later look at easiest matchups for all current games, not just consistent streaks bc we may find an exploit)
            
            #print("streak_tables: " + str(streak_tables))
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

                    #source_matchup_ratings={ source1: {position:'', average:'', rank:''}, source2...}
                    avg_source_matchup_ratings = {} # so we can sort by average rank
                    source_matchup_ratings = {}


                    print(tabulate(matchup_table))

