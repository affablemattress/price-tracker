import json
import os as fs
from utilities import Validation
from utilities import Mail

validate = Validation()

def main():
	print("Waiting for command...")
	inputString = input("> ")
	if inputString == "mail":
		if inputString := input("Modify sender or receiver: ") == "sender":
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
		changeCredential()
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
		json.dump({"mail": "foobar", "logs": []}, path, nsure_ascii=False)
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
	while not validate.gmailCredentials():
		print("Invalid e-mail/password.")
		mail = input("Gmail: ")
		while not validate.gmail(mail):
			print("Invalid Gmail address.")
			mail = input("Gmail Address: ")
		password = input("Password: ")
	login["mail"] = [mail, password]
	with open("login.json", "w") as path:
		json.dump(login, path, ensure_ascii=False)


def add():
	address = input("Page address: ")
	validation = validate.address(address, False)
	if validation[0] == "unique":
		addressInfo = inspectAddress(address)
		productLog = {
			"adress": address,
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
