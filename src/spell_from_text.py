from spell import Spell
from helper import *
import re


class SpellFromText(Spell):
	'''
	'''
	def __init__(self, filename=None):
		'''
		Initialization immediately calls upon parsing methods.
		'''
		super().__init__()
		self.slug = filename[0:-3]
		self.path = './spells/' + str(filename)
		self.get() # very important!

	def get(self):
		with open(self.path, 'r') as file:
			lines = file.readlines()
			description_active = False
			for line in lines:
				# adding description
				if description_active:
					if re.search(r'^---', line):
						description_active = False
						self.description = self.description.strip()
					else:
						self.description += str(line)

				# check if we are starting to add description
				elif re.search(r'^---', line):
					description_active = True
					self.description = ''

				elif re.search(r'^#\s.+\n', line):
					name = line
					name = re.sub(r'^#\s', '', name)
					name = re.sub(r'\n', '', name)
					self.name = name

				# check if it is a homebrew spell
				elif re.search(r'^- \[.\] Homebrew', line):
					if line[3] == ' ':
						self.homebrew = False
					else:
						self.homebrew = True

				# extract level and school
				elif re.search(r'^\*\*\*.+-level.+\*\*\*', line):
					# set level
					level = line
					level = re.search(r'\d', level)
					level = level.group()
					level = level.strip()
					self.level = int(level)
					# set school
					school = line
					school = re.sub(r'\*\*\*', '', school)
					school = re.sub(r'\d.*-level\s', '', school)
					school = school.strip()
					self.school = school

				# get casting time
				elif re.search(r'^\*\*Casting Time:\*\*\s', line):
					cast_time = line
					cast_time = re.sub(r'^\*\*Casting Time:\*\*\s', '', cast_time)
					cast_time = cast_time.strip()
					if cast_time in {'action', 'bonus action', 'reaction', 'special'}:
						self.cast_time['quality'] = cast_time
						# TODO fix reaction conditions
					else:
						cast_time = cast_time.split(' ')
						amount = int(cast_time[0])
						unit = cast_time[1]
						cast_time = time2num(amount, unit)
						self.cast_time['seconds'] = cast_time

				# get durations
				elif re.search(r'^\*\*Duration:\*\*\s', line):
					duration = line
					duration = re.sub(r'^\*\*Duration:\*\*\s', '', duration)
					duration = duration.strip()
					if duration in {'instantaneous', 'indefinate', 'activated', 'special'}:
						self.duration['quality'] = duration
						# TODO fix activated conditions
					else:
						duration = duration.split(' ')
						amount = int(duration[0])
						unit = duration[1]
						duration = time2num(amount, unit)
						self.duration['seconds'] = duration

				# get ranges
				elif re.search(r'^\*\*Range:\*\*\s', line):
					range = line
					range = re.sub(r'^\*\*Range:\*\*\s', '', range)
					range = range.strip()
					if range in {'self', 'touch', 'unlimited', 'special'}:
						self.range['quality'] = range
						# TODO fix special conditions
					else:
						range = range.split(' ')
						amount = int(range[0])
						unit = range[1]
						range = space2num(amount, unit)
						# print(range)
						self.range['distance'] = range

				# get shape
				elif re.search(r'^\*\*Shape:\*\*\s', line):
					shape = line
					shape = re.sub(r'^\*\*Shape:\*\*\s', '', shape)
					shape = shape.strip()
					self.area['shape'] = shape

				# get radius
				elif re.search(r'^\*\*Radius:\*\*\s', line):
					radius = line
					radius = re.sub(r'^\*\*Radius:\*\*\s', '', radius)
					radius = radius.strip()
					radius = radius.split(' ')
					amount = int(radius[0])
					unit = radius[1]
					radius = space2num(amount, unit)
					self.area['radius'] = radius

				# get length
				elif re.search(r'^\*\*Length:\*\*\s', line):
					length = line
					length = re.sub(r'^\*\*Length:\*\*\s', '', length)
					length = length.strip()
					length = length.split(' ')
					amount = int(length[0])
					unit = length[1]
					length = space2num(amount, unit)
					self.area['length'] = length

				# get width
				elif re.search(r'^\*\*Width:\*\*\s', line):
					width = line
					width = re.sub(r'^\*\*Width:\*\*\s', '', width)
					width = width.strip()
					width = width.split(' ')
					amount = int(width[0])
					unit = width[1]
					width = space2num(amount, unit)
					self.area['width'] = width

				# get height
				elif re.search(r'^\*\*Height:\*\*\s', line):
					height = line
					height = re.sub(r'^\*\*Height:\*\*\s', '', height)
					height = height.strip()
					height = height.split(' ')
					amount = int(height[0])
					unit = height[1]
					height = space2num(amount, unit)
					self.area['height'] = height

				# get effect instances
				elif re.search(r'^\*\*Effect Instances:\*\*\s', line):
					instances = line
					instances = re.sub(r'^\*\*Effect Instances:\*\*\s', '', instances)
					instances = instances.strip()
					instances = int(instances)
					self.instances = instances

				# get tags
				elif re.search(r'^\*\*Tags:\*\*\s', line):
					tags = line
					tags = re.sub(r'^\*\*Tags:\*\*\s', '', tags)
					tags = tags.strip()
					tags = tags.split(', ')
					for tag in self.tags:
						if tag in tags:
							self.tags[tag] = True
						else:
							self.tags[tag] = False

				# get verbal components
				elif re.search(r'^\*\*Verbal Components:\*\*\s', line):
					components = line
					components = re.sub(r'^\*\*Verbal Components:\*\*\s', '', components)
					components = components.strip()
					self.components['verbal'] = components

				# get somatic components
				elif re.search(r'^\*\*Somatic Components:\*\*\s', line):
					components = line
					components = re.sub(r'^\*\*Somatic Components:\*\*\s', '', components)
					components = components.strip()
					self.components['somatic'] = components

				# get material components
				elif re.search(r'^\*\*Material Components:\*\*\s', line):
					components = line
					components = re.sub(r'^\*\*Material Components:\*\*\s', '', components)
					components = components.strip()
					self.components['material'] = components

				# get classes
				elif re.search(r'^\*\*Classes:\*\*\s', line):
					classes = line
					classes = re.sub(r'^\*\*Classes:\*\*\s', '', classes)
					classes = classes.strip()
					classes = classes.split(', ')
					self.access['classes'] = classes

				# get subclasses
				elif re.search(r'^\*\*Subclasses:\*\*\s', line):
					subclasses = line
					subclasses = re.sub(r'^\*\*Subclasses:\*\*\s', '', subclasses)
					subclasses = subclasses.strip()
					subclasses = subclasses.split(', ')
					self.access['subclasses'] = subclasses

				# get races
				elif re.search(r'^\*\*Races:\*\*\s', line):
					races = line
					races = re.sub(r'^\*\*Races:\*\*\s', '', races)
					races = races.strip()
					races = races.split(', ')
					self.access['races'] = races

				# get subraces
				elif re.search(r'^\*\*Subraces:\*\*\s', line):
					subraces = line
					subraces = re.sub(r'^\*\*Subraces:\*\*\s', '', subraces)
					subraces = subraces.strip()
					subraces = subraces.split(', ')
					self.access['subraces'] = subraces

				# get sources
				elif re.search(r'^\*\*Sources:\*\*\s', line):
					sources = line
					sources = re.sub(r'^\*\*Sources:\*\*\s', '', sources)
					sources = sources.strip()
					sources = sources.split('; ')

					for source in sources:
						source = source.split(', ')
						citation = {}
						citation['book'] = source[0]
						if len(source) == 2:
							page = source[1]
							page = re.sub(r'page\s', '', page)
							citation['page'] = int(page)
						self.citations.append(citation)

				else:
					if line != '\n':
						print(line.strip())
