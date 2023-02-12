# isolator.py
# isolate data elements of the same type or with matching features
# eg isolate one game from all games and isolate all games with certain scores

import re
from tabulate import tabulate # display output

def isolate_games(raw_data):
    print("\n===Isolate Games===\n")
    print("raw_data: " + str(raw_data))
    all_games = []
    game = []
    existing_game = False
    for line in raw_data:
        print("line: " + str(line))
        # if first element has game label or date consider it a new game
        if line[0] == 'Game' or re.search('/',line[0]): # we tell date by slash (/)
            print("New Game")
            existing_game = True
            # new game
            if len(game) != 0: # if no game data yet, do not add game to all games until adding lines to game
                all_games.append(game)
            game = [line]

        # continue to append lines to the current game until we encounter another game or date label
        if existing_game == True:
            game.append(line)

    print("all_games: " + str(all_games))
    return all_games


# game data has headers and each month is separated by monthly averages
# which happen to be differentiated by uppercase letters
def isolate_player_game_data(player_data, player_name=''):
    player_game_data = []

    if len(player_data) > 0:
        for row in player_data:
            if not row[0].isupper():
                player_game_data.append(row)

        # display player game data in formatted table for observation
        #print("player_game_data: " + str(player_game_data))

        header_row = player_data[0]

        table = [header_row]
        for row in player_game_data:
            table.append(row)

        print("\n===" + player_name + "===\n")
        print(tabulate(table))
    else:
        print("Warning: No Player Data from file.")

    return player_game_data