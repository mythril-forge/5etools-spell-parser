# python packages
import re
from slugify import slugify
# project imports
pass

class Book:
	'''
	A book contains many spells in an orderly fashion.
	'''
	def __init__(self):
		self.name = None
		self.slug = None
		self.acronym = None
		self.spells = {}


	def add_name(self, acronym):
		# simply add an acronym
		self.acronym = acronym
		# also look up the name
		self.name = book_acronyms[acronym]
		# might as well fix up a slug too
		slug = re.sub(r'([^\s\w/]|_)+', '', self.name)
		slug = slug.lower()
		slug = slugify(slug)
		self.slug = slug


	def add_spell(self, Spell):
		self.spells[Spell.slug] = Spell
