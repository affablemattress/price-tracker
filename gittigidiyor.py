from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions 
from time import sleep
import json
import re


def scrapeGittigidiyor(address, tryLogin):
	with open("login.json", "r") as path:
		login = json.load(path)
	with webdriver.Opera() as driver:
		if tryLogin:
			driver.get("https://www.gittigidiyor.com/uye-girisi")
			try:
				driver.find_element_by_id("L-UserNameField").send_keys(login["gittigidiyor"]["email"])
				driver.find_element_by_id("L-PasswordField").send_keys(login["gittigidiyor"]["password"])
				driver.find_element_by_id("L-PasswordField").send_keys(Keys.RETURN)
			except selenium.common.exceptions.NoSuchElementException:
				print("Couldn't establish connection. (login-gittigidiyor)")
			try:
				if driver.find_element_by_id("L-PasswordField"):
					print("Invalid (gittigidiyor) credentials.")
			except selenium.common.exceptions.NoSuchElementException:
				None
		driver.get(address)
		try:
			name = driver.find_element_by_css_selector("#sp-title").text
			price = int(re.search(re.compile(r"^₺?(([0-9]|\.)+)"), driver.find_element_by_css_selector(".lastPrice").text).group(1).replace(".", ""))
			return {
				"name": name,
				"price": price
			}
		except selenium.common.exceptions.NoSuchElementException:
			print("Couldn't establish connection. (product page-gittigidiyor)")
			return False
