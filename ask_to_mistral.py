from mistralai import Mistral
import json 
from manage_articles import * 

def ask_to_mistral(api_key, prompt, ARTICLES, dir_name):

	print("ASKING TO MISTRAL")

	# Extraction de la cle API
	with open(api_key, 'r') as f:
		api_key = f.read()

	# Extraction du prompt
	with open(prompt, 'r') as f:
		prompt = f.read()

	# Initialisation du modele
	client = Mistral(api_key=api_key)
	agent = client.beta.agents.create(
	    model="mistral-small-2503",
	    description="Ce chatbot permet de faire le tri dans la sélection d'articles en lisant l'abstract et le titre",
	    name="Assistant tri d'articles",
	    instructions = prompt,
	    completion_args = {"temperature" : 0.2}
	)

	# Liste des réponses
	RESPONSES = []

	# Boucle pour demander article par article
	cpt_1 = 0
	cpt_m1 = 0
	cpt_0 = 0
	cpt = 0
	for article in ARTICLES:
		cpt += 1
		response = client.beta.conversations.start(
		    agent_id = agent.id,
		    inputs = json.dumps(article.to_dict(), indent = 4),
		    store = False
		)
		response = response.outputs[0].content.lower()

		print('Article', cpt, ':', response)

		# Sauvegarde des réponses
		if response.find('oui') >= 0:
			RESPONSES.append(1)
			cpt_1 += 1
		elif response.find('non') >= 0:
			RESPONSES.append(0)
			cpt_0 += 1
		else:
			print("An error occured")
			cpt_m1 += 1
			RESPONSES.append(-1) # Error

	# Fichier contenant le résultats
	save_addr_0 = os.path.join(dir_name, f'ineligible_by_mistral_{cpt_0}.json')
	save_addr_m1 = os.path.join(dir_name, f'mistral_error_{cpt_m1}.json')
	save_addr_1 = os.path.join(dir_name, f'records_screened_{cpt_1}.json')
	saves = [save_addr_0, save_addr_1, save_addr_m1]
	for i in range(cpt):
		file = saves[RESPONSES[i]]
		with open(file, 'a') as f:
			f.write(json.dumps(ARTICLES[i].to_dict(), indent = 4))
			f.write('\n\n')
	print('Articles removed :', cpt_0, sep = '\t')
	print('Articles remaining :', cpt_1, sep = '\t')
	print('DONE !')

