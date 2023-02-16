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