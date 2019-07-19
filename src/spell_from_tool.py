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
		self.get_cast_time()
		self.get_duration()
		self.get_instances() # covered by get_range
		self.get_range()
		self.verify_range()
		# self.get_area() # covered by get_range
		# self.get_tags()
		# self.get_components()
		# self.get_info()
		# self.get_access()
		# self.get_citation()
		# self.get_markdown()
		# self.get_slug()
		# self.get_path()
		# raise Exception('HOORAY')

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

	def get_instances(self):
		'''deferred to get_range'''
		pass

	def get_range(self):
		'''
		origin ranges come in all shapes and sizes.
		---
		HACK: this function is absurdly long.
		it is in a dire need of refactor.
		'''
		def check_error(data = []):
			print(self.name)
			for item in data:
				print(item)
			return Exception('!!! unexpected range type !!!')



		# clean data extras from internally collected json.
		# these extras contains the missing data.
		extra = self.extra[self.name]['Range'].lower()
		self.instances = self.extra[self.name]['Instances']
		# refine extra variables.
		# these data are held as string; they need parsed.
		# NOTE add good comments!
		extra_shape = ''.join(re.findall('\(.*?\)', extra))
		extra_shape = extra_shape.strip()
		extra_shape = extra_shape.replace('(', '')
		extra_shape = extra_shape.replace(')', '')
		extra_shape = extra_shape.split('; ')
		extra_shape_dict = {}
		for index, dimension in enumerate(extra_shape):
			# the dimension array
			dimension = dimension.split(' ')
			if len(dimension) == 3:
				if dimension[2] in ['sphere','hemisphere']:
					dimension.pop()
			if len(dimension) == 2:
				key = dimension[1]
				val = dimension[0]
				val = val.split('-')
				if val[1] in ['inch','inches']:
					val = float(val[0]) / 12
				elif val[1] == 'foot':
					val = int(val[0])
				elif val[1] == 'mile':
					val = int(val[0]) * 5280
				else:
					raise check_error([dimension])
				extra_shape_dict[key] = val
			elif len(dimension) > 3 or len(dimension) < 1:
				print(dimension)
				raise check_error()
		# NOTE add good comments!
		extra_shape = extra_shape_dict
		del extra_shape_dict
		# NOTE add good comments!
		extra_range = re.sub("[\(\[].*?[\)\]]", "", extra)
		extra_range = extra_range.strip()
		extra_range = extra_range.split(' ')
		# NOTE add good comments!
		if len(extra_range) > 1:
			# NOTE add good comments!
			extra_type = extra_range[1]
			extra_range = int(extra_range[0])
			# NOTE add good comments!
			if extra_type in ['feet','foot']:
				pass
			elif extra_type in ['miles','mile']:
				extra_range = extra_range * 5280
			else:
				raise check_error([extra_shape,extra_range,extra_type])
		else:
			extra_range = extra_range[0]
		# NOTE add good comments!
		if extra_range in ['sight', 'unlimited']:
			extra_range = 'indefinate'



		# NOTE add good comments!
		# clean the prime source data from external json.
		# this prime source is missing data.
		prime = self.json['range']
		# refine prime variables.
		# the object is a bit wonky so it needs cleaning.
		prime_shape = prime['type']
		if 'distance' in prime:
			prime_type = prime['distance']['type']
			# if there is a distance & point, it is not an AoE.
			# there is one exception: it could be a wall.
			if prime_shape == 'point':
				# feet and miles give a discrete value to range.
				if prime_type == 'feet':
					prime_range = prime['distance']['amount']
				elif prime_type == 'miles':
					prime_range = prime['distance']['amount'] * 5280
				# self & touch get no distance. it overwrites range.
				elif prime_type in ['self', 'touch']:
					prime_range = prime_type
				# sight & unlimited are abstracted to "indefinate".
				elif prime_type in ['sight', 'unlimited']:
					prime_range = 'indefinate'
				else:
					raise check_error()
			# if there is a radius, it implies an aura.
			# a range overwrites a description of a shape.
			elif prime_shape in ['radius', 'sphere', 'hemisphere', 'cone', 'line']:
				prime_range = 'self'
			elif prime_shape == 'cube':
				prime_range = 'self'
			else:
				raise check_error()
		# special is just a sort of catch-all for oddities.
		elif prime_shape == 'special':
			prime_range = 'special'
		else:
			raise check_error()
		# NOTE add good comments!
		# extra_range == 'self'
		# prime_range == 5
		# extra_shape == {radius 5}
		# prime_shape == 'point'



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



		# finish things out with some assertions
		assert(extra_range == prime_range)
		assert(extra_shape == prime_shape)
		# great! let's get to the data-getter.
		self.range = prime_range
		if prime_shape != {} and isinstance(prime_shape,dict):
			if prime_shape.get('sphere'):
				self.area['shape'] = 'sphere'
				self.area['radius'] = prime_shape['sphere']
			elif prime_shape.get('cube'):
				self.area['shape'] = 'cube'
				self.area['length'] = prime_shape['cube']
			elif prime_shape.get('cone'):
				self.area['shape'] = 'cone'
				self.area['radius'] = prime_shape['cone']
			elif prime_shape.get('line'):
				self.area['shape'] = 'line'
				self.area['length'] = prime_shape['line']
				self.area['width'] = 5
			elif prime_shape.get('wall'):
				self.area['shape'] = 'wall'
				self.area['length'] = prime_shape['wall']
				self.area['width'] = prime_shape['width']
				self.area['height'] = prime_shape['height']
			elif prime_shape.get('height'):
				self.area['shape'] = 'cylinder'
				self.area['radius'] = prime_shape['radius']
				self.area['height'] = prime_shape['height']
			elif prime_shape.get('radius'):
				if prime_range == 'self':
					self.area['shape'] = 'aura'
				else:
					self.area['shape'] = 'sphere'
				self.area['radius'] = prime_shape['radius']
			else:
				print(prime_shape)
				raise Exception(f'\n{prime_shape}\n{prime_range}')
		else:
			# pass to keep shape undefined.
			if prime_shape == {}:
				pass
			elif prime_shape == 'point':
				pass
			elif prime_shape == 'self':
				pass
			elif prime_shape == 'special':
				pass
			else:
				raise Exception(f'\n{prime_shape}\n{prime_range}')

	def get_area(self):
		'''deferred to get_range'''
		pass

	def get_tags(self):
		self.tags = {
			'verbal': False,
			'somatic': False,
			'material': False,
			'concentration': False,
			'ritual': False,
			'royalty': False
		}
		if 'components' in self.json:
			if 'v' in self.json['components']:
				self.tags['verbal'] = True
			if 's' in self.json['components']:
				self.tags['somatic'] = True
			if 'm' in self.json['components']:
				self.tags['material'] = True
			if 'r' in self.json['components']:
				self.tags['royalty'] = True
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
		if self.tags['material'] == True:
			material = self.json['components'].get('m')
			if not isinstance(material, str):
				self.components['material'] = material['text']
			else:
				self.components['material'] = material
		else:
			pass

	def clean_info(self, info):
		# work around
		info = re.sub(r'animated object \(','',info)
		info = re.sub(r'\)\|phb\|.*?}','}',info)
		info = re.sub(r'1d20.*?\|','',info)
		# general case
		info = re.sub(r'}','',info) # can't use (?<={@.*? .*?)}
		info = re.sub(r'{@.*? ','',info)
		info = re.sub(r'\n\n+', '\n\n', info)
		info = re.sub(r'dretch\|\|', '', info) # jeeze :\
		info = re.sub(r'\d+d\d+\|\d-\d\|', '', info)
		info = info.strip()
		return info

	def get_info(self):
		result = ''
		for entry in self.json['entries']:
			if isinstance(entry,str):
				result += '\n\n'
				result += entry

			else:
				if entry['type'] == 'quote':
					result += '\n'
					for sub_entry in entry['entries']:
						result += '\n'
						result += '> '
						result += sub_entry
					result += '\n> \n> &mdash;'
					result += entry['by']

				elif entry['type'] == 'list':
					for item in entry['items']:
						result += '\n'
						result += '- '
						result += item

				elif entry['type'] == 'entries':
					result += '\n\n### '
					result += entry['name']
					first = True
					for sub_entry in entry['entries']:
						if first:
							first = False
						else:
							result += '\n'
						result +='\n'
						
						if isinstance(sub_entry,dict):
							if sub_entry['type'] == 'list':
								for item in sub_entry['items']:
									result += '\n'
									result += '- '
									result += item
						else:
							result += sub_entry

				elif entry['type'] == 'table':
					if entry.get('caption'):
						result += '\n\n#### '
						result += entry['caption']
					result += '\n\n|'
					for col in entry['colLabels']:
						result += ' '
						result += col
						result += ' |'
					result += '\n|'
					for col in entry['colLabels']:
						result += ' '
						result += '---'
						result += ' |'
					for row in entry['rows']:
						result += '\n|'
						for data in row:
							if isinstance(data, dict):
								if data.get('type') == 'cell':
									if data['roll'].get('exact'):
										result += ' '
										result += str(data['roll']['exact'])
										result += ' |'
									elif data['roll'].get('min') and data['roll'].get('max'):
										result += ' '
										result += str(data['roll']['min'])
										result += '&mdash;'
										result += str(data['roll']['max'])
										result += ' |'
							else:
								if not isinstance(data, str):
									raise Exception(data)
								data = self.clean_info(data)
								result += ' '
								result += data
								result += ' |'
					result += '\n\n'
				else:
					raise
				pass

		if self.json.get('entriesHigherLevel'):
			for entry in self.json.get('entriesHigherLevel'):
				if isinstance(entry,str):
					result += '\n\n'
					result += entry

				else:
					if entry['type'] == 'quote':
						result += '\n'
						for sub_entry in entry['entries']:
							result += '\n'
							result += '> '
							result += sub_entry
						result += '\n> \n> &mdash;'
						result += entry['by']

					elif entry['type'] == 'list':
						for item in entry['items']:
							result += '\n'
							result += '- '
							result += item

					elif entry['type'] == 'entries':
						result += '\n\n## '
						result += entry['name']
						first = True
						for sub_entry in entry['entries']:
							if first:
								first = False
							else:
								result += '\n'
							result +='\n'
							
							if isinstance(sub_entry,dict):
								if sub_entry['type'] == 'list':
									for item in sub_entry['items']:
										result += '\n'
										result += '- '
										result += item
							else:
								result += sub_entry

					elif entry['type'] == 'table':
						if entry.get('caption'):
							result += '\n\n#### '
							result += entry['caption']
						result += '\n\n|'
						for col in entry['colLabels']:
							result += ' '
							result += col
							result += ' |'
						result += '\n|'
						for col in entry['colLabels']:
							result += ' '
							result += '---'
							result += ' |'
						for row in entry['rows']:
							result += '\n|'
							for data in row:
								if isinstance(data, dict):
									if data.get('type') == 'cell':
										if data['roll'].get('exact'):
											result += ' '
											result += str(data['roll']['exact'])
											result += ' |'
										elif data['roll'].get('min') and data['roll'].get('max'):
											result += ' '
											result += str(data['roll']['min'])
											result += '&mdash;'
											result += str(data['roll']['max'])
											result += ' |'
								else:
									if not isinstance(data, str):
										raise Exception(data)
									data = self.clean_info(data)
									result += ' '
									result += data
									result += ' |'
						result += '\n\n'
					else:
						raise
					pass

		self.info = self.clean_info(result)


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

	def distill_cast_time(self):
		result = ''
		if self.cast_time.get('quality') == 'special':
			result += self.cast_time['quality']
		elif self.cast_time.get('quality') == 'action':
			result += self.cast_time['quality']
		elif self.cast_time.get('quality') == 'bonus action':
			result += self.cast_time['quality']
		elif self.cast_time.get('quality') == 'reaction':
			result += self.cast_time['quality']
			result += ', '
			result += self.cast_time['condition']
		elif self.cast_time.get('seconds'):
			if self.cast_time['seconds'] % 604800 == 0:
				number = self.cast_time['seconds'] // 604800
				result += str(number)
				if number == 1:
					result += ' week'
				else:
					result += ' weeks'
			elif self.cast_time['seconds'] % 86400 == 0:
				number = self.cast_time['seconds'] // 86400
				result += str(number)
				if number == 1:
					result += ' day'
				else:
					result += ' days'
			elif self.cast_time['seconds'] % 3600 == 0:
				number = self.cast_time['seconds'] // 3600
				result += str(number)
				if number == 1:
					result += ' hour'
				else:
					result += ' hours'
			elif self.cast_time['seconds'] % 60 == 0:
				number = self.cast_time['seconds'] // 60
				result += str(number)
				if number == 1:
					result += ' minute'
				else:
					result += ' minutes'
			elif self.cast_time['seconds'] % 10 == 0:
				number = self.cast_time['seconds'] // 10
				result += str(number)
				if number == 1:
					result += ' round'
				else:
					result += ' rounds'
			elif self.cast_time['seconds'] % 1 == 0:
				number = self.cast_time['seconds']
				result += str(number)
				if number == 1:
					result += ' second'
				else:
					result += ' seconds'
			else:
				raise
		else:
			raise
		return result

	def distill_range(self):
		result = ''
		if self.range in ['self','touch','special','indefinate']:
			result = self.range
		elif isinstance(self.range, int):
			if self.range % 5280 == 0:
				number = self.range // 5280
				result += str(number)
				if number == 1:
					result += ' mile'
				else: 
					result += ' miles'
			elif self.range % 1 == 0:
				number = self.range
				result += str(number)
				if number == 1:
					result += ' foot'
				else: 
					result += ' feet'
			elif self.range % (1/12) == 0:
				number = int(self.range * 12)
				result += number
				if number == 1:
					result += ' inch'
				else:
					result += ' inches'
			else:
				raise
		else:
			raise
		return result
		
	def distill_duration(self):
		result = ''
		if self.duration.get('quality') == 'instantaneous':
			result += self.duration['quality']
		elif self.duration.get('quality') == 'indefinate':
			result += self.duration['quality']
		elif self.duration.get('quality') == 'special':
			result += self.duration['quality']
		elif self.duration.get('seconds'):
			if self.duration['seconds'] % 604800 == 0:
				number = self.duration['seconds'] // 604800
				result += str(number)
				if number == 1:
					result += ' week'
				else:
					result += ' weeks'
			elif self.duration['seconds'] % 86400 == 0:
				number = self.duration['seconds'] // 86400
				result += str(number)
				if number == 1:
					result += ' day'
				else:
					result += ' days'
			elif self.duration['seconds'] % 3600 == 0:
				number = self.duration['seconds'] // 3600
				result += str(number)
				if number == 1:
					result += ' hour'
				else:
					result += ' hours'
			elif self.duration['seconds'] % 60 == 0:
				number = self.duration['seconds'] // 60
				result += str(number)
				if number == 1:
					result += ' minute'
				else:
					result += ' minutes'
			elif self.duration['seconds'] % 10 == 0:
				number = self.duration['seconds'] // 10
				result += str(number)
				if number == 1:
					result += ' round'
				else:
					result += ' rounds'
			elif self.duration['seconds'] % 1 == 0:
				number = self.duration['seconds']
				result += str(number)
				if number == 1:
					result += ' second'
				else:
					result += ' seconds'
			else:
				raise
		else:
			raise
		return result

	def distill_shape(self):
		result = ''
		if not self.area.get('shape'):
			result += str(None)
		elif self.area.get('shape') == 'cube':
			if self.area['length'] % 5280 == 0:
				number = self.area['length'] // 5280
				result += str(number)
				result += '-mile'
			elif self.area['length'] % 1 == 0:
				number = self.area['length']
				result += str(number)
				result += '-foot'
			elif self.area['length'] % (1/12) == 0:
				number = int(self.area['length'] * 12)
				result += str(number)
				result += '-inch'
			else:
				raise
			result += ' cube'
		elif self.area.get('shape') == 'aura':
			if self.area['radius'] % 5280 == 0:
				number = self.area['radius'] // 5280
				result += str(number)
				result += '-mile'
			elif self.area['radius'] % 1 == 0:
				number = self.area['radius']
				result += str(number)
				result += '-foot'
			elif self.area['radius'] % (1/12) == 0:
				number = int(self.area['radius'] * 12)
				result += str(number)
				result += '-inch'
			else:
				raise
			result += ' aura'
		# CHECK XXX WALLS A BIGGIE
		elif self.area.get('shape') == 'wall':
			if self.area['length'] % 5280 == 0:
				number = self.area['length'] // 5280
				result += str(number)
				result += '-mile'
			elif self.area['length'] % 1 == 0:
				number = self.area['length']
				result += str(number)
				result += '-foot'
			elif self.area['length'] % (1/12) == 0:
				number = int(self.area['length'] * 12)
				result += str(number)
				result += '-inch'
			else:
				raise
			result += ' long, '
			###
			if self.area['height'] % 5280 == 0:
				number = self.area['height'] // 5280
				result += str(number)
				result += '-mile'
			elif self.area['height'] % 1 == 0:
				number = self.area['height']
				result += str(number)
				result += '-foot'
			elif self.area['height'] % (1/12) == 0:
				number = int(self.area['height'] * 12)
				result += str(number)
				result += '-inch'
			else:
				raise
			result += ' high, '
			###
			if self.area['width'] % 5280 == 0:
				number = self.area['width'] // 5280
				result += str(number)
				result += '-mile'
			elif self.area['width'] % 1 == 0:
				number = self.area['width']
				result += str(number)
				result += '-foot'
			else:
				number = self.area['width'] * 12
				result += str(number)
				result += '-inch'
			result += ' wide wall'
		elif self.area.get('shape') == 'cone':
			if self.area['radius'] % 5280 == 0:
				number = self.area['radius'] // 5280
				result += str(number)
				result += '-mile'
			elif self.area['radius'] % 1 == 0:
				number = self.area['radius']
				result += str(number)
				result += '-foot'
			elif self.area['radius'] % (1/12) == 0:
				number = int(self.area['radius'] * 12)
				result += str(number)
				result += '-inch'
			else:
				raise
			result += ' cone'
		elif self.area.get('shape') == 'sphere':
			if self.area['radius'] % 5280 == 0:
				number = self.area['radius'] // 5280
				result += str(number)
				result += '-mile'
			elif self.area['radius'] % 1 == 0:
				number = self.area['radius']
				result += str(number)
				result += '-foot'
			elif self.area['radius'] % (1/12) == 0:
				number = int(self.area['radius'] * 12)
				result += str(number)
				result += '-inch'
			else:
				raise
			result += ' sphere'
		elif self.area.get('shape') == 'cylinder':
			if self.area['radius'] % 5280 == 0:
				number = self.area['radius'] // 5280
				result += str(number)
				result += '-mile'
			elif self.area['radius'] % 1 == 0:
				number = self.area['radius']
				result += str(number)
				result += '-foot'
			elif self.area['radius'] % (1/12) == 0:
				number = int(self.area['radius'] * 12)
				result += str(number)
				result += '-inch'
			else:
				raise
			result += ' radius'
			### CONTINUE CYLINDER
			if self.area['height'] % 5280 == 0:
				number = self.area['height'] // 5280
				result += str(number)
				result += '-mile'
			elif self.area['height'] % 1 == 0:
				number = self.area['height']
				result += str(number)
				result += '-foot'
			elif self.area['height'] % (1/12) == 0:
				number = int(self.area['height'] * 12)
				result += str(number)
				result += '-inch'
			else:
				raise
			result += ' high, '

		# CHECK XXX WALLS A BIGGIE
		elif self.area.get('shape') == 'line':
			if self.area['length'] % 5280 == 0:
				number = self.area['length'] // 5280
				result += str(number)
				result += '-mile'
			elif self.area['length'] % 1 == 0:
				number = self.area['length']
				result += str(number)
				result += '-foot'
			elif self.area['length'] % (1/12) == 0:
				number = int(self.area['length'] * 12)
				result += str(number)
				result += '-inch'
			else:
				raise
			result += ' long, '
			###
			if self.area['width'] % 5280 == 0:
				number = self.area['width'] // 5280
				result += str(number)
				result += '-mile'
			elif self.area['width'] % 1 == 0:
				number = self.area['width']
				result += str(number)
				result += '-foot'
			elif self.area['width'] * 12 % 1 == 0:
				number = int(self.area['width'] * 12)
				result += str(number)
				result += '-inch'
			else:
				raise
			result += ' wide line'
		else:
			raise
		return result

	def distill_tags(self):
		result = ''
		result_array = []
		for tag in self.tags:
			if self.tags[tag] == True:
				result_array.append(tag)
		result = ', '.join(result_array)
		return result

	def distill_components(self):
		result = ''
		result += str(self.components['material'])
		return result

	def distill_classes(self):
		result = ''
		result_array = []
		for player_class in self.access['class']:
			result_array.append(player_class)
		result = ', '.join(result_array)
		return result

	def distill_subclasses(self):
		result = ''
		result_array = []
		for player_class in self.access['subclass']:
			result_array.append(player_class)
		if result_array == []:
			return None
		result = ', '.join(result_array)
		return result

	def distill_races(self):
		result = ''
		result_array = []
		for player_race in self.access['race']:
			result_array.append(player_race)
		if result_array == []:
			return None
		result = ', '.join(result_array)
		return result

	def distill_subraces(self):
		result = ''
		result_array = []
		for player_subrace in self.access['subrace']:
			result_array.append(player_subrace)
		if result_array == []:
			return None
		result = ', '.join(result_array)
		return result

	def get_citation(self):
		self.citation['book'] = self.json['source']
		self.citation['page'] = self.json.get('page')

	def distill_citation(self):
		result = ''
		result += self.citation['book']
		if self.citation['page']:
			result += ', page '
			result += str(self.citation['page'])
		return result

	def get_markdown(self):
		self.markdown = f'''# {self.name}

{nth_number(self.level)}-level {self.school}

casting time: {self.distill_cast_time()}

duration: {self.distill_duration()}

range: {self.distill_range()}

shape: {self.distill_shape()}

&numero; effects: {str(self.instances)}

tags: {self.distill_tags()}

verbal components: None

somatic components: None

material components: {self.distill_components()}

---

## Description
{self.info}

---

classes: {self.distill_classes()}

subclasses: {self.distill_subclasses()}

races: {self.distill_races()}

subraces: {self.distill_subraces()}

citation: {self.distill_citation()}
'''

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
