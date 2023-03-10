# reader.py
# functions for a reader

import re
import pandas as pd # read html results from webpage
from urllib.request import Request, urlopen # request website, open webpage given req
from bs4 import BeautifulSoup # read html from webpage
from tabulate import tabulate # display output, which for the reader is input files to confirm and review their contents

from selenium import webdriver # need to read html5 webpages
from webdriver_manager.chrome import ChromeDriverManager # need to access dynamic webpages
import time # need to read dynamic webpages
from selenium.webdriver.chrome.options import Options # block ads

import csv
import json # we need projected lines table to be json so we can refer to player when analyzing stats

import determiner # determine played season before reading webpage to avoid exception/error
import isolator # isolate_player_game_data to read data from file

import math # round up to nearest integer while reading

# get data from a file and format into a list (same as generator version of this fcn but more general)
# input such as Game Data - All Games
# or Game Log - All Players
def extract_data(data_type, input_type, extension='csv', header=False):
	input_type = re.sub('/','_',input_type)
	catalog_filename = "data/" + data_type.title() + " - " + input_type.title() + "." + extension
	#print("catalog_filename: " + catalog_filename)
	

	lines = []
	data = []
	all_data = []

	try: 

		with open(catalog_filename, encoding="UTF8") as catalog_file:

			current_line = ""
			for catalog_info in catalog_file:
				current_line = catalog_info.strip()
				#print("current_line: " + str(current_line))
				lines.append(current_line)

			catalog_file.close()

		# skip header line
		read_lines = lines
		if not header: # file includes header but we do not want header
			read_lines = lines[1:]

		for line in read_lines:
			#print("line: " + str(line))
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

		print('Success', espn_id, player_name.title())

	except Exception as e:
		print('Error', espn_id, player_name.title())

	print("espn_id: " + espn_id)
	return espn_id

def read_all_player_espn_ids(player_names, player_of_interest=''):
	espn_ids_dict = {}

	if player_of_interest != '':
		player_names = [player_of_interest]

	for name in player_names:
		espn_id = read_player_espn_id(name)
		espn_ids_dict[name] = espn_id

	return espn_ids_dict


# get game log from espn.com
def read_player_season_log(player_name, season_year=2023, player_url='', player_id=''):
	print("\n===Read Player Game Log: " + player_name.title() + "===\n")

	# get espn player id from google so we can get url
	if player_url == '':
		if player_id == '':
			player_id = read_player_espn_id(player_name)
		season_year = 2023
		player_url = 'https://www.espn.com/nba/player/gamelog/_/id/' + player_id + '/type/nba/year/' + str(season_year) #.format(df_Players_Drafted_2000.loc[INDEX, 'ESPN_GAMELOG_ID'])
		print("player_url: " + player_url)

	player_game_log = []

	#dfs = pd.read_html(player_url)
	#print(f'Total tables: {len(dfs)}')

	#try:

	html_results = pd.read_html(player_url)
	#print("html_results: " + str(html_results))

	parts_of_season = [] # pre season, regular season, post season

	len_html_results = len(html_results) # each element is a dataframe/table so we loop thru each table

	for order in range(len_html_results):
		#print("order: " + str(order))

		if len(html_results[order].columns.tolist()) == 17:

			part_of_season = html_results[order]

			# look at the formatting to figure out how to separate table and elements in table
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

	player_game_log_df = pd.DataFrame()

	if len(parts_of_season) > 0:

		player_game_log_df = pd.concat(parts_of_season, sort=False, ignore_index=True)

		player_game_log_df = player_game_log_df[(player_game_log_df['OPP'].str.startswith('@')) | (player_game_log_df['OPP'].str.startswith('vs'))].reset_index(drop=True)

		player_game_log_df['Season'] = str(season_year-1) + '-' + str(season_year-2000)

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

	# display player game log in readable format
	#pd.set_option('display.max_columns', 100)
	pd.set_option('display.max_columns', None)
	print("player_game_log_df:\n" + str(player_game_log_df))

	# except Exception as e:
	# 	print("Error reading game log " + str(e))
	# 	pass

	# if we want to format table in 1 window we can get df elements in lists and then print lists in table
	# header_row = ['Date', 'OPP', 'Result', 'MIN', 'FG', 'FG%', '3P', '3P%', 'FT', 'FT%', 'REB', 'AST', 'BLK', 'STL', 'PF', 'TO', 'PTS']

	# table = [header_row]
	# for row in player_game_data:
	# 	table.append(row)

	# print("\n===" + player_name + "===\n")
	# print(tabulate(table))
	#print("player_game_log: " + str(player_game_log))
	return player_game_log_df # can return this df directly or first arrange into list but seems simpler and more intuitive to keep df so we can access elements by keyword

