import os
from slugify import slugify

class Spell_5e_Tools:
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

		# metadata
		self.slug = None
		self.file = None # What is this?
		self.TEMP_BOOK = 'phb' # FIXME
		self.path = None

		# overview content
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

		self.access = {
			'class': 'what',
			'race': None,
			'subclass': None,
			'subrace': None,
		}

		print(self.access['class'])
		# finally, get everything!
		self.get() # very important!

	def get(self):
		'''
		get() calls every "get_" helper function.
		This retrieves and cleans all data of a spell,
		which is then stored in this spell object.
		'''
		self.get_slug()
		self.get_file()
		self.get_path()
		self.get_name()
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

	def get_slug(self):
		'''
		get_slug() uses a package called "slugify".
		"slugify" can make our markdown files kabab-case.
		'''
		self.slug = slugify(self.json['name'])

	def get_file(self):
		'''
		WHAT DOES GET FILE DO? XXX
		'''
		pass ### TODO

	def get_path(self):
		'''
		get_path() generates a filepath for this spell.
		This is used as the destination of the output.
		---
		get_path() uses a package called "os".
		"os" can help by creating directories.
		'''
		# create a directory so python doesn't throw a fit
		if not os.path.exists(f'./{self.TEMP_BOOK}/'):
			os.makedirs(f'./{self.TEMP_BOOK}/')
		self.path = f'./{self.TEMP_BOOK}/{self.slug}.md'

	def get_name(self):
		'''
		get_name() simply retrieves the name of a spell.
		'''
		self.name = self.json['name'].lower()

	def get_level(self):
		'''
		get_level simply retrieves the level of a spell.
		'''
		self.level = self.json['level']

	def get_school(self):
		'''
		get_school() converts a character into a word.
		Specifically, it gives one of eight schools of magic.
		'''
		letter = self.json['school']
		letter = letter.lower()
		# figure out which school the letter is
		if False:
			pass
		elif letter == 'a':
			school = 'abjuration'
		elif letter == 'c':
			school = 'conjuration'
		elif letter == 'd':
			school = 'divination'
		elif letter == 'e':
			school = 'enchantment'
		elif letter == 'i':
			school = 'illusion'
		elif letter == 'n':
			school = 'necromancy'
		elif letter == 't':
			school = 'transmutation'
		elif letter == 'v':
			school = 'evocation'
		else:
			raise
		# apply the school result
		self.school = school

	def get_cast_time(self):
		if len(self.json['duration']) == 1:
			duration = self.json['duration'][0]
			if duration['type'] == 'instant':
				self.duration.quality = 'instantaneous'
			elif duration['type'] == 'permanent':
				self.duration.quality = 'indefinate'
			elif duration['type'] == 'timed':
				# the json is a bit ugly, but usable.
				# duration['duration']['type'] exists,
				# but only if duration['type'] is timed.
				meta = duration['duration']
				if meta['type'] == 'rounds':
					self.duration.seconds = meta['amount'] * 10
				elif meta['type'] == 'minutes':
					self.duration.seconds = meta['amount'] * 60
				elif meta['type'] == 'hours':
					self.duration.seconds = meta['amount'] * 3600
				elif meta['type'] == 'days':
					self.duration.seconds = meta['amount'] * 86400
				else:
					raise
			else:
				raise
		else:
			raise

	def get_duration(self):
		if len(self.json['time']) == 1:
			time = self.json['time'][0]
			if time['unit'] == 'action':
				self.cast_time.quality = time['unit']
			elif time['unit'] == 'bonus':
				self.cast_time.quality = 'bonus action'
			elif time['unit'] == 'reaction':
				self.cast_time.quality = time['unit']
				self.cast_time.condition = time['condition']
			elif time['unit'] == 'round':
				self.cast_time.seconds = time['number'] * 10
			elif time['unit'] == 'minute':
				self.cast_time.seconds = time['number'] * 60
			elif time['unit'] == 'hour':
				self.cast_time.seconds = time['number'] * 3600
			elif time['unit'] == 'day':
				self.cast_time.seconds = time['number'] * 86400
			else:
				raise
		else:
			raise

	def get_instances(self):
		pass ### TODO

	def get_range(self):
		pass ### TODO

	def get_area(self):
		pass ### TODO

	def get_tags(self):
		pass ### TODO

	def get_components(self):
		pass ### TODO

	def get_info(self):
		pass ### TODO

	def get_access(self):
		pass ### TODO

test = Spell_5e_Tools("rip")
