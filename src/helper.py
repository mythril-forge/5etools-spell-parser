def nth_number(number):
	if number < 0 or number > 9:
		raise Exception(f'cant stringify number: {number}')
	elif number == 1:
		return '1st'
	elif number == 2:
		return '2nd'
	elif number == 3:
		return '3rd'
	else:
		return f'{str(number)}th'
