import json
import re
from slugify import slugify

def cleanse_markdown(data):
	while True:
		if re.search(r'{@.*?}', data):
			search = re.search(r'{@.*?}', data).group()
			result = remove_metadata(search)
			data = data.replace(search, result, 1)
		else:
			break
	return data

def remove_metadata(dirty):
	if re.search(r'{@chance .+?}', dirty):
		# remove typing.
		expr = r'(?<={@chance\s).+(?=})'
		dirty = re.search(expr, dirty).group()
		# add percentage.
		dirty += ' percent'

	elif re.search(r'{@condition .+?}', dirty):
		# remove typing.
		expr = r'(?<={@condition\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# || implies or in this json.
		expr = r'.+\|\|'
		dirty = re.sub(expr, '', dirty)
		# italicize conditions
		# TODO italics or bold??
		dirty = f'**{dirty}**'

	elif re.search(r'{@creature .+?}', dirty):
		# remove typing.
		expr = r'(?<={@creature\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# || implies or in this json.
		expr = r'.+\|\|'
		dirty = re.sub(expr, '', dirty)
		# remove creature data.
		expr = r'\|.+?\|.+'
		dirty = re.sub(expr, '', dirty)

	elif re.search(r'{@damage .+?}', dirty):
		# remove typing.
		expr = r'(?<={@damage\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# add code ticks to specify a dice roll.
		dirty = f'`{dirty}`'

	elif re.search(r'{@dice .+?}', dirty):
		# remove typing.
		expr = r'(?<={@dice\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# remove dice average indicator from string.
		expr = r'\|\d+'
		dirty = re.sub(expr, '', dirty)
		# Space out adding, subtracting, multiplying, dividing.
		expr = r'(?<=\d)\+(?=\d)'
		dirty = re.sub(expr, ' + ', dirty)
		expr = r'(?<=\d)\-(?=\d)'
		dirty = re.sub(expr, ' &minus; ', dirty)
		expr = r'(?<=\d)[\×|\*](?=\d)'
		dirty = re.sub(expr, ' &times; ', dirty)
		expr = r'(?<=\d)[\÷|\/](?=\d)'
		dirty = re.sub(expr, ' &divide; ', dirty)
		# add code ticks to specify a dice roll.
		dirty = f'`{dirty}`'

	elif re.search(r'{@filter .+?}', dirty):
		# remove typing.
		expr = r'(?<={@filter\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# remove all these extra metadata after |
		expr = r'\|.+'
		dirty = re.sub(expr, '', dirty)

	elif re.search(r'{@i .+?}', dirty):
		# remove typing.
		expr = r'(?<={@i\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# add italics.
		dirty = f'*{dirty}*'

	elif re.search(r'{@hit .+?}', dirty):
		# remove typing.
		expr = r'(?<={@hit\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# add code ticks to specify a dice roll.
		dirty = f'`{dirty}`'

	elif re.search(r'{@item .+?}', dirty):
		# remove typing.
		expr = r'(?<={@item\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# remove all these extra metadata after |
		expr = r'\|.+'
		dirty = re.sub(expr, '', dirty)

	elif re.search(r'{@race .+?}', dirty):
		# remove typing.
		expr = r'(?<={@race\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# || implies or in this json.
		expr = r'.+\|\|'
		dirty = re.sub(expr, '', dirty)

	elif re.search(r'{@scaledice .+?}', dirty):
		# remove typing.
		expr = r'(?<={@scaledice\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# || implies reads-as in this json.
		expr = r'.+\|'
		dirty = re.sub(expr, '', dirty)
		# add code ticks to specify a dice roll.
		dirty = f'`{dirty}`'

	elif re.search(r'{@skill .+?}', dirty):
		# remove typing.
		expr = r'(?<={@skill\s).+?(?=})'
		dirty = re.search(expr, dirty).group()

	elif re.search(r'{@spell .+?}', dirty):
		# remove typing.
		expr = r'(?<={@spell\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# embolden other spell names
		slug = slugify(dirty)
		#TODO add markdown link to other spell
		dirty = f'[*{dirty}*](./{slug})'

	else:
		raise

	return dirty

if __name__ == '__main__':
	md = ''
	with open('bad_strings.json', 'r') as file:
		gross = json.load(file)
	for bad in gross:
		md += cleanse_markdown(bad)