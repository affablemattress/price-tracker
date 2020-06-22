import requests
from bs4 import BeautifulSoup
from time import sleep
import json
import re

def scrapeAkakce(address: str):
	page = requests.get(address)
	print(page.status_code)
	if page.status_code == 200:
		soup = BeautifulSoup(page.text, 'html.parser')
		name = soup.select('.pdt_v8 h1')[0].get_text()
		price = soup.select('.pt_v8')[0].get_text()
		print(name, price)
	else: 
		print("Couldn't establish connection. (product page-akakce)")
		return False

scrapeAkakce("https://www.akakce.com/oyun-kolu/en-ucuz-logitech-f710-kablosuz-pc-fiyati,421564.html")