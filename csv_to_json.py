import pandas as pd
import json
import os
from article import *

def csv_to_json(csv_addr, prefix, save_dir):
	print('CONVERTING', csv_addr, 'TO A JSON FILE')

	# Parsing the csv
	articles = pd.read_csv(csv_addr)

	# List of all articles
	ARTICLES_FOUND = []

	cpt = 0
	for article in articles.iterrows():
		cpt += 1
		article = article[1]
		title = article['Document Title']
		authors = article['Authors']
		if isinstance(authors, float):
			authors = []
		else:
			authors = authors.split(';')
			for i in range(len(authors)):
				authors[i] = authors[i].strip()
		abstract = article['Abstract']
		link = article['PDF Link']

		# Computing the number of pages
		try:
			start = article['Start Page'].split()[0]
			end = article['End Page'].split()[0]
			numpages = str(int(end) - int(start) + 1)
		except:
			numpages = '0'
		ARTICLES_FOUND.append(Article(title, link, authors, abstract, numpages))

	print('Number of articles found :', cpt, sep = '\t')

	# Building the output file
	save_addr = os.path.join(save_dir, prefix + f"_{cpt}.json")

	# Storing every article in a json file
	with open(save_addr, 'w') as f:
		for article in ARTICLES_FOUND:
			f.write(json.dumps(article.to_dict(), indent = 4))
			f.write('\n\n')

	print('DONE !\n')
	return save_addr