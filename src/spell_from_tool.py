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
		# self.get_instances() # covered by get_range
		self.get_range()
		# self.get_area() # covered by get_range
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
			'ritual': False
		}
		if 'components' in self.json:
			if 'v' in self.json['components']:
				self.tags['verbal'] = True
			if 's' in self.json['components']:
				self.tags['somatic'] = True
			if 'm' in self.json['components']:
				self.tags['material'] = True
			# if 'r' in self.json['components']:
			# 	raise FIXME
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
		return info

	def get_info(self):
		# print(self.json)
		result = ''
		for entry in self.json['entries']:
			if isinstance(entry,str):
				result += '\n\n'
				result += entry
				# print(result)

			else:
				if entry['type'] == 'quote':
					result += '\n'
					for sub_entry in entry['entries']:
						result += '\n'
						result += '> '
						result += sub_entry
					result += '\n> \n> &mdash;'
					result += entry['by']
					# print(result)

				elif entry['type'] == 'list':
					for item in entry['items']:
						result += '\n'
						result += '- '
						result += item
					# print(result)

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
					# print(result)

				elif entry['type'] == 'table':
					# print(entry['rows'])
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
					# print(entry)
					raise
				pass

		if self.json.get('entriesHigherLevel'):
			for entry in self.json.get('entriesHigherLevel'):
				if isinstance(entry,str):
					result += '\n\n'
					result += entry
					# print(result)

				else:
					if entry['type'] == 'quote':
						result += '\n'
						for sub_entry in entry['entries']:
							result += '\n'
							result += '> '
							result += sub_entry
						result += '\n> \n> &mdash;'
						result += entry['by']
						# print(result)

					elif entry['type'] == 'list':
						for item in entry['items']:
							result += '\n'
							result += '- '
							result += item
						# print(result)

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
						# print(result)

					elif entry['type'] == 'table':
						# print(entry['rows'])
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
						# print(entry)
						raise
					pass

		self.info = self.clean_info(result).strip()
		self.info = re.sub(r'\n\n+', '\n\n', self.info)

	def get_access(self):
		pass ### TODO

	def get_markdown(self):
		self.markdown = f'''# {self.name}
{self.info}'''
