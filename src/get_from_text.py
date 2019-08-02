# python packages
import os
# project imports
from spell_from_text import SpellFromText
from book import Book
from library import Library

def main():
	# A sanctum will be made to store parsed tome objects.
	Sanctum =  Library()
	# We have to track just the names of the books now,
	# and keep an array of spell pointers linked.
	# The tome objects will be made later.
	tome_dict = {}

	# This for-loop identifies files within the spells folder.
	for dir_data in os.walk('./spells/'):
		dir_filenames = dir_data[2]

		# Loop through all the spells from our directories.
		for filename in dir_filenames:
			# The arcanum object tracks parsed spell data.
			# Here the data generates qualitative properties.
			# This can later be used to generate markdown or json.
			Arcanum = SpellFromText(filename)
			# A spell can be sourced from several books;
			# therefore a loop is needed to capture all of them.
			for book_acronym in Arcanum.citations:
				# The book acronym is most important for now.
				book_acronym = book_acronym['book']
				book_acronym = book_acronym.lower()
				# Add to temporary tome_dict via this acronym.
				if tome_dict.get(book_acronym, False):
					tome_dict[book_acronym].append(Arcanum)
				# If the acronym key doesn't exist yet, create it.
				else:
					tome_dict[book_acronym] = [Arcanum]

	# This dictionary will be used to create book objects.
	for book_acronym in tome_dict:
		# A tome will be made to store parsed spell objects...
		Tome = Book()
		# ...and a tome needs a good title.
		book_acronym = book_acronym.lower()
		Tome.add_title(book_acronym)

		# These spells can be added to the Tome object at last.
		for Arcanum in tome_dict[book_acronym]:
			# Add an arcanum to the tome.
			Tome.log_spell(Arcanum)
		# Add a tome to the sanctum.
		Sanctum.log_book(Tome)
	# Sanctum holds all the wizardly research you could need.
	return Sanctum

if __name__ == '__main__':
	Sanctum = main()
	text = Sanctum.extract_markdown()
	print(text)
