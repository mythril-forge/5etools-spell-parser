import json
import re

example = '''
## Description
Objects come to life at your command. Choose up to ten nonmagical objects within range that are not being worn or carried. Medium targets count as two objects, Large targets count as four objects, Huge targets count as eight objects. You can't animate any object larger than Huge. Each target animates and becomes a creature under your control until the spell ends or until reduced to 0 hit points.

As a bonus action, you can mentally command any creature you made with this spell if the creature is within 500 feet of you (if you control multiple creatures, you can command any or all of them at the same time, issuing the same command to each one). You decide what action the creature will take and where it will move during its next turn, or you can issue a general command, such as to guard a particular chamber or corridor. If you issue no commands, the creature only defends itself against hostile creatures. Once given an order, the creature continues to follow it until its task is complete.
| Size | HP | AC | Attack | Str | Dex |
|-----|-----|-----|-----|-----|-----|
| {@creature animated object (tiny)|phb|Tiny} | 20 | 18 | {@hit +8} to hit, {@damage 1d4 + 4} damage | {@dice 1d20-3|4} | {@dice 1d20+4|18} |
| {@creature animated object (small)|phb|Small} | 25 | 16 | {@hit +6} to hit, {@damage 1d8 + 2} damage | {@dice 1d20-2|6} | {@dice 1d20+2|14} |
| {@creature animated object (medium)|phb|Medium} | 40 | 13 | {@hit +5} to hit, {@damage 2d6 + 1} damage | {@dice 1d20|10} | {@dice 1d20+1|12} |
| {@creature animated object (large)|phb|Large} | 50 | 10 | {@hit +6} to hit, {@damage 2d10 + 2} damage | {@dice 1d20+2|14} | {@dice 1d20|10} |
| {@creature animated object (huge)|phb|Huge} | 80 | 10 | {@hit +8} to hit, {@damage 2d12 + 4} damage | {@dice 1d20+4|18} | {@dice 1d20-3|6} |

An animated object is a construct with AC, hit points, attacks, Strength, and Dexterity determined by its size. Its Constitution is 10 and its Intelligence and Wisdom are 3, and its Charisma is 1. Its speed is 30 feet; if the object lacks legs or other appendages it can use for locomotion, it instead has a flying speed of 30 feet and can hover. If the object is securely attached to a surface or a larger object, such as a chain bolted to a wall, its speed is 0. It has blindsight with a radius of 30 feet and is blind beyond that distance. When the animated object drops to 0 hit points, it reverts to its original object form, and any remaining damage carries over to its original object form.

If you command an object to attack, it can make a single melee attack against a creature within 5 feet of it. It makes a slam attack with an attack bonus and bludgeoning damage determined by its size. The DM might rule that a specific object inflicts slashing or piercing damage based on its form.

## At Higher Levels
If you cast this spell using a spell slot of 6th level or higher, you can animate two additional objects for each slot level above 5th.
'''

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
		expr = r'\|\d+?'
		dirty = re.sub(expr, '', dirty)
		# Space out adding, subtracting, multiplying, dividing.
		# TODO
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

	else:
		raise

	return dirty

if __name__ == '__main__':
	with open('bad_strings.json', 'r') as file:
		BadStrings = json.load(file)
	BadStrings = list(dict.fromkeys(BadStrings))
	BadStrings = sorted(BadStrings)
	for bad in BadStrings:
		remove_metadata(bad)