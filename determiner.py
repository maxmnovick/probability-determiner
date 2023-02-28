# determiner.py
# determine conditions 
# eg if streak is considered consistent

import re # see if keyword in column name
import reader # format stat val

from datetime import datetime # convert date str to date so we can see if games 1 day apart and how many games apart

import requests # check if webpage exists while we are looping through player game log seasons until we cannot find game log for that year (note rare players may take a year off and come back but for now assume consistent years)
# request not working by checking status code 200 so test httplib2
import httplib2

import pandas as pd # read html results from webpage to determine if player played season

# if streak resembles pattern we have seen consistently such as 3/3,3/4,4/5,5/6,6/7,6/9,7/10
def determine_consistent_streak(stat_counts):
    print("\n===Determine Consistent Streak===\n")
    print("stat_counts: " + str(stat_counts))
    consistent = False

    # even if it is consistent it does not mean they will hit it next game
    # instead we must determine if likely to hit next game based on previous game pattern
    if len(stat_counts) >= 10:
        if stat_counts[9] >= 7: # arbitrary 7/10
            consistent = True
        elif stat_counts[9] <= 3: # arbitrary 7/10
            consistent = True
    elif len(stat_counts) >= 7: # 5 <= x <= 10
        if stat_counts[6] <= 1 or stat_counts[6] >= 6: # arbitrary 1/7 or 6/7
            consistent = True
    elif len(stat_counts) == 4: # x=4
        if stat_counts[3] == 4 or stat_counts[3] == 0: # arbitrary 4/4 or 0/4. if only 4 samples for the whole season and both are same then check other seasons for extended streak
            consistent = True
    elif len(stat_counts) == 3: # x=3
        if stat_counts[2] == 3 or stat_counts[2] == 0: # arbitrary 3/3. if only 3 samples for the whole season and both are same then check other seasons for extended streak
            consistent = True
    elif len(stat_counts) == 2: # x=2
        if stat_counts[1] == 2 or stat_counts[1] == 0: # arbitrary 2/2. if only 2 samples for the whole season and both are same then check other seasons for extended streak
            consistent = True

    if consistent:
        print('consistent')

    return consistent

def determine_col_name(keyword,data):
    #print("\n===Determine Column Name===\n")

    final_col_name = '' # eg PTS or Sort: PTS
    for col_name in data.columns:
        if re.search(keyword.lower(),col_name.lower()):
            final_col_name = col_name
            break

    #print("final_col_name: " + final_col_name)
    return final_col_name

def determine_team_abbrev(team_name, team_abbrevs_dict={}):
    #print("\n===Determine Team Abbrev===\n")
    team_abbrevs_dict = {'atl':'atlanta hawks', 
                    'bos':'boston celtics', 
                    'bkn':'brooklyn nets', 
                    'cha':'charlotte hornets', 
                    'chi':'chicago bulls',
                    'cle':'cleveland cavaliers',
                    'dal':'dallas mavericks',
                    'den':'denver nuggets',
                    'det':'detroit pistons',
                    'gsw':'golden state warriors',
                    'hou':'houston rockets',
                    'ind':'indiana pacers',
                    'lac':'los angeles clippers',
                    'lal':'los angeles lakers',
                    'mem':'memphis grizzlies',
                    'mia':'miami heat',
                    'mil':'milwaukee bucks',
                    'min':'minnesota timberwolves',
                    'nop':'new orleans pelicans',
                    'nyk':'new york knicks',
                    'okc':'oklahoma city thunder',
                    'orl':'orlando magic',
                    'phi':'philadelphia 76ers',
                    'phx':'phoenix suns',
                    'por':'portland trail blazers',
                    'sac':'sacramento kings',
                    'sas':'san antonio spurs',
                    'tor':'toronto raptors',
                    'uta':'utah jazz',
                    'wsh':'washington wizards'} # could get from fantasy pros table but simpler to make once bc only 30 immutable vals

    team_abbrev = ''
    if team_name[:3].isupper():
        team_abbrev = team_name[:3].lower()

        irregular_abbrevs = {'bro':'bkn', 'okl':'okc', 'nor':'nop', 'pho':'phx', 'was':'wsh', 'uth': 'uta' } # for these match the first 3 letters of team name instead
        if team_abbrev in irregular_abbrevs.keys():
            #print("irregular abbrev: " + team_abbrev)
            team_abbrev = irregular_abbrevs[team_abbrev]
    else:
        for abbrev, name in team_abbrevs_dict.items():
            if team_name.lower() == name:
                team_abbrev = abbrev
                break

        # if we only have the abbrevs in list we can determine team name by structure
        # for abbrev in team_abbrevs:
        #     # see if abbrev in first 3 letters of name, like atl in atlanta
        #     if re.search(abbrev, team_name[:3].lower()):
        #         team_abbrev = abbrev
        #         break
        # # if abbrev not first 3 letters of name, check initials like nop, lal, lac
        # if team_abbrev == '':
        #     initials = [ s[0] for s in team_name.lower().split() ]
        #     for abbrev in team_abbrevs:
        #         if abbrev == initials:
        #             team_abbrev = abbrev
        #             break
        # # if abbrev not first 3 letters nor initials, then check 1st 2 letters like phx and okc
        # if team_abbrev == '':
        #     for abbrev in team_abbrevs:
        #         if re.search(abbrev[:2], team_name[:2].lower()):
        #             team_abbrev = abbrev
        #             break
        # # check 1st and last letters for bkn brooklyn nets
        # if team_abbrev == '':
        #     initials = [ s[0] for s in team_name.lower().split() ]
        #     for abbrev in team_abbrevs:
        #         first_last = abbrev[0] + abbrev[-1]
        #         if first_last == initials:
        #             team_abbrev = abbrev
        #             break

    #print("team_abbrev: " + str(team_abbrev))
    return team_abbrev