def read_player_season_logs(player_name, read_all_seasons=True, player_espn_ids={}):

	player_game_logs = []

	player_espn_id = ''
	if len(player_espn_ids.keys()) == 0:
		player_espn_id = read_player_espn_id(player_name)
	else:
		player_espn_id = player_espn_ids[player_name]

	if player_espn_id == '':
		print('Warning: player_espn_id blank while trying to get player url! ')
		
	season_year = 2023
	player_url = 'https://www.espn.com/nba/player/gamelog/_/id/' + player_espn_id + '/type/nba/year/' + str(season_year) #.format(df_Players_Drafted_2000.loc[INDEX, 'ESPN_GAMELOG_ID'])
	
	#read_all_seasons = True
	while determiner.determine_played_season(player_url):

		print("player_url: " + player_url)
		game_log_df = read_player_season_log(player_name, season_year, player_url)
		if not game_log_df.empty:
			player_game_logs.append(game_log_df)

		if not read_all_seasons:
			break

		season_year -= 1
		player_url = 'https://www.espn.com/nba/player/gamelog/_/id/' + player_espn_id + '/type/nba/year/' + str(season_year) #.format(df_Players_Drafted_2000.loc[INDEX, 'ESPN_GAMELOG_ID'])
		

	return player_game_logs

def read_all_players_season_logs(player_names, read_all_seasons=True, player_espn_ids={}):

	all_players_season_logs = {}

	for player_name in player_names:
		players_season_logs = read_player_season_logs(player_name, read_all_seasons, player_espn_ids)
		all_players_season_logs[player_name] = players_season_logs

	return all_players_season_logs


# get team season schedule from espn.com
def read_team_season_schedule(team_name, season_year=2023, team_url='', team_id=''):
	print("\n===Read Team " + team_name.title() + ", Season " + str(season_year) + " Schedule===\n")

	# get espn player id from google so we can get url
	if team_url == '':
		if team_id == '':
			team_id = read_team_espn_id(team_name)
		season_year = 2023
		team_url = 'https://www.espn.com/nba/player/gamelog/_/id/' + team_id + '/type/nba/year/' + str(season_year) #.format(df_Players_Drafted_2000.loc[INDEX, 'ESPN_GAMELOG_ID'])
		print("team_url: " + team_url)

	player_game_log = []

	#dfs = pd.read_html(player_url)
	#print(f'Total tables: {len(dfs)}')

	#try:

	html_results = pd.read_html(team_url)
	#print("html_results: " + str(html_results))

	parts_of_season = [] # pre season, regular season, post season

	len_html_results = len(html_results) # each element is a dataframe/table so we loop thru each table

	for order in range(len_html_results):
		#print("order: " + str(order))

		if len(html_results[order].columns.tolist()) == 17:

			part_of_season = html_results[order]

			# look at the formatting to figure out how to separate table and elements in table
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

	player_game_log_df = pd.DataFrame()

	if len(parts_of_season) > 0:

		player_game_log_df = pd.concat(parts_of_season, sort=False, ignore_index=True)

		player_game_log_df = player_game_log_df[(player_game_log_df['OPP'].str.startswith('@')) | (player_game_log_df['OPP'].str.startswith('vs'))].reset_index(drop=True)

		player_game_log_df['Season'] = str(season_year-1) + '-' + str(season_year-2000)

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

	# display player game log in readable format
	#pd.set_option('display.max_columns', 100)
	pd.set_option('display.max_columns', None)
	print("player_game_log_df:\n" + str(player_game_log_df))

	# except Exception as e:
	# 	print("Error reading game log " + str(e))
	# 	pass

	# if we want to format table in 1 window we can get df elements in lists and then print lists in table
	# header_row = ['Date', 'OPP', 'Result', 'MIN', 'FG', 'FG%', '3P', '3P%', 'FT', 'FT%', 'REB', 'AST', 'BLK', 'STL', 'PF', 'TO', 'PTS']

	# table = [header_row]
	# for row in player_game_data:
	# 	table.append(row)

	# print("\n===" + player_name + "===\n")
	# print(tabulate(table))
	#print("player_game_log: " + str(player_game_log))
	return player_game_log_df # can return this df directly or first arrange into list but seems simpler and more intuitive to keep df so we can access elements by keyword



