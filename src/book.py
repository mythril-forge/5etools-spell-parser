# python packages
import re
from slugify import slugify
# project imports
from helper import *



class Book:
	'''
	A book contains many spells in an orderly fashion.
	'''
	def __init__(self):
		self.name = None
		self.slug = None
		self.acronym = None
		self.spells = {}


	def add_title(self, acronym):
		# simply add an acronym
		self.acronym = acronym
		# also look up the name
		self.name = book_acronym_dict[acronym]
		# might as well fix up a slug too
		slug = re.sub(r'([^\s\w/]|_)+', '', self.name)
		slug = slug.lower()
		slug = slugify(slug)
		self.slug = slug


	def log_spell(self, Spell):
		self.spells[Spell.slug] = Spell


	def extract_json(self):
		json_book = {}
		for slug in self.spells:
			Spell = self.spells[slug]
			json_spell = Spell.extract_json()
			json_book[slug] = json_spell
		return json_book


	def extract_markdown(self, by_level = False):
		if not by_level:
			text_book = {}
			for slug in self.spells:
				Spell = self.spells[slug]
				text_spell = Spell.extract_markdown()
				text_book[slug] = text_spell
			return text_book

		else:
			text_level = {}
			for slug in self.spells:
				Spell = self.spells[slug]
				text_spell = Spell.extract_markdown()
				if not text_level.get(Spell.level):
					text_level[Spell.level] = {}
				text_level[Spell.level][slug] = text_spell
			return text_level
