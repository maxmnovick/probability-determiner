# reader.py
# functions for a reader

import re
import pandas as pd # read html results from webpage
from urllib.request import Request, urlopen # request website, open webpage given req
from bs4 import BeautifulSoup # read html from webpage

# get data from a file and format into a list (same as generator version of this fcn but more general)
# input such as Game Data - All Games
# or Game Log - All Players
def extract_data(data_type, input_type, extension='csv'):
	catalog_filename = "data/" + data_type.title() + " - " + input_type.title() + "." + extension

	lines = []
	data = []
	all_data = []

	try: 

		with open(catalog_filename, encoding="UTF8") as catalog_file:

			current_line = ""
			for catalog_info in catalog_file:
				current_line = catalog_info.strip()
				lines.append(current_line)

			catalog_file.close()

		# skip header line
		for line in lines[1:]:
			if len(line) > 0:
				if extension == "csv":
					data = line.split(",")
				else:
					data = line.split("\t")
			all_data.append(data)

	except Exception as e:
		print("Error opening file. ")
	
	#print("all_data: " + str(all_data))


	return all_data


# get espn id from google
def read_player_espn_id(player_name):
	espn_id = ''

	try:

		site = 'https://www.google.com/search?q=' + player_name.replace(' ', '+') + '+nba+espn+gamelog'

		req = Request(site, headers={
			'User-Agent': 'Mozilla/5.0',
		})

		page = urlopen(req) # open webpage given request

		soup = BeautifulSoup(page, features="lxml")

		links_with_text = [] # id is in first link with text

		for a in soup.find_all('a', href=True):
			if a.text and a['href'].startswith('/url?'):
				links_with_text.append(a['href'])

		links_with_id_text = [x for x in links_with_text if 'id/' in x]

		espn_id_link = links_with_id_text[0] # string starting with player id

		espn_id = re.findall(r'\d+', espn_id_link)[0]

		print('Success', espn_id, player_name)

	except Exception as e:
		print('Error', espn_id, player_name)

	print("espn_id: " + espn_id)
	return espn_id


# get game log from espn.com
def read_player_game_log(player_name):
	print("\n===Read Player Game Log===\n")

	# get espn player id from google so we can get url
	player_espn_id = read_player_espn_id(player_name)
	year = '2023'
	player_url = 'https://www.espn.com/nba/player/gamelog/_/id/' + player_espn_id + '/type/nba/year/' + year #.format(df_Players_Drafted_2000.loc[INDEX, 'ESPN_GAMELOG_ID'])
	print("player_url: " + player_url)

	player_game_log = []

	#dfs = pd.read_html(player_url)
	#print(f'Total tables: {len(dfs)}')

	#try:

	html_results = pd.read_html(player_url)
	print("html_results: " + str(html_results))

	parts_of_season = [] # pre season, regular season, post season

	len_html_results = len(html_results)

	for order in range(len_html_results):
		print("order: " + str(order))

		if len(html_results[order].columns.tolist()) == 17:

			part_of_season = html_results[order]

			if len_html_results - 2 == order:
				part_of_season['Type'] = 'Preseason'

			else:
				if len(part_of_season[(part_of_season['OPP'].str.contains('GAME'))]) > 0:
					part_of_season['Type'] = 'Postseason'
				else:
					part_of_season['Type'] = 'Regular'

			parts_of_season.append(part_of_season)

		else:
			print("Warning: table does not have 17 columns so it is not valid game log.")
			pass

	player_game_log_df = pd.concat(parts_of_season, sort=False, ignore_index=True)

	player_game_log_df = player_game_log_df[(player_game_log_df['OPP'].str.startswith('@')) | (player_game_log_df['OPP'].str.startswith('vs'))].reset_index(drop=True)

	player_game_log_df['Season'] = str(int(year)-1) + '-' + str(int(year)-2000)

	player_game_log_df['Player'] = player_name

	player_game_log_df = player_game_log_df.set_index(['Player', 'Season', 'Type']).reset_index()

	# Successful 3P Attempts
	player_game_log_df['3PT_SA'] = player_game_log_df['3PT'].str.split('-').str[0]

	# All 3P Attempts
	player_game_log_df['3PT_A'] = player_game_log_df['3PT'].str.split('-').str[1]
	player_game_log_df[
		['MIN', 'FG%', '3P%', 'FT%', 'REB', 'AST', 'BLK', 'STL', 'PF', 'TO', 'PTS', '3PT_SA', '3PT_A']

		] = player_game_log_df[

			['MIN', 'FG%', '3P%', 'FT%', 'REB', 'AST', 'BLK', 'STL', 'PF', 'TO', 'PTS', '3PT_SA', '3PT_A']

			].astype(float)

	print("player_game_log_df:\n" + str(player_game_log_df))

	# except Exception as e:
	# 	print("Error reading game log " + str(e))
	# 	pass

	#print("player_game_log: " + str(player_game_log))
	return player_game_log_df # can return this df directly or first arrange into list but seems simpler and more intuitive to keep df so we can access elements by keyword