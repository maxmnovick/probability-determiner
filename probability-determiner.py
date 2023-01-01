# game-outcome-predictor.py
# not only determine weights of most important (non-negligible) factors
# but also determine degree of belief of outcome

from tabulate import tabulate

import reader # read game data
import isolator # isolate games


# record data from game
# given set of seemingly important factors contributing to outcome, determine values for each of these factors
# each time an important event occurs, we know it is important because it falls under a given category, such as bad shot selection
# record data for team 1
# each time an event occurs, we add a level of severity to the array
# see predication-data sheet
team1_turnovers = [0.5, 0.5, 0.5] # 1 = turnovers that lead to layups
team1_bad_shots = [1, 0.5, 0.5] # 1 = heavily guarded out of rhythm far away
team1_missed_layups = [0.5] # 1 = wide open layup
team1_allowed_layups = [] # 1 = wide open layup
team1_data = [team1_turnovers, team1_bad_shots, team1_missed_layups, team1_allowed_layups]

# record data for team 2
team2_turnovers = [0.5] # 1 = turnovers that lead to layups
team2_bad_shots = [0.5, 0.5, 1, 0.5, 0.5, 0.5] # 1 = heavily guarded out of rhythm far away
team2_missed_layups = [] # 1 = wide open layup
team2_allowed_layups = [] # 1 = wide open layup
team2_data = [team2_turnovers, team2_bad_shots, team2_missed_layups, team2_allowed_layups]

all_team_data = [team1_data, team2_data]


# win advantage is the difference in win rate 
# combined with the win rate weight, based on the significance of the win records by sample size
def determine_win_advantage(current_game, all_games):

    print("\n===Determine Win Advantage===\n")

    team1_win_qty = 19
    team1_loss_qty = 17
    team1_total_game_qty = team1_win_qty + team1_loss_qty
    team1_win_rate = team1_win_qty / ( team1_total_game_qty )

    team2_win_qty = 19
    team2_loss_qty = 17
    team2_total_game_qty = team2_win_qty + team2_loss_qty
    team2_win_rate = team2_win_qty / ( team2_total_game_qty )

    win_advantage = team1_win_rate - team2_win_rate

    # what is the conclusion from win advantage? 
    # identical records
    if win_advantage == 0:
        print("Identical Records")
        qty_identical_records = 2 # read from raw data # qty of games played with 2 teams having identical win records
        print("No. Games Sampled with Identical Records: " + str(qty_identical_records))
        game1 = { 'final_team1_score':110, 'final_team2_score':113, 'q1_team1_score':31, 'q1_team2_score':33 }
        game2 = { 'final_team1_score':105, 'final_team2_score':108, 'q1_team1_score':25, 'q1_team2_score':18 }
        games_with_identical_records = [ game1, game2 ] # game data needed to make conclusions such as final score
        final_score_margins = []
        q1_score_margins = []
        print("In games with identical records, we have seen the following:")
        for game in games_with_identical_records:
            print("\nGame: ")

            q1_team1_score = game['q1_team1_score']
            q1_team2_score = game['q1_team2_score']
            q1_score_margin = q1_team1_score - q1_team2_score
            #print("-Q1 score margin: " + str(q1_score_margin))
            row1 = ['Q1 Score Margin', q1_score_margin]
            q1_score_margins.append(q1_score_margin)

            

            final_team1_score = game['final_team1_score']
            final_team2_score = game['final_team2_score']
            final_score_margin = final_team1_score - final_team2_score
            #print("-Final score margin: " + str(final_score_margin))
            row2 = ['Final Score Margin', final_score_margin]
            final_score_margins.append(final_score_margin)
            
            table = [row1, row2]
            print(tabulate(table))
            
        headers = ['Q1 Score Margin', 'Final Score Margin']
        table = [headers]
        for game_idx in range(len(q1_score_margins)):
            q1_score_margin = q1_score_margins[game_idx]
            final_score_margin = final_score_margins[game_idx]
            row = [q1_score_margin, final_score_margin]
            table.append(row)

        print(tabulate(table))
            

        # extremely likely to be win margin 1-10

        # check q1 score margin as well to see if much different than others
    # very close records
    elif win_advantage < 2:
        print("Very Close Records")
        # extremely likely to be win margin 1-10
    # close records
    elif win_advantage < 5:
        print("Significantly Close Records")
        # extremely likely to be win margin 1-10
    # somewhat close records
    elif win_advantage < 15:
        print("Somewhat Close Records")
    # somewhat significantly different records
    elif win_advantage < 25:
        print("Somewhat Different Records")
    # significantly different records
    elif win_advantage < 50:
        print("Significantly Different Records")
    # else very significantly different records
    else:
        print("Very Different Records")

    return win_advantage


# win rate weight based on sample size
# the more samples, the more stable and therefore the more weight it is given in predicting winner 
def determine_win_rate_weight():
    print("\n===Determine Win Rate Weight===\n")

