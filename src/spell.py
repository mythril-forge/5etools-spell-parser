import re
import os
from slugify import slugify
from helper import *

class Spell:
	'''
	Represents a magic spell in D&D 5th Edition.
	This app was created to accomidate homebrew;
	there are foreign properties in this class.
	The extra properties are left empty for vanilla spells.
	'''
	def __init__(self, json):
		'''
		a spell has many fascets
		'''
		self.json = json

		# basic data
		self.name = None
		self.slug = None
		self.path = None
		self.source = None
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
		self.instances = 1
		self.range = None
		self.area = {
			'shape': None,
			'radius': None,
			'length': None,
			'width': None,
			'height': None,
		}

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
		self.info = {
			'description': None,
			'higher_levels': None,
		}

		# which characters can use this spell?
		self.access = {
			'class': None,
			'race': None,
			'subclass': None,
			'subrace': None,
		}

		# generate the outputs!!
		self.markdown = None
		self.tools_json = None
		self.clean_json = None

	# helper funcitons
	def tagify(self):
		result = []
		if self.tags['verbal']:
			result.append('V')
		if self.tags['somatic']:
			result.append('S')
		if self.tags['material']:
			result.append('M')
		if self.tags['concentration']:
			result.append('C')
		if self.tags['ritual']:
			result.append('R')
		result =  ', '.join(result)
		return result

	def castify(self):
		if self.cast_time['quality']:
			return self.cast_time['quality']
		elif self.cast_time['seconds']:
			return str(self.cast_time['seconds']) + ' seconds'
		else:
			raise

	def durify(self):
		print(self.duration['quality'])
		if self.duration['quality']:
			return self.duration['quality']
		elif self.duration['seconds']:
			return str(self.duration['seconds']) + ' seconds'
		else:
			raise
