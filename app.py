import json
import threading
import os as fs
from time import sleep
from utility import Validation, Mail, inspectAddress

validate = Validation()
active = False

print("""
                     __                               __                                   __                            
                    |  \                             |  \                                 |  \                           
  ______    ______   \$$  _______   ______          _| $$_     ______   ______    _______ | $$   __   ______    ______   
 /      \  /      \ |  \ /       \ /      \  ______|   $$ \   /      \ |      \  /       \| $$  /  \ /      \  /      \  
|  $$$$$$\|  $$$$$$\| $$|  $$$$$$$|  $$$$$$\|      \\$$$$$$  |  $$$$$$\ \$$$$$$\|  $$$$$$$| $$_/  $$|  $$$$$$\|  $$$$$$\ 
| $$  | $$| $$   \$$| $$| $$      | $$    $$ \$$$$$$ | $$ __ | $$   \$$/      $$| $$      | $$   $$ | $$    $$| $$   \$$ 
| $$__/ $$| $$      | $$| $$_____ | $$$$$$$$         | $$|  \| $$     |  $$$$$$$| $$_____ | $$$$$$\ | $$$$$$$$| $$       
| $$    $$| $$      | $$ \$$     \ \$$     \          \$$  $$| $$      \$$    $$ \$$     \| $$  \$$\ \$$     \| $$       
| $$$$$$$  \$$       \$$  \$$$$$$$  \$$$$$$$           \$$$$  \$$       \$$$$$$$  \$$$$$$$ \$$   \$$  \$$$$$$$ \$$       
| $$                                                                                                                     
| $$                                                                                                                v1.0 
 \$$                                                                                                                     
""")
def main():
	sleep(0.5)
	print("Waiting for command...")
	inputString = input("> ")
	if inputString == "mail":
		inputString = input("Modify sender or receiver: ")
		if inputString == "sender":
			changeSender()
		elif inputString == "receiver":
			changeReceiver()
		else: 
			print("Unknown command.")
	elif inputString == "add":
		add()
	elif inputString == "remove":
		remove()
	elif inputString == "credentials":
		if inputString := input("Modify n11 or hepsiburada or gittigidiyor or amazon: ") == "n11":
			changeCredentials("n11")
		elif inputString == "hepsiburada":
			changeCredentials("hepsiburada")
		elif inputString == "gittigidiyor":
			changeCredentials("gittigidiyor")
		elif inputString == "amazon":
			changeCredentials("amazon")
		else: 
			print("Unknown command.")
	elif inputString == "list":
		printList()
	elif inputString == "reset":
		reset()
	elif inputString == "activate":
		activate()
	elif inputString == "deactivate":
		deactivate()
	elif inputString == "exit":
		deactivate()
		exit()
	else:
		print("Unknown command.")


def init():
	with open("log.json", "w") as path:
		json.dump({"mail": "foobar", "logs": []}, path, ensure_ascii=False)
	with open("login.json", "w") as path:
		json.dump({"mail":[]}, path, ensure_ascii=False)
	changeReceiver()
	changeSender()


def reset():
	fs.remove("log.json")
	fs.remove("login.json")
	init()


def changeReceiver():
	with open("log.json", "r") as path:
		log = json.load(path)
	mail = input("E-mail: ")
	while not validate.mail(mail):
		print("Invalid E-Mail.")
		mail = input("E-mail: ")
	log["mail"] = mail
	with open("log.json", "w") as path:
		json.dump(log, path, ensure_ascii=False)


def changeSender():
	with open("login.json", "r") as path:
		login = json.load(path)
	mail = input("G-mail Address: ")
	while not validate.gmail(mail):
			print("Invalid Gmail address.")
			mail = input("Gmail Address: ")
	password = input("Password: ")
	while not validate.gmailCredentials(mail, password):
		print("Invalid e-mail/password.")
		mail = input("Gmail: ")
		while not validate.gmail(mail):
			print("Invalid Gmail address.")
			mail = input("Gmail Address: ")
		password = input("Password: ")
	login["mail"] = [mail, password]
	with open("login.json", "w") as path:
		json.dump(login, path, ensure_ascii=False)


