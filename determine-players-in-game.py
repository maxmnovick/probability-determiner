# read a team's schedule or player's game log
# then see the box score of each game played
# then list all active players in the game on both teams (for and aginst given player of interest)

import reader, determiner

import pandas as pd # read html results from webpage
from urllib.request import Request, urlopen # request website, open webpage given req
from bs4 import BeautifulSoup # read html from webpage

import re # search opp string in game log to see if home or away

# ===read a team's schedule
# we need to see how a given player performs with given teammates and opponent players, specifically the individuals for and against a given player, not just the team as a whole bc the team consists of individuals that determine matchups
# also check the affect of individuals for and against a given player bc not enough samples with exact lineups but many samples against individuals
# we already have a given players game log so we can see games played bc we only need matchups for the given player

# def read_team_schedule(team_abbrev):

#     print('\n===Read Team Schedule===\n')

player_names = ['naji marshall']

player_espn_ids_dict = reader.read_all_player_espn_ids(player_names)

# read game logs
read_all_seasons = False # saves time during testing other parts if we only read 1 season
all_player_season_logs_dict = reader.read_all_players_season_logs(player_names, read_all_seasons, player_espn_ids_dict)


# read teams so we can find game id by team opp and date
player_teams = reader.read_all_players_teams(player_espn_ids_dict, read_new_teams=False)

# find teammates and opponents for each game played by each player
# all_players_in_games_dict = {player:{game:{teammates:[],opponents:[]}}}
def read_all_players_in_games(all_player_season_logs_dict, player_teams):

    print('\n===Read All Players in Games===\n')

    all_players_in_games_dict = {} # {player:{game:{teammates:[],opponents:[]}}}

    season_year = 2023

    for player_name, player_season_logs in all_player_season_logs_dict.items():

        print('player_name: ' + player_name)

        team_abbrev = player_teams[player_name]
        print('team_abbrev: ' + team_abbrev)

        
        # see if game id saved in file
        # check for each player bc we add new games for each player and they may overlap
        data_type = 'game ids'
        game_ids = reader.extract_data(data_type, header=True)
        existing_game_ids_dict = {}
        for row in game_ids:
            print('row: ' + str(row))
            game_key = row[0]
            game_id = row[1]

            existing_game_ids_dict[game_key] = game_id
        print('existing_game_ids_dict: ' + str(existing_game_ids_dict))
        
        
        
        
        for player_season_log in player_season_logs:

            player_reg_season_log = determiner.determine_regular_season_games(player_season_log)

            players_in_game = [] # unordered list of all players in game independent of team
            players_in_game_dict = {} # {teammates:[],opponents:[]}
            
            for game_idx, row in player_reg_season_log.iterrows():
                
                print('\n===Game ' + str(game_idx) + '===')
                # season year-1 for first half of season oct-dec bc we say season year is end of season
                init_game_date_string = player_reg_season_log.loc[game_idx, 'Date'].lower().split()[1] # 'wed 2/15'[1]='2/15'
                game_mth = init_game_date_string.split('/')[0]
                final_season_year = str(season_year)
                if int(game_mth) in range(10,13):
                    final_season_year = str(season_year - 1)

                date_str = player_reg_season_log.loc[game_idx, 'Date'] + '/' + str(final_season_year) # dow m/d/y
                date_data = date_str.split()
                date = date_data[1] # m/d/y
                print('date: ' + date)
                opp_str = player_reg_season_log.loc[game_idx, 'OPP'].lower()
                opp_abbrev = re.sub('@|vs','',opp_str)
                print('opp_abbrev: ' + opp_abbrev)

                # if we always use format 'away home m/d/y' then we can check to see if key exists and get game id from local file
                away_abbrev = opp_abbrev
                home_abbrev = team_abbrev
                player_loc = 'home' # for box score players in game sort by teammates
                if re.search('@',opp_str):
                    away_abbrev = team_abbrev
                    home_abbrev = opp_abbrev
                    player_loc = 'away'

                
                game_key = away_abbrev + ' ' + home_abbrev + ' ' + date
                print('game_key: ' + game_key)
                
                game_espn_id = reader.read_game_espn_id(game_key, existing_game_ids_dict)


                # get the game box score page using the game id
                # get the box score from the page in a df
                game_box_scores_dict = reader.read_game_box_scores(game_key, game_espn_id)

                # given box scores for each team, return lists of teammates and opponents
                players_in_box_score_dict = reader.read_players_in_box_score(game_box_scores_dict)
                players_in_game_dict = {'teammates':[],'opponents':[]}
                for team_loc, players in players_in_box_score_dict.items():
                    # if player is away set teammates as such
                    if team_loc == player_loc:
                        players_in_game_dict['teammates'] = players
                    else:
                        players_in_game_dict['opponents'] = players
                
                # opp_loc = 'away'
                # players_in_game_dict['teammates'] = players_in_box_score_dict[player_loc]
                # players_in_game_dict['opponents'] = players_in_box_score_dict[opp_loc]
                # if player_loc == 'away':
                #     opp_loc = 'home'
                #     players_in_game_dict['opponents'] = players_in_box_score_dict[opp_loc]

                print('players_in_game_dict: ' + str(players_in_game_dict))

                if not player_name in all_players_in_games_dict.keys():
                    all_players_in_games_dict[player_name] = {}
                all_players_in_games_dict[player_name][game_key] = players_in_game_dict


                # test first game
                if game_idx == 0:
                    break
                



            season_year -= 1

    print('all_players_in_games_dict: ' + str(all_players_in_games_dict))
    return all_players_in_games_dict

all_players_in_games_dict = read_all_players_in_games(all_player_season_logs_dict, player_teams)
