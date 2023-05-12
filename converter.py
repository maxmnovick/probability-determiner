# converter.py

def convert_dict_to_list(dict):

    dict_list = []

    for val in dict.values():

        dict_list.append(val)

    return dict_list


def convert_dicts_to_lists(all_consistent_stat_dicts):

    dict_lists = []

    for dict in all_consistent_stat_dicts:

        dict_list = convert_dict_to_list(dict)

        dict_lists.append(dict_list)
        
    return dict_lists