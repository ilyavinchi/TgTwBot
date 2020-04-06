import pickle
from shutil import rmtree
from os import remove, system, listdir, mkdir
from os.path import exists, abspath
from time import sleep, gmtime, strftime, time, timezone, altzone, ctime
from random import choice, randint
from json import dump, load, dumps, loads
from math import ceil
from threading import Thread

import clipboard
from uuid import uuid1
from requests import get
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from names import get_full_name
from telebot import TeleBot


ALPHABET = list('abcdefghijklmnopqrstuvwxyz')
OFFER_LINK = "http://wait3seconds.ga/"
MAX_FOLLOWING_THREADS = 0
POSTS_PER_DAY = 8
PAUSE_BETWEEN_POSTS = ceil(24 / POSTS_PER_DAY) * 3600
COUNT_OF_FOLLOW_THREADS = 5
PARSE_AT_A_TIME = 5
SEND_PARSING_TEXT = "(nude OR sex OR tits)"
PAUSE_BETWEEN_FOLLOWINGS = [60, 90]
MAX_FOLLOWING_PER_DAY = 300
USERTELEGRAMID = -415164113
HELPER = '''/start - выведет именна всех ботов
/off - выведет именна всех не активных ботов
/active - выведет именна всех активных ботов
/s - Включить бота
/b - Узнать баланс
/code - Получить код активации аккаунта
/new - Создает новый аккаунт (если хватает ДЕНЮЖЕК)
/del - Удаляет аккаунт
/stat - Высвечивает статистику всех ботов
/pcheck - Показывает включенна ли пауза
/autoposting - Запускает автопостинг
/autofollowing - Запускает автофолловинг'''
active_bots_following = []
active_bots_posting = []
autoposting_mode = True
autofollowing_mode = True
def jload(jload_path):
	if exists(jload_path):
		while True:
			try:
				with open(jload_path, "r") as f:
					return load(f) 
			except Exception as e:
				print(e)
				sleep(0.1)
				continue
	else:
		return
def jdump(jdump_path, what_dump):
	if exists(jdump_path.replace(jdump_path.split("/")[-1], "")):
		while True:
			try:
				with open(jdump_path, "w") as f:
					dump(what_dump, f)
				return True
			except:
				sleep(0.1)
				continue
	else:
		return
def pload(pload_path):
	if exists(pload_path):
		while True:
			try:
				with open(pload_path, "rb") as f:
					return pickle.load(f) 
			except:
				time.sleep(1)
				continue
	else:
		return
def pdump(pdump_path, what_dump):
	if exists(pdump_path.replace(pdump_path.split("/")[-1], "")):
		while True:
			try:
				with open(pdump_path, "wb") as f:
					pickle.dump(what_dump, f)     
				return True
			except:
				time.sleep(1)
				continue
	else:
			return

bnames = listdir("Bots/")
for x in bnames:
	jdump("Bots/" + x + "/stat.json", {"Followings": "OFF", "Posts": "OFF"})
	jdump("Bots/" + x + "/pause.json", 0)
	# jdump("Bots/" + x + "/base.json", [])

def changearrayval(changefile_path, change_key, change_val):
	if exists(changefile_path):
		while True:
			try:
				filearray = jload(changefile_path)
				filearray[change_key] = change_val
				jdump(changefile_path, filearray)
				break
			except:
				time.sleep(0.1)
				continue
	else:
		raise Exception('Файл не существует')
def removearrayval(changefile_path, remove_val):
	if exists(changefile_path):
		while True:
			try:
				filearray = jload(changefile_path)
				if type(filearray) is list:
					filearray.remove(remove_val)
				elif type(filearray) is dict:
					filearray.pop(remove_val)
				else:
					print('Неизвестный тип файла')
					return
				jdump(changefile_path, filearray)
				break
			except:
				sleep(0.1)
				continue
	else:
		raise Exception('Файл не существует')
def removefiles(*files_pathes):
	for x in files_pathes:
		remove(x)

