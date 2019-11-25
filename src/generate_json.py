import generate_json

def main():
	library = generate_json.main()
	for acronym in library:
		book = library[acronym]
		for slug in book:
			spell = book[slug]
			print(spell)


if __name__ == '__main__':
	main()
