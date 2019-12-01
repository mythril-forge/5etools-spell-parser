# python packages
import os
import re
from slugify import slugify
# project imports
from helper import *
from bad_string_parser import *
from spell import Spell



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
		# basic spell data
		self.get_name()
		self.get_homebrew()
		self.get_level()
		self.get_school()
		# high-level metadata
		self.get_slug()
		self.get_path()
		# temporal metadata
		self.get_cast_time()
		self.get_duration()
		# spacial metadata
		self.get_range()
		self.get_area()
		self.get_instances()
 		# boolean metadata
		self.get_tags()
		# phrasal metadata
		self.get_components()
		# long-form description
		self.get_description()
		# sources to find this spell
		self.get_citation()

	def get_name(self):
		'''
		Retrieve the name of the spell.
		'''
		self.name = self.spell_json['name']


	def get_homebrew(self):
		'''
		Check if the spell is a homebrew.
		In this class object, it will never be homebrew.
		'''
		self.homebrew = False


	def get_level(self):
		'''
		Retrieve the level of a spell.
		'''
		self.level = self.spell_json['level']


	def get_school(self):
		'''
		The data holds a spell's school as a single character.
		This converts that character into its full name.
		Note, we have 8 schools of magic, plus psionics.
		'''
		# Mark is a character representing a school of magic.
		mark = self.spell_json['school']
		mark = mark.lower()
		# This is a dictionary of all the spell schools in 5e.
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
		# Figure out which school the mark points to.
		self.school = schools[mark]


	def get_slug(self):
		'''
		Generates a kabab-case spell name for use on the web.
		slugify() can make our markdown files kabab-case.
		'''
		slug = re.sub(r'([^\s\w/]|_)+', '', self.name)
		slug = slug.lower()
		slug = slugify(slug)
		self.slug = slug


	def get_path(self):
		'''
		Path is used internally to know where to put files.
		'''
		path = './spells/'
		path += self.slug
		path += '.md'
		self.path = path


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
				self.cast_time['timespan'] = time2num(amount, type)

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
					self.duration['timespan'] = time2num(amount, type)

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
		# But first, the shape_data needs cleaning.
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

			# A dimension of 2 is typical.
			if len(dimension) == 2:
				# Split up the string-data into seperate variables.
				measurement = dimension[1]
				data = dimension[0].split('-')
				amount = float(data[0])
				type = data[1]
				# Sometimes we have gunked up data like this.
				if measurement in {'cube', 'wall', 'line'}:
					if measurement == 'line':
						shape_dict['width'] = space2num(5, 'feet')
					shape = measurement
					measurement = 'length'
				elif measurement in {'sphere', 'cone'}:
					shape = measurement
					measurement = 'radius'
				# Gather data based on amount and type.
				shape_dict[measurement] = space2num(amount, type)

		# Give data to the main parameter.
		for key in self.area:
			self.area[key] = shape_dict.get(key)

		# Shape could still be unspecified by now.
		has_radius = self.area.get('radius')
		has_height = self.area.get('height')
		if not shape and has_radius and has_height:
			shape = 'cylinder'
		elif not shape and has_radius:
			shape = 'sphere'

		# Descripe the area's shape from extracted data.
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
				has_distance = self.range['distance']
				has_sphere = self.area['shape'] == 'sphere'
				has_line = self.area['shape'] == 'line'

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


	def get_instances(self):
		'''
		An instance is a point of origin for a spell's effect.
		Some spells have more than one instance.
		For example, scorching ray can target 3 creatures.
		'''
		self.instances = self.extra_json['Instances']


	def get_tags(self):
		'''
		Sets the boolean value of each spell tag.
		Royalty is a wierd one that is still acceptable;
		it represents an amount of gold consumed,
		equal to the spell's level.
		'''
		# Initialize all tags to false.
		self.tags = {
			'verbal': False,
			'somatic': False,
			'material': False,
			'concentration': False,
			'ritual': False,
			'royalty': False
		}
		# Set basic components
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

		# Add concentration and ritual if applicable
		if 'concentration' in self.spell_json['duration'][0]:
			self.tags['concentration'] = True
		if 'meta' in self.spell_json:
			if 'ritual' in self.spell_json['meta']:
				self.tags['ritual'] = True


	def get_components(self):
		'''
		Grabs sentances describing a spell's components.
		'''
		# Normally, only material components have a phrase.
		if self.tags['material'] == True:
			material = self.spell_json['components'].get('m')
			if not isinstance(material, str):
				self.components['material'] = material['text']
			else:
				self.components['material'] = material
		else:
			pass


	def get_description(self):
		'''
		Gathers the object containing the details
		of a spell's description, which holds much data.
		'''
		# To keep things DRY, the object must stay consistant.
		# To do so, the two main entries are put into an object.
		primary = self.spell_json.get('entries')
		powerup = self.spell_json.get('entriesHigherLevel')

		# The `entries` object is a supermassive clusterfuck.
		# Sorry! Just saying, its not pretty.
		entries = [{
			'type': 'entries',
			'name': 'Description',
			'entries': primary,
		}]
		if powerup is not None:
			entries.append(powerup)

		# Some subroutines are required to parse the data.
		def scrub_data(entry, depth=0):
			'''
			This will take the entries object and clean it.
			It does a thorough job; it cleans entries recursively.
			The function takes in the expected 5etools object,
			and it returns a markdown-like string.
			'''
			# A string can't be deconstructed any more;
			# this just parses it a bit before returning.
			if isinstance(entry, str):
				# Each sentance needs to be on a different line.
				# The `tails` regex finds areas that break this rule.
				tails= r'(?<=[ .!?]) '
				# All that needs to be done is adding some extra
				# new-line breaks to keep GitHub diffs prettier.
				cleaned = re.sub(tails, '\n', entry)
				cleaned = f'{cleaned}\n'
				return cleaned

			# The entry is type list.
			# Just iterate through and clean each item!
			elif isinstance(entry, list):
				cleaned = ''
				# This entry has yet more entries.
				for item in entry:
					cleaned += scrub_data(item, depth)
				return cleaned

			# The entry is type `entries`.
			# As ambiguous as that is, it is easy to explain.
			# This is just a heading with content.
			elif entry.get('type') == 'entries':
				cleaned = f"{'#' * (depth + 2)} {entry['name']}\n"
				cleaned += scrub_data(entry['entries'], depth + 1)
				return cleaned

			elif entry.get('type') == 'quote':
				# The entry is expected to be a string,
				# but it might work with other formats.
				# Naturally, the entry must be cleaned.
				cleaned = scrub_data(entry['entries'], depth).strip()
				cleaned = re.sub(r'^', '> ', cleaned) + '\n'
				cleaned = re.sub(r'\n', '\n> ', cleaned)
				cleaned += f"\n> &mdash; {entry['by']}\n"
				return cleaned

			# An entry with type=list is not a list-type object.
			# Instead, it represents a bulleted list.
			elif entry.get('type') == 'list':
				cleaned = ''
				# This entry has yet more entries...eerrr, items.
				for item in entry['items']:
					# The item is expected to be a string,
					# but it might work with other formats.
					# Naturally, the item must be cleaned.
					content = scrub_data(item, depth)
					content = f'- {content}'
					# If the item is a multiline string, then
					# each line after the first must be indented.
					content = re.sub(r'\n', '\n\t', content)
					cleaned += content.strip() + '\n'
				return cleaned

			# The entry is a table.
			# Iterate through the contents and build it up!
			elif entry.get('type') == 'table':
				cleaned = ''
				# Start with the caption, if any.
				if entry.get('caption'):
					cleaned += f"#### {entry['caption']}\n"
				# This entry has yet more entries...eerrr, cells.
				cleaned += '|'
				for cell in entry.get('colLabels'):
					cleaned += (
						f' {scrub_data(cell, depth).strip()} |'
					)
				cleaned += (
					f"\n{'|-----' * len(entry['colLabels'])}|"
				)
				# This entry has yet more entries...eerrr, cells.
				for row in entry.get('rows'):
					cleaned += '\n|'
					for cell in row:
						cleaned += (
							f' {scrub_data(cell, depth).strip()} |'
						)
				cleaned += '\n'
				return cleaned

			# The `cell` type is a bit of a misnomer.
			# It only allows for number-based dice-roll results.
			elif entry.get('type') == 'cell':
				# Check whether its a roll range, or an exact roll.
				if entry['roll'].get('exact'):
					cleaned = str(entry['roll']['exact'])
				else:
					minimum = entry['roll']['min']
					maximum = entry['roll']['max']
					cleaned = f'{minimum}&ndash;{maximum}'
				# The result will be formatted as a table-item
				# higher in the recursive stack-trace.
				return cleaned

			else:
				print(entry)
				input('Something went wrong. See logs above.')
				raise Exception('INVALID ENTRY TYPE')

		# From there we still need to clean the entries more...
		# Specifically, some text needs bolded or other formats.
		# Looks like we need another subroutine!
		def parse_metadata(text):
			tag = re.search(r'{@.*? ', text)
			if tag is None:
				# There are no special tags in the text.
				return text

			# Split left, middle, and right based on tag result.
			# The tag is the middle, but we will be deleting it.
			left_text = text[:tag.span()[0]]
			right_text = text[tag.span()[1]:]
			tag = tag.group()[2:-1]

			# Recursively clean the right side of the text first.
			# This takes care of any nested text-tagging.
			right_text = parse_metadata(right_text)

			# Since the right text is cleaned, we can safely find
			# text leading to the next available closing brace.
			middle_text = re.search(r'.*?(?=})', right_text)
			right_text = right_text[middle_text.span()[1] + 1:]
			middle_text = middle_text.group()

			# ==NOTE==
			# Now there are four variables.
			# 1. tag
			# 2. left_text
			# 3. right_text
			# 4. middle_text

			if tag == 'action':
				# Actions are italicized.
				middle_text = f'*{middle_text}*'

			elif tag == 'chance':
				# Dice, randomness, and other math use code blocks.
				middle_text = f'`{middle_text}%`'

			elif tag == 'condition':
				# ==NOTE==
				# This `||` delimiter is a binary operator.
				# It means the item on the right should be used.
				middle_text = re.sub(r'.*\|\|', '', middle_text)
				# Conditions get emphasized/bolded.
				middle_text = f'**{middle_text}**'

			elif tag == 'creature':
				# ==NOTE==
				# This `||` delimiter is a binary operator.
				# It means the item on the right should be used.
				middle_text = re.sub(r'.*\|\|', '', middle_text)
				# Certain game mechanics get capitalized.
				middle_text = middle_text.title()
				# ==FIXME==
				# "The Celestial" should not be capitalized.

			elif tag == 'damage':
				# Use proper mathematics symbols.
				middle_text = re.sub(r'[\+]',   ' + ', middle_text)
				middle_text = re.sub(r'[\–\-]', ' – ', middle_text)
				middle_text = re.sub(r'[\×\*]', ' × ', middle_text)
				middle_text = re.sub(r'[\÷\/]', ' ÷ ', middle_text)
				# Dice modifiers must have one space of padding.
				middle_text = re.sub(r' +', ' ', middle_text)
				# Dice, randomness, and other math use code blocks.
				middle_text = f'`{middle_text}`'

			elif tag == 'dice':
				# ==NOTE==
				# This `|` delimiter is a binary operator.
				# It means the item on the left should be used.
				middle_text = re.sub(r'\|.*', '', middle_text)
				# Use proper mathematics symbols.
				middle_text = re.sub(r'[\+]',   ' + ', middle_text)
				middle_text = re.sub(r'[\-\–]', ' – ', middle_text)
				middle_text = re.sub(r'[\*\×]', ' × ', middle_text)
				middle_text = re.sub(r'[\/\÷]', ' ÷ ', middle_text)
				# Dice modifiers must have one space of padding.
				middle_text = re.sub(r' +', ' ', middle_text)
				# Dice, randomness, and other math use code blocks.
				middle_text = f'`{middle_text}`'

			elif tag == 'filter':
				# ==NOTE==
				# This `|` delimiter is a binary operator.
				# It means the item on the left should be used.
				middle_text = re.sub(r'\|.*', '', middle_text)

			elif tag == 'hit':
				# Use proper mathematical symbols.
				middle_text = re.sub(r'[\+]',   '+', middle_text)
				middle_text = re.sub(r'[\-\–]', '–', middle_text)
				middle_text = re.sub(r'[\*\×]', '×', middle_text)
				middle_text = re.sub(r'[\/\÷]', '÷', middle_text)
				# Dice, randomness, and other math use code blocks.
				middle_text = f'`{middle_text}`'

			elif tag == 'i':
				# Weird inline quotes get italics + double-quotes.
				middle_text = f'*"{middle_text}"*'

			elif tag == 'item':
				# Items need to be italic
				middle_text = f'*{middle_text}*'

			elif tag == 'note':
				# Notes might be good in blockquotes, but naw.
				pass

			elif tag == 'race':
				# Certain game mechanics get capitalized.
				middle_text = middle_text.title()

			elif tag == 'scaledice':
				# Dice, randomness, and other math use code blocks.
				middle_text = f'`{middle_text}`'
				# input(middle_text)

			elif tag == 'sense':
				# Senses don't get any special format.
				pass

			elif tag == 'skill':
				# Certain game mechanics get capitalized.
				middle_text = middle_text.title()

			elif tag == 'spell':
				# Spells should be italicized and become anchored.
				middle_text = f'[*{middle_text}*][link]'

			else:
				print('\n', tag)
				input(middle_text)
				raise Exception(tag)

			# Return post-formatted text.
			return left_text + middle_text + right_text

		# Awesome! Now we can actually call those functions.
		entries = scrub_data(entries)
		entries = parse_metadata(entries)
		self.description = entries

	def get_citation(self):
		'''
		Defines the book that this spell can be found in.
		'''
		# grab variables
		source = self.spell_json['source']
		page = self.spell_json.get('page')
		# create object
		citation = {
			'book': self.spell_json['source'],
			'page': self.spell_json.get('page'),
		}
		# throw citation on class
		self.citations.append(citation)
