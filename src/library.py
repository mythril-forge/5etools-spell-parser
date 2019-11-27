# python packages
import json
import os
import re
# project imports
pass



class Library:
	'''
	A library contains many books in an orderly fashion.
	'''
	def __init__(self):
		self.name = None
		self.slug = None
		self.books = {}


	def log_book(self, Book):
		self.books[Book.acronym] = Book


	def extract_json(self):
		json_library = {}
		for acronym in self.books:
			Book = self.books[acronym]
			json_book = Book.extract_json()
			json_library[acronym] = json_book
		return json_library


	def extract_markdown(self):
		text_library = {}
		for acronym in self.books:
			Book = self.books[acronym]
			level_book = Book.extract_markdown()
			for level in level_book:
				for slug in level_book[level]:
					if not text_library.get(level):
						text_library[level] = {}
					text_library[level][slug] = level_book[level][slug]
		return text_library
