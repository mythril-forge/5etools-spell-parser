from spell import *
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
			for line in lines:
				# get the spell name
				if re.search(r'^#\s.+\n', line):
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
					self.level = level
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
					if cast_time in {'action', 'bonus action', 'reaction'}:
						self.cast_time['quality'] = cast_time
						# TODO fix reaction conditions
					else:
						# TODO fix duration cast times
						pass

				# get durations
				elif re.search(r'^\*\*Duration:\*\*\s', line):
					duration = line
					duration = re.sub(r'^\*\*Duration:\*\*\s', '', duration)
					duration = duration.strip()
					if duration in {'instantaneous', 'indefinate', 'activated'}:
						self.duration['quality'] = duration
						# TODO fix activated conditions
					else:
						# TODO fix duration durations
						pass

				# get ranges
				elif re.search(r'^\*\*Range:\*\*\s', line):
					range = line
					range = re.sub(r'^\*\*Range:\*\*\s', '', range)
					if range in {'self', 'touch', 'unlimited'}:
						self.range['quality'] = range
						# TODO fix special conditions
					else:
						# TODO fix duration durations
						pass

				else:
					print(line)