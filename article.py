class Article:
	def __init__(self, title, link, authors, abstract, numpages, year = '0'):
		self.title = title
		self.link = link
		self.authors = authors
		self.abstract = abstract
		self.numpages = numpages
		self.year = year

	def __repr__(self):
		res = ''
		res += '======== Article ========\n'
		res += 'Title : ' + self.title + '\n' 
		res += 'Authors : ' + str(self.authors) + '\n'
		res += 'Link : ' + self.link + '\n'
		res += 'Year : ' +  self.year + '\n'
		res += 'Num-pages : ' +  self.numpages + '\n'
		res += 'Abstract :\n' +  self.abstract + '\n'
		res += '=========================\n'
		return res

	def __str__(self):
		return self.__repr__()

	def to_dict(self):
		d = {'Title' : self.title,
			'Authors' : self.authors,
			'Link' : self.link,
			'Year' : self.year,
			'Numpages' : self.numpages,
			'Abstract' : self.abstract}
		return d

	def key(self):
		return reduce_string(self.title)

	def __eq__(self, other):
		return reduce_string(self.title) == reduce_string(other.title)

def reduce_string(s):
	s = s.replace('.', '')
	s = s.replace(',', '')
	s = s.lower()
	return s