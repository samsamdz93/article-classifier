import bibtexparser as btp
import json
import os
from article import *

def bib_to_json(bib_addr, prefix, save_dir):
	print('CONVERTING', bib_addr, 'TO A JSON FILE')

	# Parsing the library
	library = btp.parse_file(bib_addr)

	n = len(library.entries)
	print('Number of articles found :', n, sep = '\t')

	# Building the output file
	save_addr = os.path.join(save_dir, prefix + f"_{n}.json")

	# List of all articles
	ARTICLES_FOUND = []

	for i in range(n):
		article = library.entries[i]
		fields_keys = article.fields_dict.keys()

		# Getting the title
		if not 'title' in fields_keys:
			title = ''
		else:
			title = article.fields_dict['title'].value

		# Getting the authors
		if not 'author' in fields_keys:
			authors = []
		else:
			authors = article.fields_dict['author'].value
			authors = authors.replace(',', '')
			authors = authors.replace(' and ', ',')
			authors = authors.split(',')
			for i in range(len(authors)):
				authors[i] = authors[i].strip()

		# Getting the abstract
		if not 'abstract' in fields_keys:
			abstract = ''
		else:
			abstract = article.fields_dict['abstract'].value

		# Getting the url
		if not 'url' in fields_keys:
			url = ''
		else:
			url = article.fields_dict['url'].value

		# Getting the number of pages
		if not 'numpages' in fields_keys:
			numpages = '0'
		else:
			numpages = article.fields_dict['numpages'].value

		ARTICLES_FOUND.append(Article(title, url, authors, abstract, numpages))

	# Storing every article in a json file
	with open(save_addr, 'w') as f:
		for article in ARTICLES_FOUND:
			f.write(json.dumps(article.to_dict(), indent = 4))
			f.write('\n\n')

	print('DONE !\n')
	return save_addr