def determine_all_team_abbrevs(position_matchup_data):
    #print("\n===Determine All Team Abbrevs===\n")
    team_abbrevs = []
    for team_idx, row in position_matchup_data.iterrows():
        team_col_name = determine_col_name('team',position_matchup_data)
        team_name = str(position_matchup_data.loc[team_idx, team_col_name])
        if team_name[:3].isupper():
            team_abbrev = team_name[:3].lower()
            # correct irregular abbrevs
            irregular_abbrevs = {'bro':'bkn', 'okl':'okc'} # for these match the first 3 letters of team name instead
            # if team_abbrev == 'bro':
            #     team_abbrev = 'bkn'
            if team_abbrev in irregular_abbrevs.keys():
                team_abbrev = irregular_abbrevs[team_abbrev]

            team_abbrevs.append(team_abbrev)

    #print("team_abbrevs: " + str(team_abbrevs))
    return team_abbrevs

# rating or ranking bc shows average value and orders from easiest ot hardest by position and stat
def determine_matchup_rating(opponent, stat, all_matchup_data):
    print("\n===Determine Matchup Rating for " + opponent.upper() + ", " + stat + "===\n")

    

    positions = ['pg','sg','sf','pf','c']
    all_matchup_ratings = { 'pg':{}, 'sg':{}, 'sf':{}, 'pf':{}, 'c':{} } # { 'pg': { 'values': [source1,source2,..], 'ranks': [source1,source2,..] }, 'sg': {}, ... }
    #position_matchup_rating = { 'values':[], 'ranks':[] } # comparing results from different sources

    #team_abbrevs = []
    for source_matchup_data in all_matchup_data:
        #print("source_matchup_data: " + str(source_matchup_data))

        for position_idx in range(len(source_matchup_data)):
            position_matchup_data = source_matchup_data[position_idx]
            position = positions[position_idx]

            stat_col_name = determine_col_name(stat,position_matchup_data)

            # get all values for stat and sort so we can rank current team
            all_stat_vals = []
            for team_idx, row in position_matchup_data.iterrows():
                
                
                col_val = position_matchup_data.loc[team_idx, stat_col_name]
                stat_val = reader.format_stat_val(col_val)
                #print("stat_val: " + str(stat_val))
                all_stat_vals.append(stat_val)

            #print("all_stat_vals: " + str(all_stat_vals))
            all_stat_vals.sort()
            #print("all_stat_vals: " + str(all_stat_vals))

            # get all team abbrevs from source using abbrevs so we can relate name to abbrevs for sources only giving full name
            # if len(team_abbrevs) == 0:
            #     team_abbrevs = determine_all_team_abbrevs(position_matchup_data)
            
                

            for team_idx, row in position_matchup_data.iterrows():

                # for fantasypros.com source, format OKCoklahoma city, so take first 3 letters
                # for hashtag bball source, format OKC <rank>, so take first 3 letters also
                # but the header name is 'Sort: Team' not just 'Team'
                # team_col_name = 'Team'
                # for col_name in position_matchup_data.columns:
                #     if re.search('team',col_name.lower()):
                #         team_col_name = col_name
                team_col_name = determine_col_name('team',position_matchup_data)
                team_name = str(position_matchup_data.loc[team_idx, team_col_name])
                #print("team_name: " + team_name)
                team = determine_team_abbrev(team_name) # fantasy pros gives both name and abbrev together so use that source to make dict
                #print("team: " + team)
                #print("opponent: " + opponent)

                #if opponent in different_abbrevs:

                if team == opponent:

                    #stat_col_name = determine_col_name(stat,position_matchup_data)
                    #stat_val = float(position_matchup_data.loc[team_idx, stat_col_name])
                    col_val = position_matchup_data.loc[team_idx, stat_col_name]
                    stat_val = reader.format_stat_val(col_val)
                    rank = all_stat_vals.index(stat_val) + 1

                    position_matchup_rating = all_matchup_ratings[position]
                    if 'averages' in position_matchup_rating.keys():
                        position_matchup_rating['averages'].append(stat_val)

                        position_matchup_rating['ranks'].append(rank)
                    else:
                        position_matchup_rating['averages'] = [stat_val]

                        position_matchup_rating['ranks'] = [rank]
                    
                    

                    break # found team so move to next position

    #print("all_matchup_ratings: " + str(all_matchup_ratings))                  
    return all_matchup_ratings

