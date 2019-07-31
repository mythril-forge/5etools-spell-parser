import os
import re

class Library:
	'''
	A library contains many books in an orderly fashion.
	'''
	def __init__(self):
		self.name = None
		self.books = {}

	def add(self, Book):
		self.books[Book.acronym] = Book

	def write_to_file(self, level = 0):
		# grab all the books
		if not os.path.exists(f'./spells/'):
			os.makedirs(f'./spells/')
		for book_title in self.books:
			Book = self.books[book_title]
			# make a folder
			# grab all the spells
			for spell_name in Book.spells:
				Spell = Book.spells[spell_name]
				filepath = f'./spells/{Spell.slug}.md'
				if level == None or level == Spell.level:
					with open(filepath, 'w+') as file:
						file.write(Spell.get_text())
