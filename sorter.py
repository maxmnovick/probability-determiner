# sorter.py
# sorting fcns like sorting dictionaries by one common key
# eg sort predictions by degree of belief

# predictions = { 'prediction':'','overall record':[],..,'degree of belief':0 }
def sort_predictions_by_deg_of_bel(predictions):
    sorted_predictions = sorted(predictions, key=lambda d: d['degree of belief']) 

    return sorted_predictions

# given a list of dicts with corresponding keys, 
# we want to see which dict has the highest value at a given key they all share
def sort_dicts_by_key(dicts, key):

    return sorted(dicts, key=lambda d: d[key], reverse=True) # reverse so we see highest first

# sort so we see all condition types grouped together for separate analysis and viewing
# players_outcomes = {player: stat name: outcome dict}
def sort_players_outcomes(players_outcomes):
    print('sort players outcomes')

    print('players_outcomes: ' + str(players_outcomes))