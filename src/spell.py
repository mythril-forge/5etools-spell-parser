# python packages
import re
# project imports
from helper import *
from spell_to_text import SpellToText
from book import Book
from library import Library
# project settings
VERBOSE = True



class Spell:
	'''
	A Spell represents an arcane spell ability in D&D 5e.
	This object was created to accomidate homebrew;
	foreign properties here support special scenarios.
	These extra properties are left empty for vanilla spells.
	'''


	def __init__(self):
		'''
		Initialization leaves behind an empty husk of metadata.
		It can be filled in when extended by other classes.
		'''
		# basic spell data
		self.name = None
		self.homebrew = None
		self.level = None
		self.school = None

		# temporal metadata
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

		# spacial metadata
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

		# boolean metadata
		self.tags = {
			'verbal': None,
			'somatic': None,
			'material': None,
			'concentration': None,
			'ritual': None,
		}

		# phrasal metadata
		self.components = {
			'verbal': None,
			'somatic': None,
			'material': None,
		}

		# long-form description
		self.description = None,

		# declare spell users
		self.access = {
			'classes': None,
			'races': None,
			'subclasses': None,
			'subraces': None,
		}

		# sources to find this spell
		self.citations = []


	def get_text(self):
		'''
		Markdown helps DMs create, modify, or publish spells.
		'''
		return SpellToText(self).markdown


	def get_json(self):
		'''
		This json object is more specific than other apis'.
		'''
		return SpellToJson(self).json
