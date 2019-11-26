# python packages
import os
# project imports
import get_from_text
import get_from_tool



def main(library):
	organize_by_level(library)



def organize_by_source(library):
	for acronym in library:
		book = library[acronym]
		for slug in book:
			# grab spell markdown
			spell = book[slug]
			# get directory and path strings
			directory = os.path.dirname('./spells/')
			directory += '/'
			directory += acronym
			path = directory
			path += '/'
			path += slug
			path += '.md'
			# create directory
			if not os.path.exists(directory):
				os.makedirs(directory)
			# create file and add to directory
			with open(path, 'w') as file:
				file.write(spell)



def organize_by_level(level_library):
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



def disorganize(library):
	for acronym in library:
		book = library[acronym]
		for slug in book:
			# grab spell markdown
			spell = book[slug]
			# get directory and path strings
			directory = os.path.dirname('./spells/')
			# directory += '/'
			# directory += acronym
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


# ==TODO==
# def organize_via_book(library):



# ==TODO==
# def organize_via_level(library):



# ==TODO==
# def do_not_organize(library):



if __name__ == '__main__':
	data_option = input(
		'You are about to generate spell markdown files.\n'
		'Please choose a source of your data below.\n'
		'┌──┬─────────────┐\n'
		'│TX│get from text│\n'
		'│5E│get from tool│\n'
		'│JS│get from json│\n'
		'├──┴─────────────┘\n'
		'╘input: '
	)
	sort_option = input(
		'How would you like to sort folders?\n'
		'┌──┬─────────────┐\n'
		'│NO│dont sort    │\n'
		'│LV│sort by level│\n'
		'│BK│sort by book │\n'
		'├──┴─────────────┘\n'
		'╘input: '
	)
	if data_option.upper() == 'TX':
		Sanctum = get_from_text.main()
	elif data_option.upper() == '5E':
		Sanctum = get_from_tool.main()
	elif data_option.upper() == 'JS':
		Sanctum = get_from_json.main()
	else:
		Sanctum = get_from_tool.main()

	if sort_option.upper() == 'NO':
		library = Sanctum.extract_markdown()
		disorganize(library)
	elif sort_option.upper() == 'LV':
		library = Sanctum.extract_markdown(True)
		organize_by_level(library)
	elif sort_option.upper() == 'BK':
		library = Sanctum.extract_markdown()
		organize_by_source(library)
	else:
		library = Sanctum.extract_markdown(True)
		organize_by_level(library)
