import json
import os as fs
from utilities import Validation, Mail, toHTTP

validate = Validation()

def main():
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
	elif inputString == "credential":
		if inputString := input("Modify n11 or hepsiburada or gittigidiyor or amazon: ") == "n11":
			changeCredential("n11")
		elif inputString == "hepsiburada":
			changeCredential("hepsiburada")
		elif inputString == "gittigidiyor":
			changeCredential("gittigidiyor")
		elif inputString == "amazon":
			changeCredential("amazon")
		else: 
			print("Unknown command.")
	elif inputString == "list":
		printList()
	elif inputString == "reset":
		reset()
	elif inputString == "activate":
		activate()
	elif inputString == "exit":
		exit()
	else:
		print("Unknown command.")


def init():
	with open("log.json", "w") as path:
		json.dump({"mail": "foobar", "logs": []}, path, ensure_ascii=False)
	with open("login.json", "w") as path:
		json.dump({"mail":[],"secrets": []}, path, ensure_ascii=False)
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


def changeCredential(site):
	with open("login.json", "r") as path:
		login = json.load(path)
	mail = input("E-mail: ")
	while not validate.mail(mail):
			print("Invalid e-mail.")
			mail = input("E-mail: ")
	password = input("Password: ")
	login["site"] = {"email": mail, "password": password}
	with open("login.json", "w") as path:
		json.dump(login, path, ensure_ascii=False)


def add():
	address = input("Page address: ")
	validation = validate.address(address, False)
	if validation[0] == "unique":
		addressInfo = inspectAddress(address)
		productLog = {
			"adress": toHTTP(address),
			"site": addressInfo.site,
			"name": addressInfo.name,
			"maxPrice": addressInfo.price,
			"lastPrice": addressInfo.price,
			"minPrice": addressInfo.price
		}
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
	validation = validate.address(address, True)
	with open("log.json", "r") as path:
		log = json.load(path)
	if validation[0] == "duplicate":
		for product in log["logs"]:
			if product["adress"] == validation[1]:
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
			html += '<h4>{}</h5><a href="{}">Link</a> <p>   Max. Price: {}   Min. Price: {}   Current Price: {}</p>'.format(product["name"], product["address"], product["maxPrice"], product["minPrice"], product["lastPrice"])
		print(text)
		html += "</body></html>"
		with Mail() as mail:
			if mail.send([text, html]):
				print("Sent mail.")
			else:
				print("Couldn't send mail.")
			


if not fs.path.isfile("log.json") and not fs.path.isfile("login.json"):
	init()	

while True:
	main()



""" {
	"mail": "foo@bar.com",
	"logs": [
		{
			"adress": "adress",
			"site": "foo",
			"name": "bar",
			"maxPrice": 0,
			"lastPrice": 0,
			"minPrice": 0
		}
	]
} """

""" {
	"mail": {
		"address": "foobar@gmail.com",
		"password": "password"
	},
	"n11": {
		"username": "foo@bar.com",
		"password": "password"
	},
	"hepsiburada": {
		"username": "foo@bar.com",
		"password": "password"
	},
	"amazon: {
		"username": "foo@bar.com",
		"password": "password"
	},
	"gittigidiyor": {
		"username": "foo@bar.com",
		"password": "password"
	}
} """
