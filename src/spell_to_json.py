class SpellToJson:
	def __init__(self, Spell):
		super().__init__()
		self.spell = Spell
		# initialize empty object
		Spell = self.spell
		SpellData = {}
		# these data are never empty
		SpellData['slug'] = Spell.slug
		SpellData['name'] = Spell.name
		SpellData['homebrew'] = Spell.homebrew
		SpellData['level'] = Spell.level
		SpellData['school'] = Spell.school
		SpellData['cast_time'] = Spell.cast_time
		SpellData['duration'] = Spell.duration
		SpellData['range'] = Spell.range
		SpellData['area'] = Spell.area
		SpellData['instances'] = Spell.instances
		SpellData['tags'] = Spell.tags
		SpellData['components'] = Spell.components
		SpellData['description'] = Spell.description
		SpellData['access'] = Spell.access
		SpellData['citations'] = Spell.citations
		self.json = SpellData
