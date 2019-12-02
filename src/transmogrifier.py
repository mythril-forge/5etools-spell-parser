from language import *
import re



# Some subroutines are required to parse the data.
def scrub_data(entry, depth=0):
	'''
	This will take the entries object and clean it.
	It does a thorough job; it cleans entries recursively.
	The function takes in the expected 5etools object,
	and it returns a markdown-like string.
	'''
	# A string can't be deconstructed any more;
	# this just parses it a bit before returning.
	if isinstance(entry, str):
		# Each sentance needs to be on a different line.
		# The `tails` regex finds areas that break this rule.
		tails = r'((?<=([!\?\.]))|(?<=([!\?\.]\)))) '
		# All that needs to be done is adding some extra
		# new-line breaks to keep GitHub diffs prettier.
		cleaned = re.sub(tails, '\n', entry)
		cleaned = f'{cleaned}'
		cleaned = cleaned.strip()
		cleaned = f'\n{cleaned}\n'
		return cleaned

	# The entry is type list.
	# Just iterate through and clean each item!
	elif isinstance(entry, list):
		cleaned = ''
		# This entry has yet more entries.
		for item in entry:
			cleaned += scrub_data(item, depth)
		cleaned = cleaned.strip()
		cleaned += '\n\n'
		return cleaned

	# The entry is type `entries`.
	# As ambiguous as that is, it is easy to explain.
	# This is just a heading with content.
	elif entry.get('type') == 'entries':
		cleaned = f"{'#' * (depth + 2)} {entry['name']}\n"
		cleaned += scrub_data(entry['entries'], depth + 1)
		return cleaned

	elif entry.get('type') == 'quote':
		# The entry is expected to be a string,
		# but it might work with other formats.
		# Naturally, the entry must be cleaned.
		cleaned = scrub_data(entry['entries'], depth).strip()
		cleaned = re.sub(r'^', '> ', cleaned) + '\n'
		cleaned = re.sub(r'\n', '\n> ', cleaned)
		cleaned += f"\n> &mdash; {entry['by']}"
		cleaned = cleaned.strip()
		cleaned += '\n'
		return cleaned

	# An entry with type=list is not a list-type object.
	# Instead, it represents a bulleted list.
	elif entry.get('type') == 'list':
		cleaned = ''
		# This entry has yet more entries...eerrr, items.
		for item in entry['items']:
			# The item is expected to be a string,
			# but it might work with other formats.
			# Naturally, the item must be cleaned.
			content = scrub_data(item, depth)
			content = f'- {content.strip()}'
			# If the item is a multiline string, then
			# each line after the first must be indented.
			content = re.sub(r'\n', '\n\t', content)
			content = content.strip()
			content += '\n'
			cleaned += content
		cleaned = cleaned.strip()
		cleaned += '\n'
		return cleaned

	# The entry is a table.
	# Iterate through the contents and build it up!
	elif entry.get('type') == 'table':
		cleaned = ''
		# Start with the caption, if any.
		if entry.get('caption'):
			cleaned += f"#### {entry['caption']}\n"
		# This entry has yet more entries...eerrr, cells.
		cleaned += '|'
		for cell in entry.get('colLabels'):
			cleaned += (
				f' {scrub_data(cell, depth).strip()} |'
			)
		cleaned += (
			f"\n{'|-----' * len(entry['colLabels'])}|"
		)
		# This entry has yet more entries...eerrr, cells.
		for row in entry.get('rows'):
			cleaned += '\n|'
			for cell in row:
				cell = scrub_data(cell, depth).strip()
				cell = re.sub('\n', ' ', cell)
				cleaned += (
					f' {cell} |'
				)
		cleaned = cleaned.strip()
		cleaned = f'\n{cleaned}\n'
		return cleaned

	# The `cell` type is a bit of a misnomer.
	# It only allows for number-based dice-roll results.
	elif entry.get('type') == 'cell':
		# Check whether its a roll range, or an exact roll.
		if entry['roll'].get('exact'):
			cleaned = str(entry['roll']['exact'])
		else:
			minimum = entry['roll']['min']
			maximum = entry['roll']['max']
			cleaned = f'{minimum}&ndash;{maximum}'
		# The result will be formatted as a table-item
		# higher in the recursive stack-trace.
		return cleaned

	else:
		print(entry)
		input('Something went wrong. See logs above.')
		raise Exception('INVALID ENTRY TYPE')


