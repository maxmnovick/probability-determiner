# determiner.py
# determine conditions 
# eg if streak is considered consistent

import re # see if keyword in column name
import reader # format stat val

def determine_consistent_streak(stat_counts):
    print("\n===Determine Consistent Streak===\n")
    #print("stat_counts: " + str(stat_counts))
    consistent = False

    if len(stat_counts) > 10:
        if stat_counts[9] >= 7: # arbitrary 7/10
            consistent = True
        elif stat_counts[9] <= 3: # arbitrary 7/10
            consistent = True

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
    print("\n===Determine All Team Abbrevs===\n")
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

    print("team_abbrevs: " + str(team_abbrevs))
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
                team = determine_team_abbrev(team_name) # fantasy pros gives both name and abbrev together so use that source to make dict
                
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
