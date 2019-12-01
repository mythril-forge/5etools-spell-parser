# Capitalized Words
CAPITAL_PHRASES = [
	# roll targets
	r'\bac\b',
	r'\b(spell save )?dc\b',
	r'\barmor class(es)?\b',
	r'\bdifficulty class(es)?\b',

	# ability scores
	r'\b((mental|physical|strength|dexterity|constitution|intelligence|wisdom|charisma) )?ability scores?\b',
	# ability checks
	r'\b((mental|physical|strength|dexterity|constitution|intelligence|wisdom|charisma|\}\)) )checks?\b',
	r'\b((mental|physical|strength|dexterity|constitution|intelligence|wisdom|charisma|\}\)) )?ability checks?\b',
	# saving throws
	r'\b((mental|physical|strength|dexterity|constitution|intelligence|wisdom|charisma|death) )?saving throws?\b',
	# abilities
	r'\b(strength|dexterity|constitution|intelligence|wisdom|charisma)\b',

	# attacks
	r'\b((ranged|melee) )?((spell|weapon) )attacks?\b',
	r'\b(ranged|melee) attacks?\b',

	# various rolls
	r'\b(attack|damage) rolls?\b',
	r'\battack and damage rolls?\b',

	# rare key game terms
	r'\bdamage (reduction|threshold)\b',

	# various races and creatures
	r'\bhumans?\b',
	r'\bunicorns?\b',
]

# Phrases that must be all-capitalized, like abbreviations
ALLCAP_PHRASES = [
	r'\bac\b',
	r'\bdc\b',
]


'''
strength
dexterity
constitution
intelligence
wisdom
charisma
'''