# get player position from espn game log page bc we already have urls for each player
def read_player_position(player_name, player_id, season_year=2023):
	print("\n===Read Player Position: " + player_name.title() + "===\n")
	position = ''

	try:
		
		site = 'https://www.espn.com/nba/player/gamelog/_/id/' + player_id + '/type/nba/year/' + str(season_year)

		req = Request(site, headers={
			'User-Agent': 'Mozilla/5.0',
		})

		page = urlopen(req) # open webpage given request

		soup = BeautifulSoup(page, features="lxml")

		# find last element of ul with class PlayerHeader__Team_Info
		position = str(list(soup.find("ul", {"class": "PlayerHeader__Team_Info"}).descendants)[-1])
		#print("position_elementn:\n" + str(position_element))

		if len(position) > 2: # use abbrev
			pos_abbrev = ''
			words = position.split()
			for word in words:
				pos_abbrev += word[0].lower()

			if pos_abbrev == 'f': # some just say forward so make it small forward but actually better to use height to determine bc if over 6'6 then pf maybe?
				pos_abbrev = 'sf'
			elif pos_abbrev == 'g':
				pos_abbrev = 'sg'
			position = pos_abbrev

		# links_with_text = [] # id is in first link with text

		# for a in soup.find_all('a', href=True):
		# 	if a.text and a['href'].startswith('/url?'):
		# 		links_with_text.append(a['href'])

		# links_with_id_text = [x for x in links_with_text if 'id/' in x]

		# espn_id_link = links_with_id_text[0] # string starting with player id

		# position = re.findall(r'\d+', espn_id_link)[0]

		print('Success', position.upper(), player_name.title())

	except Exception as e:
		print('Error', position.upper(), player_name.title())

	print("position: " + position)
	return position

def read_all_players_positions(player_espn_ids_dict):
	#print("\n===Read All Players Positions===\n")
	players_positions = {}

	for name, id in player_espn_ids_dict.items():
		pos = read_player_position(name, id)
		players_positions[name] = pos

	#print("players_positions: " + str(players_positions))
	return players_positions

# get player position from espn game log page bc we already have urls for each player
def read_player_team(player_name, player_id, season_year=2023):
	print("\n===Read Player Team: " + player_name.title() + "===\n")
	team = ''

	try:
		
		site = 'https://www.espn.com/nba/player/gamelog/_/id/' + player_id + '/type/nba/year/' + str(season_year)

		req = Request(site, headers={
			'User-Agent': 'Mozilla/5.0',
		})

		page = urlopen(req) # open webpage given request

		soup = BeautifulSoup(page, features="lxml")

		# find last element of ul with class PlayerHeader__Team_Info
		team = str(list(soup.find("ul", {"class": "PlayerHeader__Team_Info"}).descendants)[0]).strip()#.split('<')[0]#.split('>')[-1]
		#print("team_element:\n" + str(team))
		
		#<li class="truncate min-w-0"><a class="AnchorLink clr-black" data-clubhouse-uid="s:40~l:46~t:21" href="https://www.espn.com/nba/team/_/name/phx/phoenix-suns" tabindex="0">Phoenix Suns</a></li>

		team_name = re.split('</',str(team))[0]
		team_name = re.split('>',team_name)[-1]
		#print("team_name: " + team_name)
		team_abbrev = determiner.determine_team_abbrev(team_name)

		print('Success', team_abbrev.upper(), player_name.title())

	except Exception as e:
		print('Error', team_abbrev.upper(), player_name.title())

	

	#print("final team: " + team_abbrev)
	return team_abbrev

def read_all_players_teams(player_espn_ids_dict):
	#print("\n===Read All Players Positions===\n")
	players_positions = {}

	for name, id in player_espn_ids_dict.items():
		team = read_player_team(name, id)
		players_positions[name] = team

	#print("players_positions: " + str(players_positions))
	return players_positions


