from linguistic import getPOS
from sentiment import getSentiment

import random

import logging
logging.basicConfig(level=logging.DEBUG)

logging.debug("Comenzando generate_reply_completed...")



greetings = [ "hi", "hello", "hey", "Good morning", "Good after", "greetings" ]
greetings_responses = [ "Hi there." , "Greetings friend.", "Hello there.", "Hey." ]


farewell = [ "bye", "see you" ]
farewell_responses = [ "Bye friend." , "see you later", "see you soon." ]

"""
	e.g. I think that you are stupid
	
[('I', 'PRP'), ('think', 'VBP'), ('that', 'IN'), ('you', 'PRP'), ('are', 'VBP'), ('stupid', 'JJ')]

 @returns JJ if sentence structure is You Are {word}+ JJ {word}+.
"""
def findYouAreJJ(pos):
	foundYou = False
	foundYouAre = False

	logging.debug('You Are JJ(pos)')
	logging.debug(pos)

	"""
	NOTA: el pos es una arreglo con dupla, estilo 
		[('you', 'PRP'), ('are', 'VBP'), ('increible', 'JJ')]
		
	en el for el objeto  e: (por eso acceso a  e[0])
		('you', 'PRP')


	NOTA2: como no al otro else
	en: i thing that you are very stupid!
		no entra en ningun if, solo entran  "you are stupid"
	"""
	for e in pos:
		#logging.debug(e)

		if e[0].lower() == 'you':
			logging.debug('you')
			foundYou = True
		elif e[0].lower() == 'are' and foundYou:
			logging.debug('are')
			foundYouAre = True
		elif foundYou and not foundYouAre:
			logging.debug('foundYou and not foundYouAre')
			foundYou = False
		# =========================================================================
		# Si reconoce la tupla ('stupid', 'JJ') , regresa y deja de analizar lo demas 
		# =========================================================================
		elif foundYouAre and e[1] == 'JJ':
			logging.debug('JJ')
			return e[0]

	return False

"""
[('I', 'PRP'), ("'m", 'VBP'), ('looking', 'VBG'), ('for', 'IN'), ('something', 'NN'),
 ('where', 'WRB'), ('I', 'PRP'), ('spend', 'VBP'), ('around', 'IN'), ('7', 'CD'), ('pesos', 'NNS')]


 [('Where', 'WRB'), ('can', 'MD'), ('I', 'PRP'), ('eat', 'VB'), ('for', 'IN'), ('15', 'CD'), 
 ('dollars', 'NNS'), ('?', '.')]
"""
# Returns JJ if sentence structure is I want {word}+ JJ {word}+.
def findIWantQP(pos):
	foundI = False
	foundIWant = False
	foundIWantAround = False

	logging.debug('I want (pos)')
	logging.debug(pos)

	for e in pos:
		if ( e[0].lower() == 'i' or e[0].lower() == 'can'):
			foundI = True
		elif ( e[0].lower() == 'want' or e[0].lower() == 'spend' or e[0].lower() == 'eat') and foundI:
			foundIWant = True
		elif ( e[0].lower() == 'around' or e[0].lower() == 'with' or e[0].lower() == 'for') and foundIWant:
			foundIWantAround = True
		elif foundI and not foundIWant:
			foundI = False
		elif foundIWantAround and e[1] == 'CD':
			return e[0]

	return False
	


# Returns JJ if sentence structure is I Am {word}+ JJ {word}+.
def findIAmJJ(pos):
	foundI = False
	foundIAm = False

	logging.debug('I am (pos)')
	logging.debug(pos)


	for e in pos:
		if e[0].lower() == 'i':
			foundI = True
		elif e[0].lower() == 'am' and foundI:
			foundIAm = True
		elif foundI and not foundIAm:
			foundI = False
		elif foundIAm and e[1] == 'JJ':
			return e[0]
	return False


# Returns JJ if sentence structure is where is {word} + JJ {word} +.
def findWhereIsJJ(pos):
	foundWhere = False
	foundIs = False

	logging.debug('Where Is JJ(pos)')
	logging.debug(pos)


	for e in pos:
		if e[0].lower() == 'where':
			foundWhere = True
		elif e[0].lower() == 'is' and foundWhere:
			foundIs = True
		elif foundWhere and not foundIs:
			foundWhere = False
		elif foundIs and e[1] == 'NN':
			return e[0]
	return False



"""
1. En general revisa linealmente cada funcion 

2. si contigo lo dicho en la funcion entra al sig. if

3. donde muestra el sentimiento de la oracion "positivo 1" 

4. y de ahi regresa una respuesta

"""
# Generates a bot response from a user message
def generateReply(message):
	pos = getPOS(message)
	sentiment = getSentiment(message)

	# If error occurred getting POS
	if not pos:
		return "I am not functioning at the moment. Perhaps check your API keys."

	# If user greeted
	if pos[0][0].lower() in greetings:
		return random.choice(greetings_responses)

	# If user farewell
	if pos[0][0].lower() in farewell:
		return random.choice(farewell_responses)

	# If user said 'You are ... {adjective} ...'
	youAreJJ = findYouAreJJ(pos)   
	if youAreJJ:
		if sentiment >= 0.5: # SENTIMIENTO POSITIVO "BUENO"
			return "Thank you, I know I'm "+youAreJJ+"."
		else:
			return "No! I'm not "+youAreJJ+"!"

	# If user said 'where is ... {adjective} ...'
	WhereIsJJ = findWhereIsJJ(pos)   
	if WhereIsJJ:
		if sentiment >= 0.5:
			return "You search "+WhereIsJJ+", you can go to Zocalo subway."
		else:
			return "Excuse me I do not know where the "+WhereIsJJ+" is!"

	# If user said 'where is ... {adjective} ...'
	WantAround = findIWantQP(pos)   
	if WantAround:
		if sentiment >= 0.5:
			return "We recommend going to Restaurante Richi's"
		else:
			return "You can spend a little less by ordering at 453535452!"

			
	# If user said 'I am ... {adjective} ...'
	IAmJJ = findIAmJJ(pos)   
	if IAmJJ:
		if sentiment >= 0.5:
			return "I'm happy for you that you're "+IAmJJ+"."
		else:
			return "Don't be mean on yourself. I'm sure you're not really "+IAmJJ+"!"

	if sentiment >= 0.5:
		return "I'm happy to hear that!"
	else:
		return "I feel sad about that."

	

