from helper import *
from bad_string_parser import *

class SpellToText:
	def __init__(self, Spell):
		self.spell = Spell
		self.text = None
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
			f'\n\n***{nth_number(Spell.level)}'
			f'-level {Spell.school}***'
		)
		# Casting time is right up there
		result += (
			f'\n\n**Casting Time:** {time2str(Spell.cast_time)}'
		)
		if Spell.cast_time['quality'] == 'reaction':
			result += (
				f' ({Spell.cast_time["condition"]})'
			)
		# Duration is easy to grab
		if Spell.duration['quality']:
			duration = Spell.duration['quality']
		else:
			duration = time2str(Spell.duration)
		result += f'\n\n**Duration:** {duration}'
		# The range is just a number or string.
		if Spell.range['distance']:
			measurement = Spell.range['distance']
			measurement = space2str(measurement)
			result += f'\n\n**Range:** {measurement}'
		else:
			result += f'\n\n**Range:** {Spell.range["quality"]}'
		# The shape can be deconstructed with a for loop.
		shape = Spell.area['shape']
		if shape:
			result += f'\n\n**Shape:** {shape}'
			for dimension in shape_parameters[shape]:
				measurement = Spell.area[dimension]
				measurement = space2str(measurement)
				dimension = dimension.capitalize()
				result += f'\n\n**{dimension}:** {measurement}'
		# Instances isn't a good name but its what we got
		if Spell.instances != 1:
			result += f'\n\n**Effect Instances:** {Spell.instances}'
		# Spell tags
		for tag in Spell.tags:
			if Spell.tags[tag]:
				tag_list = self.distill_tags(Spell.tags).lower()
				result += f'\n\n**Tags:** {tag_list}'
				break
		# Spell components
		for component in Spell.components:
			if Spell.components[component]:
				result += (
					f'\n\n**{component.capitalize()} Components:** '
					f'{Spell.components[component]}'
				)
		# Spell description
		result += '\n\n---\n\n'
		result += Spell.description
		result += '\n\n---'
		# Spell class access
		classes = Spell.access['classes']
		if classes != [] and classes:
			classes = self.distill_access(classes).lower()
			result += f'\n\n**Classes:** {classes}'
		subclasses = Spell.access['subclasses']
		if subclasses != [] and subclasses:
			subclasses = self.distill_access(subclasses).lower()
			result += f'\n\n**Subclasses:** {subclasses}'
		races = Spell.access['races']
		if races != [] and races:
			races = self.distill_access(races).lower()
			result += f'\n\n**Races:** {races}'
		subraces = Spell.access['subraces']
		if subraces != [] and subraces:
			subraces = self.distill_access(subraces).lower()
			result += f'\n\n**Subraces:** {subraces}'
		# Finally, add the citation.
		book_abbr = Spell.citations[0]['book']
		if book_transition_temp.get(book_abbr):
			book = book_transition_temp[book_abbr].upper()
		else:
			book = book_abbr

		page = Spell.citations[0].get('page')
		cite = self.distill_citation(book, page)
		result += f'\n\n**Sources:** {cite}'
		# Don't forget to set the markdown...
		result += '\n'
		result = cleanse_markdown(result)
		self.text = result

	def distill_tags(self, tags):
		tag_list = []
		for tag in tags:
			if tags[tag]:
				tag_list.append(tag)
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