def driver_start_empty(start_url, headless_mode = True):
	options = Options()
	options.add_argument("--disable-notifications")
	options.add_argument("--disable-extensions")
	headless = headless_mode
	if headless:
		options.add_argument('--headless')
		options.add_argument('--disable-gpu')
	options.add_experimental_option("useAutomationExtension", False)
	driver = Chrome("chromedriver.exe", options = options)
	driver.set_window_size(1366, 768) if headless == True else driver.maximize_window() 
	driver.get(start_url)
	return driver
def driver_start(bot_name, headless_mode = True):
	options = Options()
	options.add_argument("--disable-notifications")
	options.add_argument("--disable-extensions")
	headless = headless_mode
	if headless:
		options.add_argument('--headless')
		options.add_argument('--disable-gpu')
	options.add_experimental_option("useAutomationExtension", False)
	driver = Chrome("chromedriver.exe", options = options)
	driver.set_window_size(1366, 768) if headless == True else driver.maximize_window() 
	driver.get("https://twitter.com/login")
	for cookie in pickle.load(open("Bots/" + bot_name + "/cookie.pkl", "rb")):
		if 'expiry' in cookie:
			del cookie['expiry']
			driver.add_cookie(cookie)
	driver.refresh()
	return driver
def wait(dr, el_info, tries, wait_type):
	if wait_type == 1:
		for x in range(tries*10):
			try:
				elem = dr.find_element(By.XPATH, el_info)
				return elem
			except:
				sleep(0.1)
	elif wait_type == 2:
		for x in range(tries*10):
			try:
				elem = dr.find_elements(By.XPATH, el_info)
				return elem
			except:
				sleep(0.1)
	return False
def cookie_creator(cname):
	driver = driver_start_empty("https://twitter.com/login", False)
	input("Готово?: ", )
	pdump("Bots/"+cname+"/cookie.pkl", driver.get_cookies())
	driver.quit()
def test_account(t_name):
	driver = driver_start(t_name, False)
	print("READY")
	input()
	driver.quit()
