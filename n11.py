from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions 
from time import sleep
import json
import re
		

def scrapeN11(address, tryLogin):
	with open("login.json", "r") as path:
		login = json.load(path)
	with webdriver.Opera() as driver:
		if tryLogin:
			driver.get("https://www.n11.com/giris-yap")
			try:
				driver.find_element_by_id("email").send_keys(login["n11"]["email"])
				driver.find_element_by_id("password").send_keys(login["n11"]["password"])
				driver.find_element_by_id("password").send_keys(Keys.RETURN)
			except selenium.common.exceptions.NoSuchElementException:
				print("Couldn't establish connection. (login-n11)")
			if driver.find_element_by_id("password"):
				print("Invalid n11 credentials.")
		driver.get(address)
		try:
			name = driver.find_element_by_css_selector(".proName").text
			price = int(re.search(re.compile(r"^₺?(([0-9]|\.)+)"), driver.find_element_by_css_selector("ins").text).group(1).replace(".", ""))
			return {
				"name": name,
				"price": price
			}
		except selenium.common.exceptions.NoSuchElementException:
			print("Couldn't establish connection. (product page-n11)")
			return False