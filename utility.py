import smtplib, ssl, re, json
from random import randint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from n11 import scrapeN11
from gittigidiyor import scrapeGittigidiyor
from amazon import scrapeAmazon
from hepsiburada import scrapeHepsiburada

class Validation:
	def mail(self, mail: str) -> bool:
		validation = True if re.search(re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"), mail) else False
		return validation


	def gmail(self, mail: str) -> bool:
		validation = True if re.search(re.compile(r"(^[a-zA-Z0-9_.+-]+@gmail\.com$)"), mail) else False
		return validation


	def address(self, address: str) -> list: 
		regex = re.search(re.compile(r"^(https?:\/\/)?([a-z]+\.)?([a-z0-9]+)(\.com|\.com\.tr)(\/.+)"), address)
		validation = True if re.search(re.compile(r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+çşğüİÇŞĞÜöÖ.~#?&//=]*)$"), address) and regex else False
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
				returnList.append(regex.group(3))
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

validate = Validation()

class Mail:
	def __init__(self):
		with open("log.json", "r") as path:
			log = json.load(path)
		with open("login.json", "r") as path:
			login = json.load(path)
		self.receiverMail = log["mail"]
		self.senderMail = login["mail"][0]
		self.senderPassword = login["mail"][1]
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
			if price < item["lastPrice"]:
				newProduct = item
				newProduct["name"] = info["name"]
				newProduct["lastPrice"] = price
				newProduct["minPrice"] = price if price < newProduct["minPrice"] else newProduct["minPrice"]
				if sendMail:
					mail = Mail()
					text = "{}   Max. Price: {}   Min. Price: {}   Last Price: {}   Price Before: {}".format(newProduct["name"], item["maxPrice"], item["minPrice"], item["lastPrice"], newProduct["lastPrice"])
					html = '<a href="{}">{}</a> <p>   Max. Price: {}   Min. Price: {}   Price Before: {}   <b>Current Price: {}</b></p>'.format(item["address"], newProduct["name"], item["maxPrice"], item["minPrice"], item["lastPrice"], newProduct["lastPrice"])
					if mail.send([text, html]):
						print("Sent mail.")
					else:
						print("Couldn't send mail.")
				log["logs"].remove(item)
				log["logs"].append(newProduct)
				with open("log.json", "w") as path:
					json.dump(log, path, ensure_ascii=False)
			elif price > item["lastPrice"]:
				newProduct = item
				newProduct["lastPrice"] = price
				newProduct["maxPrice"] = price if price > newProduct["maxPrice"] else newProduct["maxPrice"]
				log["logs"].remove(item)
				log["logs"].append(newProduct)
				with open("log.json", "w") as path:
					json.dump(log, path, ensure_ascii=False)
			break


def inspectAddress(address: str, sendMail: bool, tryLogin: bool) -> int:
	validation = validate.address(address)
	site = validation[2]
	print(type(site))
	if site == "n11":
		if info := scrapeN11(address, tryLogin):
			updateLog(address, info, sendMail)
		return info
	elif site == "hepsiburada":
		if info := scrapeHepsiburada(address, tryLogin):
			updateLog(address, info, sendMail)
		return info
	elif site == "gittigidiyor":
		if info := scrapeGittigidiyor(address, tryLogin):
			updateLog(address, info, sendMail)
		return info
	elif site == "amazon":
		if info := scrapeAmazon(address, tryLogin):
			updateLog(address, info, sendMail)
		return info