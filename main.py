import pickle
from shutil import rmtree
from os import remove, system, listdir, mkdir
from os.path import exists, abspath
from time import sleep, gmtime, strftime, time, timezone, altzone, ctime
from random import choice, randint
from json import dump, load, dumps, loads
from math import ceil

import clipboard
from uuid import uuid1
from requests import get
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from names import get_full_name
from telebot import TeleBot
from threading import Thread

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
/pcheck - Показывает включенна ли пауза'''
active_bots_following = []
active_bots_posting = []

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
			driver.get(account_settings["IMG URL"])
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
			if picture_req.status_code == 200:
				with open("3.jpg", 'wb') as f:
					f.write(picture_req.content)

			system("nconvert -out jpeg -o %_.jpg -q 95 -rmeta -rexifthumb -noise uniform 0.1 3.jpg")
			wait(driver, '//input[@type="file"]', 10, 1).send_keys(abspath("3_.jpg"))

			with open("texts.txt", 'r', encoding="utf-8") as f:
				all_texts = f.read().split("\n\n")
			contents_from_file = all_texts[randint(0, len(all_texts) - 1)] + url_shortener(autoposting_bot_name)
			clipboard.copy(contents_from_file)
			wait(driver, '//div[@role="textbox"]', 10, 1).send_keys(Keys.CONTROL, 'v')

			wait(driver, '//div[@data-testid="tweetButtonInline"]', 10, 1).click()
			sleep(5)
			changearrayval("Bots/" + autoposting_bot_name + "/stat.json", "Posts", "Next post: " + strftime("%X", gmtime(time() - timezone + PAUSE_BETWEEN_POSTS)))
			remove("3.jpg")
			remove("3_.jpg")
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
def autofollowing(autofollowing_bot_name, follow_mode = 0, last_count = 0):
	try:
		changearrayval("Bots/" + autofollowing_bot_name + "/stat.json", "Followings", "START")
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
		changearrayval("Bots/" + autofollowing_bot_name + "/stat.json", "Followings", "ERROR")
		settings = jload("Bots/" + autofollowing_bot_name + "/settings.json")
		s_m = "Account banned"
		for x in settings:
			s_m = s_m + '\n' + str(x) + ": " + str(settings[x])
		bot.send_message(USERTELEGRAMID, s_m)
		
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
	while True:
		letter_choice = choice(ALPHABET)
		driver = driver_start_empty("https://www.kindgirls.com/girls/?i=" + letter_choice, True)
		while True:
			sleep(1)
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
				driver.get("https://www.kindgirls.com/girls/?i=" + letter_choice)
				continue
def newaccount():
	try:
		# Получение телефона
		print("TRY GET PHONE")
		phone, tzid = phone_gen()
		if phone:
			print(phone)
			driver = driver_start_empty("https://twitter.com/i/flow/signup", False)
			name = get_full_name(gender='female')
			wait(driver, "//input[@type='text']", 60, 1).send_keys(name)
			wait(driver, "//input[@type='tel']", 60, 1).send_keys(phone)

			if wait(driver, "//div[@role='group']/div/div/div[1]/div/select/option[@value='" + str(randint(1,12))+"']", 2, 1):
				wait(driver, "//div[@role='group']/div/div/div[1]/div/select/option[@value='" + str(randint(1,12))+"']", 10, 1).click()
				wait(driver, "//div[@role='group']/div/div/div[2]/div/select/option[@value='" + str(randint(1,28))+"']", 10, 1).click()
				wait(driver, "//div[@role='group']/div/div/div[3]/div/select/option[@value='" + str(randint(1996,2001))+"']", 10, 1).click()

			while not wait(driver, "//div[@data-testid='confirmationSheetConfirm']", 1, 1):
				wait(driver, '//div[@aria-labelledby="modal-header"]/*//div[@role="button"]/div/span/span', 1, 1).click()
			wait(driver, "//div[@data-testid='confirmationSheetConfirm']", 1, 1).click()
			print("TRY GET CODE")
			code = sms_get(tzid)
			if not code:
				raise Exception("Код не пришел")
			wait(driver, "//input[@name='verfication_code']", 10, 1).send_keys(code)
			wait(driver, "//div/div/div/div[@role='button']/div/span/span", 10, 1).click()
			password = str(uuid1()).replace("-", "")[:8]
			print(password)
			wait(driver, "//input[@name='password']", 10, 1).send_keys(password)
			while wait(driver, "//div/div/div/div[@role='button']/div/span/span", 1, 1):
				wait(driver, "//div/div/div/div[@role='button']/div/span/span", 1, 1).click()
			driver.get("https://twitter.com/home")
			mkdir("Bots/" + name)
			pdump("Bots/"+name+"/cookie.pkl", driver.get_cookies())
			driver.get("https://twitter.com/settings/screen_name")
			split_name = name.split(" ")
			try_combinations = [split_name[0] + split_name[1], split_name[1] + split_name[0], split_name[1] +"_"+ split_name[0], split_name[0] +"_"+ split_name[1], split_name[1] + split_name[0] + "_", split_name[0] + split_name[1] + "_", split_name[0] + "_" + split_name[1] + "_", split_name[1] + "_" + split_name[0] + "_"]
			login = None
			for x in range(8):
				if driver.current_url == "https://twitter.com/settings/screen_name":
					while wait(driver, "//input", 10, 1).get_attribute("value") != "":
						wait(driver, "//input", 10, 1).send_keys(Keys.BACK_SPACE)
					wait(driver, "//input", 10, 1).send_keys(try_combinations[x])
					wait(driver, '//div[@data-testid="settingsDetailSave"]', 10, 1).click()
					login = try_combinations[x]
					sleep(2)
				else:
					break

			try:
				login = wait(driver, "//div[@role='tablist']/div/h2", 10, 1).text
			except Exception as e:
				pass
			print("LOGIN: ", login)
			driver.get("https://twitter.com/settings/language")
			if wait(driver, "//option[@value='en']", 10, 1):
				wait(driver, "//option[@value='en']", 10, 1).click()
				wait(driver, "//div/div/div/span/span", 10, 1).click()
			driver.get("https://twitter.com/settings/country")
			if wait(driver, "//option[@value='us']", 10, 1):
				wait(driver, "//option[@value='us']", 10, 1).click()
				wait(driver, "//div[@aria-haspopup='false'][1]", 10, 1).click()

			imgs_url = url_to_imgs()
			driver.get(imgs_url)
			wait(driver, '//div[@class="gal_list"]', 10, 2)[0].click()
			wait(driver, '//div[@class="gal_list"]', 10, 2)[0].click()
			picture_req = get(wait(driver, '//img', 10, 1).get_attribute("src"))
			if picture_req.status_code == 200:
				with open("2.jpg", 'wb') as f:
					f.write(picture_req.content)
			system("nconvert -out jpeg -o %_.jpg -q 95 -rmeta -rexifthumb -noise uniform 0.1 *.jpg")

			driver.get("https://twitter.com/settings/profile")
			wait(driver, "//div[1]/div[1]/div/div/div/input[@type='file']", 10, 1).send_keys(abspath("1_.jpg"))
			wait(driver, "//div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/span/span", 10, 1).click()
			wait(driver, "//div[1]/div[2]/div/div/div/input[@type='file']", 10, 1).send_keys(abspath("2_.jpg"))
			wait(driver, "//div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/span/span", 10, 1).click()
			offer_url = url_shortener_main(name)
			wait(driver, "//textarea[@name='description']", 10, 1).send_keys("Register and find me here - " + offer_url)
			wait(driver, "//input[@name='url']", 10, 1).send_keys(offer_url)
			wait(driver, "//div[1]/div/div/div/div/div/div/div/div/div/div/div/div/span/span", 10, 1).click()
			sleep(5)
			remove("1_.jpg")
			remove("2_.jpg")
			remove("2.jpg")
			driver.get("https://twitter.com/home")
			get('http://api.sms-reg.com/setOperationOk.php?tzid=' + tzid + '&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
			account_settings = {}
			account_settings["Bot name"] = name
			account_settings["Login"] = login
			account_settings["Password"] = password
			account_settings["TZID"] = tzid
			account_settings["IMG URL"] = imgs_url
			account_settings["ALBOM ID"] = 0
			account_settings["PHOTO ID"] = 1
			jdump("Bots/" + name + "/settings.json", account_settings)
			stat = {}
			stat["Followings"] = "OFF"
			stat["Posts"] = "OFF"
			jdump("Bots/" + name + "/stat.json", stat)
			jdump("Bots/" + name + "/base.json", [])
			jdump("Bots/" + name + "/pause.json", 0)
			balance_info = get('http://api.sms-reg.com/getBalance.php?apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
			balance_info = balance_info.text
			json_balance_info = loads(balance_info)
			bot.send_message(USERTELEGRAMID, "Ваш балланс: " + json_balance_info['balance'])			
			driver.quit()
			bot.send_message(USERTELEGRAMID, "Имя нового бота: " + name)
			return name
	except Exception as e:
		print(e)
		return False

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
# cookie_creator("Celia Brown")
# test_account("Bot Name")

bot = TeleBot('1107563794:AAHwpuyWE1JWF2ZLTfGp7pMnMmWX_ys8omw')
Thread(target=pausecheker).start()

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

def start_bot(message):
	b_name = message.text
	if exists("Bots/" + b_name):
		pause = jload("Bots/" + b_name + "/pause.json") - time()
		if pause < 0:
			active_bots_following.append(b_name)
			Thread(target=autofollowing, args=(b_name,)).start()
		else:
			bot.send_message(USERTELEGRAMID, "Пауза, вы сможете повторно запустить автофоловинг в: " + strftime("%X", gmtime(pause)))

		active_bots_posting.append(b_name)
		Thread(target=autoposting, args=(b_name,)).start()
		Thread(target=pause_actions).start()
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