import argparse
from time import strftime, gmtime
import os
from bib_to_json import *
from csv_to_json import *
from manage_articles import *
from ask_to_mistral import *

# Parsing arguments
parser = argparse.ArgumentParser(
        prog = "Make_prisma_diagram",
        description = "This programm makes the first steps of the prisma diagram")

parser.add_argument("--input", type = str, required = True, nargs = '*', help = "path to the input files")
parser.add_argument("--save_dir", type = str, default = '', help = "where to save the output files")
parser.add_argument("--min_pages", type = int, default = 0, help = "Number of pages required in order to sought the article for retrieval")
parser.add_argument("--api", type = str, default = 'API_key.txt', help = "Adress of the API key for mistral")
parser.add_argument("--prompt", type = str, default = 'prompt.txt', help = "Adress of the prompt for mistral")
args = parser.parse_args()



# Format can we can parse in this program
known_format = {'csv' : csv_to_json, 'bib' : bib_to_json}

# Directory in which files will be stored
dir_name = os.path.join(args.save_dir, strftime("%Y-%m-%d_%H-%M-%S", gmtime()))
os.makedirs(dir_name)

def get_prefixes(inputs):
	suffixes = get_suffixes(inputs)
	n = len(suffixes)
	prefixes = [inputs[i][:len(inputs[i])-len(suffixes[i])-1] for i in range(n)]
	prefixes = [prefix.split('/')[-1] for prefix in prefixes]
	if len(set(prefixes)) != len(prefixes):
		raise ValueError('Error : Two files in input cannot have the save prefix')
	return prefixes

def get_suffixes(inputs):
	global known_format
	suffixes = [file.split('.')[-1] for file in inputs]
	if not (set(suffixes) <= set(known_format.keys())):
		raise ValueError('Error : Input file with unkown format.')
	return suffixes

def main(inputs, dir_name, api, prompt, min_pages):
	# Getting all prefixes and suffixes
	prefixes = get_prefixes(inputs)
	suffixes = get_suffixes(inputs)
	n = len(prefixes)

	# Converting each input file into a json file
	json_files = []
	for i in range(n):
		prefix = prefixes[i]
		suffix = suffixes[i]
		current = inputs[i]
		json_files.append(known_format[suffix](current, prefix, dir_name)) # Convert into json

	# Getting the articles
	remaining_articles = extract_articles_from(json_files)

	# Deleting doubles
	print("DELETING DUPLICATES")
	remaining_articles = delete_doubles(remaining_articles, dir_name) # remaining_articles is the list of articles without doubles
	print("Articles remaining :", len(remaining_articles), sep = '\t')
	print("DONE !\n")

	# Deleting articles that have not enough pages
	print("DELETING ARTICLES THAT HAVE NOT ENOUGH PAGES")
	remaining_articles = delete_min_pages(remaining_articles, dir_name, min_pages)
	print("Articles remaining :", len(remaining_articles), sep = '\t')
	print("DONE !\n")

	# Asking to mistral
	ask_to_mistral(args.api, args.prompt, remaining_articles, dir_name)
	return

main(args.input, dir_name, args.api, args.prompt, args.min_pages)


