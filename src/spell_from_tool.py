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
	def __init__(self, json, json_extra, source):
		super().__init__(json)
		# this is upsetting, but needed for now.
		# somehow, the shape is not specified in the json.
		# example: we need to know certain info about fireball.
		# fireball is 150ft range, but also 20ft radius AoE.
		self.extra = json_extra
		self.source = source
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
		self.get_source()
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
		if not os.path.exists(f'./{self.source}/'):
			os.makedirs(f'./{self.source}/')
		self.path = f'./{self.source}/{self.slug}.md'

	def get_source(self):
		'''deferred to __init__'''
		pass

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
		elif mark == 'p':
			school = 'psionic'
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
		'''deferred to get_area'''
		pass

	def get_range(self):
		'''
		origin ranges come in all shapes and sizes.
		- self
		- touch
		- number of feet
		- unlimited
		- special
		'''
		extra = self.extra[self.name]['Range'].lower()
		extra_shape = ''.join(re.findall('\(.*?\)', extra)).strip()
		extra_shape = extra_shape.replace('(', '')
		extra_shape = extra_shape.replace(')', '')
		extra_range = re.sub("[\(\[].*?[\)\]]", "", extra).strip()
		dirty = self.json['range']
		# now for the main part of the function
		if extra_range == 'self':
			self.range = 'self'
		elif extra_range == 'touch':
			self.range = 'touch'
		elif extra_range == 'unlimited' or extra_range == 'sight':
			self.range = 'indefinate'
		elif extra_range == 'special':
			self.range = 'special'
		elif 'feet' in extra_range:
			self.range = int(extra_range.replace(' feet',''))
		elif 'miles' in extra_range:
			self.range = int(extra_range.replace(' miles','')) * 5280
		elif 'mile' in extra_range:
			self.range = int(extra_range.replace(' mile','')) * 5280
		else:
			raise Exception(self.name)

	def get_area(self):
		'''
		unfortunately we need to call a secondary api for this.
		we are using extracted data from elsewhere; "extra"
		---
		areas come in all shapes and sizes.
		- point
		- creature
		- sphere
		- aura
		- cone
		- cube
		- line
		- wall
		- cylinder
		- special
		'''
		extra = self.extra[self.name]['Range'].lower()
		extra_shape = ''.join(re.findall('\(.*?\)', extra)).strip()
		extra_shape = extra_shape.replace('(', '')
		extra_shape = extra_shape.replace(')', '')
		extra_range = re.sub("[\(\[].*?[\)\]]", "", extra).strip()
		dirty = self.json['range']
		dirty_range = ''
		print()
		print(self.name)
		print('-'*len(self.name))
		print(f'DIRTY 1: {dirty_range}')
		print(f'DIRTY 2: {dirty}')
		print(f'EXTRA 1: {extra_range}')
		print(f'EXTRA 2: {extra_shape}')
		shape = "TODO"

		has_radius = 'radius' in extra_shape
		has_width = 'width' in extra_shape
		has_length = 'cube' in extra_shape or 'line' in extra_shape or 'wall' in extra_shape
		has_height = 'wall' in extra_shape or 'cylinder' in extra_shape or 'height' in extra_shape
		# check for point
		if dirty['type'] == 'special':
			shape = 'special'
		elif dirty['type'] == 'line':
			shape = 'line'
		elif dirty['type'] == 'cube':
			shape = 'cube'
		elif 'wall' in extra_shape:
			shape = 'wall'
		elif 'cone' in extra_shape:
			print("CONE")
			shape = 'cone'
		elif dirty['type'] == 'point':
			if 'amount' in dirty['distance']:
				dirty_range = dirty['distance']['amount']
			elif has_radius:
				if has_height and has_width:
					print("HEIHGT WIDTH POINT!?")
					raise
				elif has_height and has_radius:
					shape='cylinder'
				else:
					shape = 'sphere'
			elif extra_shape:
				raise
			# here we're pretty sure the item is a point.
			else:
				if dirty['distance']['type'] == 'self':
					shape = 'point'
				elif dirty['distance']['type'] == 'touch':
					shape = 'point'
				elif dirty['distance']['type'] == 'sight':
					shape = 'point'
				elif dirty['distance']['type'] == 'unlimited':
					shape = 'point'
				elif dirty['distance']['type'] == 'feet':
					shape = 'point'
				elif dirty['distance']['type'] == 'mile':
					shape = 'point'
				elif dirty['distance']['type'] == 'miles':
					shape = 'point'
				else:
					raise
		elif dirty['type'] == 'radius' or dirty['type'] == 'sphere' or dirty['type'] == 'hemisphere':
			if extra_range == 'self' or extra_range == 'touch':
				shape = 'aura'
			else:
				raise
		else:
			raise

		# NOW THAT WE HAVE THE SHAPE WE CAN DECONSTRUCT THINGS
		# hooray, point is good!
		if shape == 'point':
			self.area['shape'] = 'point'

		# creature-centered aura
		elif shape == 'creature':
			self.area['shape'] = 'creature'

		elif shape == 'sphere':
			self.area['shape'] = 'sphere'
			self.area['radius'] = 0

		elif shape == 'aura':
			self.area['shape'] = 'aura'
			dirty_radius = 0
			extra_radius = 0
			# get radius from dirty
			if dirty['distance']['type'] == 'feet':
				dirty_radius = dirty['distance']['amount']
			elif dirty['distance']['type'] == 'miles':
				dirty_radius = dirty['distance']['amount'] * 5280
			else:
				print(f'!{self.name}{dirty} is {shape}: unacceptable data')
				print(self.name)
			# get radius from extra
			if 'foot' in extra_shape:
				extra_radius = extra_shape.split(' ')[0]
				extra_radius = extra_shape.split('-')[0]
				extra_radius = int(extra_radius)
			elif 'mile' in extra_shape:
				extra_radius = extra_shape.split(' ')[0]
				extra_radius = extra_shape.split('-')[0]
				extra_radius = int(extra_radius) * 5280
			else:
				raise
			if dirty_radius == extra_radius:
				self.area['radius'] = dirty_radius
			else:
				raise

		elif shape == 'cone':
			self.area['shape'] = 'cone'
			dirty_radius = 0
			extra_radius = 0
			# get radius from dirty
			if dirty['distance']['type'] == 'feet':
				dirty_radius = dirty['distance']['amount']
			elif dirty['distance']['type'] == 'miles':
				dirty_radius = dirty['distance']['amount'] * 5280
			else:
				print(f'!{self.name}{dirty} is {shape}: unacceptable data')
				print(self.name)
			# get radius from extra
			if 'foot' in extra_shape:
				extra_radius = extra_shape.split(' ')[0]
				extra_radius = extra_shape.split('-')[0]
				extra_radius = int(extra_radius)
			elif 'mile' in extra_shape:
				extra_radius = extra_shape.split(' ')[0]
				extra_radius = extra_shape.split('-')[0]
				extra_radius = int(extra_radius) * 5280
			else:
				raise
			if dirty_radius == extra_radius:
				self.area['radius'] = dirty_radius
			else:
				raise

		elif shape == 'cube':
			self.area['shape'] = 'cube'
			dirty_length = 0
			extra_length = 0
			# get length from dirty
			if dirty['distance']['type'] == 'feet':
				dirty_length = dirty['distance']['amount']
			elif dirty['distance']['type'] == 'miles':
				dirty_length = dirty['distance']['amount'] * 5280
			else:
				print(f'!{self.name}{dirty} is {shape}: unacceptable data')
				print(self.name)
				pass
			# get length from extra
			if 'foot' in extra_shape:
				extra_length = extra_shape.split(' ')[0]
				extra_length = extra_shape.split('-')[0]
				extra_length = int(extra_length)
			elif 'mile' in extra_shape:
				extra_length = extra_shape.split(' ')[0]
				extra_length = extra_shape.split('-')[0]
				extra_length = int(extra_length) * 5280
			else:
				raise
			# if dirty_length == extra_length: ### BROKEN DATA
			self.area['length'] = dirty_length
			# else:
			# 	raise

		elif shape == 'line':
			# get length from dirty
			if dirty['distance']['type'] == 'feet':
				dirty_length = dirty['distance']['amount']
			elif dirty['distance']['type'] == 'miles':
				dirty_length = dirty['distance']['amount'] * 5280
			else:
				print(f'!{self.name}{dirty} is {shape}: unacceptable data')
				print(self.name)
				pass
			# get length from extra
			if 'foot' in extra_shape:
				extra_length = extra_shape.split(' ')[0]
				extra_length = extra_shape.split('-')[0]
				extra_length = int(extra_length)
			elif 'mile' in extra_shape:
				extra_length = extra_shape.split(' ')[0]
				extra_length = extra_shape.split('-')[0]
				extra_length = int(extra_length) * 5280
			else:
				raise
			# if dirty_length == extra_length: ### BROKEN DATA
			self.area['length'] = dirty_length
			self.area['width'] = 5
			# else:
			# 	raise

		elif shape == 'wall':
			self.area['shape'] = 'wall'
			self.area['radius'] = 0
			self.area['length'] = 0
			self.area['width'] = 0
			self.area['height'] = 0

		elif shape == 'cylinder':
			self.area['shape'] = 'cylinder'
			self.area['radius'] = 0
			self.area['height'] = 0

		elif shape == 'special':
			self.area['shape'] = 'special'

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
		if 'components' in self.json:
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
		elif self.school == 'psionic':
			pass
		else:
			raise

	def get_components(self):
		pass ### TODO

	def get_info(self):
		pass ### TODO

	def get_access(self):
		pass ### TODO

	def get_markdown(self):
		self.markdown = 'atleast it works'