# features are important factors, unweighted
# eg features = [turnovers, bad shots, missed layups]
# eg counts = [1,1,1]
# arranged as arrays for compute efficiency of large data
# event type may be needed to weigh factors
def determine_probability(event_info):
    print("\n===Determine Probability===\n")

    probabilities = []
    probability = 0 #0-1

    data_type = "game data"
    input_type = "all games"
    raw_data = reader.extract_data(data_type, input_type)
    all_games = isolator.isolate_games(raw_data)

    # team1_info = { 'mistake_score': 1, 'wins': 1, 'losses': 1, 'q1_score': 1, 'final_score': 1 }
    # team2_info = { 'mistake_score': 1, 'wins': 1, 'losses': 1, 'q1_score': 1, 'final_score': 1 }
    # current_game = [team1_info, team2_info] switched to param event info bc this is user input to fcn
    
    win_advantage = determine_win_advantage(event_info, all_games)

    # take feature data collected from sample
    feature_data = [] #[team1_feature_data, etc.]

    # compare teams scores
    mistake_scores = [] # [6.0, 8.5]
    win_records = [] # ['16-17', '16-17']
    current_score = [] # [33, 30]

    # weigh importance of scores to determine final score
    # degree of belief of outcome


    for team_idx in range(len(event_info)):
        team = event_info[team_idx]
        team_name = team['name']
        print("\nTeam 1: " + team_name)
        # p(a|b) = (p(b|a)p(a))/p(b) # a=team1 wins, b=team1 mistake score less than that of team2
        # prob that team1 mistake score less than that of team2 given team1 wins. look at winning teams mistake score and see rate of less. then can narrow down to teams with similar records for more accuracy. 
        p_of_b_given_a = 0.8 # winning team should have less mistake score most often almost 95% of the time if calculated correctly
        wins = team['wins']
        losses = team['losses']
        p_a = wins / ( wins + losses) #0.6 # prob that team1 wins, based on record. narrow down to prob that team1 wins against teams with this win record?
        # determine p_b by seeing teams with similar win rates and mistake scores, not just the current team in question
        p_b = p_a # prob that team1 mistake score is less than their opponents, no matter if win or loss. should mostly align with their wins if mistake score computed correctly. 

        # if team 1 mistake score is significantly x higher than team 2's and all other factors are equal, 
        # then team 1 will lose by a significant y margin
        signicant_mistake_differential = 5 # based on absolute value of average mistake score
        team1_mistake_score = team['mistake_score']
        print("team1_mistake_score: " + str(team1_mistake_score))
        for opponent_idx in range(len(event_info)):
            if opponent_idx != team_idx:
                opponent = event_info[opponent_idx]
                opponent_name = opponent['name']
                print("Team 2: " + opponent_name)
                team2_mistake_score = opponent['mistake_score']
                print("team2_mistake_score: " + str(team2_mistake_score))
                mistake_difference = team1_mistake_score - team2_mistake_score
                print("mistake_difference: " + str(mistake_difference))
                # team1 mistake much more than team2 so team1 loses
                if mistake_difference > signicant_mistake_differential: # significant difference in no. mistakes
                    print("team1 made much more mistakes")
                    min_final_score_differential = 11 # points
                    outcome = 'Team 1 will lose by ' + str(min_final_score_differential) + '+ points. '

                    p_of_b_given_a = 0.2 # winning team should have less mistake score most often almost 95% of the time if calculated correctly
                    # if big difference in mistake scores, 80% chance team with less mistakes wins
                    probability = p_of_b_given_a * p_a / p_b #0.8 # p(a|b) = (p(b|a)p(a))/p(b) # a=team1 wins, b=team1 mistake score less than that of team2
                    
                # team1 mistake much less than team2 so team1 wins
                elif mistake_difference < -signicant_mistake_differential:
                    print("team1 made much less mistakes")
                    min_final_score_differential = 11 # points
                    outcome = 'Team 1 will win by ' + str(min_final_score_differential) + '+ points. '

                    p_of_b_given_a = 0.8 # winning team should have less mistake score most often almost 95% of the time if calculated correctly
                    # if big difference in mistake scores, 80% chance team with less mistakes wins
                    probability = p_of_b_given_a * p_a / p_b #0.8 # p(a|b) = (p(b|a)p(a))/p(b) # a=team1 wins, b=team1 mistake score less than that of team2
                    
                elif mistake_difference == 0:
                    probability = 0.5
                else:
                    probability = 0.5

                #print("probability: " + str(probability))
                print("Chance " + team_name + " Wins: " + str(int(probability * 100)) + "%")
                probabilities.append(probability)


    return probabilities




#features = [mistake_scores, win_advantage, point_advantage]

team1_info = { 'name':'CHI', 'mistake_score': 17, 'wins': 1, 'losses': 1, 'q1_score': 1, 'final_score': 1 }
team2_info = { 'name':'NOP', 'mistake_score': 1, 'wins': 1, 'losses': 1, 'q1_score': 1, 'final_score': 1 }
event_info = [team1_info, team2_info]

outcome = determine_probability(event_info)