def changeCredentials(site: str):
	with open("login.json", "r") as path:
		login = json.load(path)
	print("Editing {} credentials.".format(site))
	mail = input("E-mail: ")
	while not validate.mail(mail):
			print("Invalid e-mail.")
			mail = input("E-mail: ")
	password = input("Password: ")
	login[site] = {"email": mail, "password": password}
	with open("login.json", "w") as path:
		json.dump(login, path, ensure_ascii=False)


def add():
	address = input("Page address: ")
	validation = validate.address(address)
	if validation[0] == "unique":
		name = validation[3]
		if addressInfo := inspectAddress(validation[1], False, False):
			price = addressInfo["price"]
			name = addressInfo["name"]
		else: 
			price = 0
		productLog = {
		"address": validation[1],
		"site": validation[2],
		"name": name,
		"maxPrice": price,
		"lastPrice": price,
		"minPrice": price}	
		with open("log.json", "r") as path:
			log = json.load(path)
		log["logs"].append(productLog)
		with open("log.json", "w") as path:
			json.dump(log, path, ensure_ascii=False)
	elif validation[0] == "duplicate":
		print("Already in logs.")
	else:
		print("Invalid address.")


def remove():
	address = input("Page address: ")
	validation = validate.address(address)
	with open("log.json", "r") as path:
		log = json.load(path)
	if validation[0] == "duplicate":
		for product in log["logs"]:
			if product["address"] == validation[1]:
				log["logs"].remove(product)
				with open("log.json", "w") as path:
					json.dump(log, path, ensure_ascii=False)
	elif validation[0] == "unique":
		print("Address not found in log.")
	else:
		print("Invalid address.")


def printList():
	with open("log.json", "r") as path:
		log = json.load(path)
	if len(log["logs"]) == 0:
		print("List empty.")
	else:
		text = ""
		html = "<html><body>"
		for product in log["logs"]:
			text += "{}   Max. Price: {}   Min. Price: {}   Current Price: {}\n".format(product["name"], product["maxPrice"], product["minPrice"], product["lastPrice"])
			html += '<a href="{}"> {} </a> <p>   Max. Price: {}   Min. Price: {}   <b>Current Price: {}</b></p><hr>'.format(product["address"], product["name"], product["maxPrice"], product["minPrice"], product["lastPrice"])
		print(text)
		html += "</body></html>"
		mail = Mail()
		if mail.send([text, html]):
			print("Sent mail.")
		else:
			print("Couldn't send mail.")


def activate():
	with open("log.json", "r") as path:
		log = json.load(path)
	with open("login.json", "r") as path:
		login = json.load(path)
	for product in log["logs"]:
		if not product["site"] in login:
			changeCredentials(product["site"])
			with open("login.json", "r") as path:
				login = json.load(path)
	global active
	if active == False:
		active = True
		print("Activated script.")
		print(threading.activeCount())
		if threading.activeCount() == 1:
			loopThread = threading.Thread(target=loop)
			loopThread.start()
	else:
		print("Script already active.")


def deactivate():
	print("Deactivating script.")
	global active
	active = False


def loop():
	global active
	while active:
		with open("log.json", "r") as path:
			log = json.load(path)
		for product in log["logs"]:
			if not activate:
				break
			productInfo = inspectAddress(product["address"], True, True)
			if productInfo:
				print(productInfo["name"])
				print(productInfo["price"])
			else: print("Couldn't scrape " + product["address"])
			print("Waiting for command...")
			print(">", end=" ")
			sleep(90)


if not fs.path.isfile("log.json") and not fs.path.isfile("login.json"):
	init()	

while True:
	main()