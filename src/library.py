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


	def add(self, Book):
		self.books[Book.acronym] = Book
