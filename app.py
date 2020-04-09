import json
import os as fs
from utilities import Validation
from utilities import Mail

validate = Validation()

def main():
	print("Waiting for command...")
	inputString = input("> ")
	if inputString == "email":
		changeEmail()
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
	else:
		print("Unknown command.")


def init():
	with open("log.json", "w") as path:
		json.dump({"email": "foobar", "logs": []}, path, ensure_ascii=False)
	with open("login.json", "w") as path:
		json.dump({"secrets": []}, path, ensure_ascii=False)
	changeEmail()


def reset():
	fs.remove("log.json")
	fs.remove("login.json")
	init()


def changeEmail():
	with open("log.json", "r") as path:
		log = json.load(path)
	email = input("E-mail: ")
	print(email)
	while not validate.mail(email):
		print("Invalid E-Mail.")
		email = input("E-mail: ")
	log["email"] = email
	with open("log.json", "w") as path:
		json.dump(log, path, ensure_ascii=False)


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


if not fs.path.isfile("log.json"):
	init()
else:
	printList()

while True:
	main()

""" {
	"email": "foo@bar.com",
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
