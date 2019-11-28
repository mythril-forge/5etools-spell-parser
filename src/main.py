# python packages
import os
# project imports
import library_from_tool



def main(Library):
	'''
	==NOTE==
	This only fetches markdown for now.
	==NOTE==
	This only sorts outputs by level for now.
	==TODO==
	This could be expanded, but would need to be refactored.
	'''
	# We don't really care about which book the data is in.
	# Really we just need the data so we can parse through it.
	for _, Book in Library.books.items():
		# Loop through every spell.
		for _, Spell in Book.spells.items():

			# Get current directory.
			directory = os.path.dirname('./spells/')
			# Get the directory where the spell will be placed.
			if Spell.level == 0:
				directory += '/cantrips'
			else:
				directory += f'/level-{str(Spell.level)}'

			# Create a special directory for this spell's level,
			# or reuse one if it already exists.
			if not os.path.exists(directory):
				os.makedirs(directory)

			# Get spell-path string.
			path = f'{directory}/{Spell.slug}.md'

			# create file from path and add to directory
			with open(path, 'w', encoding='utf-8') as file:
				file.write(Spell.extract_markdown())



if __name__ == '__main__':
	'''
	This app takes spell data from 5etools and
	transforms them into readable markdown formats.
	5etools isnt really an API, but it has better info.
	At this juncture, the app assumes you just want markdown.
	You could get json,	but right now that is not supported.
	'''
	# ==NOTE==
	# utilizing `library_from_tool.py`.
	Sanctum = library_from_tool.main()
	main(Sanctum)
