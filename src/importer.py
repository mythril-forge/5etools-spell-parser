import json
import requests
from spell_from_tool import ToolSpell

URL='https://raw.githubusercontent.com/TheGiddyLimit/TheGiddyLimit.github.io/master/data/spells/'
SOURCE = {
	"AI": "spells-ai.json",
	"GGR": "spells-ggr.json",
	"LLK": "spells-llk.json",
	"PHB": "spells-phb.json",
	"SCAG": "spells-scag.json",
	"Stream": "spells-stream.json",
	"UAArtificerRevisited": "spells-ua-ar.json",
	"UAModernMagic": "spells-ua-mm.json",
	"UAStarterSpells": "spells-ua-ss.json",
	"UAThatOldBlackMagic": "spells-ua-tobm.json",
	"XGE": "spells-xge.json"
}

def parse_book(book_abbr, DATA_EXTRA):
	book_sfx = SOURCE[book_abbr]
	book_src = ''.join([URL,book_sfx])
	print(f'getting data from\n{book_src}\n...')
	DATA_PRIME = requests.get(f'{book_src}').json()

	for spell_data in DATA_PRIME['spell']:
		# extra_data = DATA_EXTRA[spell_data['name']]
		# print(extra_data)
		Spell = ToolSpell(spell_data, DATA_EXTRA, book_abbr)
		with open(Spell.path, 'w+') as file:
			file.write(Spell.markdown)

if __name__ == '__main__':
	DATA_EXTRA = ''
	with open('spells_area.json', 'r') as file:
		DATA_EXTRA = json.load(file)
	
	for book_abbr in SOURCE:
		parse_book(book_abbr, DATA_EXTRA)
