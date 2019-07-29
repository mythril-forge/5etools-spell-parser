import os
# project imports
from library import Library
from book import Book
from spell_from_text import SpellFromText

def main():
	# A sanctum will be made to store parsed tome objects.
	Sanctum =  Library()
	# A tome will be made to store parsed spell objects.
	Tome = Book()

	for dir_data in os.walk('./spells/'):
		dir_filenames = dir_data[2]
		for filename in dir_filenames:
			# The arcanum object tracks parsed spell data.
			# Here the data generates quality properties.
			# This can later be used to generate markdown or json.
			Arcanum = SpellFromText(filename)

if __name__ == '__main__':
	main()
	# Sanctum = main()
	# Sanctum.write_to_json()
