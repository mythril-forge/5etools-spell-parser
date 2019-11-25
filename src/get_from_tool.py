# python packages
import requests
import json
# project imports
from spell_from_tool import SpellFromTool
from book import Book
from library import Library
# project settings
VERBOSE = True



def verbose_get(resource):
	'''
	This function checks the VERBOSE project setting.
	It can print resources to console as they are retrieved.
	Otherwise, it acts the same as requests.get()
	'''
	if VERBOSE:
		output = f'getting data from {resource} ...'
		print('\n' + '+'*len(output))
		print(output)
	return requests.get(resource)



def main():
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
	url = 'https://raw.githubusercontent.com/TheGiddyLimit' \
	'/TheGiddyLimit.github.io/master/data/spells/'

	# == HACK ==
	# The problem noted above had some trickle-down effects.
	# A 2nd resource had to be found to fill in missing data.
	# Wierdly, the extra data is from 5etools' csv generator.
	with open('spells_area.json', 'r') as file:
		ExtraData = json.load(file)

	# The url is not complete without a filename.
	# Each d&d book is associated with a different filename.
	# The reference chosen has a json object for these books.
	SourceData = verbose_get(url + 'index.json').json()

	# A sanctum will be made to store parsed tome objects.
	Sanctum = Library()
	for book in SourceData:
		# Every book is associated with a filename.
		# This filname can be used to find the url.
		BookData = verbose_get(url + SourceData[book]).json()

		# A tome will be made to store parsed spell objects...
		Tome = Book()
		# ...and a tome needs a good title.
		acronym = SourceData[book].replace('spells-', '')
		acronym = acronym.replace('.json', '').lower()
		Tome.add_title(acronym)

		# Loop through all the spells from the API.
		for SpellData in BookData['spell']:
			# The arcanum object tracks parsed spell data.
			# Here the data generates quality properties.
			# This can later be used to generate markdown or json.
			Arcanum = SpellFromTool(SpellData, ExtraData)

			# Add an arcanum to the tome.
			Tome.log_spell(Arcanum)
		# Add a tome to the sanctum.
		Sanctum.log_book(Tome)
	# Sanctum holds all the wizardly research you could need.
	return Sanctum



if __name__ == '__main__':
	Sanctum = main()
	json = Sanctum.extract_json()
	# print(json)
