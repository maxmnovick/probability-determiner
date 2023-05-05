# player outcome generator
# updated version of player probability determiner
# instead of generating predictions for all players
# we generate outcomes with probabilities for a given player of interest


import generator, writer

# suns, nugs
#players_names = ['deandre ayton', 'bismack biyombo', 'devin booker', 'torrey craig', 'kevin durant', 'jock landale', 'damion lee', 'josh okogie', 'chris paul', 'cameron payne', 'terrence ross', 'landry shamet', 'ish wainwright', 'christian braun', 'bruce brown', 'thomas bryant', 'kentavious caldwell pope', 'vlatko cancar', 'aaron gordon', 'jeff green', 'reggie jackson', 'nikola jokic', 'jamal murray', 'michael porter jr']

# gsw, lal
players_names = ['malik beasley', 'troy brown jr', 'anthony davis', 'wenyan gabriel', 'rui hachimura', 'lebron james', 'austin reaves', 'dangelo russell', 'dennis schroder', 'jarred vanderbilt', 'stephen curry', 'donte divincenzo', 'draymond green', 'jamychal green', 'jonathan kuminga', 'anthony lamb', 'kevon looney', 'moses moody', 'gary payton ii', 'jordan poole', 'klay thompson', 'andrew wiggins']

players_outcomes = generator.generate_players_outcomes(players_names)

writer.display_players_outcomes(players_outcomes)