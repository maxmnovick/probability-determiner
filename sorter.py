# sorter.py
# sorting fcns like sorting dictionaries by one common key
# eg sort predictions by degree of belief

# predictions = { 'prediction':'','overall record':[],..,'degree of belief':0 }
def sort_predictions_by_deg_of_bel(predictions):
    sorted_predictions = sorted(predictions, key=lambda d: d['degree of belief']) 

    return sorted_predictions

def sort_dicts_by_key(dicts, key):

    return sorted(dicts, key=lambda d: d[key], reverse=True) # reverse so we see highest first