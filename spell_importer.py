import requests

URL='https://raw.githubusercontent.com/ariestae/5etools/master/data/spells/'
SOURCE = {
	'PHB': 'spells-phb.json',
	'SCAG': 'spells-scag.json',
	'UAModernMagic': 'spells-ua-mm.json',
	'UAStarterSpells': 'spells-ua-ss.json',
	'UAThatOldBlackMagic': 'spells-ua-tobm.json',
	'XGE': 'spells-xge.json',
	'BoLS 3pp': 'spells-3pp-bols.json'
}
SOURCE_DATA = {
	requests.get(f'{URL}{SOURCE['SCAG']}').json()


def get_school(letter):
	letter = letter.lower()
	if False:
		pass
	elif letter == 'a':
		return 'abjuration'
	elif letter == 'c':
		return 'conjuration'
	elif letter == 'd':
		return 'divination'
	elif letter == 'e':
		return 'enchantment'
	elif letter == 'i':
		return 'illusion'
	elif letter == 'n':
		return 'necromancy'
	elif letter == 't':
		return 'transmutation'
	elif letter == 'v':
		return 'evocation'

def get_nth(number):
	if number < 0 or number > 9:
		pass
	elif number == 1:
		return '1st'
	elif number == 2:
		return '2nd'
	elif number == 3:
		return '3rd'
	else:
		return f'{str(number)}th'

def grab_entries(entries_list):
	for entry in entries_list:
		print(entry)

if __name__ == '__main__':
	print(f'getting data from {"".join([URL, SOURCE["SCAG"]])}')
	for spell in TEMP_DATA['spell']:
		slug = slugify(spell['name'])
		href = ''.join(['./scag/',slug,'.md'])
		spell['school'] = get_school(spell['school'])
		with open(href, 'w+') as file:
			# put title in h1
			file.write('# ' + spell['name'] + '\n')
			# state level and school
			file.write(get_nth(spell['level']) + '-level ' + spell['school'] + '\n')
			# get casting time
			file.write('Casting Time: ' + '\n')
			# get lasting time
			file.write('Duration: ' + '\n')
			# get range
			file.write('Casting Time: ' + '\n')
			# get shape and shape parameters:
			file.write('Shape: ' + '\n')
			# find spell tags (VSMCR)
			file.write('Tags: ' + '\n')
			# retrieve material components
			file.write('Verbal Components: ' + '\n')
			file.write('Somatic Components: ' + '\n')
			file.write('Material Components: ' + '\n')
			
			# seperate next section
			file.write('\n---\n\n')
			for entry in spell['entries']:
				print(entry)
				file.write(''.join([entry, '\n']))
