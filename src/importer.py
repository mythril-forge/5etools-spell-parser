# python packages
import requests
import json
# project imports
from spell_from_tool import ToolSpell

def verbose_resource(resource):
	'''
	Prints resources to console as they are retrieved.
	'''
	print()
	output = f'getting data from {resource} ...'
	print('+'*len(output))
	print(output)

def main(verbose = None):
	'''
	Retrieves spellbook data from a particular github project:
	https://github.com/TheGiddyLimit/TheGiddyLimit.github.io
	Once recieved, the importer scans the spells in each book.
	A class is assigned for each spell as the data is parsed.
	'''
	# == HACK ==
	# Much of the spell json is found at this url.
	# Unfortunately, I am still looking for a better resource,
	# as this data omits things such as a spell's shape.
	URL='https://raw.githubusercontent.com/TheGiddyLimit' \
	'/TheGiddyLimit.github.io/master/data/spells/'
	
	# == HACK ==
	# The problem above had some trickle-down effects.
	# A 2nd resource had to be found to fill in missing data.
	# Wierdly, this data is from 5etools' csv generator.
	with open('spells_area.json', 'r') as file:
		EXTRA_DATA = json.load(file)

	# The url is not complete without a filename.
	# Each d&d book is associated with a different filename.
	# The reference chosen has a json object for these books.
	SOURCES = ''.join([URL,'index.json'])
	SOURCES = requests.get(SOURCES).json()

	for book in SOURCES:
		resource = ''.join([URL,SOURCES[book]])

		if verbose:
			verbose_resource(resource)

		PRIME_DATA = requests.get(resource).json()

		for spell_data in PRIME_DATA['spell']:
			Spell = ToolSpell(spell_data, EXTRA_DATA, book)

			with open(Spell.path, 'w+') as file:
				file.write(Spell.markdown)

if __name__ == '__main__':
	main()