# show matchup data against each position so we can see which position has easiest matchup
def read_matchup_data(source_url):

	print("\n===Read Matchup Data===\n")

	matchup_data = [] 

	# swish source which uses html 5 is default for now bc we need to define df outside if statement
	
	matchup_df = pd.DataFrame()
	
	

	if re.search('fantasypro|hashtag|swish',source_url): # swish analytics uses html5
		

		#chop = webdriver.ChromeOptions()
		#chop.add_extension('adblock_5_4_1_0.crx')
		#driver = webdriver.Chrome(chrome_options = chop)

		driver = webdriver.Chrome(ChromeDriverManager().install())
		driver.implicitly_wait(3)

		driver.get(source_url) # Open the URL on a google chrome window
		
		#time.sleep(3) # As this is a dynamic html web-page, wait for 3 seconds for everything to be loaded

		# if needed, Accept the cookies policy
		# driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
		#time.sleep(3)

		# click on the pagination elements to select not only the page 1 but all pages
		#position_btn_path = '/html/body/div' #main/div/div/div/div/div/ul/li[1]/a'
		#driver.find_element('xpath', '/html/body/div').click()

		#position_btn = (driver.find_element('xpath', '/html/body/div').text())
		#print("position_btn: " + str(position_btn))
		#driver.find_element_by_xpath(position_btn_path).click()
		#time.sleep(3)

		#ad = driver.find_element('id', 'div-gpt-ad-1556117653136-0').find_element('xpath','div/iframe')
		#print("ad: " + ad.get_attribute('outerHTML'))

		# click x on advertisement so we can click btns below it
		#ad_close = driver.find_element('xpath','//*[@id="closebutton"]')
		#print("ad_close: " + ad_close.get_attribute('outerHTML'))
		#ad_close.click(); #Close Ad
		#time.sleep(3)

		if re.search('fantasypro',source_url):
			if driver.find_elements("id", "google_ads_iframe_/2705664/fantasypros_interstitial_1_0"):
				driver.switch_to.frame(driver.find_element("id", "google_ads_iframe_/2705664/fantasypros_interstitial_1_0"))
				#l = driver.find_element('xpath', 'html/body/div')
				l = driver.find_element('id', 'closebutton')
				h1= driver.execute_script("return arguments[0].outerHTML;",l)
				print("h1: " + str(h1))
				# driver.switch_to.frame(driver.find_element("tag name", "iframe"))
				# l = driver.find_element('xpath', 'html/body')
				# h2= driver.execute_script("return arguments[0].innerHTML;",l)
				# print("h2: " + str(h2))
				l.click(); #Close Ad

				driver.switch_to.default_content()

			# get the defense matchup table as text

			#defense_table_path = 'html/body/' #main/div/div/div/div[6]/data-table/tbody'
			#matchup_table = driver.find_element('id', 'data-table')
			#print("matchup_table: " + str(matchup_table))

			# not all sources have all team defense and not needed yet so add later
			# position_btn = driver.find_element('class name','main-content').find_element('xpath','div/div[4]/div/ul/li[1]/a')
			# print("position_btn: " + position_btn.get_attribute('innerHTML'))
			# position_btn.click()
			# #time.sleep(3)

			# team_matchup_df=pd.read_html(driver.find_element('id', "data-table").get_attribute('outerHTML'))[0]
			# print("team_matchup_df\n" + str(team_matchup_df))


			pg_btn = driver.find_element('class name','main-content').find_element('xpath','div/div[4]/div/ul/li[2]/a')
			print("pg_btn: " + pg_btn.get_attribute('innerHTML'))
			pg_btn.click()
			#time.sleep(3)

			pg_matchup_df=pd.read_html(driver.find_element('id', "data-table").get_attribute('outerHTML'))[0]
			print("pg_matchup_df\n" + str(pg_matchup_df))


			sg_btn = driver.find_element('class name','main-content').find_element('xpath','div/div[4]/div/ul/li[3]/a')
			print("sg_btn: " + sg_btn.get_attribute('innerHTML'))
			sg_btn.click()
			#time.sleep(3)

			sg_matchup_df=pd.read_html(driver.find_element('id', "data-table").get_attribute('outerHTML'))[0]
			print("sg_matchup_df\n" + str(sg_matchup_df))


			sf_btn = driver.find_element('class name','main-content').find_element('xpath','div/div[4]/div/ul/li[4]/a')
			print("sf_btn: " + sf_btn.get_attribute('innerHTML'))
			sf_btn.click()
			#time.sleep(3)

			sf_matchup_df=pd.read_html(driver.find_element('id', "data-table").get_attribute('outerHTML'))[0]
			print("sf_matchup_df\n" + str(sf_matchup_df))


			pf_btn = driver.find_element('class name','main-content').find_element('xpath','div/div[4]/div/ul/li[5]/a')
			print("pf_btn: " + pf_btn.get_attribute('innerHTML'))
			pf_btn.click()
			#time.sleep(3)

			pf_matchup_df=pd.read_html(driver.find_element('id', "data-table").get_attribute('outerHTML'))[0]
			print("pf_matchup_df\n" + str(pf_matchup_df))


			c_btn = driver.find_element('class name','main-content').find_element('xpath','div/div[4]/div/ul/li[6]/a')
			print("c_btn: " + c_btn.get_attribute('innerHTML'))
			c_btn.click()
			#time.sleep(3)

			c_matchup_df=pd.read_html(driver.find_element('id', "data-table").get_attribute('outerHTML'))[0]
			print("c_matchup_df\n" + str(c_matchup_df))

			matchup_data = [pg_matchup_df, sg_matchup_df, sf_matchup_df, pf_matchup_df, c_matchup_df]

		elif re.search('hashtag',source_url):
			print("Pull data from hastag bball.")
			all_matchup_df=pd.read_html(driver.find_element('id', "ContentPlaceHolder1_GridView1").get_attribute('outerHTML'))[0]
			print("all_matchup_df\n" + str(all_matchup_df))

			pg_matchup_df = all_matchup_df[all_matchup_df['Sort: Position'] == 'PG']
			print("pg_matchup_df\n" + str(pg_matchup_df))
			sg_matchup_df = all_matchup_df[all_matchup_df['Sort: Position'] == 'SG']
			print("sg_matchup_df\n" + str(sg_matchup_df))
			sf_matchup_df = all_matchup_df[all_matchup_df['Sort: Position'] == 'SF']
			print("sf_matchup_df\n" + str(sf_matchup_df))
			pf_matchup_df = all_matchup_df[all_matchup_df['Sort: Position'] == 'PF']
			print("pf_matchup_df\n" + str(pf_matchup_df))
			c_matchup_df = all_matchup_df[all_matchup_df['Sort: Position'] == 'C']
			print("c_matchup_df\n" + str(c_matchup_df))

			# they do not give all team defense so we must calculate or remove from other sources if not needed. it is needed bc good to know overall defense in positionless bball
			# get list of all team names and then make subset tables by team
			# team_names = all_matchup_df['Sort: Team'].unique
			# print("team_names: " + str(team_names))
			# for team_name in team_names:
			# 	team_matchup_df = all_matchup_df[all_matchup_df['Sort: Team'] == team_name]
			# 	print("team_matchup_df\n" + str(team_matchup_df))

			# 	pts_mean = team_matchup_df['Sort: PTS'].mean()

			matchup_data = [pg_matchup_df, sg_matchup_df, sf_matchup_df, pf_matchup_df, c_matchup_df]
			
		elif re.search('swish',source_url):
			print("Pull data from Swish.")

			time.sleep(2) #needs to load

			pg_btn = driver.find_element('xpath','html/body/div[3]/div[2]/div[2]/div/ul/li[2]/a')
			print("pg_btn: " + pg_btn.get_attribute('innerHTML'))
			pg_btn.click()
			

			pg_matchup_df=pd.read_html(driver.find_element('id', "stat-table").get_attribute('outerHTML'))[0]
			print("pg_matchup_df\n" + str(pg_matchup_df))


			sg_btn = driver.find_element('xpath','html/body/div[3]/div[2]/div[2]/div/ul/li[3]/a')
			print("sg_btn: " + sg_btn.get_attribute('innerHTML'))
			sg_btn.click()
			
			sg_matchup_df=pd.read_html(driver.find_element('id', "stat-table").get_attribute('outerHTML'))[0]
			print("sg_matchup_df\n" + str(sg_matchup_df))


			sf_btn = driver.find_element('xpath','html/body/div[3]/div[2]/div[2]/div/ul/li[4]/a')
			print("sf_btn: " + sf_btn.get_attribute('innerHTML'))
			sf_btn.click()
			
			sf_matchup_df=pd.read_html(driver.find_element('id', "stat-table").get_attribute('outerHTML'))[0]
			print("sf_matchup_df\n" + str(sf_matchup_df))


			pf_btn = driver.find_element('xpath','html/body/div[3]/div[2]/div[2]/div/ul/li[5]/a')
			print("pf_btn: " + pf_btn.get_attribute('innerHTML'))
			pf_btn.click()
			
			pf_matchup_df=pd.read_html(driver.find_element('id', "stat-table").get_attribute('outerHTML'))[0]
			print("pf_matchup_df\n" + str(pf_matchup_df))


			c_btn = driver.find_element('xpath','html/body/div[3]/div[2]/div[2]/div/ul/li[6]/a')
			print("c_btn: " + c_btn.get_attribute('innerHTML'))
			c_btn.click()
			
			c_matchup_df=pd.read_html(driver.find_element('id', "stat-table").get_attribute('outerHTML'))[0]
			print("c_matchup_df\n" + str(c_matchup_df))

			matchup_data = [pg_matchup_df, sg_matchup_df, sf_matchup_df, pf_matchup_df, c_matchup_df]
			
		else:
			team_matchup_df=pd.read_html(driver.find_element('id', "ContentPlaceHolder1_GridView1").get_attribute('outerHTML'))[0]
			print("team_matchup_df\n" + str(team_matchup_df))

		# close the google chrome window
		driver.quit()

		
	else:
		# first get the html as a pandas dataframe format
		html_results = pd.read_html(source_url)
		print("html_results: " + str(html_results))

	return matchup_data

