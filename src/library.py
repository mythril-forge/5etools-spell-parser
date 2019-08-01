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

	def write_to_text(self):
		print('writing library')
		# grab all the books
		if not os.path.exists(f'./spells/'):
			os.makedirs(f'./spells/')
		for book_title in self.books:
			Book = self.books[book_title]
			Book.write_to_text()

	def write_to_json(self):
		# grab all the books
		pass