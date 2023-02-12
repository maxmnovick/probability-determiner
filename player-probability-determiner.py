# player-probability-determiner.py
# determine the probability that a player will perform an action

import reader # input data
import numpy # mean, median
import scipy
from scipy import stats # calculate mode
from tabulate import tabulate # display output
import isolator # isolate player game data which exludes headers and monthly averages
import re # split result data into score data

# input: game log
# player name
# date, opponent, result, min, fg, fg%, 3pt, 3p%, ft, ft%, reb, ast, blk, stl, pf, to, pts

data_type = 'Player Data'
player_name = 'Jalen Brunson'
# count no. times player hit over line
pts_line = 11
r_line = 6
a_line = 6
print("\n===" + player_name + "===\n")
#row1 = ['Tue 2/7','vs OKC','L 133-130', '34','13-20','65.0','4-6','66.7','8-10','80.0','7','3','0','3','3','4','38']

all_player_game_logs = []


player_names = [player_name]
for p_name in player_names:

    player_game_log = reader.read_player_game_log(p_name) # player url includes year at this point

    all_player_game_logs.append(player_game_log) # could continue to process in this loop or save all player game logs to process in next loop


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

player_game_log = all_player_game_logs[0]
if len(player_game_log) > 0:
    print("player_game_log:\n" + str(player_game_log))
    # we pulled game log from internet
    for game_idx, row in player_game_log.iterrows():
        #game = player_game_log[game_idx, row]
        #print("game:\n" + str(game))
        #print("player_game_log.loc[game_idx, 'Type']: " + player_game_log.loc[game_idx, 'Type'])

        if player_game_log.loc[game_idx, 'Type'] == 'Regular':

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

    pts_mean = round(numpy.mean(all_pts), 1)
    pts_median = int(numpy.median(all_pts))
    pts_mode = stats.mode(all_pts, keepdims=False)[0]
    pts_min = numpy.min(all_pts)
    pts_max = numpy.max(all_pts)

    rebs_mean = round(numpy.mean(all_rebs), 1)
    rebs_median = int(numpy.median(all_rebs))
    rebs_mode = stats.mode(all_rebs, keepdims=False)[0]
    rebs_min = numpy.min(all_rebs)
    rebs_max = numpy.max(all_rebs)

    asts_mean = round(numpy.mean(all_asts), 1)
    asts_median = int(numpy.median(all_asts))
    asts_mode = stats.mode(all_asts, keepdims=False)[0]
    asts_min = numpy.min(all_asts)
    asts_max = numpy.max(all_asts)


    winning_score_mean = round(numpy.mean(all_winning_scores), 1)
    winning_score_median = int(numpy.median(all_winning_scores))
    winning_score_mode = stats.mode(all_winning_scores, keepdims=False)[0]
    winning_score_min = int(numpy.min(all_winning_scores))
    winning_score_max = int(numpy.max(all_winning_scores))

    losing_score_mean = round(numpy.mean(all_losing_scores), 1)
    losing_score_median = int(numpy.median(all_losing_scores))
    losing_score_mode = stats.mode(all_losing_scores, keepdims=False)[0]
    losing_score_min = int(numpy.min(all_losing_scores))
    losing_score_max = int(numpy.max(all_losing_scores))

    result_mean = str(winning_score_mean) + "-" + str(losing_score_mean)
    result_median = str(winning_score_median) + "-" + str(losing_score_median)
    result_mode = str(winning_score_mode) + "-" + str(losing_score_mode)
    result_min = str(winning_score_min) + "-" + str(losing_score_min)
    result_max = str(winning_score_max) + "-" + str(losing_score_max)


    minutes_mean = round(numpy.mean(all_minutes), 1)
    minutes_median = int(numpy.median(all_minutes))
    minutes_mode = stats.mode(all_minutes, keepdims=False)[0]
    minutes_min = int(numpy.min(all_minutes))
    minutes_max = int(numpy.max(all_minutes))

    fgm_mean = round(numpy.mean(all_fgms), 1)
    fgm_median = int(numpy.median(all_fgms))
    fgm_mode = stats.mode(all_fgms, keepdims=False)[0]
    fgm_min = numpy.min(all_fgms)
    fgm_max = numpy.max(all_fgms)

    fga_mean = round(numpy.mean(all_fgas), 1)
    fga_median = int(numpy.median(all_fgas))
    fga_mode = stats.mode(all_fgas, keepdims=False)[0]
    fga_min = numpy.min(all_fgas)
    fga_max = numpy.max(all_fgas)

    fg_mean = str(fgm_mean) + "-" + str(fga_mean)
    fg_median = str(fgm_median) + "-" + str(fga_median)
    fg_mode = str(fgm_mode) + "-" + str(fga_mode)
    fg_min = str(fgm_min) + "-" + str(fga_min)
    fg_max = str(fgm_max) + "-" + str(fga_max)

    fg_rate_mean = round(numpy.mean(all_fg_rates), 1)
    fg_rate_median = round(float(numpy.median(all_fg_rates)), 1)
    fg_rate_mode = stats.mode(all_fg_rates, keepdims=False)[0]
    fg_rate_min = numpy.min(all_fg_rates)
    fg_rate_max = numpy.max(all_fg_rates)



    threes_made_mean = round(numpy.mean(all_threes_made), 1)
    threes_made_median = int(numpy.median(all_threes_made))
    threes_made_mode = stats.mode(all_threes_made, keepdims=False)[0]
    threes_made_min = numpy.min(all_threes_made)
    threes_made_max = numpy.max(all_threes_made)

    threes_attempts_mean = round(numpy.mean(all_threes_attempts), 1)
    threes_attempts_median = int(numpy.median(all_threes_attempts))
    threes_attempts_mode = stats.mode(all_threes_attempts, keepdims=False)[0]
    threes_attempts_min = numpy.min(all_threes_attempts)
    threes_attempts_max = numpy.max(all_threes_attempts)

    threes_mean = str(threes_made_mean) + "-" + str(threes_attempts_mean)
    threes_median = str(threes_made_median) + "-" + str(threes_attempts_median)
    threes_mode = str(threes_made_mode) + "-" + str(threes_attempts_mode)
    threes_min = str(threes_made_min) + "-" + str(threes_attempts_min)
    threes_max = str(threes_made_max) + "-" + str(threes_attempts_max)

    threes_rate_mean = round(numpy.mean(all_three_rates), 1)
    threes_rate_median = round(float(numpy.median(all_three_rates)), 1)
    threes_rate_mode = stats.mode(all_three_rates, keepdims=False)[0]
    threes_rate_min = numpy.min(all_three_rates)
    threes_rate_max = numpy.max(all_three_rates)



    ftm_mean = round(numpy.mean(all_ftms), 1)
    ftm_median = int(numpy.median(all_ftms))
    ftm_mode = stats.mode(all_ftms, keepdims=False)[0]
    ftm_min = numpy.min(all_ftms)
    ftm_max = numpy.max(all_ftms)

    fta_mean = round(numpy.mean(all_ftas), 1)
    fta_median = int(numpy.median(all_ftas))
    fta_mode = stats.mode(all_ftas, keepdims=False)[0]
    fta_min = numpy.min(all_ftas)
    fta_max = numpy.max(all_ftas)

    ft_mean = str(ftm_mean) + "-" + str(fta_mean)
    ft_median = str(ftm_median) + "-" + str(fta_median)
    ft_mode = str(ftm_mode) + "-" + str(fta_mode)
    ft_min = str(ftm_min) + "-" + str(fta_min)
    ft_max = str(ftm_max) + "-" + str(fta_max)

    ft_rate_mean = round(numpy.mean(all_ft_rates), 1)
    ft_rate_median = round(float(numpy.median(all_ft_rates)), 1)
    ft_rate_mode = stats.mode(all_ft_rates, keepdims=False)[0]
    ft_rate_min = numpy.min(all_ft_rates)
    ft_rate_max = numpy.max(all_ft_rates)



    b_mean = round(numpy.mean(all_bs), 1)
    b_median = int(numpy.median(all_bs))
    b_mode = stats.mode(all_bs, keepdims=False)[0]
    b_min = numpy.min(all_bs)
    b_max = numpy.max(all_bs)

    s_mean = round(numpy.mean(all_ss), 1)
    s_median = int(numpy.median(all_ss))
    s_mode = stats.mode(all_ss, keepdims=False)[0]
    s_min = numpy.min(all_ss)
    s_max = numpy.max(all_ss)

    f_mean = round(numpy.mean(all_fs), 1)
    f_median = int(numpy.median(all_fs))
    f_mode = stats.mode(all_fs, keepdims=False)[0]
    f_min = numpy.min(all_fs)
    f_max = numpy.max(all_fs)

    to_mean = round(numpy.mean(all_tos), 1)
    to_median = int(numpy.median(all_tos))
    to_mode = stats.mode(all_tos, keepdims=False)[0]
    to_min = numpy.min(all_tos)
    to_max = numpy.max(all_tos)

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
    print(tabulate(output_table))

    # header_row = ['Points', 'All Season']
    # mean_row = ['Mean', pts_mean]
    # median_row = ['Median', pts_median]
    # mode_row = ['Mode', pts_mode]
    # output_table = [header_row, mean_row, median_row, mode_row]

    # print("\n===" + player_name + "===\n")
    # print(tabulate(output_table))

    

    pts_count = 0
    r_count = 0
    a_count = 0
    all_pts_counts = []
    all_rebs_counts = []
    all_asts_counts = []
    for game_idx in range(len(all_pts)):
        pts = all_pts[game_idx]
        rebs = all_rebs[game_idx]
        asts = all_asts[game_idx]

        if pts >= pts_line:
            pts_count += 1
        if rebs >= r_line:
            r_count += 1
        if asts >= a_line:
            a_count += 1

        all_pts_counts.append(pts_count)
        all_rebs_counts.append(r_count)
        all_asts_counts.append(a_count)

    header_row = ['Games']
    over_pts_line = 'Points ' + str(pts_line) + "+"
    over_rebs_line = 'Rebounds ' + str(r_line) + "+"
    over_asts_line = 'Assists ' + str(a_line) + "+"
    prob_pts_row = [over_pts_line]
    prob_rebs_row = [over_rebs_line]
    prob_asts_row = [over_asts_line]
    for game_idx in range(len(all_pts)):
        p_count = all_pts_counts[game_idx]
        r_count = all_rebs_counts[game_idx]
        a_count = all_asts_counts[game_idx]

        current_total = str(game_idx + 1)
        current_total_games = current_total# + ' Games'
        header_row.append(current_total_games)

        prob_over_pts_line = str(p_count) + "/" + current_total
        prob_pts_row.append(prob_over_pts_line)
        prob_over_rebs_line = str(r_count) + "/" + current_total
        prob_rebs_row.append(prob_over_rebs_line)
        prob_over_asts_line = str(a_count) + "/" + current_total
        prob_asts_row.append(prob_over_asts_line)

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

    
