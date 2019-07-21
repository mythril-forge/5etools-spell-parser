import re
from slugify import slugify
from helper import *
from spell_to_markdown import SpellToMarkdown

class Spell:
	'''
	Represents a magic spell in D&D 5th Edition.
	This app was created to accomidate homebrew;
	there are foreign properties in this class.
	The extra properties are left empty for vanilla spells.
	'''
	def __init__(self):
		'''
		a spell has many fascets
		'''
		# basic data
		self.name = None
		self.level = None
		self.school = None

		# a question of time
		self.cast_time = {
			"quality": None,
			"seconds": None,
			"condition": None,
		}
		self.duration = {
			"quality": None,
			"seconds": None,
			"condition": None,
		}

		# physical space
		self.range = {
			'quality': None,
			'distance': None,
		}
		self.area = {
			'shape': None,
			'radius': None,
			'length': None,
			'width': None,
			'height': None,
		}
		self.instances = 1

		# boolean summary of tags
		self.tags = {
			'verbal': None,
			'somatic': None,
			'material': None,
			'concentration': None,
			'ritual': None
		}

		# component details in sentance form
		self.components = {
			'verbal': None,
			'somatic': None,
			'material': None,
		}

		# spell information in paragraph form
		self.description = None,

		# which characters can use this spell?
		self.access = {
			'classes': None,
			'races': None,
			'subclasses': None,
			'subraces': None,
		}

		# where to find the original version of this spell
		self.citation = {
			'book': None,
			'page': None
		}

		self.markdown = None

	def get_markdown(self):
		self.markdown = SpellToMarkdown(self).markdown
