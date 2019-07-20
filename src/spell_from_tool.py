from spell import Spell
import re
import os
from slugify import slugify
from helper import *

class SpellFromTool(Spell):
	'''
	This class gives methods to fill in a Spells attributes.
	'''
	def __init__(self, SpellData, ExtraData):
		'''
		Initialization immediately calls upon parsing methods.
		'''
		super().__init__()
		# The json passed in will be useful as attributes.
		self.spell_json = SpellData
		self.extra_json = ExtraData[SpellData['name']]
		# The class runs a series of methods to parse json data.
		self.parse_data()
		# Once parsed, these attributes are unneeded clutter.
		del self.spell_json
		del self.extra_json

	def parse_data(self):
		'''
		get() calls every get_*() helper function.
		This retrieves and cleans all data of a spell,
		which is then stored in this spell object.
		'''
		self.get_name()
		self.get_level()
		self.get_school()
		self.get_instances()
		self.get_cast_time()
		self.get_duration()
		self.get_range()
		self.get_area()
		self.verify_range()
		# self.verify_area()
		# self.get_tags()
		# self.get_components()
		# self.get_info()
		# self.get_access()
		# self.get_citation()
		# self.get_slug()
		# self.get_path()

	def get_name(self):
		'''
		Retrieves the name of a spell.
		TODO This should ensure only valid characters:
		a-z;A-Z;0-9; ;-;';&; etc.
		'''
		self.name = self.spell_json['name']
		# print()
		# print(self.name) # TODO REMOVE WHEN DONE

	def get_level(self):
		'''
		Retrieves the level of a spell.
		Note that cantrips are level 0.
		'''
		self.level = self.spell_json['level']

	def get_school(self):
		'''
		get_school() converts a character into a word.
		Specifically, it gives one of eight schools of magic.
		'''
		mark = self.spell_json['school']
		mark = mark.lower()
		# figure out which school the mark is
		if mark == 'a':
			self.school = 'abjuration'
		elif mark == 'c':
			self.school = 'conjuration'
		elif mark == 'd':
			self.school = 'divination'
		elif mark == 'e':
			self.school = 'enchantment'
		elif mark == 'i':
			self.school = 'illusion'
		elif mark == 'n':
			self.school = 'necromancy'
		elif mark == 't':
			self.school = 'transmutation'
		elif mark == 'v':
			self.school = 'evocation'
		elif mark == 'p':
			self.school = 'psionic'

	def get_instances(self):
		'''
		TODO NOTE
		'''
		self.instances = self.extra_json['Instances']

	def get_cast_time(self):
		'''
		Valid data includes:
		- action
		- bonus action
		- reaction
		- special
		- discrete (# seconds)
		'''
		# Normal results.
		if len(self.spell_json['time']) == 1:
			# Deconstruct this large json object...
			cast_time = self.spell_json['time'][0]
			type = cast_time['unit']

			# Qualitative results.
			if type == 'action':
				self.cast_time['quality'] = 'action'
			elif type == 'bonus':
				self.cast_time['quality'] = 'bonus action'
			elif type == 'reaction':
				condition = cast_time['condition']
				self.cast_time['quality'] = 'reaction'
				self.cast_time['condition'] = condition
			elif type == 'special':
				self.cast_time['quality'] = 'special'

			# Quantitative results.
			elif type in singularize_time or pluralize_time:
				amount = cast_time['number']
				self.cast_time['seconds'] = time2num(amount, type)

		# Special results.
		elif len(self.spell_json['time']) > 1:
			self.cast_time['quality'] = 'special'

	def get_duration(self):
		'''
		Valid data includes:
		- instantaneous
		- indefinate
		- activated
		- special
		- discrete (# seconds)
		'''
		# Normal results.
		if len(self.spell_json['duration']) == 1:
			# Deconstruct this large json object...
			duration = self.spell_json['duration'][0]
			type = duration['type']

			# Qualitative results.
			if type == 'instant':
				self.duration['quality'] = 'instantaneous'
			elif type == 'permanent':
				if 'trigger' in duration.get('ends', {}):
					self.duration['quality'] = 'activated'
				else:
					self.duration['quality'] = 'indefinate'
			elif type == 'special':
				self.duration['quality'] = 'special'

			# Quantitative results.
			elif type == 'timed':
				# The json here is a bit ugly, but usable.
				# ['duration'][0]['duration']['type'] exists,
				# but only if ['duration'][0]['type'] is timeds.
				amount = duration['duration']['amount']
				type = duration['duration']['type']
				if type in singularize_time or pluralize_time:
					self.duration['seconds'] = time2num(amount, type)

		# Special results.
		elif len(self.spell_json['duration']) > 1:
			self.duration['quality'] = 'special'

	def get_range(self):
		'''
		TODO NOTE
		'''
		# First, clean data extras from the internal json.
		# These extras contain missing shape data.
		# We rely on these extras for range & shape data.
		range_data = self.extra_json['Range']
		range_data = re.sub(r'\(.*?\)', '', range_data)
		range_data = range_data.strip()
		range_data = range_data.lower()
		range_data = re.split(r'[\s-]+', range_data)

		# Normal results.
		if len(range_data) == 1:
			type = range_data[0]

			# Qualitative results.
			if type == 'sight' or type == 'unlimited':
				self.range['quality'] = 'indefinate'
			elif type == 'self':
				self.range['quality'] = 'self'
			elif type == 'touch':
				self.range['quality'] = 'touch'
			elif type == 'special':
				self.range['quality'] = 'special'

		# Quantitative results.
		elif len(range_data) == 2:
			amount = int(range_data[0])
			type = range_data[1]
			self.range['distance'] = space2num(amount, type)

		# Special results.
		elif len(range_data) > 2:
			self.range['quality'] = 'special'

	def get_area(self):
		'''
		TODO
		'''
		# these extras contains the missing data.
		shape_data = self.extra_json['Range']
		shape_data = shape_data.lower()
		shape_data = re.findall(r'\(.*?\)', shape_data)
		shape_data = ''.join(shape_data)
		shape_data = shape_data.replace('(', '')
		shape_data = shape_data.replace(')', '')
		shape_data = shape_data.strip()
		shape_data = shape_data.split('; ')

		# lets get this loop going!! YEAH!!!
		shape_dict = {}
		for index, dimension in enumerate(shape_data):
			# the dimension array
			dimension = dimension.split(' ')
			if len(dimension) == 3:

				# these parts are just not needed
				if dimension[2] in {'sphere','hemisphere'}:
					dimension.pop()

			# a dimension of 2 is pretty normal
			if len(dimension) == 2:
				measurement = dimension[1]
				foobar = dimension[0].split('-')
				amount = float(foobar[0])
				type = foobar[1]

				# sometimes we have gunked up data like this
				if measurement in {'cube','wall','line'}:
					measurement = 'length'
				elif measurement in {'sphere','cone'}:
					measurement = 'radius'
				shape_dict[measurement] = space2num(amount, type)

		for key in self.area:
			self.area[key] = shape_dict.get(key)

	def verify_range(self):
		'''
		TODO NOTE
		'''
		# Clean data sourced from the main external json.
		# Note that this source is missing data...
		# ...but is useful for cross-check data verification.
		range_data = self.spell_json['range']
		shape = range_data['type']
		# These variables are needed later for assertions.
		amount = None
		type = None

		# Normal results.
		if 'distance' in range_data:
			type = range_data['distance']['type']

			# Qualitative results.
			if shape in shape_parameters:
				type = 'self'
			elif type in {'self', 'touch', 'special'}:
				pass
			elif type in {'sight', 'unlimited'}:
				type = 'indefinate'

			# Quantitative results.
			elif type in singularize_space or type in pluralize_space:
				amount = range_data['distance']['amount']
				amount = space2num(amount, type)
				type = None

		# Special results.
		elif shape == 'special':
			type = 'special'

		# Our json shifts around a self-centered sphere to have
		# a range of its radius rather than a range of self.
		if amount and self.range['quality'] == 'self':
			pass
		else:
			assert(type == self.range['quality'])
			assert(amount == self.range['distance'])

	def verify_area(self):
		pass
		# further cleaning with both extra and prime are needed.
		# this dynamic will deduce things like aura spells.
		if prime_range == extra_range and isinstance(prime_range, int):
			if False:
				pass
			elif extra_shape.get('sphere'):
				prime_shape = extra_shape
			elif extra_shape.get('radius'):
				prime_shape = extra_shape
			elif extra_shape.get('cube'):
				prime_shape = extra_shape
			elif extra_shape.get('wall'):
				prime_shape = extra_shape
			elif extra_shape == {} and prime_shape == 'point':
				extra_shape = 'point'
		elif prime_range == extra_range == 'self':
			if False:
				pass
			elif prime_shape == 'radius':
				prime_shape = extra_shape
			elif prime_shape == 'sphere':
				prime_shape = extra_shape
			elif prime_shape == 'hemisphere':
				prime_shape = extra_shape
			elif prime_shape == 'cone':
				prime_shape = extra_shape
			elif prime_shape == 'cube':
				prime_shape = extra_shape
			elif prime_shape == 'line':
				prime_shape = extra_shape
			elif extra_shape.get('radius'):
				prime_shape = extra_shape
			elif extra_shape.get('cone'):
				prime_shape = extra_shape
			elif extra_shape == {} and prime_shape == 'point':
				prime_shape = 'self'
				extra_shape = 'self'
		elif prime_range == extra_range == 'touch':
			if False:
				pass
			elif extra_shape == {}:
				prime_shape = 'point'
				extra_shape = 'point'
			elif extra_shape.get('radius'):
				prime_shape = extra_shape
			elif extra_shape.get('cube'):
				prime_shape = extra_shape
		elif prime_range == extra_range == 'point':
			print('point')
		elif prime_range == extra_range == 'indefinate':
			if False:
				pass
			elif extra_shape.get('wall'):
				prime_shape = extra_shape
			elif extra_shape.get('radius'):
				prime_shape = extra_shape
			elif extra_shape == {}:
				prime_shape = 'point'
				extra_shape = 'point'
		elif prime_range == extra_range == prime_shape == 'special':
			extra_shape = 'special'
		elif prime_range != extra_range:
			if False:
				pass
			elif extra_shape.get('radius') == prime_range and prime_shape =='point':
				prime_shape = extra_shape
				prime_range = extra_range
			elif extra_shape.get('line') == prime_range and prime_shape =='point':
				prime_shape = extra_shape
				prime_range = extra_range

	def get_tags(self):
		self.tags = {
			'verbal': False,
			'somatic': False,
			'material': False,
			'concentration': False,
			'ritual': False,
			'royalty': False
		}
		if 'components' in self.spell_json:
			components = self.spell_json['components']
			if 'v' in components:
				self.tags['verbal'] = True
			if 's' in components:
				self.tags['somatic'] = True
			if 'm' in components:
				self.tags['material'] = True
			if 'r' in components:
				self.tags['royalty'] = True

		if 'concentration' in self.spell_json['duration'][0]:
			self.tags['concentration'] = True
		if 'meta' in self.spell_json:
			if 'ritual' in self.spell_json['meta']:
				self.tags['ritual'] = True

	def get_components(self):
		if self.tags['material'] == True:
			material = self.json['components'].get('m')
			if not isinstance(material, str):
				self.components['material'] = material['text']
			else:
				self.components['material'] = material
		else:
			pass

	def get_info(self):
		raise

	def get_access(self):
		classes = []
		subclasses = []
		races = []
		subraces = []
		# print(self.json['classes']['fromClassList'])
		for player_class in self.json['classes'].get('fromClassList'):
			classes.append(player_class['name'])
		if self.json['classes'].get('fromSubclass'):
			for player_subclass in self.json['classes'].get('fromSubclass'):
				subclass =''
				subclass += player_subclass['subclass']['name']
				subclass += ' '
				subclass += player_subclass['class']['name']
				subclasses.append(subclass)

		if self.json.get('races'):
			for entry in self.json['races']:
				if entry.get('baseName'):
					subrace = ''
					subrace += entry['name']
					subraces.append(subrace)
				else:
					race = ''
					race += entry['name']

		self.access['class'] = classes
		self.access['subclass'] = subclasses
		self.access['race'] = races
		self.access['subrace'] = subraces

	def get_citation(self):
		self.citation['book'] = self.json['source']
		self.citation['page'] = self.json.get('page')

	def get_slug(self):
		'''
		Generates a kabab-case spell name for use on the web.
		slugify() can make our markdown files kabab-case.
		'''
		result = re.sub(r'([^\s\w/]|_)+', '', self.name)
		result = result.lower()
		result = slugify(result)
		self.slug = slugify(result)

	def get_path(self):
		'''
		Generates a markdown filepath for this spell.
		This is used as the destination of the output.
		'''
		# create a directory so python doesn't throw a fit
		self.path = f'./{self.source}/{self.slug}.md'