# sources disagree so we need to find consensus or just be aware of the risk of inaccurate data
# show all 5 sources so we can see the conflicts and therefore risk of inaccurate data
def read_all_matchup_data(matchup_data_sources):

	print("\n===Read All Matchup Data===\n")

	all_matchup_data = []

	for source in matchup_data_sources:
		
		source_matchup_data = read_matchup_data(source)
		all_matchup_data.append(source_matchup_data)

	return all_matchup_data

# def read_projected_lines(date):
# 	lines = []

# 	return lines


def extract_json_from_file(data_type, input_type, extension='csv'):
	catalog_filename = "data/" + data_type.title() + " - " + input_type.title() + "." + extension

	# create a dictionary
	data_dict = {}
	
	lines = []
	#data = []
	all_data = []

	try: 

		with open(catalog_filename, encoding="UTF8") as catalog_file:

			csvReader  =csv.DictReader(catalog_file)

			# Convert each row into a dictionary
			# and add it to data
			for rows in csvReader:
				
				# Assuming a column named 'No' to
				# be the primary key
				key = rows['Name']
				data_dict[key] = rows

		# 	current_line = ""
		# 	for catalog_info in catalog_file:
		# 		current_line = catalog_info.strip()
		# 		lines.append(current_line)

		# 	catalog_file.close()

		# # skip header line
		# read_lines = lines
		# if not header:
		# 	read_lines = lines[1:]

		# for line in read_lines:
		# 	if len(line) > 0:
		# 		if extension == "csv":
		# 			data = line.split(",")
		# 		else:
		# 			data = line.split("\t")
		# 	all_data.append(data)

	except Exception as e:
		print("Error opening file. ")
	
	print("data_dict: " + str(data_dict))


	return data_dict


