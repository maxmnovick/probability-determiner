# read a team's schedule or player's game log
# then see the box score of each game played
# then list all active players in the game on both teams (for and aginst given player of interest)

import reader, determiner

import pandas as pd # read html results from webpage
from urllib.request import Request, urlopen # request website, open webpage given req
from bs4 import BeautifulSoup # read html from webpage


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
player_teams = reader.read_all_players_teams(player_espn_ids_dict)

# find teammates and opponents for each game played by each player
def read_all_players_in_games(all_player_season_logs_dict, player_teams):

    print('\n===Read All Players in Games===\n')

    all_players_in_games_dict = {} # {player:{game:{teammates:[],opponents:[]}}}

    season_year = 2023

    for player_name, player_season_logs in all_player_season_logs_dict.items():

        print('player_name: ' + player_name)

        team_abbrev = player_teams[player_name]
        print('team_abbrev: ' + team_abbrev)

        for player_season_log in player_season_logs:

            player_reg_season_log = determiner.determine_regular_season_games(player_season_log)

            for game_idx, row in player_reg_season_log.iterrows():
                
                print('\n===Game ' + str(game_idx) + '===')
                date = player_reg_season_log.loc[game_idx, 'Date'] + '/' + str(season_year)
                print('date: ' + date)
                opp_abbrev = player_reg_season_log.loc[game_idx, 'OPP']
                print('opp_abbrev: ' + opp_abbrev)
                

                game_espn_id = reader.read_game_espn_id(date, opp_abbrev, team_abbrev)




            season_year -= 1

    return all_players_in_games_dict

all_players_in_games_dict = read_all_players_in_games(all_player_season_logs_dict, player_teams)


# player_url = 'https://www.espn.com/nba/player/gamelog/_/id/3908845/john-collins'
# html_results = pd.read_html(player_url)
# print("html_results: " + str(html_results))


# req = Request(player_url, headers={
#     'User-Agent': 'Mozilla/5.0',
# })

# page = urlopen(req) # open webpage given request

# soup = BeautifulSoup(page, features="lxml")
# print('soup: ' + str(soup))