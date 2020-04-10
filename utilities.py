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


	def address(self, address: str, returnAddress: bool) -> list: 
		regex = re.search(re.compile(r"^(https?:\/\/)?([a-z]+\.)?([a-z0-9]+)(\.com|\.com\.tr)(\/.+)"), address)
		validation = True if re.search(re.compile(r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$"), address) and regex else False
		returnList = [validation]
		if returnAddress and validation:
			try:
				returnList.append(''.join([regex.group(iter) for iter in range(3,6)]))
			except AttributeError:
				pass
		return returnList


	def gmailCredentials(self, email: str, password: str):
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


	def send(self, message: list):
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
