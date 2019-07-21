import os

class Library:
	'''
	A library contains many books in an orderly fashion.
	'''
	def __init__(self):
		self.books = {}

	def add(self, Book):
		self.books[Book.acronym] = Book

	def write_to_file(self):
		for book_title in self.books:
			Book = self.books[book_title]
			if not os.path.exists(f'./{Book.acronym}/'):
				os.makedirs(f'./{Book.acronym}/')
			for spell_name in Book.spells:
				Spell = Book.spells[spell_name]
				filepath = f'./{Book.acronym}/{Spell.slug}.md'
				with open(filepath, 'w+') as file:
					file.write(Spell.description)