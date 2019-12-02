# Naturally Capitalized Words
NATURAL_UPPERCASE = [
	r'(?<=\n)(\t|"|\(|\[)?\b\w',
	r'(?<=\n)- \b\w(?=.*\.)',
]

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

PREUPPER_ITALICS = [
	# Actions
	r'\b((?<!Weapon )Attack|Cast a Spell|Dash|Disengage|Dodge|Help|Hide|Ready|Search|Use an Object)\b(?=.+action)(?! [A-Z])',
	r'\b(Tiny|Small|Medium|Large|Huge|Gargantuan)\b',
]

ITALIC_PHRASES = [
	# r'\bdash\b',
	# r'\bdisengage\b',
	# r'\bdodge\b',

	# Actions
	# r'\b(Attack|Cast a Spell|Dash|Disengage|Dodge|Help|Hide|Ready|Search|Use an Object)(?=.+action)'
	# Sizes
	# r'\bTiny\b', 1.25 foot; 16 in a square
	# r'\bSmall\b', 2.5 feet; 4 in a square
	# r'\bMedium\b', 5 feet; 1 in a square
	# r'\bLarge\b', 10 feet; 4 squares
	# r'\bHuge\b', 20 feet; 16 squares
	# r'\bGargantuan\b',
	# r'\bTitanic\b',
]

DICE_PHRASES = [
	r'\d*d\d+( ?[\+–\-×\*÷\/] ?\d*d\d+)?',
	r'(?<= )[\+–\-×\*÷\/]\d+',
]

PERCENT_PHRASES = [
	r'\d+ percent'
]

'''
strength
dexterity
constitution
intelligence
wisdom
charisma
'''
