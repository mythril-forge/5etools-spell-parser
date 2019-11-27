# python packages
import re
from slugify import slugify
# project imports
from helper import *



class Book:
	'''
	A book contains many spells in an orderly fashion.
	Literally speaking, a book represents a
	sourcebook from D&D, such as the Player's Handbook.
	There are some exceptions to this rule, because
	not all sourcebooks share the same officiality.
	For example, Unearthed Arcana are usually less
	than ten pages, but still use this book object.
	'''
	def __init__(self):
		'''
		Initialization leaves behind a husk of book metadata.
		It's just a few strings and an empty spell container.
		'''
		# Each book has a unique name, slug, and acronym.
		# The acronym is usually preferable to the slug.
		self.name = None
		self.slug = None
		self.acronym = None

		# The focus of a spellbook is, of course, its spells.
		# Like a dictionary, you can look up spell-slugs and
		# find their full markdown definitions.
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


	def extract_markdown(self):
		text_level = {}
		for slug in self.spells:
			Spell = self.spells[slug]
			text_spell = Spell.extract_markdown()
			if not text_level.get(Spell.level):
				text_level[Spell.level] = {}
			text_level[Spell.level][slug] = text_spell
		return text_level
