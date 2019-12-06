# Capitalized Words
CAPITAL_PHRASES = [
	# roll targets
	r'\bac\b',
	r'\b(spell save )?dc\b',
	r'\barmor class(es)?\b',
	r'\bdifficulty class(es)?\b',

	# ability modifiers
	r'\b(spellcasting|attack|strength|dexterity|constitution|intelligence|wisdom|charisma) modifiers?\b',
	r'\b((spellcasting|attack|strength|dexterity|constitution|intelligence|wisdom|charisma) )?ability modifiers?\b',
	# ability scores
	r'\b(mental|physical|strength|dexterity|constitution|intelligence|wisdom|charisma) scores?\b',
	r'\b((mental|physical|strength|dexterity|constitution|intelligence|wisdom|charisma) )?ability scores?\b',
	# ability checks
	r'\b(mental|physical|strength|dexterity|constitution|intelligence|wisdom|charisma|\}\)) checks?\b',
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
	r'\bdm\b'
]

BOLD_PHRASES = [
	r'\bblinded\b',
	r'\bcharmed\b',
	r'\bdeafened\b',
	r'\bfrightened\b',
	r'\bgrappled\b',
	r'\bincapacitated\b',
	r'\binsane\b',
	r'\binvisible\b',
	r'\bparalyzed\b',
	r'\bpetrified\b',
	r'\bpoisoned\b',
	r'\bprone\b',
	r'\brestrained\b',
	r'\bstunned\b',
	r'\bunconscious\b',
	r'\bconcentration\b',
	r'\bexhaust(ed|ion)\b',
	r'\bfatigued?\b',
]

DICE_PHRASES = [
	r'\d*d\d+( ?[\+–\-×\*÷\/] ?\d*d\d+)?',
	r'(?<!(\w|\+|–|\-|×|\*|÷|\/))[\+–\-×\*÷\/]\d+',
]

PERCENT_PHRASES = [
	r'\d+ percent'
]
