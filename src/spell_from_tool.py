from spell import Spell
import re
import os
from slugify import slugify
from helper import *

class ToolSpell(Spell):
	'''
	"ToolSpell()" grabs spell data from 5etools.
	This data can be found on their github repo.
	'''
	def __init__(self, json, json_xtra):
		super().__init__(json)
		# this is upsetting, but needed for now.
		# somehow, the shape is not specified in the json.
		# example: we need to know certain info about fireball.
		# fireball is 150ft range, but also 20ft radius AoE.
		self.xtra = json_xtra
		# finally, get everything
		self.get() # very important!

	def get(self):
		'''
		"get()" calls every "get_*" helper function.
		This retrieves and cleans all data of a spell,
		which is then stored in this spell object.
		'''
		self.get_name()
		self.get_slug()
		self.get_path()
		self.get_level()
		self.get_school()
		self.get_cast_time()
		self.get_duration()
		self.get_instances()
		self.get_range()
		self.get_area()
		self.get_tags()
		self.get_components()
		self.get_info()
		self.get_access()
		self.get_markdown()

	def get_name(self):
		'''
		"get_name()" simply retrieves the name of a spell.
		'''
		self.name = self.json['name']

	def get_slug(self):
		'''
		"get_slug()" uses a package called "slugify".
		"slugify()" can make our markdown files kabab-case.
		'''
		expression = re.compile('([^\s\w/]|_)+')
		clean_name = expression.sub('', self.name).lower()
		self.slug = slugify(clean_name)

	def get_path(self):
		'''
		"get_path()" generates a filepath for this spell.
		This is used as the destination of the output.
		---
		"get_path()" uses a package called "os".
		"os" can help by creating directories.
		'''
		# create a directory so python doesn't throw a fit
		if not os.path.exists(f'./{self.TEMP_BOOK}/'):
			os.makedirs(f'./{self.TEMP_BOOK}/')
		self.path = f'./{self.TEMP_BOOK}/{self.slug}.md'

	def get_level(self):
		'''
		"get_level()" simply retrieves the level of a spell.
		'''
		self.level = self.json['level']

	def get_school(self):
		'''
		"get_school()" converts a character into a word.
		Specifically, it gives one of eight schools of magic.
		'''
		mark = self.json['school']
		mark = mark.lower()
		# figure out which school the mark is
		if mark == 'a':
			school = 'abjuration'
		elif mark == 'c':
			school = 'conjuration'
		elif mark == 'd':
			school = 'divination'
		elif mark == 'e':
			school = 'enchantment'
		elif mark == 'i':
			school = 'illusion'
		elif mark == 'n':
			school = 'necromancy'
		elif mark == 't':
			school = 'transmutation'
		elif mark == 'v':
			school = 'evocation'
		else:
			raise Exception(self.name)
		# apply the school result
		self.school = school

	def get_cast_time(self):
		'''
		"get_cast_time()" has a few possibilities.
		Usually, a spell has a quality:
		- action
		- bonus action
		- reaction
		- special
		However, it can also have a duration.
		If a spell has a duration, its converted to seconds.
		'''
		# check for a special condition
		if len(self.json['time']) > 1:
			self.cast_time['quality'] = 'special'
		# this is a regular condition
		elif len(self.json['time']) == 1:
			time = self.json['time'][0]
			# quality of cast_time
			if time['unit'] == 'action':
				self.cast_time['quality'] = 'action'
			elif time['unit'] == 'bonus':
				self.cast_time['quality'] = 'bonus action'
			elif time['unit'] == 'reaction':
				self.cast_time['quality'] = 'reaction'
				self.cast_time['condition'] = time['condition']
			# seconds of cast_time
			elif time['unit'] == 'round':
				self.cast_time['seconds'] = time['number'] * 10
			elif time['unit'] == 'minute':
				self.cast_time['seconds'] = time['number'] * 60
			elif time['unit'] == 'hour':
				self.cast_time['seconds'] = time['number'] * 3600
			elif time['unit'] == 'day':
				self.cast_time['seconds'] = time['number'] * 86400
			else:
				raise Exception(self.name)
		else:
			raise Exception(self.name)

	def get_duration(self):
		
		'''
		"get_duration()" has a few possibilities.
		Usually, a spell has a quality:
		- instantaneous
		- indefinate
		- activated
		- special
		However, it can also have a duration.
		If a spell has a duration, its converted to seconds.
		'''
		# check for a special condition
		if len(self.json['duration']) > 1:
			self.duration['quality'] = 'special'
		# this is a regular condition
		elif len(self.json['duration']) == 1:
			duration = self.json['duration'][0]
			# type is a quality
			if duration['type'] == 'instant':
				self.duration['quality'] = 'instantaneous'
			elif duration['type'] == 'permanent':
				self.duration['quality'] = 'indefinate'
			elif duration['type'] == 'special':
				self.duration['quality'] = 'special'
			# type is timed
			elif duration['type'] == 'timed':
				# the json is a bit ugly, but usable.
				# duration['duration']['type'] exists,
				# but only if duration['type'] is timed.
				meta = duration['duration']
				if meta['type'] == 'round':
					self.duration['seconds'] = meta['amount'] * 10
				elif meta['type'] == 'minute':
					self.duration['seconds'] = meta['amount'] * 60
				elif meta['type'] == 'hour':
					self.duration['seconds'] = meta['amount'] * 3600
				elif meta['type'] == 'day':
					self.duration['seconds'] = meta['amount'] * 86400
				else:
					raise Exception(self.name)
			else:
				raise self.name
		else:
			raise self.name

	def get_instances(self):
		pass ### TODO

	def get_range(self):
		'''
		origin ranges come in all shapes and sizes.
		- self
		- touch
		- number of feet
		- unlimited
		- special
		'''
		xtra = self.xtra[self.name]['Range'].lower()
		xtra_shape = ''.join(re.findall('\(.*?\)', xtra)).strip()
		xtra_range = re.sub("[\(\[].*?[\)\]]", "", xtra).strip()
		dirt_shape = self.json['range']
		# now for the main part of the function
		if xtra_range == 'self':
			self.range = 'self'
		elif xtra_range == 'touch':
			self.range = 'touch'
		elif xtra_range == 'unlimited' or xtra_range == 'sight':
			self.range = 'indefinate'
		elif xtra_range == 'special':
			self.range = 'special'
		elif 'feet' in xtra_range:
			self.range = int(xtra_range.replace(' feet',''))
		elif 'miles' in xtra_range:
			self.range = int(xtra_range.replace(' miles','')) * 5280
		elif 'mile' in xtra_range:
			self.range = int(xtra_range.replace(' mile','')) * 5280
		else:
			raise Exception(self.name)

	def get_area(self):
		'''
		unfortunately we need to call a secondary api for this.
		we are using extracted data from elsewhere; "xtra"
		---
		areas come in all shapes and sizes.
		- point
		- ~~creature~~
		- sphere
		- aura
		- cone
		- cube
		- line
		- wall
		- cylinder
		- special
		'''
		xtra = self.xtra[self.name]['Range'].lower()
		xtra_shape = ''.join(re.findall('\(.*?\)', xtra))
		xtra_range = re.sub("[\(\[].*?[\)\]]", "", xtra)
		dirt_shape = self.json['range']
		print(xtra_shape)
		print(dirt_shape)
		print()
		shape = "TODO"
		if shape == 'point':
			pass
		elif shape == 'creature':
			pass
		elif shape == 'sphere':
			self.shape['radius'] = 0
			pass
		elif shape == 'aura':
			self.shape['radius'] = 0
			pass
		elif shape == 'cone':
			self.shape['radius'] = 0
			pass
		elif shape == 'cube':
			self.shape['length'] = 0
			pass
		elif shape == 'line':
			self.shape['length'] = 0
			self.shape['width'] = 0
			pass
		elif shape == 'wall':
			self.shape['radius'] = 0
			self.shape['length'] = 0
			self.shape['width'] = 0
			self.shape['height'] = 0
			pass
		elif shape == 'cylinder':
			self.shape['radius'] = 0
			self.shape['height'] = 0
			pass
		elif shape == 'special':
			pass
		else:
			raise

	def get_tags(self):
		self.tags = {
			'verbal': False,
			'somatic': False,
			'material': False,
			'concentration': False,
			'ritual': False
		}
		if 'v' in self.json['components']:
			self.tags['verbal'] = True
		if 's' in self.json['components']:
			self.tags['somatic'] = True
		if 'm' in self.json['components']:
			self.tags['material'] = True
		if 'concentration' in self.json['duration'][0]:
			self.tags['concentration'] = True
		if 'meta' in self.json:
			if 'ritual' in self.json['meta']:
				self.tags['ritual'] = True

	def get_components(self):
		pass ### TODO

	def get_info(self):
		pass ### TODO

	def get_access(self):
		pass ### TODO

	def get_markdown(self):
		self.markdown = 'atleast it works'
