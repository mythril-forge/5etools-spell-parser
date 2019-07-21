from helper import *

class SpellToMarkdown:
	def __init__(self, Spell):
		self.spell = Spell
		self.markdown = None
		self.main()

	def main(self):
		Spell = self.spell

		result = ''
		# Basic spell name as header
		result += f'# {Spell.name}'
		# Homebrew indicator
		result += '\n\n- [ ] Homebrew'
		# Adding spell level and school
		result += (
			f'\n\n{nth_number(Spell.level)}'
			f'-level {Spell.school}'
		)
		# Casting time is right up there
		result += (
			f'\n\nCasting Time: {time2str(Spell.cast_time)}'
		)
		# Instances isn't a good name but its what we got
		result += f'\n\nEffect Instances: {Spell.instances}'
		# The range is just a number or string.
		if Spell.range['distance']:
			measurement = Spell.range['distance']
			measurement = space2str(measurement)
			result += f'\n\nRange: {measurement}'
		else:
			result += f'\n\nRange: {Spell.range["quality"]}'
		# The shape can be deconstructed with a for loop.
		shape = Spell.area['shape']
		if shape:
			result += f'\n\nShape: {shape}'
			for dimension in shape_parameters[shape]:
				measurement = Spell.area[dimension]
				measurement = space2str(measurement)
				dimension = dimension.capitalize()
				result += f'\n\n{dimension}: {measurement}'
		# Don't forget to set the markdown...
		self.markdown = result

def nth_number(number):
	if number < 0 or number > 9:
		raise Exception(f'stringify number {number}: ' \
		'out of range')
	elif number == 1:
		return '1st'
	elif number == 2:
		return '2nd'
	elif number == 3:
		return '3rd'
	else:
		return f'{str(number)}th'


# shape: {self.distill_shape()}

# &numero; effects: {str(self.instances)}

# tags: {self.distill_tags()}

# verbal components: None

# somatic components: None

# material components: {self.distill_components()}

# ---

# ## Description
# {self.info}

# ---

# classes: {self.distill_classes()}

# subclasses: {self.distill_subclasses()}

# races: {self.distill_races()}

# subraces: {self.distill_subraces()}

# citation: {self.distill_citation()}
# '''

# def clean_info(self, info):
# 	# work around
# 	info = re.sub(r'animated object \(','',info)
# 	info = re.sub(r'\)\|phb\|.*?}','}',info)
# 	info = re.sub(r'1d20.*?\|','',info)
# 	# general case
# 	info = re.sub(r'}','',info) # can't use (?<={@.*? .*?)}
# 	info = re.sub(r'{@.*? ','',info)
# 	info = re.sub(r'\n\n+', '\n\n', info)
# 	info = re.sub(r'dretch\|\|', '', info) # jeeze :\
# 	info = re.sub(r'\d+d\d+\|\d-\d\|', '', info)
# 	info = info.strip()
# 	return info

# def get_info(self):
# 	result = ''
# 	for entry in self.json['entries']:
# 		if isinstance(entry,str):
# 			result += '\n\n'
# 			result += entry

# 		else:
# 			if entry['type'] == 'quote':
# 				result += '\n'
# 				for sub_entry in entry['entries']:
# 					result += '\n'
# 					result += '> '
# 					result += sub_entry
# 				result += '\n> \n> &mdash;'
# 				result += entry['by']

# 			elif entry['type'] == 'list':
# 				for item in entry['items']:
# 					result += '\n'
# 					result += '- '
# 					result += item

# 			elif entry['type'] == 'entries':
# 				result += '\n\n### '
# 				result += entry['name']
# 				first = True
# 				for sub_entry in entry['entries']:
# 					if first:
# 						first = False
# 					else:
# 						result += '\n'
# 					result +='\n'

# 					if isinstance(sub_entry,dict):
# 						if sub_entry['type'] == 'list':
# 							for item in sub_entry['items']:
# 								result += '\n'
# 								result += '- '
# 								result += item
# 					else:
# 						result += sub_entry

