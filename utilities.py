import re

class Validation:
	def mail(self, email: str) -> bool:
		validation = True if re.search(re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"), email) else False
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

class Mail:
	def __init__(self, email):
		self.address = email
	
	def test(self):
		
