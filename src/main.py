# python packages
import os
# project imports
import library_from_tool



def main(level_library):
	'''
	==NOTE==
	This only fetches markdown for now.
	==NOTE==
	This only sorts outputs by level for now.
	==TODO==
	This could be expanded, but would need to be refactored.
	'''
	for level in level_library:
		level_set = level_library[level]
		for slug in level_set:
			# grab spell markdown
			spell = level_set[slug]
			# get directory and path strings
			directory = os.path.dirname('./spells/')
			directory += '/level-'
			directory += str(level)
			# print(directory)
			path = directory
			path += '/'
			path += slug
			path += '.md'
			# print(path)
			# create directory
			if not os.path.exists(directory):
				os.makedirs(directory)
			# create file and add to directory
			with open(path, 'w') as file:
				file.write(spell)



if __name__ == '__main__':
	# ==NOTE==
	# utilizing `library_from_tool.py`.
	Sanctum = library_from_tool.main()
	library = Sanctum.extract_markdown()
	main(library)
