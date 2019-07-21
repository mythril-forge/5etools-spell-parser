from spell import Spell
from spell_to_markdown import SpellToMarkdown
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
		self.verify_area()
		self.get_tags()
		self.get_components()
		self.get_description()
		self.get_access()
		self.get_citation()
		self.get_slug()
		self.get_markdown()
		# create a directory so python doesn't throw a fit


	def get_name(self):
		'''
		After retrieving the name of the spell, it is checked
		for errors before allowing the program to continue.
		'''
		self.name = self.spell_json['name']
		# Raise an error if something is wrong with the name.
		if re.search(r'[^\w\/\-\'\ \(\)]+', self.name):
			error = f'spell name is unexpected: {self.name}'
			raise Exception(error)

	def get_level(self):
		'''
		Retrieves the level of a spell.
		Note that cantrips are level 0.
		'''
		self.level = self.spell_json['level']

	def get_school(self):
		'''
		The data holds a spell's school as a single character.
		This converts that character into its full name.
		Note, we have 8 schools of magic plus psionics.
		'''
		# list all potential schools
		schools = {
			'a':'abjuration',
			'c':'conjuration',
			'd':'divination',
			'e':'enchantment',
			'i':'illusion',
			'n':'necromancy',
			't':'transmutation',
			'v':'evocation',
			'p':'psionic',
		}
		mark = self.spell_json['school']
		mark = mark.lower()
		# figure out which school the mark is
		self.school = schools[mark]

	def get_instances(self):
		'''
		An instance is a point of origin for a spell's effect.
		Some spells have more than one instance.
		For example, scorching ray can target 3 creatures.
		'''
		self.instances = self.extra_json['Instances']

	def get_cast_time(self):
		'''
		A json object holds casting time data.
		In order to extract it, there are a variety of
		if statements that the program must traverse.
		---
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
		A complex json object holds the duration data.
		In order to extract a duration, there are a variety
		of if statements that the program must traverse.
		---
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
		This uses internal json rather than collected data.
		The external data is not always correct for range.
		Rather, the internal json is stored as a string,
		so this function can parse it into useable data.
		---
		Valid data includes:
		- self
		- touch
		- unlimited
		- special
		- discrete (# points; 72 in an inch)
		'''
		# First, clean data extras from the internal json.
		# These extras contain missing shape data.
		# We rely on these extras for range & shape data.
		range_data = self.extra_json['Range']
		range_data = re.sub(r'\(.*?\)', '', range_data)
		range_data = range_data.strip()
		range_data = range_data.lower()
		range_data = re.split(r'[\s-]+', range_data)

		# Typical results.
		if len(range_data) == 1:
			type = range_data[0]

			# Qualitative results.
			if type == 'sight' or type == 'unlimited':
				self.range['quality'] = 'unlimited'
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
		This uses internal json rather than collected data.
		The external data is not always correct for shape area.
		Rather, the internal json is stored as a string,
		so this function can parse it into useable data.
		---
		For valid data, see shape_parameter object in helper.py.
		'''
		# These extras contain the missing data.
		shape_data = self.extra_json['Range']
		shape_data = shape_data.lower()
		shape_data = re.findall(r'\(.*?\)', shape_data)
		shape_data = ''.join(shape_data)
		shape_data = shape_data.replace('(', '')
		shape_data = shape_data.replace(')', '')
		shape_data = shape_data.replace('-radius',' radius')
		shape_data = shape_data.strip()
		shape_data = shape_data.split('; ')

		# Needed for later
		shape = None
		# This dictionary will store extracted data.
		shape_dict = {}
		# Each item in shape_data is scanned.
		# Note that after splitting the original string,
		# the resulting data is itself still a string.
		for index, dimension in enumerate(shape_data):
			# A 'dimension' is a measurement type, for example,
			# length, width, height, or radius with measurements.
			dimension = dimension.split(' ')
			if len(dimension) == 3:
				# The third indice of data is extraneous.
				if dimension[2] in {'sphere', 'hemisphere'}:
					dimension.pop()
				else:
					raise

			# A dimension of 2 is typical.
			if len(dimension) == 2:
				measurement = dimension[1]
				data = dimension[0].split('-')
				amount = float(data[0])
				type = data[1]
				# Sometimes we have gunked up data like this.
				if measurement in {'cube', 'wall', 'line'}:
					shape = measurement
					measurement = 'length'
				elif measurement in {'sphere', 'cone'}:
					shape = measurement
					measurement = 'radius'
				shape_dict[measurement] = space2num(amount, type)

		# Give data to the main parameter.
		for key in self.area:
			self.area[key] = shape_dict.get(key)

		# Shape was unspecified if it was a cylinder or sphere.
		has_radius = self.area.get('radius')
		has_height = self.area.get('height')
		if not shape and has_radius and has_height:
			shape = 'cylinder'
		elif not shape and has_radius:
			shape = 'sphere'
		self.area['shape'] = shape

	def verify_range(self):
		'''
		We can use external data to cross-check internal data.
		Although the shape data isn't always in the right place,
		it can be used to support or verify data.
		---
		At the end of this function, assert
		statements will ensure data integity.
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
				type = 'unlimited'

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
		'''
		We can use external data to cross-check internal data.
		Although the AoE data isn't always in the right place,
		it can be used to support or verify data.
		---
		At the end of this function, assert
		statements will ensure data integity.
		'''
		area_data = self.spell_json['range']
		# type1 and type2 can be units or shapes.
		type1 = area_data['type']
		type2 = area_data.get('distance', {}).get('type')
		distance = area_data.get('distance', {}).get('amount')

		# a few exceptions need to be converted
		shape_transformations = {
			'radius': 'sphere',
			'hemisphere': 'sphere',
			'sight': 'unlimited',
		}
		if type1 in shape_transformations:
			type1 = shape_transformations[type1]

		# further cleaning with both extra and prime are needed.
		# this dynamic will deduce things like aura spells.
		if type1 == 'point':
			if type2 in {'touch', 'self'}:
				assert(self.range['quality'] == type2)
				assert(self.range['distance'] == None)
			elif type2 in {'sight', 'unlimited'}:
				assert(self.range['quality'] == 'unlimited')
			elif type2 in convert_space:
				# Get distance amount from distance and unit.
				amount = space2num(distance, type2)
				# Deconstruct these longer boolean calculations...
				has_sphere = self.area['shape'] == 'sphere'
				has_line = self.area['shape'] == 'line'
				has_distance = self.range['distance']
				# Conditionally assert based on shape type.
				if has_distance:
					assert(self.range['distance'] == amount)
				elif has_sphere:
					assert(self.area['radius'] == amount)
				elif has_line:
					assert(self.area['length'] == amount)
		elif type1 == 'special':
			assert(self.range['quality'] == type1)
			assert(self.range['distance'] == None)
		elif type1 in shape_parameters:
			amount = space2num(distance, type2)
			if type1 in {'sphere', 'cone'}:
				assert(self.area['radius'] == amount)
			elif type1 in {'cube', 'line'}:
				assert(self.area['length'] == amount)

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
			material = self.spell_json['components'].get('m')
			if not isinstance(material, str):
				self.components['material'] = material['text']
			else:
				self.components['material'] = material
		else:
			pass

	def get_description(self):
		entries = self.spell_json['entries']
		entries = self.classify_desc_info(entries)
		entries = entries.strip()
		markdown = '## Description\n'
		markdown += entries
		if self.spell_json.get('entriesHigherLevel'):
			higher_levels = self.spell_json['entriesHigherLevel']
			higher_levels = self.classify_desc_info(higher_levels)
			higher_levels = higher_levels.strip()
			markdown += '\n\n## At Higher Levels\n'
			markdown += higher_levels
		self.description = markdown

	def classify_desc_info(self, data):
		markdown = ''
		for entry in data:
			if isinstance(entry, str):
				markdown += '\n'
				markdown += entry
				markdown += '\n'

			elif entry.get('type') == 'entries':
				markdown += '\n'
				if entry['name'] != 'At Higher Levels':
					markdown += '### '
					markdown += entry['name']
				markdown += self.classify_desc_info(entry['entries'])

			elif entry.get('type') == 'quote':
				quote = self.classify_desc_info(entry['entries'])
				quote = re.sub(r'\n+', '\n', quote)
				quote = re.sub(r'^(?=\w|.*? )', '> ', quote)
				quote = re.sub(r'\n(?=\w|.*? )', '\n> ', quote)
				quote = quote.strip()
				markdown += '\n'
				markdown += quote
				markdown += '\n> &mdash; '
				markdown += entry['by']
				markdown += '\n'

			elif entry.get('type') == 'list':
				md_list = self.classify_desc_info(entry['items'])
				md_list = re.sub(r'\n+', '\n', md_list)
				md_list = re.sub(r'^(?=\w|.*? )', '- ', md_list)
				md_list = re.sub(r'\n(?=\w|.*? )', '\n- ', md_list)
				md_list = md_list.strip()
				markdown += md_list
				markdown += '\n'

			elif entry.get('type') == 'table':
				labels = self.classify_desc_info(entry['colLabels'])
				labels = re.sub(r'\n+', '\n', labels)
				labels = re.sub(r'^(?=\w|.*? )', '| ', labels)
				labels = re.sub(r'\n(?=\w|.*? )', ' | ', labels)
				labels = labels.strip()
				markdown += labels
				markdown += ' |\n|'
				# add seperator
				for col in entry['colLabels']:
					markdown += '-----|'
				markdown += '\n'
				# add details
				for row in entry['rows']:
					details = self.classify_desc_info(row)
					details = re.sub(r'\n+', '\n', details)
					details = re.sub(r'^(?=\w|.*? )', '| ', details)
					details = re.sub(r'\n(?=\w|.*? )', ' | ', details)
					details = details.strip()
					markdown += details
					markdown += ' |\n'

			elif entry.get('type') == 'cell':
				if entry['roll'].get('exact'):
					roll = str(entry['roll']['exact'])
				else:
					roll = str(entry['roll']['min'])
					roll += '&mdash;'
					roll += str(entry['roll']['max'])
				markdown += roll
		# finally, return our result
		return markdown

	def clean_info(self, entry):
		return entry

		raise
	def get_access(self):
		classes = []
		subclasses = []
		races = []
		subraces = []
		for player_class in self.spell_json['classes'].get('fromClassList'):
			classes.append(player_class['name'])
		if self.spell_json['classes'].get('fromSubclass'):
			for player_subclass in self.spell_json['classes'].get('fromSubclass'):
				subclass =''
				subclass += player_subclass['subclass']['name']
				subclass += ' '
				subclass += player_subclass['class']['name']
				subclasses.append(subclass)

		if self.spell_json.get('races'):
			for entry in self.spell_json['races']:
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
		self.citation['book'] = self.spell_json['source']
		self.citation['page'] = self.spell_json.get('page')

	def get_slug(self):
		'''
		Generates a kabab-case spell name for use on the web.
		slugify() can make our markdown files kabab-case.
		'''
		result = re.sub(r'([^\s\w/]|_)+', '', self.name)
		result = result.lower()
		result = slugify(result)
		self.slug = result
