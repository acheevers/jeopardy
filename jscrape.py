# Import libraries
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import pandas as pd

game_test = "https://www.j-archive.com/showgame.php?game_id=6960"


def get_game_df(game_url):

	# scraping j-archive
	page = requests.get(game_url)
	soup = BeautifulSoup(page.content, 'html.parser')

	# initializing game_df
	game_df  = pd.DataFrame(
		columns=[
		'game_title',
		'clue_id',
		'clue_value',
		'clue_order_num',
		'clue_text',
		'correct_response',
		'cont_1_correct',
		'cont_2_correct',
		'cont_3_correct',
		'cont_1_wrong',
		'cont_2_wrong',
		'cont_3_wrong',
		'triple_stumper',
		'daily_double'
		]
		)

	# Get title
	print('getting title...')
	game_title = soup.find(id="game_title").get_text()

	# Get contestants
	print('getting contestants...')
	cont_list = soup.find_all('p', class_='contestants')
	cont_1 = cont_list[0].get_text().split(' ')[0]
	cont_2 = cont_list[1].get_text().split(' ')[0]
	cont_3 = cont_list[2].get_text().split(' ')[0]

	for clue in soup.find_all('td', class_ = 'clue'):
		for tag in clue.find_all(onmouseover=True):
			# get clue id
			clue_id = tag['onclick'].split('\'')[1]


			# get clue value
			daily_double = False

			try:
				clue_value = tag.find('td', class_ = 'clue_value').get_text()
			except:
				clue_value = tag.find('td', class_ = 'clue_value_daily_double').get_text()
				daily_double = True


			# get clue order
			clue_order_num = tag.find('td', class_ = 'clue_order_number').get_text()


			# get clue text
			clue_text = tag['onmouseout'].split(',')[2].lstrip(' \'').rstrip('\')')


			# get clue response
			correct_response = tag['onmouseover'].split('class=\"correct_response\">')[1].split('/')[0]
			correct_response = correct_response.replace('<i>', '').split('<')[0]


			triple_stumper = False
			cont_1_correct = False
			cont_2_correct = False
			cont_3_correct = False
			cont_1_wrong = False
			cont_2_wrong = False
			cont_3_wrong = False

			# get who answered
			try:
				correct_person = tag['onmouseover'].split('class="right">')[1].split('<')[0]
			except:
				correct_person = None
			if correct_person == cont_1:
				cont_1_correct = True
			elif correct_person == cont_2:
				cont_2_correct = True
			elif correct_person == cont_3:
				cont_3_correct = True

			try:
				wrong_person_list = tag['onmouseover'].split('class="wrong">')[1:]
				for i in wrong_person_list:
					i = i.split('<')[0]

					if 'Triple Stumper' in i:
						triple_stumper = True
						del wrong_person_list[i]

					if i == cont_1:
						cont_1_wrong = True
					if i == cont_2:
						cont_2_wrong = True
					if i == cont_3:
						cont_3_wrong = True


			except:
				wrong_person_list = None


			game_df = game_df.append({
					'game_title': game_title,
					'clue_id': clue_id,
					'clue_value': clue_value,
					'clue_order_num': clue_order_num,
					'clue_text': clue_text,
					'correct_response': correct_response,
					'cont_1_correct': cont_1_correct,
					'cont_2_correct': cont_2_correct,
					'cont_3_correct': cont_3_correct,
					'cont_1_wrong': cont_1_wrong,
					'cont_2_wrong': cont_2_wrong,
					'cont_3_wrong': cont_3_wrong,
					'triple_stumper': triple_stumper,
					'daily_double': daily_double
				}, ignore_index=True)

	return game_df

