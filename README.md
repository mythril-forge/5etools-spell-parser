# D&D Spell Parser
## Regex Keeper
```markdown
Letter
# Letter Letter
## Letter Letter
### Letter Letter
*Letter
**Letter
***Letter
> Letter
_Letter
__Letter
___Letter
- Letter
	Letter
	- Letter
		Letter
		- Letter
			Letter
possible text | Letter
possible text {@possible_text Letter Letter
(Letter
[Letter
{Letter
```

```python
# This picks up the all-important first-letter of a line.
'\b[a-z]'

# Sometimes a newline starts in parenthesis.
# Or asterisks. Hell, even underscores, or quotes maybe.
'[\(\[\{\*_"]*\b[a-z]'

# Newline words always start capitalized.
# Sometimes they have some tabs in there.
'(^|\n)(\t)*[\(\[\{\*_"]*\b[a-z]'

# Table items always start capitalized.
'\| [\(\[\{\*_"]*\b[a-z]'

# Block-quotes always start capitalized.
'> [\(\[\{\*_"]*\b[a-z]

```

```python
# get a whole line up to any capital letter
r'[\n^].*[A-Z]'

# get anything that isn't starting at a new line
rf'(?<![\n^]){{regex}}'

# get anything that does not have a hashtag at the start
# or even, tab, dash, asterisk, underscore, parenthesis...
rf'(?<!([\n^][\{\[\(\t*>_-])).*\n{{regex}}

# get anything that does not start with a tab character
rf(?<!([\n^]))
```
