from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions 
from time import sleep
import json
import re


def scrapeAmazon(address, tryLogin):
	amazonLoginURL = "https://www.amazon.com.tr/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=trflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com.tr%2F%3Fref_%3Dnav_custrec_signin&switch_account="
	with open("login.json", "r") as path:
		login = json.load(path)
	with webdriver.Opera() as driver:
		if tryLogin:
			driver.get(amazonLoginURL)
			try:
				driver.find_element_by_id("ap_email").send_keys(login["amazon"]["email"])
				driver.find_element_by_id("ap_email").send_keys(Keys.RETURN)
				try:
					driver.find_element_by_id("ap_password").send_keys(login["amazon"]["password"])
					driver.find_element_by_id("ap_password").send_keys(Keys.RETURN)
				except selenium.common.exceptions.NoSuchElementException: 
					print("Couldn't establish connection. (login-amazon)")
			except selenium.common.exceptions.NoSuchElementException:
				print("Couldn't establish connection. (login-amazon)")
			try:
				if driver.find_element_by_id("L-PasswordField"):
					print("Invalid (amazon) credentials.")
			except selenium.common.exceptions.NoSuchElementException:
				None
		driver.get(address)
		try:
			name = driver.find_element_by_css_selector("#title").text.replace('"', "")
			print(name)
			price = int(re.search(re.compile(r"^₺?(([0-9]|\.)+)"), driver.find_elements_by_css_selector(".a-size-medium.a-color-price")[0].text).group(1).replace(".", ""))
			print(price)
			return {
				"name": name,
				"price": price
			}
		except selenium.common.exceptions.NoSuchElementException:
			print("Couldn't establish connection. (product page-amazon)")
			return False
