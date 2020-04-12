import smtplib, ssl, re, json
from random import randint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Validation:
	def mail(self, mail: str) -> bool:
		validation = True if re.search(re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"), mail) else False
		return validation


	def gmail(self, mail: str) -> bool:
		validation = True if re.search(re.compile(r"(^[a-zA-Z0-9_.+-]+@gmail\.com$)"), mail) else False
		return validation


	def address(self, address: str) -> list: 
		regex = re.search(re.compile(r"^(https?:\/\/)?([a-z]+\.)?([a-z0-9]+)(\.com|\.com\.tr)(\/.+)"), address)
		validation = True if re.search(re.compile(r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$"), address) and regex else False
		with open("log.json", "r") as path:
			log = json.load(path)
		if validation:
			try:
				http = ('https://www.' + ''.join([regex.group(iter) for iter in range(3,6)]))
				if not any(item["address"] == http for item in log['logs']):
					returnList = ["unique"]
				else:
					returnList = ["duplicate"]
				returnList.append(http)
				returnList.append(regex.group(2))
				returnList.append(regex.group(5))
			except AttributeError:
				pass
		else:
			returnList = ["invalid"]
		return returnList


	def gmailCredentials(self, email: str, password: str) -> bool:
		server = smtplib.SMTP("smtp.gmail.com", 587)
		try:
			server.ehlo()
			server.starttls(context=ssl.create_default_context())
			server.login(email, password)
			server.quit()
		except smtplib.SMTPAuthenticationError or smtplib.SMTPServerDisconnected:
			return False
		return True


class Mail:
	def __init__(self):
		with open("log.json", "r") as path:
			log = json.load(path)
		with open("login.json", "r") as path:
			login = json.load(path)
		self.receiverMail = log["mail"]
		self.senderMail = login["mail"]["address"]
		self.senderPassword = login["mail"]["password"]
		self.instanceID = "Price Tracker " + str(randint(1000, 9999))


	def send(self, message: list) -> bool:
		server = smtplib.SMTP("smtp.gmail.com", 587)
		try:
			server.ehlo()
			server.starttls(context=ssl.create_default_context())
			server.login(self.senderMail, self.senderPassword)
			body = MIMEMultipart("alternative")
			body["Subject"] = self.instanceID
			body.attach(MIMEText(message[0], "plain"))
			body.attach(MIMEText(message[1], "html"))
			server.sendmail(self.senderMail, self.receiverMail, body.as_string())
			server.quit()
		except smtplib.SMTPAuthenticationError or smtplib.SMTPServerDisconnected or smtplib.SMTPHeloError:
			return False
		return True


def updateLog(address: str, info: dict, sendMail: bool):
	price = info["price"]
	with open("log.json", "r") as path:
			log = json.load(path)
	for item in log["logs"]:
		if item["address"] == address:
			product = item
			break
	if price < product["lastPrice"]:
		newProduct = product
		newProduct["name"] = info["name"]
		newProduct["lastPrice"] = price
		newProduct["minPrice"] = price if price < newProduct["minPrice"] else newProduct["minPrice"]
		if sendMail:
			with Mail as mail:
				text = "{}   Max. Price: {}   Min. Price: {}   Last Price: {}\nCurrent Price: {}".format(newProduct["name"], product["maxPrice"], product["minPrice"], product["lastPrice"], newProduct["lastPrice"])
				html = '<h4>{}</h5><a href="{}">Link</a> <p>   Max. Price: {}   Min. Price: {}   Last Price: {}   <b>Current Price: {}</b></p>'.format(newProduct["name"], product["address"], product["maxPrice"], product["minPrice"], product["lastPrice"], newProduct["lastPrice"])
				if mail.send([text, html]):
					print("Sent mail.")
				else:
					print("Couldn't send mail.")
		log["logs"].remove(product)
		log["logs"].append(newProduct)
		with open("log.json", "w") as path:
			json.dump(log, path, ensure_ascii=False)
	elif price > product["lastPrice"]:
		newProduct = product
		newProduct["lastPrice"] = price
		newProduct["maxPrice"] = price if price > newProduct["maxPrice"] else newProduct["maxPrice"]
		log["logs"].remove(product)
		log["logs"].append(newProduct)
		with open("log.json", "w") as path:
			json.dump(log, path, ensure_ascii=False)


def inspectAddress(address: str, sendMail: bool) -> int:
	with Validation as validate:
		site = validate.address(address)[2]
	if site == "n11":
		if info := scrapeN11(address):
			price = info["price"]
			updateLog(address, info, sendMail)
		return info
	elif site == "hepsiburada":
		if info := scrapeHepsiburada(address):
			price = info["price"]
			updateLog(address, info, sendMail)
		return info
	elif site == "gittigidiyor":
		if info := scrapeGittigidiyor(address):
			price = info["price"]
			updateLog(address, info, sendMail)
		return info
	elif site == "amazon":
		if info := scrapeGittigidiyor(address):
			price = info["price"]
			updateLog(address, info, sendMail)
		return info