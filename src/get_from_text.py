import os
# project imports
from library import Library
from book import Book
from spell_from_text import SpellFromText

def main():
	# A sanctum will be made to store parsed tome objects.
	Sanctum =  Library()
	# We have to track just the names of the books now,
	# and keep an array of spell pointers linked.
	# The tome objects will be made later.
	tome_dict = {}

	for dir_data in os.walk('./spells/'):
		dir_filenames = dir_data[2]
		# Loop through all the spells from our directories.
		for filename in dir_filenames:
			# The arcanum object tracks parsed spell data.
			# Here the data generates qualitative properties.
			# This can later be used to generate markdown or json.
			Arcanum = SpellFromText(filename)
			# Grab the book name.
			book_abbr = Arcanum.citations[0]['book']
			book_abbr = book_abbr.lower()
			# Add the spell to the tome_dict via its main source.
			if tome_dict.get(book_abbr, None):
				tome_dict[book_abbr].append(Arcanum)
			# If the book key doesn't exist yet, create it.
			else:
				tome_dict[book_abbr] = [Arcanum]

	for book_abbr in tome_dict:
		book_abbr = book_abbr.lower()
		# A tome will be made to store parsed spell objects...
		Tome = Book()
		# ...and a tome needs a good title.
		Tome.add_name(book_abbr)
		for Arcanum in tome_dict[book_abbr]:
			# Add an arcanum to the tome.
			Tome.add(Arcanum)
		# Add a tome to the sanctum.
		Sanctum.add(Tome)
	# Sanctum holds all the wizardly research you could need.
	return Sanctum

if __name__ == '__main__':
	main()
	Sanctum = main()
	Sanctum.write_to_json()
