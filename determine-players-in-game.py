# read a team's schedule
# then see the box score of each game
# then list all active players in the game on both teams (for and aginst given player of interest)

# ===read a team's schedule
# we need to see how a given player performs with given teammates and opponent players, specifically the individuals for and against a given player, not just the team as a whole bc the team consists of individuals that determine matchups
# also check the affect of individuals for and against a given player bc not enough samples with exact lineups but many samples against individuals
# we already have a given players game log so we can see games played bc we only need matchups for the given player

def read_team_schedule(team_abbrev):

    print('\n===Read Team Schedule===\n')
