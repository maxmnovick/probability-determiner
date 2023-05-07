# player outcome generator
# updated version of player probability determiner
# instead of generating predictions for all players
# we generate outcomes with probabilities for a given player of interest


import generator, writer

# suns, nugs
#players_names = ['deandre ayton', 'bismack biyombo', 'devin booker', 'torrey craig', 'kevin durant', 'jock landale', 'damion lee', 'josh okogie', 'chris paul', 'cameron payne', 'terrence ross', 'landry shamet', 'ish wainwright', 'christian braun', 'bruce brown', 'thomas bryant', 'kentavious caldwell pope', 'vlatko cancar', 'aaron gordon', 'jeff green', 'reggie jackson', 'nikola jokic', 'jamal murray', 'michael porter jr']

# bos phi, den phx
players_names = ['deandre ayton']#, 'bismack biyombo', 'devin booker', 'torrey craig', 'kevin durant', 'jock landale', 'damion lee', 'josh okogie', 'chris paul', 'cameron payne', 'terrence ross', 'landry shamet', 'ish wainwright', 'christian braun', 'bruce brown', 'thomas bryant', 'kentavious caldwell pope', 'vlatko cancar', 'aaron gordon', 'jeff green', 'reggie jackson', 'nikola jokic', 'jamal murray', 'michael porter jr', 'malcolm brogdan', 'jaylen brown', 'al horford', 'marcus smart', 'jayson tatum', 'derrick white', 'grant williams', 'robert williams iii', 'joel embiid', 'james harden', 'tobias harris', 'tyrese maxey', 'jalen mcdaniels', 'deanthony melton', 'georges niang', 'paul reed', 'pj tucker']

# gsw, lal
#players_names = ['malik beasley', 'troy brown jr', 'anthony davis', 'wenyan gabriel', 'rui hachimura', 'lebron james', 'austin reaves', 'dangelo russell', 'dennis schroder', 'jarred vanderbilt', 'stephen curry', 'donte divincenzo', 'draymond green', 'jamychal green', 'jonathan kuminga', 'anthony lamb', 'kevon looney', 'moses moody', 'gary payton ii', 'jordan poole', 'klay thompson', 'andrew wiggins']

# nyk mia
#players_names = ['rj barrett', 'jalen brunson', 'quentin grimes', 'josh hart', 'isaiah hartenstein', 'immanuel quickley', 'julius randle', 'mitchell robinson', 'obi toppin', 'bam adebayo', 'jimmy butler', 'kevin love', 'kyle lowry', 'caleb martin', 'duncan robinson', 'max strus', 'gabe vincent', 'cody zeller']

players_outcomes = generator.generate_players_outcomes(players_names)

writer.display_players_outcomes(players_outcomes)