# 			elif entry['type'] == 'table':
# 				if entry.get('caption'):
# 					result += '\n\n#### '
# 					result += entry['caption']
# 				result += '\n\n|'
# 				for col in entry['colLabels']:
# 					result += ' '
# 					result += col
# 					result += ' |'
# 				result += '\n|'
# 				for col in entry['colLabels']:
# 					result += ' '
# 					result += '---'
# 					result += ' |'
# 				for row in entry['rows']:
# 					result += '\n|'
# 					for data in row:
# 						if isinstance(data, dict):
# 							if data.get('type') == 'cell':
# 								if data['roll'].get('exact'):
# 									result += ' '
# 									result += str(data['roll']['exact'])
# 									result += ' |'
# 								elif data['roll'].get('min') and data['roll'].get('max'):
# 									result += ' '
# 									result += str(data['roll']['min'])
# 									result += '&mdash;'
# 									result += str(data['roll']['max'])
# 									result += ' |'
# 						else:
# 							if not isinstance(data, str):
# 								raise Exception(data)
# 							data = self.clean_info(data)
# 							result += ' '
# 							result += data
# 							result += ' |'
# 				result += '\n\n'
# 			else:
# 				raise
# 			pass

# 	if self.json.get('entriesHigherLevel'):
# 		for entry in self.json.get('entriesHigherLevel'):
# 			if isinstance(entry,str):
# 				result += '\n\n'
# 				result += entry

# 			else:
# 				if entry['type'] == 'quote':
# 					result += '\n'
# 					for sub_entry in entry['entries']:
# 						result += '\n'
# 						result += '> '
# 						result += sub_entry
# 					result += '\n> \n> &mdash;'
# 					result += entry['by']

# 				elif entry['type'] == 'list':
# 					for item in entry['items']:
# 						result += '\n'
# 						result += '- '
# 						result += item

# 				elif entry['type'] == 'entries':
# 					result += '\n\n## '
# 					result += entry['name']
# 					first = True
# 					for sub_entry in entry['entries']:
# 						if first:
# 							first = False
# 						else:
# 							result += '\n'
# 						result +='\n'

# 						if isinstance(sub_entry,dict):
# 							if sub_entry['type'] == 'list':
# 								for item in sub_entry['items']:
# 									result += '\n'
# 									result += '- '
# 									result += item
# 						else:
# 							result += sub_entry

# 				elif entry['type'] == 'table':
# 					if entry.get('caption'):
# 						result += '\n\n#### '
# 						result += entry['caption']
# 					result += '\n\n|'
# 					for col in entry['colLabels']:
# 						result += ' '
# 						result += col
# 						result += ' |'
# 					result += '\n|'
# 					for col in entry['colLabels']:
# 						result += ' '
# 						result += '---'
# 						result += ' |'
# 					for row in entry['rows']:
# 						result += '\n|'
# 						for data in row:
# 							if isinstance(data, dict):
# 								if data.get('type') == 'cell':
# 									if data['roll'].get('exact'):
# 										result += ' '
# 										result += str(data['roll']['exact'])
# 										result += ' |'
# 									elif data['roll'].get('min') and data['roll'].get('max'):
# 										result += ' '
# 										result += str(data['roll']['min'])
# 										result += '&mdash;'
# 										result += str(data['roll']['max'])
# 										result += ' |'
# 							else:
# 								if not isinstance(data, str):
# 									raise Exception(data)
# 								data = self.clean_info(data)
# 								result += ' '
# 								result += data
# 								result += ' |'
# 					result += '\n\n'
# 				else:
# 					raise
# 				pass

# 	self.info = self.clean_info(result)


