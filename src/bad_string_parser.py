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
		'''
		Chances should be in backticks
		and must have a (%) percentile sign.
		In some rare cases, a (‰) permille sign
		may be more appropriate instead.
		'''
		# remove typing.
		expr = r'(?<={@chance\s).+(?=})'
		dirty = re.search(expr, dirty).group()
		# add code ticks to specify statistics or randomness.
		# then add a percentage.
		dirty += f'`{dirty}%`'

	elif re.search(r'{@condition .+?}', dirty):
		'''
		Conditions should be emboldened; they are more
		important to notice than other game statistics.
		'''
		# remove typing.
		expr = r'(?<={@condition\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# || implies a semantic split in the json.
		# in this case, we just want the final item.
		expr = r'.+\|\|'
		dirty = re.sub(expr, '', dirty)
		# embolden conditions.
		dirty = f'**{dirty}**'

	elif re.search(r'{@creature .+?}', dirty):
		'''
		Creatures, races, classes, and their various subtypes
		should be modestly distinguishable so they can be read
		as a proper game mechanic versus their english meaning.
		'''
		# remove typing.
		expr = r'(?<={@creature\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# || implies a semantic split in the json.
		# in this case, we just want the final item.
		expr = r'.+\|\|'
		dirty = re.sub(expr, '', dirty)
		# remove creature data.
		expr = r'\|.+?\|.+'
		dirty = re.sub(expr, '', dirty)
		# add italics.
		dirty = f'*{dirty}*'

	elif re.search(r'{@damage .+?}', dirty):
		'''
		Damage is formatted like all other dice.
		'''
		# remove typing.
		expr = r'(?<={@damage\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# add code ticks to specify statistics or randomness.
		dirty = f'`{dirty}`'

	elif re.search(r'{@dice .+?}', dirty):
		'''
		Dice, randomness, and mathematical operators are
		within code blocks to show their mathematical nature.
		==NOTE==
		HTML entities cannot be used within code blocks;
		math symbols (such as &minus;) are used naked.
		==FIXME==
		Invalid spacing, like {@dice 3+ 3d6}, will
		not be properly formatted by this function.
		'''
		# remove typing.
		expr = r'(?<={@dice\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# remove dice average indicator from string.
		expr = r'\|\d+'
		dirty = re.sub(expr, '', dirty)
		# add padding to mathematical operators.
		expr = r'(?<=\d)\+(?=\d)'
		dirty = re.sub(expr, ' + ', dirty)
		expr = r'(?<=\d)[\-|\–](?=\d)'
		dirty = re.sub(expr, ' – ', dirty)
		expr = r'(?<=\d)[\×|\*](?=\d)'
		dirty = re.sub(expr, ' × ', dirty)
		expr = r'(?<=\d)[\÷|\/](?=\d)'
		dirty = re.sub(expr, ' &divide; ', dirty)
		# add code ticks to specify statistics or randomness.
		dirty = f'`{dirty}`'

	elif re.search(r'{@filter .+?}', dirty):
		'''
		Filters are incredibly complex because they
		have a variety of indications and inputs.
		Thus, they are just transformed into normal strings.
		'''
		# remove typing.
		expr = r'(?<={@filter\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# remove all these extra metadata after |
		expr = r'\|.+'
		dirty = re.sub(expr, '', dirty)

	elif re.search(r'{@i .+?}', dirty):
		'''
		This literally means quoted italics.
		'''
		# remove typing.
		expr = r'(?<={@i\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# add italics.
		dirty = f'*"{dirty}"*'

	elif re.search(r'{@hit .+?}', dirty):
		'''
		To-hit bonuses are specially formatted.
		They have no padding after the plus/minus sign.
		Otherwise they behave like other dice operators.
		'''
		# remove typing.
		expr = r'(?<={@hit\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# add code ticks to specify statistics or randomness.
		dirty = f'`{dirty}`'

	elif re.search(r'{@item .+?}', dirty):
		'''
		Items, spells, and other miscellaneous game mechanics
		should be modestly distinguishable so they can be read
		as a proper game mechanic versus their english meaning.
		'''
		# remove typing.
		expr = r'(?<={@item\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# remove all these extra metadata after |
		expr = r'\|.+'
		dirty = re.sub(expr, '', dirty)
		# add italics.
		dirty = f'*{dirty}*'

	elif re.search(r'{@race .+?}', dirty):
		'''
		Creatures, races, classes, and their various subtypes
		should be modestly distinguishable so they can be read
		as a proper game mechanic versus their english meaning.
		'''
		# remove typing.
		expr = r'(?<={@race\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# || implies a semantic split in the json.
		# in this case, we just want the final item.
		expr = r'.+\|\|'
		dirty = re.sub(expr, '', dirty)
		# add italics.
		dirty = f'*{dirty}*'

	elif re.search(r'{@scaledice .+?}', dirty):
		'''
		Scale-Damage is formatted like all other dice.
		'''
		# remove typing.
		expr = r'(?<={@scaledice\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# remove all these extra metadata after |
		expr = r'.+\|'
		dirty = re.sub(expr, '', dirty)
		# add code ticks to specify statistics or randomness.
		dirty = f'`{dirty}`'

	elif re.search(r'{@sense .+?}', dirty):
		'''
		Senses, like hit points, challenge rating and others,
		does not have any special formatting.
		The phrase itself should infer its game mechanics.
		'''
		# remove typing.
		expr = r'(?<={@sense\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# remove all these extra metadata after |
		expr = r'.+\|'
		dirty = re.sub(expr, '', dirty)

	elif re.search(r'{@skill .+?}', dirty):
		'''
		Skills, like hit points, challenge rating and others,
		does not have any special formatting.
		The phrase itself should infer its game mechanics.
		'''
		# remove typing.
		expr = r'(?<={@skill\s).+?(?=})'
		dirty = re.search(expr, dirty).group()

	elif re.search(r'{@spell .+?}', dirty):
		'''
		Items, spells, and other miscellaneous game mechanics
		should be modestly distinguishable so they can be read
		as a proper game mechanic versus their english meaning.
		Spells especially have anchored links.
		'''
		# remove typing.
		expr = r'(?<={@spell\s).+?(?=})'
		dirty = re.search(expr, dirty).group()
		# ==TODO==
		# properly add markdown link to other spell
		slug = slugify(dirty)
		# add italics.
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