def balance():
	b = get('http://api.sms-reg.com/getBalance.php?apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
	b = b.text
	json_b = loads(b)
	if int(json_b["balance"].split(".")[0]) > 4:
		return True
	else:
		return

def url_shortener(bot_name):
	driver = driver_start_empty("https://is.gd/create.php")
	link_to_shorter = OFFER_LINK
	wait(driver, '//input[@class="urlbox"]', 10, 1).send_keys(link_to_shorter)
	wait(driver, "//div[@id='shorturllabel']/label", 10, 1).click()

	bot_name = bot_name.split(" ")[0] + bot_name.split(" ")[1]
	link_save = bot_name + '_' + str(uuid1()).replace("-", "")[:6]
	driver.find_element(By.XPATH , "//input[@class='shorturlbox']").send_keys(link_save)
	driver.find_element(By.XPATH, "//input[@id='logstats']").send_keys(Keys.SPACE)
	driver.find_element(By.XPATH , "//input[@class='submitbutton']").submit()
	link_save = wait(driver, '//input[@id="short_url"]', 10, 1).get_attribute("value")
	return link_save
def url_shortener_main(bot_name):
	driver = driver_start_empty("https://is.gd/create.php")
	link_to_shorter = OFFER_LINK
	wait(driver, '//input[@class="urlbox"]', 10, 1).send_keys(link_to_shorter)
	wait(driver, "//div[@id='shorturllabel']/label", 10, 1).click()

	bot_name = bot_name.split(" ")[0] + bot_name.split(" ")[1]
	link_save = bot_name
	driver.find_element(By.XPATH , "//input[@class='shorturlbox']").send_keys(link_save)
	driver.find_element(By.XPATH, "//input[@id='logstats']").send_keys(Keys.SPACE)
	driver.find_element(By.XPATH , "//input[@class='submitbutton']").submit()
	link_save = wait(driver, '//input[@id="short_url"]', 10, 1).get_attribute("value")
	return link_save
def autoposting(autoposting_bot_name):
	try:
		while True:
			changearrayval("Bots/" + autoposting_bot_name + "/stat.json", "Posts", "WORKS")
			bot.send_message(USERTELEGRAMID, autoposting_bot_name + " AUTOPOSTING START")
			account_settings = jload("Bots/" + autoposting_bot_name + "/settings.json")
			driver = driver_start(autoposting_bot_name, False)
			driver.get(account_settings["URL"])
			alboms = wait(driver, '//div[@class="gal_list"]', 10, 2)
			alboms[account_settings["ALBOM ID"]].click()
			photos = wait(driver, '//div[@class="gal_list"]', 10, 2)
			photos[account_settings["PHOTO ID"]].click()
			URL = wait(driver, '//img', 10, 1).get_attribute("src")
			account_settings["PHOTO ID"] += 1
			if account_settings["PHOTO ID"] == len(photos):
				if (account_settings["ALBOM ID"] + 1) > len(alboms) - 1:
					account_settings["PHOTO ID"] = 0
					account_settings["ALBOM ID"] = 0
				else:
					account_settings["PHOTO ID"] = 0
					account_settings["ALBOM ID"] += 1
			jdump("Bots/" + autoposting_bot_name + "/settings.json", account_settings)

			driver.get("https://twitter.com/home")	

			picture_req = get(URL)
			img_name = str(uuid1()).replace("-", "")[:4]
			if picture_req.status_code == 200:
				with open(img_name+".jpg", 'wb') as f:
					f.write(picture_req.content)

			system("nconvert -out jpeg -o %_.jpg -q 95 -rmeta -rexifthumb -noise uniform 0.1 "+img_name+".jpg")
			wait(driver, '//input[@type="file"]', 10, 1).send_keys(abspath(img_name+"_.jpg"))

			with open("texts.txt", 'r', encoding="utf-8") as f:
				all_texts = f.read().split("\n\n")
			contents_from_file = all_texts[randint(0, len(all_texts) - 1)] + url_shortener(autoposting_bot_name)
			clipboard.copy(contents_from_file)
			wait(driver, '//div[@role="textbox"]', 10, 1).send_keys(Keys.CONTROL, 'v')

			wait(driver, '//div[@data-testid="tweetButtonInline"]', 10, 1).click()
			sleep(5)
			changearrayval("Bots/" + autoposting_bot_name + "/stat.json", "Posts", "Next post: " + strftime("%X", gmtime(time() - timezone + PAUSE_BETWEEN_POSTS)))
			remove(img_name+".jpg")
			remove(img_name+"_.jpg")
			driver.quit()
			sleep(PAUSE_BETWEEN_POSTS)
	except Exception as e:
		changearrayval("Bots/" + autoposting_bot_name + "/stat.json", "Posts", "ERROR")
		active_bots_posting.remove(autoposting_bot_name)
		driver.quit()
		settings = jload("Bots/" + autoposting_bot_name + "/settings.json")
		s_m = "Account banned"
		for x in settings:
			s_m = s_m + '\n' + str(x) + ": " + str(settings[x])
		bot.send_message(USERTELEGRAMID, s_m)
		return
def delete_last_post(delete_last_post_name):
	driver = driver_start(delete_last_post_name, False)
	wait(driver, '//header[@role="banner"]//nav[@role="navigation"]/a[7]', 10, 1).click()
	wait(driver, '//div[@data-testid="primaryColumn"]//div[@data-testid="caret"]', 10, 1).click()
	wait(driver, '//div[@role="menu"]/div/div/div/div[1]', 10, 1).click()
	wait(driver, '//div[@data-testid="confirmationSheetConfirm"]', 10, 1).click()
	sleep(10)
	driver.quit()

def parsing(dr):
	try:
		driver = dr
		wait(driver, '//a[@data-testid="AppTabBar_Explore_Link"]/div', 10, 1).click()
		el = wait(driver, "//input[@data-testid='SearchBox_Search_Input']", 10, 1)
		el.click()
		el.send_keys(SEND_PARSING_TEXT)
		el.send_keys(Keys.ENTER)
		wait(driver, '//nav/div[@role="tablist"]/div[2]/a/div', 10, 1).click()
		driver.refresh()
		driver.refresh()
		for x in range(60):
			try:
				logins = wait(driver, '//div[@data-testid="tweet"]/div/div/div/div/div/div/a/div/div[2]', 10, 2)
				ready_logins = []
				for i in range(PARSE_AT_A_TIME):
					user_name = logins[i].text.replace("@", "")
					if user_name:
						ready_logins.append(user_name)
				return ready_logins
			except:
				sleep(1)
				continue
	except:
		raise Exception("Ошибка парсинга")

def autofollowing(autofollowing_bot_name, follow_mode = 0, last_count = 0):
	try:
		changearrayval("Bots/" + autofollowing_bot_name + "/stat.json", "Followings", "START")
		jdump("Bots/" + autofollowing_bot_name + "/pause.json", time() + 86400)
		bot.send_message(USERTELEGRAMID, autofollowing_bot_name + " AUTOFOLLOWING START")
		driver = driver_start(autofollowing_bot_name, True)
		count_of_followings = last_count
		count_of_unfollowings = last_count
		following_base = []
		following_save_base = jload("Bots/" + autofollowing_bot_name + "/base.json")
		mode = follow_mode
		if len(following_save_base) < 4500 and mode == 0:
			while count_of_followings < MAX_FOLLOWING_PER_DAY:
				if len(following_base) == 0:
					changearrayval("Bots/" + autofollowing_bot_name + "/stat.json", "Followings", "PARSING")
					following_base = parsing(driver)

				driver.get("https://twitter.com/" + following_base[0])
				if wait(driver, "//div[@data-testid='placementTracking']", 10, 1) and wait(driver, "//div[@data-testid='placementTracking']", 10, 1).text == "Follow":
					wait(driver, "//div[@data-testid='placementTracking']", 10, 1).click()
					if wait(driver, '//div[@role="alert"]', 3, 1):
						raise Exception('Аккаунт забанен')
					else:
						following_save_base = jload("Bots/" + autofollowing_bot_name + "/base.json")
						following_save_base.append(following_base[0])
						jdump("Bots/" + autofollowing_bot_name + "/base.json", following_save_base)
						count_of_followings += 1
						following_base.pop(0)
						changearrayval("Bots/" + autofollowing_bot_name + "/stat.json", "Followings", str(count_of_followings) + "/" + str(MAX_FOLLOWING_PER_DAY))
						if count_of_followings == MAX_FOLLOWING_PER_DAY:
							changearrayval("Bots/" + autofollowing_bot_name + "/stat.json", "Followings", "End Following Successful")
							active_bots_following.remove(autofollowing_bot_name)
							jdump("Bots/" + autofollowing_bot_name + "/pause.json", time() + 86400)
							bot.send_message(USERTELEGRAMID, "Бот " + autofollowing_bot_name + " закончил автоподписку")
							return True, 0
						else:
							sleep(randint(PAUSE_BETWEEN_FOLLOWINGS[0], PAUSE_BETWEEN_FOLLOWINGS[1]))
				else:
					following_base.pop(0)
		else:
			mode = 1
			changearrayval("Bots/" + autofollowing_bot_name + "/stat.json", "Followings", "UNFOLLOWING")
			while count_of_unfollowings < 300:
				following_save_base = jload("Bots/" + autofollowing_bot_name + "/base.json")
				driver.get("https://twitter.com/" + following_save_base[0])
				if wait(driver, '//div[@data-testid="primaryColumn"]/div/div/div/div/div/div/div/div/div/div/div[2]', 10, 1):
					following_save_base.append(following_save_base.pop(0))
					jdump("Bots/" + autofollowing_bot_name + "/base.json", following_save_base)
				else:
					if wait(driver, "//div[@data-testid='placementTracking']", 10, 1):
						wait(driver, "//div[@data-testid='placementTracking']", 10, 1).click()
						if wait(driver, '//div[@role="alert"]', 3, 1):
							raise Exception('Аккаунт забанен')
						else:
							following_save_base.pop(0)
							jdump("Bots/" + autofollowing_bot_name + "/base.json", following_save_base)
							count_of_unfollowings += 1
					else:
						following_save_base.pop(0)
			mode = 0
			changearrayval("Bots/" + autofollowing_bot_name + "/stat.json", "Followings", "End Unfollowing Successful")
			active_bots_following.remove(autofollowing_bot_name)
			jdump("Bots/" + autofollowing_bot_name + "/pause.json", time() + 86400)
			bot.send_message(USERTELEGRAMID, "Бот " + autofollowing_bot_name + " закончил автоодписку")
			return True, 0
	except Exception as e:
		print(e)
		driver.quit()
		active_bots_following.remove(autofollowing_bot_name)
		changearrayval("Bots/" + autofollowing_bot_name + "/stat.json", "Followings", "ERROR")
		settings = jload("Bots/" + autofollowing_bot_name + "/settings.json")
		s_m = "Account banned"
		for x in settings:
			s_m = s_m + '\n' + str(x) + ": " + str(settings[x])
		bot.send_message(USERTELEGRAMID, s_m)
		jdump("Bots/" + autofollowing_bot_name + "/pause.json", time() + 86400)
		if mode == 0:
			return False, mode, count_of_followings
		elif mode == 1:
			return False, mode, count_of_unfollowings

def phone_gen():
	phone_numb_search = get('http://api.sms-reg.com/getNum.php?country=ru&service=twitter&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
	phone_numb_search = phone_numb_search.text
	json_phone_numb_search = loads(phone_numb_search)
	phone_search_tzid = json_phone_numb_search['tzid']
	for x in range(900):
		phone_numb_info = get('http://api.sms-reg.com/getState.php?tzid=' + phone_search_tzid + '&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
		phone_numb_info = phone_numb_info.text
		json_phone_numb_info = loads(phone_numb_info)
		if json_phone_numb_info['response'] == 'WARNING_NO_NUMS':
			return
		elif json_phone_numb_info['response'] == 'TZ_INPOOL':
			sleep(1)
		elif json_phone_numb_info['response'] == 'TZ_NUM_PREPARE':
			return "+" + json_phone_numb_info['number'], phone_search_tzid

	return
def sms_get(p_tzid):
	sms_ready = get('http://api.sms-reg.com/setReady.php?tzid=' + p_tzid + '&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
	for x in range(300):
		sms_info = get('http://api.sms-reg.com/getState.php?tzid=' + p_tzid + '&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
		sms_info = sms_info.text
		json_sms_info = loads(sms_info)
		if json_sms_info['response'] == 'TZ_NUM_ANSWER':
			return json_sms_info['msg']
		elif json_sms_info['response'] == "TZ_OVER_EMPTY" or json_sms_info['response'] == "TZ_DELETED":
			return 
		else:
			sleep(1)
	return 
def tcode(t_tzid):
	for n in range(300):
		enter_info = get('http://api.sms-reg.com/getNumRepeat.php?tzid=' + t_tzid + '&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
		enter_info = enter_info.text
		json_enter_info = loads(enter_info)
		if int(json_enter_info['response']) == 0:
			bot.send_message(USERTELEGRAMID, "Код не получен")
			return
		elif int(json_enter_info['response']) == 1:
			code = sms_get(json_enter_info['tzid'])
			if code:
				get('http://api.sms-reg.com/setOperationOk.php?tzid=' + json_enter_info['tzid'] + '&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
				bot.send_message(USERTELEGRAMID, "Код: " + code)
				return
			else:
				bot.send_message(USERTELEGRAMID, "Код не получен")
				return
		elif int(json_enter_info['response']) == 2:
			bot.send_message(USERTELEGRAMID, "Код не получен")
			return
		elif int(json_enter_info['response']) == 3:
			sleep(1)
	return

def url_to_imgs():
	letter_choice = choice(ALPHABET)
	driver = driver_start_empty("https://www.kindgirls.com/girls/?i=" + letter_choice, True)
	while True:
		sleep(1)
		letter_choice = choice(ALPHABET)
		driver.get("https://www.kindgirls.com/girls/?i=" + letter_choice)
		models = wait(driver, '//div[@class="model_list"]', 10, 2)
		if len(models) > 0:
			random_model = randint(0, len(models)-1)
		else:
			continue
		models[random_model].click()
		alboms = wait(driver, '//div[@class="gal_list"]', 10, 2)
		if len(alboms) > 8:
			clipboard.copy(driver.current_url)
			return driver.current_url
		else:
			continue

def pausecheker():
	while True:
		bots_names = listdir("Bots/")
		for x in bots_names:
			pause = jload("Bots/" + x + "/pause.json")
			if pause < time():
				bot.send_message(USERTELEGRAMID, x + ": Пауза закончилась")
		sleep(600)
def pause_actions():
	bot.send_message(USERTELEGRAMID, "Подождите 30 секунд")
	sleep(30)
	bot.send_message(USERTELEGRAMID, "Пауза завершилась")

# balance_info = get('http://api.sms-reg.com/getOperations.php?opstate=active&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
# balance_info = balance_info.text
# json_balance_info = loads(balance_info)

# acs = listdir("Bots/")
# for x in acs:
# 	driver = driver_start(x, False)
# 	a = jload("Bots/" + x + "/settings.json")
# 	print(x)

# for x in json_balance_info:
# 	print(x)
# 	# print(x["msg"])
# 	try:
# 		if x["phone"] == "79028000269":
# 			print("HI")
# 			print(x["phone"])
# 			print(x["tzid"])
# 			clipboard.copy(x["tzid"])
# 	except Exception as e:
# 		continue

def autoposting_loop():
	global active_bots_posting
	bots = listdir("Bots/")
	active_bots_posting.extend(bots)
	while True:
		for x in active_bots_posting:
			bot.send_message(USERTELEGRAMID, "Запущен Автопостинг " + str(active_bots_posting.index(x) + 1) + " из " + str(len(active_bots_posting)))
			Thread(target=autoposting, args=(x,)).start()
			bot.send_message(USERTELEGRAMID, "Пауза 30 сек")
			sleep(30)

		bot.send_message(USERTELEGRAMID, "Пауза автопостинг 3 часа начата")
		sleep(10800)
		bot.send_message(USERTELEGRAMID, "Пауза автопостинг 3 часа закончилась")

def autofollowing_loop():
	while True:
		if len(active_bots_following) < COUNT_OF_FOLLOW_THREADS:
			bots = listdir("Bots/")
			for x in bots:
				b_pause = jload("Bots/" + x + "/pause.json")
				if b_pause < time():
					active_bots_following.append(x)
					Thread(target=autofollowing, args=(x,)).start()
					break
				else:
					continue
		sleep(30)

# for x in listdir("Bots/"):
# 	test_account(x)	

bot = TeleBot('1107563794:AAHwpuyWE1JWF2ZLTfGp7pMnMmWX_ys8omw')

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.send_message(USERTELEGRAMID, HELPER)
	
@bot.message_handler(commands=['start'])
def send_welcome(message):
	bots_names = listdir("Bots/")
	s_m = "Имена ботов:"
	for x in bots_names:
		s_m = s_m + "\n" + x
	bot.send_message(USERTELEGRAMID, s_m)

@bot.message_handler(commands=['off'])
def send_welcome(message):
	bots_names = listdir("Bots/")
	for x in bots_names:
		if not x in active_bots_following:
			bot.send_message(USERTELEGRAMID, x + " автоподписка не включена")
		if not x in active_bots_posting:
			bot.send_message(USERTELEGRAMID, x + " автопостинг не включен")

@bot.message_handler(commands=['active'])
def send_welcome(message):
	bots_names = listdir("Bots/")
	for x in bots_names:
		if x in active_bots_following:
			bot.send_message(USERTELEGRAMID, x + " автоподписка включена")
		if x in active_bots_posting:
			bot.send_message(USERTELEGRAMID, x + " автопостинг включен")

@bot.message_handler(commands=['s'])
def send_welcome(message):
	bot.send_message(USERTELEGRAMID, 'Имя бота?: ')
	bot.register_next_step_handler(message, start_bot)

@bot.message_handler(commands=['b'])
def send_welcome(message):
	balance_info = get('http://api.sms-reg.com/getBalance.php?apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
	balance_info = balance_info.text
	json_balance_info = loads(balance_info)
	bot.send_message(USERTELEGRAMID, "Ваш балланс: " + json_balance_info['balance'])

@bot.message_handler(commands=['code'])
def send_welcome(message):
	bot.send_message(USERTELEGRAMID, 'Введите tzid: ')
	bot.register_next_step_handler(message, getcode)

@bot.message_handler(commands=['new'])
def send_welcome(message):
	if balance():
		bot.send_message(USERTELEGRAMID, "Создание началось")
		Thread(target=newaccount).start()
	else:
		bot.send_message(USERTELEGRAMID, "Пополните баланс")

@bot.message_handler(commands=['del'])
def send_welcome(message):
	bot.send_message(USERTELEGRAMID, 'Имя бота (удаление)?: ')
	bot.register_next_step_handler(message, delbot)

@bot.message_handler(commands=['stat'])
def send_welcome(message):
	bots_names = listdir("Bots/")
	for x in bots_names:
		try:
			bot_stat = jload("Bots/" + x + "/stat.json")
			bot.send_message(USERTELEGRAMID, "Имя бота: " + x + "\nПодписок: " + bot_stat["Followings"] + "\nСледующий пост: " + bot_stat["Posts"])
		except Exception as e:
			print(e)
			continue

@bot.message_handler(commands=['pcheck'])
def send_welcome(message):
	bots_names = listdir("Bots/")
	for x in bots_names:
		pause = jload("Bots/" + x + "/pause.json")
		if pause < time():
			bot.send_message(USERTELEGRAMID, x + ": Пауза закончилась")
		else:
			bot.send_message(USERTELEGRAMID, x + ": Пауза до " + ctime(pause))

@bot.message_handler(commands=['autoposting'])
def send_welcome(message):
	global autoposting_mode
	if autoposting_mode:
		Thread(target=autoposting_loop).start()
		bot.send_message(USERTELEGRAMID, "Автопостинг запущен!")
		autoposting_mode = False
	else:
		bot.send_message(USERTELEGRAMID, "Автопостинг уже запущен")

@bot.message_handler(commands=['autofollowing'])
def send_welcome(message):
	global autofollowing_mode
	if autofollowing_mode:
		Thread(target=autofollowing_loop).start()
		bot.send_message(USERTELEGRAMID, "Автофолловинг запущен!")
		autofollowing_mode = False
	else:
		bot.send_message(USERTELEGRAMID, "Автофолловинг уже запущен")

def start_bot(message):
	b_name = message.text
	if exists("Bots/" + b_name):
		pause = jload("Bots/" + b_name + "/pause.json")
		if not b_name in active_bots_following:
			if pause < time():
				active_bots_following.append(b_name)
				Thread(target=autofollowing, args=(b_name,)).start()
			else:
				bot.send_message(USERTELEGRAMID, "Пауза, вы сможете повторно запустить автофоловинг в: " + strftime("%X", gmtime(pause)))
		else:
			bot.send_message(USERTELEGRAMID, "Автофолловинг уже запущен")

		if not b_name in active_bots_posting:
			active_bots_posting.append(b_name)
			Thread(target=autoposting, args=(b_name,)).start()
			Thread(target=pause_actions).start()
		else:
			bot.send_message(USERTELEGRAMID, "Автопостинг уже запущен")
	else:
		bot.send_message(USERTELEGRAMID, "Неверное имя бота")
	# Thread(target=autoposting, args=(b_name,)).start()
def getcode(message):
	tzid = message.text
	Thread(target=tcode, args=(tzid,)).start()
def delbot(message):
	bname = message.text
	if exists("Bots/" + bname):
		rmtree("Bots/" + bname)
	else:
		bot.send_message(USERTELEGRAMID, "Файл не найден")

bot.polling()