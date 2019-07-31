from helper import *

class SpellToText:
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
		# Instances isn't a good name but its what we got
		if Spell.instances != 1:
			result += f'\n\nEffect Instances: {Spell.instances}'
		# Spell tags
		for tag in Spell.tags:
			if Spell.tags[tag]:
				tag_list = self.distill_tags(Spell.tags)
				result += f'\n\nTags: {tag_list}'
				break
		# Spell components
		for component in Spell.components:
			if Spell.components[component]:
				result += (
					f'\n\n{component.capitalize()} Components: '
					f'{Spell.components[component]}'
				)
		# Spell description
		result += '\n\n---\n\n'
		result += Spell.description
		result += '\n\n---'
		# Spell class access
		classes = Spell.access['classes']
		if classes != []:
			classes = self.distill_access(classes)
			result += f'\n\nClasses: {classes}'
		subclasses = Spell.access['subclasses']
		if subclasses != []:
			subclasses = self.distill_access(subclasses)
			result += f'\n\nSubclasses: {subclasses}'
		races = Spell.access['races']
		if races != []:
			races = self.distill_access(races)
			result += f'\n\nRaces: {races}'
		subraces = Spell.access['subraces']
		if subraces != []:
			subraces = self.distill_access(subraces)
			result += f'\n\nSubraces: {subraces}'
		# Finally, add the citation.
		book = book_transition_temp[Spell.citations['book']].upper()
		page = Spell.citation['page']
		cite = self.distill_citation(book, page)
		result += f'\n\nSource: {cite}'
		# Don't forget to set the markdown...
		result += '\n'
		self.markdown = result

	def distill_tags(self, tags):
		tag_list = []
		for tag in tags:
			if tags[tag]:
				tag_list.append(tag_symbols[tag])
		return ', '.join(tag_list)

	def distill_access(self, classes):
		result = ''
		result_array = []
		for player_class in classes:
			result_array.append(player_class)
		if result_array == []:
			return None
		result = ', '.join(result_array)
		return result

	def distill_citation(self, book, page):
		result = ''
		result += str(book)
		if page:
			result += ', page '
			result += str(page)
		return result
