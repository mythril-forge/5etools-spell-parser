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
			text_book = Book.extract_markdown()
			text_library[acronym] = text_book
		return text_library
