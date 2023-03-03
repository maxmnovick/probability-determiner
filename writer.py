#writer.py
# display data

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


    #print(tabulate(game_data))

    print("Export")
    print(header_string)
    for game_data in game_data_strings:
        print(game_data)