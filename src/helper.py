# Numeric data will be stored as integers where possible.
# All units are converted to seconds.
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
# A dictionary like this helps figure out plural words.
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
	'millennia': 'millennium'}

def time2num(amount, unit):
	result = convert_time[unit] * amount
	return result
