# determiner.py
# determine conditions 
# eg if streak is considered consistent

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

# rating or ranking bc shows average value and orders from easiest ot hardest by position and stat
def determine_matchup_rating(opponent, stat, all_matchup_data):
    print("\n===Determine Matchup Rating for " + opponent.upper() + ", " + stat + "===\n")

    positions = ['all','pg','sg','sf','pf','c']
    all_matchup_ratings = { 'all':{}, 'pg':{}, 'sg':{}, 'sf':{}, 'pf':{}, 'c':{} } # { 'pg': { 'values': [source1,source2,..], 'ranks': [source1,source2,..] }, 'sg': {}, ... }
    #position_matchup_rating = { 'values':[], 'ranks':[] } # comparing results from different sources

    for source_matchup_data in all_matchup_data:
        #print("source_matchup_data: " + str(source_matchup_data))

        for position_idx in range(len(source_matchup_data)):
            position_matchup_data = source_matchup_data[position_idx]
            position = positions[position_idx]

            # get all values for stat and sort so we can rank current team
            all_stat_vals = []
            for team_idx, row in position_matchup_data.iterrows():
                stat_val = float(position_matchup_data.loc[team_idx, stat])
                #print("stat_val: " + str(stat_val))
                all_stat_vals.append(stat_val)

            #print("all_stat_vals: " + str(all_stat_vals))
            all_stat_vals.sort()
            #print("all_stat_vals: " + str(all_stat_vals))
            

            for team_idx, row in position_matchup_data.iterrows():

                team = str(position_matchup_data.loc[team_idx, 'Team'])[:3].lower()

                if team == opponent:

                    stat_val = float(position_matchup_data.loc[team_idx, stat])
                    rank = all_stat_vals.index(stat_val) + 1

                    position_matchup_rating = all_matchup_ratings[position]
                    if 'averages' in position_matchup_rating.keys():
                        position_matchup_rating['averages'].append(stat_val)

                        position_matchup_rating['ranks'].append(rank)
                    else:
                        position_matchup_rating['averages'] = [stat_val]

                        position_matchup_rating['ranks'] = [rank]
                    
                    

                    break # found team so move to next position

    print("all_matchup_ratings: " + str(all_matchup_ratings))                  
    return all_matchup_ratings