# Now we reformat special phrases.
def reformat_phrases(text):
	# There is so much data to parse through;
	# there is a seperate file to seperate concerns.
	# Now we can take the first letter of every line.
	# Naturally, those letters will become uppercase.
	for phrase in PREUPPER_ITALICS:
		shift = 0
		for match in re.finditer(phrase, text):
			left_text  = text[:match.span()[0] + shift]
			right_text = text[match.span()[1] + shift:]
			middle_text = f'*{match.group().lower()}*'
			# Track how much bigger/smaller `text` got.
			new_text = left_text + middle_text + right_text
			shift += len(new_text) - len(text)
			text = new_text

	for phrase in NATURAL_UPPERCASE:
		for match in re.finditer(phrase, text):
			left_text  = text[:match.span()[0]]
			right_text = text[match.span()[1]:]
			middle_text = match.group().upper()
			text = left_text + middle_text + right_text

	# First, capitalize special phrases.
	for phrase in CAPITAL_PHRASES:
		for match in re.finditer(phrase, text, re.I):
			left_text  = text[:match.span()[0]]
			right_text = text[match.span()[1]:]
			middle_text = match.group().title()
			text = left_text + middle_text + right_text

	# Next, all-cap ac and dc.
	for phrase in ALLCAP_PHRASES:
		for match in re.finditer(phrase, text, re.I):
			left_text  = text[:match.span()[0]]
			right_text = text[match.span()[1]:]
			middle_text = match.group().upper()
			text = left_text + middle_text + right_text

	for phrase in BOLD_PHRASES:
		shift = 0
		for match in re.finditer(phrase, text, re.I):
			left_text  = text[:match.span()[0] + shift]
			right_text = text[match.span()[1] + shift:]
			middle_text = f'**{match.group().lower()}**'
			# Track how much bigger/smaller `text` got.
			new_text = left_text + middle_text + right_text
			shift += len(new_text) - len(text)
			text = new_text

	for phrase in ITALIC_PHRASES:
		shift = 0
		for match in re.finditer(phrase, text, re.I):
			left_text  = text[:match.span()[0] + shift]
			right_text = text[match.span()[1] + shift:]
			middle_text = f'*{match.group().lower()}*'
			# Track how much bigger/smaller `text` got.
			new_text = left_text + middle_text + right_text
			shift += len(new_text) - len(text)
			text = new_text

	for phrase in DICE_PHRASES:
		shift = 0
		for match in re.finditer(phrase, text, re.I):
			left_text  = text[:match.span()[0] + shift]
			right_text = text[match.span()[1] + shift:]
			middle_text = f'`{match.group().lower()}`'
			# Track how much bigger/smaller `text` got.
			new_text = left_text + middle_text + right_text
			shift += len(new_text) - len(text)
			text = new_text

	for phrase in PERCENT_PHRASES:
		shift = 0
		for match in re.finditer(phrase, text, re.I):
			left_text  = text[:match.span()[0] + shift]
			right_text = text[match.span()[1] + shift:]
			middle_text = f'`{match.group().lower()}%`'
			middle_text = re.sub(' percent', '', middle_text)
			# Track how much bigger/smaller `text` got.
			new_text = left_text + middle_text + right_text
			shift += len(new_text) - len(text)
			text = new_text

	# Here we do arbitrary cleanup before returning.
	text = re.sub('\n\n+(?=([>-] ))', '\n', text)
	text = re.sub('\n\n+', '\n\n', text)
	text = re.sub(
		'Attack And Damage Rolls',
		'Attack &amp; Damage Rolls',
		text
	)
	return text