def format_stat_val(col_val):
	stat_val = 0.0
	if re.search('\\s',str(col_val)): # eg '20.3 15' for 'avg rank'
		stat_val = float(re.split('\\s',col_val)[0])
	else:
		stat_val = float(col_val)

	return stat_val

def read_season_log_from_file(data_type, player_name, ext):
	
	all_pts = []
	all_rebs = []
	all_asts = []
	all_winning_scores = []
	all_losing_scores = []
	all_minutes = []
	all_fgms = []
	all_fgas = []
	all_fg_rates = []
	all_threes_made = []
	all_threes_attempts = []
	all_three_rates = []
	all_ftms = []
	all_ftas = []
	all_ft_rates = []
	all_bs = []
	all_ss = []
	all_fs = []
	all_tos = []

	all_stats = []
    
	player_data = extract_data(data_type, player_name, ext)
	# first row is headers, next are games with monthly averages bt each mth

	#desired_field = 'points'
	#desired_field_idx = determiner.determine_field_idx(desired_field)
	date_idx = 0
	opp_idx = 1
	result_idx = 2
	minutes_idx = 3
	fg_idx = 4
	fg_rate_idx = 5
	three_idx = 6
	three_rate_idx = 7
	ft_idx = 8
	ft_rate_idx = 9
	r_idx = 10
	a_idx = 11
	b_idx = 12
	s_idx = 13
	f_idx = 14
	to_idx = 15
	p_idx = 16

	# isolate games from lebron data
	# exclude headers and monthly averages
	player_games_data = isolator.isolate_player_game_data(player_data, player_name)

	

	if len(player_games_data) > 0:
		for game in player_games_data:
			pts = int(game[p_idx])
			rebs = int(game[r_idx])
			asts = int(game[a_idx])

			results = game[result_idx]
			#print("results: " + results)
			results_data = re.split('\\s+', results)
			#print("results_data: " + str(results_data))
			score_data = results_data[1].split('-')
			#print("score_data: " + str(score_data))
			winning_score = int(score_data[0])
			losing_score = int(score_data[1])

			minutes = int(game[minutes_idx])

			fgs = game[fg_idx]
			fg_data = fgs.split('-')
			fgm = int(fg_data[0])
			fga = int(fg_data[1])
			fg_rate = round(float(game[fg_rate_idx]), 1)

			threes = game[three_idx]
			threes_data = threes.split('-')
			#print("threes_data: " + str(threes_data))
			threes_made = int(threes_data[0])
			threes_attempts = int(threes_data[1])
			three_rate = round(float(game[three_rate_idx]), 1)

			fts = game[ft_idx]
			ft_data = fts.split('-')
			ftm = int(ft_data[0])
			fta = int(ft_data[1])
			ft_rate = round(float(game[ft_rate_idx]), 1)

			bs = int(game[b_idx])
			ss = int(game[s_idx])
			fs = int(game[f_idx])
			tos = int(game[to_idx])

			all_pts.append(pts)
			all_rebs.append(rebs)
			all_asts.append(asts)

			all_winning_scores.append(winning_score)
			all_losing_scores.append(losing_score)

			all_minutes.append(minutes)
			all_fgms.append(fgm)
			all_fgas.append(fga)
			all_fg_rates.append(fg_rate)
			all_threes_made.append(threes_made)
			all_threes_attempts.append(threes_attempts)
			all_three_rates.append(three_rate)
			all_ftms.append(ftm)
			all_ftas.append(fta)
			all_ft_rates.append(ft_rate)
			all_bs.append(bs)
			all_ss.append(ss)
			all_fs.append(fs)
			all_tos.append(tos)

			all_stats = [all_pts,all_rebs,all_asts,all_winning_scores,all_losing_scores,all_minutes,all_fgms,all_fgas,all_fg_rates,all_threes_made,all_threes_attempts,all_three_rates,all_ftms,all_ftas,all_ft_rates,all_bs,all_ss,all_fs,all_tos]

	else:
		print("Warning: No player games data!")

	return all_stats

