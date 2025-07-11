from article import *
import json
import os

def dict_to_article(d):
	return Article(d['Title'], d['Link'], d['Authors'], d['Abstract'], d['Numpages'], d['Year'])

def extract_articles_from(list_of_files):
	ret = []
	for file_name in list_of_files:
		with open(file_name, 'r') as f:
			articles = f.read().split('\n\n')
		while articles[-1].strip() == '':
			articles.pop()
		ret.extend([dict_to_article(json.loads(article)) for article in articles])
	return ret

# Extraction des articles
def extract_articles(file):
	with open(file, 'r') as f:
		articles = f.read().split('\n\n')
	while articles[-1].strip() == '':
		articles.pop()
	return articles

def delete_doubles(articles, dir_name):
	d = {}
	ret = []
	doubles = []
	for article in articles:
		d[article.key()] = 0
	for article in articles:
		key = article.key()
		if d[key] == 1:
			doubles.append(article)
		else:
			ret.append(article)
			d[key] += 1
	save_addr = os.path.join(dir_name, f"duplicates_{len(doubles)}.json")
	with open(save_addr, 'w') as f:
		for article in doubles:
			f.write(json.dumps(article.to_dict(), indent = 4))
			f.write('\n\n')
	return ret

def delete_min_pages(articles, dir_name, m):
	ret = []
	not_enough = []
	for article in articles:
		n = int(article.numpages)
		if n == 0 or n >= m:
			ret.append(article)
		else:
			not_enough.append(article)
	save_addr = os.path.join(dir_name, f"not_enough_pages_{len(not_enough)}.json")
	with open(save_addr, 'w') as f:
		for article in not_enough:
			f.write(json.dumps(article.to_dict(), indent = 4))
			f.write('\n\n')
	return ret