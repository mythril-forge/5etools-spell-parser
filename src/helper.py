# All spacial units are converted to points.
# Note, 72 points is an inch.
# Id rather use inches but fractions of inches are utilized.
# To keep all data as integers, points are used for data.
convert_space = {
	'point': 1,
	'inch': 72,
	'foot': 864,
	# 'yard': 2592,
	'mile': 4561920,
	'points': 1,
	'inches': 72,
	'feet': 864,
	# 'yards': 2592,
	'miles': 4561920,
}

# All temporal units are converted to seconds.
# Note, month and year have approximate values.
convert_time = {
	'second': 1,
	'round': 10,
	'minute': 60,
	'hour': 3600,
	'day': 86400,
	'week': 604800,
	'month': 2592000, # 30 days
	'year': 31104000, # 360 days
	'decade': 311040000,
	'century': 3110400000,
	'millennium': 31104000000,
	'seconds': 1,
	'rounds': 10,
	'minutes': 60,
	'hours': 3600,
	'days': 86400,
	'weeks': 604800,
	'months': 2592000, # 30 days
	'years': 31104000, # 360 days
	'decades': 311040000,
	'centuries': 3110400000,
	'millennia': 31104000000,
}

# We will be converting to & from strings often.
# Dictionaries like these help figure out plural words.
pluralize_space = {
	'point': 'points',
	'inch': 'inches',
	'foot': 'feet',
	'yard': 'yards',
	'mile': 'miles',
}
singularize_space = {
	'points': 'point',
	'inches': 'inch',
	'feet': 'foot',
	'yards': 'yard',
	'miles': 'mile',
}
pluralize_time = {
	'second': 'seconds',
	'round': 'rounds',
	'minute': 'minutes',
	'hour': 'hours',
	'day': 'days',
	'week': 'weeks',
	'month': 'months',
	'year': 'years',
	'decade': 'decades',
	'century': 'centuries',
	'millennium': 'millennia',
}
singularize_time = {
	'seconds': 'second',
	'rounds': 'round',
	'minutes': 'minute',
	'hours': 'hour',
	'days': 'day',
	'weeks': 'week',
	'months': 'month',
	'years': 'year',
	'decades': 'decade',
	'centuries': 'century',
	'millennia': 'millennium',
}

# The shape parameter dictionary will help parse
# through and validate complex shape data points.
shape_parameters = {
	'aura': {
		'radius',
	},
	'sphere': {
		'radius',
	},
	'cone': {
		'radius',
	},
	'cylinder': {
		'radius',
		'height',
	},
	'cube': {
		'length',
	},
	'line': {
		'length',
		'width',
	},
	'wall': {
		'length',
		'width',
		'height',
	},
}

# these cleaned acronyms could very well be useful later...
book_acronyms = {
	'ai': 'Acquisitions Incorporated',
	'ggr': 'Guildmasters\' Guide to Ravnica',
	'llk': 'Lost Laboratory of Kwalish',
	'phb': 'Player\'s Handbook',
	'scag': 'Sword Coast Adventurer\'s Guide',
	'stream': 'Live Stream',
	'ua-ar': 'Unearthed Arcana: Artificer Revisited',
	'ua-mm': 'Unearthed Arcana: Modern Magic',
	'ua-ss': 'Unearthed Arcana: Starter Spells',
	'ua-tobm': 'Unearthed Arcana: That Old Black Magic',
	'xge': 'Xanathar\'s Guide to Everything',
}

book_transition_temp = {
	'AI': 'ai',
	'GGR': 'ggr',
	'LLK': 'llk',
	'PHB': 'phb',
	'SCAG': 'scag',
	'Stream': 'stream',
	'UAArtificerRevisited': 'ua-ar',
	'UAModernMagic': 'ua-mm',
	'UAStarterSpells': 'ua-ss',
	'UAThatOldBlackMagic': 'ua-tobm',
	'XGE': 'xge'
}

# the tag symbols help give an overview for the spell
tag_symbols = {
	'verbal': 'V',
	'somatic': 'S',
	'material': 'M',
	'concentration': 'C',
	'ritual': 'R',
	'royalty': '$'
}

def time2str(amount, delimiter=' '):
	'''
	converts an amount of seconds to a readable string.
	'''
	if amount['quality'] != None:
		return amount['quality']
	elif amount['seconds'] != None:
		best_unit = 'seconds'
		for unit in convert_time:
			if amount['seconds'] % convert_time[unit] == 0: # and amount['seconds'] >= convert_time[unit]:
				if convert_time[unit] > convert_time[best_unit]:
					best_unit = unit
		duration = amount['seconds'] / convert_time[best_unit]
		if duration > 1 and delimiter == ' ':
			best_unit = pluralize_time.get(best_unit, best_unit)
			duration = int(duration)
		elif duration <= 1 or delimiter != ' ':
			best_unit = singularize_time.get(best_unit, best_unit)
		if duration >= 1:
			duration = int(duration)
		result = f'{duration}{delimiter}{best_unit}'
		return result

def space2str(distance, delimiter=' '):
	if distance:
		best_unit = 'points'
		for unit in convert_space:
			if distance % convert_space[unit] == 0: # and distance >= convert_space[unit]:
				if convert_space[unit] > convert_space[best_unit]:
					best_unit = unit
		distance = distance / convert_space[best_unit]
		if distance > 1 and delimiter == ' ':
			best_unit = pluralize_space.get(best_unit, best_unit)
		elif distance <= 1 or delimiter != ' ':
			best_unit = singularize_space.get(best_unit, best_unit)
		if distance >= 1:
			distance = int(distance)
		result = f'{distance}{delimiter}{best_unit}'
		return result

def time2num(amount, unit):
	'''
	converts any amount of a temporal measurement to seconds.
	'''
	return int(convert_time[unit] * amount)

def space2num(amount, unit):
	'''
	converts any amount of a spacial measurement to points.
	'''
	return int(convert_space[unit] * amount)

def nth_number(number):
	if number < 0 or number > 9:
		raise Exception(f'stringify number {number}: ' \
		'out of range')
	elif number == 1:
		return '1st'
	elif number == 2:
		return '2nd'
	elif number == 3:
		return '3rd'
	else:
		return f'{str(number)}th'
