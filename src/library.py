import json
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


	def write_to_json(self):
		json_data = {}
		# grab all the books
		for book_slug in self.books:
			Book = self.books[book_slug]
			json_data[book_slug] = Book.get_json()
		with open('./spell_data.json', 'w') as file:
			json.dump(json_data, file)


	def write_to_text(self):
		# grab all the books
		if not os.path.exists(f'./spells/'):
			os.makedirs(f'./spells/')
		for book_slug in self.books:
			Book = self.books[book_slug]
			Book.write_to_text()