# def distill_cast_time(self):
# 	result = ''
# 	if self.cast_time.get('quality') == 'special':
# 		result += self.cast_time['quality']
# 	elif self.cast_time.get('quality') == 'action':
# 		result += self.cast_time['quality']
# 	elif self.cast_time.get('quality') == 'bonus action':
# 		result += self.cast_time['quality']
# 	elif self.cast_time.get('quality') == 'reaction':
# 		result += self.cast_time['quality']
# 		result += ', '
# 		result += self.cast_time['condition']
# 	elif self.cast_time.get('seconds'):
# 		if self.cast_time['seconds'] % 604800 == 0:
# 			number = self.cast_time['seconds'] // 604800
# 			result += str(number)
# 			if number == 1:
# 				result += ' week'
# 			else:
# 				result += ' weeks'
# 		elif self.cast_time['seconds'] % 86400 == 0:
# 			number = self.cast_time['seconds'] // 86400
# 			result += str(number)
# 			if number == 1:
# 				result += ' day'
# 			else:
# 				result += ' days'
# 		elif self.cast_time['seconds'] % 3600 == 0:
# 			number = self.cast_time['seconds'] // 3600
# 			result += str(number)
# 			if number == 1:
# 				result += ' hour'
# 			else:
# 				result += ' hours'
# 		elif self.cast_time['seconds'] % 60 == 0:
# 			number = self.cast_time['seconds'] // 60
# 			result += str(number)
# 			if number == 1:
# 				result += ' minute'
# 			else:
# 				result += ' minutes'
# 		elif self.cast_time['seconds'] % 10 == 0:
# 			number = self.cast_time['seconds'] // 10
# 			result += str(number)
# 			if number == 1:
# 				result += ' round'
# 			else:
# 				result += ' rounds'
# 		elif self.cast_time['seconds'] % 1 == 0:
# 			number = self.cast_time['seconds']
# 			result += str(number)
# 			if number == 1:
# 				result += ' second'
# 			else:
# 				result += ' seconds'
# 		else:
# 			raise
# 	else:
# 		raise
# 	return result

# def distill_range(self):
# 	result = ''
# 	if self.range in ['self','touch','special','indefinate']:
# 		result = self.range
# 	elif isinstance(self.range, int):
# 		if self.range % 5280 == 0:
# 			number = self.range // 5280
# 			result += str(number)
# 			if number == 1:
# 				result += ' mile'
# 			else: 
# 				result += ' miles'
# 		elif self.range % 1 == 0:
# 			number = self.range
# 			result += str(number)
# 			if number == 1:
# 				result += ' foot'
# 			else: 
# 				result += ' feet'
# 		elif self.range % (1/12) == 0:
# 			number = int(self.range * 12)
# 			result += number
# 			if number == 1:
# 				result += ' inch'
# 			else:
# 				result += ' inches'
# 		else:
# 			raise
# 	else:
# 		raise
# 	return result

# def distill_duration(self):
# 	result = ''
# 	if self.duration.get('quality') == 'instantaneous':
# 		result += self.duration['quality']
# 	elif self.duration.get('quality') == 'indefinate':
# 		result += self.duration['quality']
# 	elif self.duration.get('quality') == 'special':
# 		result += self.duration['quality']
# 	elif self.duration.get('seconds'):
# 		if self.duration['seconds'] % 604800 == 0:
# 			number = self.duration['seconds'] // 604800
# 			result += str(number)
# 			if number == 1:
# 				result += ' week'
# 			else:
# 				result += ' weeks'
# 		elif self.duration['seconds'] % 86400 == 0:
# 			number = self.duration['seconds'] // 86400
# 			result += str(number)
# 			if number == 1:
# 				result += ' day'
# 			else:
# 				result += ' days'
# 		elif self.duration['seconds'] % 3600 == 0:
# 			number = self.duration['seconds'] // 3600
# 			result += str(number)
# 			if number == 1:
# 				result += ' hour'
# 			else:
# 				result += ' hours'
# 		elif self.duration['seconds'] % 60 == 0:
# 			number = self.duration['seconds'] // 60
# 			result += str(number)
# 			if number == 1:
# 				result += ' minute'
# 			else:
# 				result += ' minutes'
# 		elif self.duration['seconds'] % 10 == 0:
# 			number = self.duration['seconds'] // 10
# 			result += str(number)
# 			if number == 1:
# 				result += ' round'
# 			else:
# 				result += ' rounds'
# 		elif self.duration['seconds'] % 1 == 0:
# 			number = self.duration['seconds']
# 			result += str(number)
# 			if number == 1:
# 				result += ' second'
# 			else:
# 				result += ' seconds'
# 		else:
# 			raise
# 	else:
# 		raise
# 	return result

