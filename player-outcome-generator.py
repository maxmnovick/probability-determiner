# player outcome generator
# updated version of player probability determiner
# instead of generating predictions for all players
# we generate outcomes with probabilities for a given player of interest


import generator, writer

players_names = ['malcolm brogdan']

players_outcomes = generator.generate_players_outcomes(players_names)

writer.display_players_outcomes(players_outcomes)