# read player lines
# input: player lines file
# output: player lines data

import reader # extract data

data_type = "Player Lines"
input_type = '3/5' # date as mth/day will become mth_day in file

# v2: copy paste raw projected lines direct from website
# raw projected lines in format: [['Player Name', 'O 10 +100', 'U 10 +100', 'Player Name', 'O 10 +100', 'U 10 +100', Name', 'O 10 +100', 'U 10 +100']]
raw_projected_lines = reader.extract_data(data_type, input_type, extension='tsv', header=True) # tsv no header
print("raw_projected_lines: " + str(raw_projected_lines))

# for now set unavailable stats=1, until we have basic fcns working
reb = 1
ast = 1
three = 1
blk = 1
stl = 1
to = 1

# get location and opponent from header row above projected stats lines


# convert raw projected lines to projected lines
header_row = ['Name', 'PTS', 'REB', 'AST', '3PT', 'BLK', 'STL', 'TO','LOC','OPP']

player_line = []
all_player_lines = []