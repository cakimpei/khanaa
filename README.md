# khanaa

Khanaa is a tool to make spelling Thai more convenient.

## Installation

For Python >=3.7

```
pip install khanaa
```

## Usage

```python
from khanaa import SpellWord, find_letter_list

basic_example = {
    'onset': 'ก', # can be more than one (required)
    'vowel': 'อา', # include vowel with ย, ว coda ex. เอียว (required)
    'silent_before': '', # silent character before coda
    'coda': '', # don't put ย, ว here (put them together with vowel)
    'silent_after': '', # silent character after coda
    'tone': -1  # -1 not specific, 0 สามัญ, 1 เอก, 2 โท, 3 ตรี, 4 จัตวา
    }
spell = SpellWord()
spell.spell_out(**basic_example)
# => 'กา'

# five tones at once
spell.all_tone(**basic_example)
# => ['กา', 'ก่า', 'ก้า', 'ก๊า', 'ก๋า']

# ย, ว coda
spell.spell_out(onset='ล', vowel='อาย')
# => 'ลาย'

# onset cluster
spell.spell_out(onset='กล', vowel='อะ', coda='น', tone=1)
# => 'กลั่น'

spell.spell_out(onset='สต', vowel='เอะ', coda='ก', tone=3)
# => 'สเต๊ก'

# silent character
spell.spell_out(onset='ฌ', vowel='อิ', coda='น', silent_after='สก')
# => 'ฌินสก์'

# can be customised (ex. add phinthu)
phinthu_spell = SpellWord(onset_style='phinthu')
phinthu_spell.all_tone(onset='ซย', vowel='อา')
# => ['ซฺยา', 'สฺย่า', 'ซฺย่า', 'ซฺย้า', 'สฺยา']

# use short length for vowel
short_spell = SpellWord(vowel_length='short')
short_spell.spell_out(onset='ป', vowel='อาย')
# => 'ไป'

# find all available consonants, vowels and true clusters in khanaa
find_letter_list()
```

## License

MIT