# From there we still need to clean the entries more...
# Specifically, some text needs bolded or other formats.
# Looks like we need another subroutine!
def parse_metadata(text):
	tag = re.search(r'{@.*? ', text)
	if tag is None:
		# There are no special tags in the text.
		return text

	# Split left, middle, and right based on tag result.
	# The tag is the middle, but we will be deleting it.
	left_text = text[:tag.span()[0]]
	right_text = text[tag.span()[1]:]
	tag = tag.group()[2:-1]

	# Recursively clean the right side of the text first.
	# This takes care of any nested text-tagging.
	right_text = parse_metadata(right_text)

	# Since the right text is cleaned, we can safely find
	# text leading to the next available closing brace.
	middle_text = re.search(r'.*?(?=})', right_text)
	right_text = right_text[middle_text.span()[1] + 1:]
	middle_text = middle_text.group()

	# ==NOTE==
	# Now there are four variables.
	# 1. tag
	# 2. left_text
	# 3. right_text
	# 4. middle_text

	# Clean up previous subroutines.
	middle_text = re.sub(r'(\*|`|_)+', '', middle_text)
	tag = re.sub(r'(\*|`|_)+', '', tag)

	def seperate(subtext, malformed = False):
		if not malformed:
			# ==NOTE==
			# `||` indicates a morphed version of the string.
			# Keep the morphed text here -- the right-side.
			subtext = re.sub(r'.*\|\|', '', subtext)
			# `|???|` indicates extraneous metadata.
			# Just keep the left-side text here.
			subtext = re.sub(r'\|.*?\|.*', '', subtext)
			# `|` indicates a semantic split.
			# Keep the left-side data in this case.
			subtext = re.sub(r'\|.*', '', subtext)
			return subtext
		else:
			# ==NOTE==
			# The seperator filter is malformed here.
			# `|` indicates a source, keep left.
			# `|???|` indicates a source & rename, keep right.
			subtext = re.sub(r'.*\|.*?\|', '', subtext)
			subtext = re.sub(r'\|.*', '', subtext)
			return subtext

	if tag == 'action':
		# Actions are italicized.
		middle_text = f'*{middle_text}*'

	elif tag == 'chance':
		# Dice, randomness, and other math use code blocks.
		middle_text = f'`{middle_text}%`'

	elif tag == 'condition':
		# Get rid of seperators.
		middle_text = seperate(middle_text)
		# Conditions get emphasized/bolded.
		middle_text = f'**{middle_text}**'

	elif tag == 'creature':
		# Get rid of seperators.
		middle_text = seperate(middle_text)
		# Certain game mechanics get capitalized.
		middle_text = middle_text.title()
		# ==FIXME==
		# "The Celestial" should not be capitalized.

	elif tag == 'damage':
		# Use proper mathematics symbols.
		middle_text = re.sub(r'[\+]',   ' + ', middle_text)
		middle_text = re.sub(r'[\–\-]', ' – ', middle_text)
		middle_text = re.sub(r'[\×\*]', ' × ', middle_text)
		middle_text = re.sub(r'[\÷\/]', ' ÷ ', middle_text)
		# Dice modifiers must have one space of padding.
		middle_text = re.sub(r' +', ' ', middle_text)
		# Dice, randomness, and other math use code blocks.
		middle_text = f'`{middle_text}`'

	elif tag == 'dice':
		# Get rid of seperators.
		middle_text = seperate(middle_text)
		# Use proper mathematics symbols.
		middle_text = re.sub(r'[\+]',   ' + ', middle_text)
		middle_text = re.sub(r'[\-\–]', ' – ', middle_text)
		middle_text = re.sub(r'[\*\×]', ' × ', middle_text)
		middle_text = re.sub(r'[\/\÷]', ' ÷ ', middle_text)
		# Dice modifiers must have one space of padding.
		middle_text = re.sub(r' +', ' ', middle_text)
		# Dice, randomness, and other math use code blocks.
		middle_text = f'`{middle_text}`'

	elif tag == 'filter':
		# Get rid of seperators.
		middle_text = seperate(middle_text)

	elif tag == 'hit':
		# Use proper mathematical symbols.
		middle_text = re.sub(r'[\+]',   '+', middle_text)
		middle_text = re.sub(r'[\-\–]', '–', middle_text)
		middle_text = re.sub(r'[\*\×]', '×', middle_text)
		middle_text = re.sub(r'[\/\÷]', '÷', middle_text)
		# Dice, randomness, and other math use code blocks.
		middle_text = f'`{middle_text}`'

	elif tag == 'i':
		# Weird inline quotes get italics + double-quotes.
		middle_text = f'*"{middle_text}"*'

	elif tag == 'item':
		# Get rid of seperators.
		middle_text = seperate(middle_text, True)
		# Items need to be italic
		middle_text = f'*{middle_text}*'

	elif tag == 'note':
		# Notes might be good in blockquotes, but naw.
		pass

	elif tag == 'race':
		# Get rid of seperators.
		middle_text = seperate(middle_text)
		# Certain game mechanics get capitalized.
		middle_text = middle_text.title()

	elif tag == 'scaledice':
		# Get rid of seperators.
		middle_text = seperate(middle_text, True)
		# Use proper mathematics symbols.
		middle_text = re.sub(r'[\+]',   ' + ', middle_text)
		middle_text = re.sub(r'[\-\–]', ' – ', middle_text)
		middle_text = re.sub(r'[\*\×]', ' × ', middle_text)
		middle_text = re.sub(r'[\/\÷]', ' ÷ ', middle_text)
		# Dice modifiers must have one space of padding.
		middle_text = re.sub(r' +', ' ', middle_text)
		# Dice, randomness, and other math use code blocks.
		middle_text = f'`{middle_text}`'

	elif tag == 'sense':
		# Senses don't get any special format.
		pass

	elif tag == 'skill':
		# Certain game mechanics get capitalized.
		middle_text = middle_text.title()

	elif tag == 'spell':
		# Spells should be italicized and become anchored.
		middle_text = f'[*{middle_text}*][link]'

	else:
		print('\n', tag)
		input(middle_text)
		raise Exception(tag)

	# Return post-formatted text.
	return left_text + middle_text + right_text
