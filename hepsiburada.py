from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions 
from time import sleep
import json
import re


def scrapeHepsiburada(address, tryLogin):
	with open("login.json", "r") as path:
		login = json.load(path)
	with webdriver.Opera() as driver:
		if tryLogin:
			driver.get("https://www.hepsiburada.com/uyelik/giris")
			try:
				driver.find_element_by_id("email").send_keys(login["hepsiburada"]["email"])
				driver.find_element_by_id("password").send_keys(login["hepsiburada"]["password"])
				driver.find_element_by_id("password").send_keys(Keys.RETURN)
			except selenium.common.exceptions.NoSuchElementException:
				print("Couldn't establish connection. (login-hepsiburada)")
			try:
				if driver.find_element_by_id("password"):
					print("Invalid (hepsiburada) credentials.")
			except selenium.common.exceptions.NoSuchElementException:
				None
		driver.get(address)
		try:
			sleep(5)
			name = driver.find_element_by_css_selector("#product-name").text.replace('"', "")
			price = int(re.search(re.compile(r"^₺?(([0-9]|\.)+)"), driver.find_element_by_css_selector(".price.merchant").get_attribute("content")).group(1).replace(".", "")[:-2])
			return {
				"name": name,
				"price": price
			}
		except selenium.common.exceptions.NoSuchElementException:
			print("Couldn't establish connection. (product page-hepsiburada)")
			return False