def get_game_info(game_url):

	# scraping j-archive
	page = requests.get(game_url)
	soup = BeautifulSoup(page.content, 'html.parser')

	# initializing game_info_df
	game_info_df  = pd.DataFrame(
		columns=[
		'game_title',
		'contestant',
		'comm_break',
		'r1',
		'r2',
		'final',
		'coryat'
		]
		)

	# Get title
	game_title = soup.find(id="game_title").get_text()

	# Get contestants
	cont_list = soup.find_all('p', class_='contestants')
	cont_1 = cont_list[0].get_text()
	cont_2 = cont_list[1].get_text()
	cont_3 = cont_list[2].get_text()

	# Getting checkpoint scores
	print('getting checkpoint scores...')

	# After commercial break
	round1 = soup.find(id = 'jeopardy_round')
	tables1 =  round1.find_all('table')
	comm_break_list = tables1[len(tables1)-2].find_all('td')
	comm_break_list = comm_break_list[3:]

	cont_1_comm_break = comm_break_list[0].get_text()
	cont_2_comm_break = comm_break_list[1].get_text()
	cont_3_comm_break = comm_break_list[2].get_text()

	# At end of board 1
	r1_list = tables1[len(tables1)-1].find_all('td')
	r1_list = r1_list[3:]

	cont_1_r1 = r1_list[0].get_text()
	cont_2_r1 = r1_list[1].get_text()
	cont_3_r1 = r1_list[2].get_text()

	# At end of double jeopardy
	tables =  soup.find_all('table')
	r2_list = tables[len(tables)-6].find_all('td')
	r2_list = r2_list[3:]

	cont_1_r2 = r2_list[0].get_text()
	cont_2_r2 = r2_list[1].get_text()
	cont_3_r2 = r2_list[2].get_text()

	# Final score
	final_list = tables[len(tables)-2].find_all('td')
	final_list = final_list[3:]

	cont_1_final = final_list[0].get_text()
	cont_2_final = final_list[1].get_text()
	cont_3_final = final_list[2].get_text()	

	# coryat score
	coryat_list = tables[len(tables)-1].find_all('td')
	coryat_list = coryat_list[3:]

	cont_1_coryat = coryat_list[0].get_text()
	cont_2_coryat = coryat_list[1].get_text()
	cont_3_coryat = coryat_list[2].get_text()

	# contestant 1
	game_info_df = game_info_df.append({
		'game_title': game_title,
		'contestant': cont_1,
		'comm_break': cont_1_comm_break,
		'r1': cont_1_r1,
		'r2': cont_1_r2,
		'final': cont_1_final,
		'coryat': cont_1_coryat
		}, ignore_index = True)

	# contestant 2
	game_info_df = game_info_df.append({
		'game_title': game_title,
		'contestant': cont_2,
		'comm_break': cont_2_comm_break,
		'r1': cont_2_r1,
		'r2': cont_2_r2,
		'final': cont_2_final,
		'coryat': cont_2_coryat
		}, ignore_index = True)

	# contestant 3
	game_info_df = game_info_df.append({
		'game_title': game_title,
		'contestant': cont_3,
		'comm_break': cont_3_comm_break,
		'r1': cont_3_r1,
		'r2': cont_3_r2,
		'final': cont_3_final,
		'coryat': cont_3_coryat
		}, ignore_index = True)

	return game_info_df

def get_game_categories(game_url):

	# scraping j-archive
	page = requests.get(game_url)
	soup = BeautifulSoup(page.content, 'html.parser')

	# initializing game_info_df
	game_cats_df  = pd.DataFrame(
		columns=[
		'game_title',
		'r1_cat1',
		'r1_cat2',
		'r1_cat3',
		'r1_cat4',
		'r1_cat5',
		'r1_cat6',
		'r2_cat1',
		'r2_cat2',
		'r2_cat3',
		'r2_cat4',
		'r2_cat5',
		'r2_cat6',
		'final_jeopardy'
		]
		)

	# Get title
	game_title = soup.find(id="game_title").get_text()

	cats_list = soup.find_all('td', class_='category_name')

	game_cats_df = game_cats_df.append({
		'game_title': game_title,
		'r1_cat1': cats_list[0].get_text(),
		'r1_cat2': cats_list[1].get_text(),
		'r1_cat3': cats_list[2].get_text(),
		'r1_cat4': cats_list[3].get_text(),
		'r1_cat5': cats_list[4].get_text(),
		'r1_cat6': cats_list[5].get_text(),
		'r2_cat1': cats_list[6].get_text(),
		'r2_cat2': cats_list[7].get_text(),
		'r2_cat3': cats_list[8].get_text(),
		'r2_cat4': cats_list[9].get_text(),
		'r2_cat5': cats_list[10].get_text(),
		'r2_cat6': cats_list[11].get_text(),
		'final_jeopardy': cats_list[12].get_text()
		}, ignore_index = True)

	return game_cats_df

# saving csvs
# test = get_game_df(game_test)
# test.to_csv('game_df.csv')
# game_info_test = get_game_info(game_test)
# game_info_test.to_csv('game_info_df.csv')
game_cats_test = get_game_categories(game_test)
game_cats_test.to_csv('cats_info_df.csv')



# To do:
# - Then, broaden to all games/seasons (go incrementally on game_id, make sure to do 2 second pause or something)