# def distill_shape(self):
# 	result = ''
# 	if not self.area.get('shape'):
# 		result += str(None)
# 	elif self.area.get('shape') == 'cube':
# 		if self.area['length'] % 5280 == 0:
# 			number = self.area['length'] // 5280
# 			result += str(number)
# 			result += '-mile'
# 		elif self.area['length'] % 1 == 0:
# 			number = self.area['length']
# 			result += str(number)
# 			result += '-foot'
# 		elif self.area['length'] % (1/12) == 0:
# 			number = int(self.area['length'] * 12)
# 			result += str(number)
# 			result += '-inch'
# 		else:
# 			raise
# 		result += ' cube'
# 	elif self.area.get('shape') == 'aura':
# 		if self.area['radius'] % 5280 == 0:
# 			number = self.area['radius'] // 5280
# 			result += str(number)
# 			result += '-mile'
# 		elif self.area['radius'] % 1 == 0:
# 			number = self.area['radius']
# 			result += str(number)
# 			result += '-foot'
# 		elif self.area['radius'] % (1/12) == 0:
# 			number = int(self.area['radius'] * 12)
# 			result += str(number)
# 			result += '-inch'
# 		else:
# 			raise
# 		result += ' aura'
# 	# CHECK XXX WALLS A BIGGIE
# 	elif self.area.get('shape') == 'wall':
# 		if self.area['length'] % 5280 == 0:
# 			number = self.area['length'] // 5280
# 			result += str(number)
# 			result += '-mile'
# 		elif self.area['length'] % 1 == 0:
# 			number = self.area['length']
# 			result += str(number)
# 			result += '-foot'
# 		elif self.area['length'] % (1/12) == 0:
# 			number = int(self.area['length'] * 12)
# 			result += str(number)
# 			result += '-inch'
# 		else:
# 			raise
# 		result += ' long, '
# 		###
# 		if self.area['height'] % 5280 == 0:
# 			number = self.area['height'] // 5280
# 			result += str(number)
# 			result += '-mile'
# 		elif self.area['height'] % 1 == 0:
# 			number = self.area['height']
# 			result += str(number)
# 			result += '-foot'
# 		elif self.area['height'] % (1/12) == 0:
# 			number = int(self.area['height'] * 12)
# 			result += str(number)
# 			result += '-inch'
# 		else:
# 			raise
# 		result += ' high, '
# 		###
# 		if self.area['width'] % 5280 == 0:
# 			number = self.area['width'] // 5280
# 			result += str(number)
# 			result += '-mile'
# 		elif self.area['width'] % 1 == 0:
# 			number = self.area['width']
# 			result += str(number)
# 			result += '-foot'
# 		else:
# 			number = self.area['width'] * 12
# 			result += str(number)
# 			result += '-inch'
# 		result += ' wide wall'
# 	elif self.area.get('shape') == 'cone':
# 		if self.area['radius'] % 5280 == 0:
# 			number = self.area['radius'] // 5280
# 			result += str(number)
# 			result += '-mile'
# 		elif self.area['radius'] % 1 == 0:
# 			number = self.area['radius']
# 			result += str(number)
# 			result += '-foot'
# 		elif self.area['radius'] % (1/12) == 0:
# 			number = int(self.area['radius'] * 12)
# 			result += str(number)
# 			result += '-inch'
# 		else:
# 			raise
# 		result += ' cone'
# 	elif self.area.get('shape') == 'sphere':
# 		if self.area['radius'] % 5280 == 0:
# 			number = self.area['radius'] // 5280
# 			result += str(number)
# 			result += '-mile'
# 		elif self.area['radius'] % 1 == 0:
# 			number = self.area['radius']
# 			result += str(number)
# 			result += '-foot'
# 		elif self.area['radius'] % (1/12) == 0:
# 			number = int(self.area['radius'] * 12)
# 			result += str(number)
# 			result += '-inch'
# 		else:
# 			raise
# 		result += ' sphere'
# 	elif self.area.get('shape') == 'cylinder':
# 		if self.area['radius'] % 5280 == 0:
# 			number = self.area['radius'] // 5280
# 			result += str(number)
# 			result += '-mile'
# 		elif self.area['radius'] % 1 == 0:
# 			number = self.area['radius']
# 			result += str(number)
# 			result += '-foot'
# 		elif self.area['radius'] % (1/12) == 0:
# 			number = int(self.area['radius'] * 12)
# 			result += str(number)
# 			result += '-inch'
# 		else:
# 			raise
# 		result += ' radius'
# 		### CONTINUE CYLINDER
# 		if self.area['height'] % 5280 == 0:
# 			number = self.area['height'] // 5280
# 			result += str(number)
# 			result += '-mile'
# 		elif self.area['height'] % 1 == 0:
# 			number = self.area['height']
# 			result += str(number)
# 			result += '-foot'
# 		elif self.area['height'] % (1/12) == 0:
# 			number = int(self.area['height'] * 12)
# 			result += str(number)
# 			result += '-inch'
# 		else:
# 			raise
# 		result += ' high, '

