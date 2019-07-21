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