# exclude all star and other special games
def determine_prev_game_date(player_game_log, season_year):
    # if not all star
    prev_game_idx = 0
    while re.search('\\*', player_game_log.loc[prev_game_idx, 'OPP']):
        prev_game_idx += 1

    init_game_date_string = player_game_log.loc[prev_game_idx, 'Date'].split()[1] # 'wed 2/15'
    game_mth = init_game_date_string.split('/')[0]
    final_season_year = str(season_year)
    if int(game_mth) in range(10,13):
        final_season_year = str(season_year - 1)
    prev_game_date_string = init_game_date_string + "/" + final_season_year


    #prev_game_date_string = player_game_log.loc[prev_game_idx, 'Date'].split()[1] + "/" + str(season_year) # eg 'wed 2/15' to '2/15/23'
    prev_game_date_obj = datetime.strptime(prev_game_date_string, '%m/%d/%Y')
    return prev_game_date_obj


# gather game logs by season and do not pull webpage if it does not exist
def determine_played_season(player_url):
    played_season = False
    # response = requests.get(player_url)
    # if response.status_code == 200:
    #     played_season = True
    #     print('played season')

    h = httplib2.Http()
    resp = h.request(player_url, 'HEAD')
    status_code = resp[0]['status']
    print('status_code: ' + str(status_code))
    if int(status_code) < 400:
        # some websites will simply not have the webpage but espn still has the webpage for all years prior to playing with blank game logs
        #if len(game_log) > 0:

        html_results = pd.read_html(player_url)
        #print("html_results: " + str(html_results))

        len_html_results = len(html_results) # each element is a dataframe/table so we loop thru each table

        for order in range(len_html_results):
            #print("order: " + str(order))

            if len(html_results[order].columns.tolist()) == 17:

                played_season = True
                print('played season')

                break

    return played_season


def determine_regular_season_games(player_game_log):

    #reg_season_games_df = pd.DataFrame()
    reg_season_games = []

    for game_idx, row in player_game_log.iterrows():
        if re.search('\\*',player_game_log.loc[game_idx, 'OPP']): # all star stats not included in regular season stats
            #print("game excluded")
            continue
        
        if player_game_log.loc[game_idx, 'Type'] == 'Regular':
            reg_season_games.append(row)

    reg_season_games_df = pd.concat(reg_season_games)

    print("reg_season_games_df:\n" + str(reg_season_games_df))
    return reg_season_games_df

# is it an over or under? above 7/10 or 4/5 or 3/3, or below 3/10 and not 2/2 bc maybe teammate injury so more playing time?
def determine_streak_direction(streak):
    direction = '+'
    # 1st idx header like [pts 10+,1/1,2/2,..]
    out_of_10 = 0
    out_of_5 = 0
    out_of_3 = 0
    out_of_2 = 0
    if len(streak) > 10:
        out_of_10 = int(streak[10].split('/')[0])
    if len(streak) > 5:
        out_of_5 = int(streak[5].split('/')[0])
    if len(streak) > 3:
        out_of_3 = int(streak[3].split('/')[0])
    if len(streak) > 2:
        out_of_2 = int(streak[2].split('/')[0])

    if out_of_10 >= 7 or out_of_5 >= 4 or out_of_3 >= 3:
        direction = '+'
    elif out_of_10 <= 3 and out_of_2 < 2: # if 3/10 but 2/2 then maybe recent change causing beginning of over streak
        direction = '-'

    return direction

# streak has header element
def determine_streak_outline(streak):
    #print("\n===Determine Streak Outline===\n")
    #print(record)
    outline = []

    outline_idxs = [0,1,2,3,4,5,6,7,8,9,14,19,29,49]

    for game_idx in range(len(streak[1:])):
        game = streak[game_idx+1] # record has header at idx 0
        if game_idx in outline_idxs:
            outline.append(game)

    print('outline: ' + str(outline))
    return outline

def determine_record_outline(record):
    print("\n===Determine Record Outline===\n")
    print(record)
    outline = []

    outline_idxs = [0,1,2,3,4,5,6,7,8,9,14,19,29,49]

    for game_idx in range(len(record)):
        game = record[game_idx] # record has header at idx 0
        if game_idx in outline_idxs:
            outline.append(game)

    print('outline: ' + str(outline))
    return outline