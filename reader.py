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

# get data from a file and format into a list (same as generator version of this fcn but more general)
# input such as Game Data - All Games
# or Game Log - All Players
def extract_data(data_type, input_type, extension='csv', header=False):
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
		read_lines = lines
		if not header:
			read_lines = lines[1:]

		for line in read_lines:
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
def read_player_season_log(player_name, season_year=2023, player_url=''):
	print("\n===Read Player Game Log===\n")

	# get espn player id from google so we can get url
	if player_url == '':
		player_espn_id = read_player_espn_id(player_name)
		season_year = 2023
		player_url = 'https://www.espn.com/nba/player/gamelog/_/id/' + player_espn_id + '/type/nba/year/' + str(season_year) #.format(df_Players_Drafted_2000.loc[INDEX, 'ESPN_GAMELOG_ID'])
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

def read_player_season_logs(player_name, read_all_seasons=True):

	player_game_logs = []

	player_espn_id = read_player_espn_id(player_name)
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

def read_all_players_season_logs(player_names, read_all_seasons=True):

	all_players_season_logs = {}

	for player_name in player_names:
		players_season_logs = read_player_season_logs(player_name, read_all_seasons)
		all_players_season_logs[player_name] = players_season_logs

	return all_players_season_logs


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

def read_projected_lines(date):
	lines = []

	return lines


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