def read_projected_lines(raw_projected_lines, all_player_teams, player_of_interest=''):
	# convert raw projected lines to projected lines
	header_row = ['Name', 'PTS', 'REB', 'AST', '3PT', 'BLK', 'STL', 'TO','LOC','OPP']

	all_game_lines_dicts = {} # each stat separately
	# split columns in raw projected lines so we can loop thru each stat separately
	pts_projected_lines = []
	reb_projected_lines = []
	ast_projected_lines = []
	three_projected_lines = []
	blk_projected_lines = []
	stl_projected_lines = []
	to_projected_lines = []

	for line in raw_projected_lines:
		print('raw line: ' + str(line))
		pts_line = line[:3]
		pts_projected_lines.append(line[:3])
		reb_projected_lines.append(line[3:6])
		ast_projected_lines.append(line[6:9])
		three_projected_lines.append(line[9:12])
		blk_projected_lines.append(line[12:15])
		stl_projected_lines.append(line[15:18])
		to_projected_lines.append(line[18:21])

	separate_projected_lines = { 'pts':pts_projected_lines, 'reb':reb_projected_lines, 'ast':ast_projected_lines, 'three':three_projected_lines, 'blk':blk_projected_lines, 'stl':stl_projected_lines, 'to':to_projected_lines }
	print('separate_projected_lines: ' + str(separate_projected_lines))
	
	all_player_lines = [header_row]

	#game_lines_dict = {} # { 'PHO SunsatDAL MavericksTODAY 1:10PM': [['Chris Paul', 'O 9.5  +105', 'U 9.5  −135'],..]}

	# raw_projected_lines: [['PHO SunsatDAL MavericksTODAY 1:10PM'], ['PLAYER', 'OVER', 'UNDER'], ['Chris Paul', 'O 9.5  +105', 'U 9.5  −135']]
	# assign player lines to a game so we can get loc and opp from game info key
	for stat_name, projected_lines in separate_projected_lines.items():
		if len(projected_lines[0]) > 0:
			print('stat_name: ' + stat_name)
			game_key = ''
			game_lines_dict = {} # { 'PHO SunsatDAL MavericksTODAY 1:10PM': [['Chris Paul', 'O 9.5  +105', 'U 9.5  −135'],..]}
		
			for row in projected_lines:
				# loop thru rows until we see header. then make header key in dict and add next rows to list of values until next header
				# if first item = 'PLAYER' skip bc not needed header
				# then if first 3 letters are uppercase we know it is team matchup header w/ needed info
				player_initials = ['og','cj','pj','rj']
				print('row: ' + str(row))
				if len(row) > 0:
					if row[0] != 'PLAYER' and row[0].lower() != 'na':
						if row[0][:3].isupper() and row[0][:2].lower() not in player_initials:
							#print('found header: ' + str(row) + ', ' + row[0][:3])
							game_key = row[0]
							# if not game_key in game_lines_dict.keys():
							#     game_lines_dict[game_key] = []

						else:
							#print('found player line: ' + str(row))
							if game_key in game_lines_dict.keys():
								game_lines_dict[game_key].append(row)
							else:
								game_lines_dict[game_key] = [row]

			#print("game_lines_dict: " + str(game_lines_dict))
			all_game_lines_dicts[stat_name] = game_lines_dict

	print("all_game_lines_dicts: " + str(all_game_lines_dicts))

	# for now set unavailable stats=1, until we have basic fcns working
	reb = 1
	ast = 1
	three = 1
	blk = 1
	stl = 1
	to = 1

	all_player_lines_dicts = {} # {'player name':{pts:0,reb:0,..}}

	# game info = 'PHO SunsatDAL MavericksTODAY 1:10PM'
	for stat_name, game_lines_dict in all_game_lines_dicts.items():

		print('stat_name: ' + stat_name)

		for game_info, game_lines in game_lines_dict.items():
			print('game_info: ' + str(game_info))
			teams = game_info.split('at')
			away_team = teams[0]
			home_team = teams[1]
			#print("away_team: " + str(away_team))
			#print("home_team: " + str(home_team))

			irregular_abbrevs = {'bro':'bkn', 'okl':'okc', 'nor':'nop', 'pho':'phx', 'was':'wsh', 'uth': 'uta' } # for these match the first 3 letters of team name instead

			away_abbrev = away_team.split()[0].lower()
			if len(away_abbrev) == 2:
				away_abbrev = away_abbrev + away_team.split()[1][0].lower()

			if away_abbrev in irregular_abbrevs.keys():
				#print("irregular abbrev: " + team_abbrev)
				away_abbrev = irregular_abbrevs[away_abbrev]

			home_abbrev = home_team.split()[0].lower()
			if len(home_abbrev) == 2:
				home_abbrev = home_abbrev + home_team.split()[1][0].lower()
			if home_abbrev in irregular_abbrevs.keys():
				#print("irregular abbrev: " + team_abbrev)
				home_abbrev = irregular_abbrevs[home_abbrev]

			print("away_abbrev: " + str(away_abbrev))
			print("home_abbrev: " + str(home_abbrev))

			for raw_player_line in game_lines:

				# each stat has 3 columns pts, reb, ast,...
				# but not all players have all stats so the lines do not line up
				# so we must divide each stat and sort by player name

				player_name = raw_player_line[0].lower()
				print("player_name: " + str(player_name))
				#if player_name in all_player_teams.keys():

				

				if player_name != '':
					if player_name in all_player_teams.keys():
						player_team_abbrev = all_player_teams[player_name]
						print("player_team_abbrev: " + str(player_team_abbrev))
						# determine opponent from game info by eliminating player's team from list of 2 teams
						loc = 'home'
						opp = away_abbrev
						if player_team_abbrev == away_abbrev:
							loc = 'away'
							opp = home_abbrev
						# only add loc and opp once per player per game
						if not player_name in all_player_lines_dicts.keys():
							all_player_lines_dicts[player_name] = { 'loc': loc, 'opp': opp }
						else:
							all_player_lines_dicts[player_name]['loc'] = loc 
							all_player_lines_dicts[player_name]['opp'] = opp

						

						stat = math.ceil(float(raw_player_line[1].split()[1])) # O 10.5 +100
						#print("pts: " + str(pts))
						#reb = math.ceil(float(raw_player_line[4].split()[1])) # O 10.5 +100

						all_player_lines_dicts[player_name][stat_name] = stat
					else:
						print('Warning: No player name ' + player_name + ' not in teams dict while reading projected lines!')
						print("raw_player_line: " + str(raw_player_line))
				else:
					print('Warning: No player name while reading projected lines!')
					print("raw_player_line: " + str(raw_player_line))


	print("all_player_lines_dicts: " + str(all_player_lines_dicts))

	for player_name, player_lines in all_player_lines_dicts.items():
		#header_row = ['Name', 'PTS', 'REB', 'AST', '3PT', 'BLK', 'STL', 'TO','LOC','OPP']
		pts = 10
		if 'pts' in player_lines.keys():
			pts = player_lines['pts']
		reb = 2
		if 'reb' in player_lines.keys():
			reb = player_lines['reb']
		ast = 2
		if 'ast' in player_lines.keys():
			ast = player_lines['ast']
		three = 1
		if 'three' in player_lines.keys():
			three = player_lines['three']
		blk = 1
		if 'blk' in player_lines.keys():
			blk = player_lines['blk']
		stl = 1
		if 'stl' in player_lines.keys():
			stl = player_lines['stl']
		to = 1
		if 'to' in player_lines.keys():
			to = player_lines['to']
		
		loc = player_lines['loc']
		opp = player_lines['opp']
		player_line = [player_name, pts, reb, ast, three, blk, stl, to, loc, opp]

		# if certain players of interest, keep only their lines for analysis
		if player_of_interest == '': # get all players
			all_player_lines.append(player_line)
		elif player_of_interest == player_name:
			all_player_lines.append(player_line)
		
	print("all_player_lines:\n" + tabulate(all_player_lines))
	return all_player_lines