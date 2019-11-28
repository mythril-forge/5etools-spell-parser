# python packages
import json
import os
import re
# project imports
pass



class Library:
	'''
	A library contains many books in an orderly fashion.
	The library is a more abstract idea, because
	it is, by definition, a collection of books.
	In most cases, you will want every book, so this will
	be a collection of all the available books from WOTC.
	'''
	def __init__(self):
		# Honestly, this class is a glorified object.
		# You can find books by name and view their contents.
		self.books = {}


	def log_book(self, Book):
		self.books[Book.acronym] = Book
