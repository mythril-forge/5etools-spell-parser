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

if __name__ == '__main__':
	print(f'getting data from {"".join([URL, SOURCE["PHB"]])}')

	XTRA_DATA = ''
	with open('spells_area.json', 'r') as file:
		XTRA_DATA = json.load(file)

	SOURCE_DATA = requests.get(f'{URL}{SOURCE["PHB"]}').json()

	for spell_data in SOURCE_DATA['spell']:
		Spell = ToolSpell(spell_data, XTRA_DATA)
		with open(Spell.path, 'w+') as file:
			file.write(Spell.markdown)