# 	# CHECK XXX WALLS A BIGGIE
# 	elif self.area.get('shape') == 'line':
# 		if self.area['length'] % 5280 == 0:
# 			number = self.area['length'] // 5280
# 			result += str(number)
# 			result += '-mile'
# 		elif self.area['length'] % 1 == 0:
# 			number = self.area['length']
# 			result += str(number)
# 			result += '-foot'
# 		elif self.area['length'] % (1/12) == 0:
# 			number = int(self.area['length'] * 12)
# 			result += str(number)
# 			result += '-inch'
# 		else:
# 			raise
# 		result += ' long, '
# 		###
# 		if self.area['width'] % 5280 == 0:
# 			number = self.area['width'] // 5280
# 			result += str(number)
# 			result += '-mile'
# 		elif self.area['width'] % 1 == 0:
# 			number = self.area['width']
# 			result += str(number)
# 			result += '-foot'
# 		elif self.area['width'] * 12 % 1 == 0:
# 			number = int(self.area['width'] * 12)
# 			result += str(number)
# 			result += '-inch'
# 		else:
# 			raise
# 		result += ' wide line'
# 	else:
# 		raise
# 	return result

# def distill_tags(self):
# 	result = ''
# 	result_array = []
# 	for tag in self.tags:
# 		if self.tags[tag] == True:
# 			result_array.append(tag)
# 	result = ', '.join(result_array)
# 	return result

# def distill_components(self):
# 	result = ''
# 	result += str(self.components['material'])
# 	return result

# def distill_classes(self):
# 	result = ''
# 	result_array = []
# 	for player_class in self.access['class']:
# 		result_array.append(player_class)
# 	result = ', '.join(result_array)
# 	return result

# def distill_subclasses(self):
# 	result = ''
# 	result_array = []
# 	for player_class in self.access['subclass']:
# 		result_array.append(player_class)
# 	if result_array == []:
# 		return None
# 	result = ', '.join(result_array)
# 	return result

# def distill_races(self):
# 	result = ''
# 	result_array = []
# 	for player_race in self.access['race']:
# 		result_array.append(player_race)
# 	if result_array == []:
# 		return None
# 	result = ', '.join(result_array)
# 	return result

# def distill_subraces(self):
# 	result = ''
# 	result_array = []
# 	for player_subrace in self.access['subrace']:
# 		result_array.append(player_subrace)
# 	if result_array == []:
# 		return None
# 	result = ', '.join(result_array)
# 	return result

# def distill_citation(self):
# 	result = ''
# 	result += self.citation['book']
# 	if self.citation['page']:
# 		result += ', page '
# 		result += str(self.citation['page'])
# 	return result

# def get_markdown(self):
# 	self.markdown = f'''# {self.name}

# {nth_number(self.level)}-level {self.school}

# casting time: {self.distill_cast_time()}

# duration: {self.distill_duration()}

# range: {self.distill_range()}

# shape: {self.distill_shape()}

# &numero; effects: {str(self.instances)}

# tags: {self.distill_tags()}

# verbal components: None

# somatic components: None

# material components: {self.distill_components()}

# ---

# ## Description
# {self.info}

# ---

# classes: {self.distill_classes()}

# subclasses: {self.distill_subclasses()}

# races: {self.distill_races()}

# subraces: {self.distill_subraces()}

# citation: {self.distill_citation()}
# '''
