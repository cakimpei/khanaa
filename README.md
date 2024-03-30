# khanaa

Khanaa is a tool to make spelling Thai more convenient.

## Installation

For Python >=3.7

```
pip install khanaa
```

## Usage

### Spelling

```python
from khanaa import Kham

basic_example = {
    'onset': 'ก', # can be more than one (required)
    'vowel': 'อา', # include vowel with ย, ว coda ex. เอียว (required)
    'silent_before': '', # silent character before coda
    'coda': '', # don't put ย, ว here (put them together with vowel)
    'silent_after': '', # silent character after coda
    'tone': -1  # -1 not specific, 0 สามัญ, 1 เอก, 2 โท, 3 ตรี, 4 จัตวา
    }
kaa = Kham(**basic_example)
kaa.form
# => 'กา'

# ย, ว coda
lai = Kham(onset='ล', vowel='อาย')
lai.form
# => 'ลาย'

# onset cluster
steak = Kham(onset='สต', vowel='เอะ', coda='ก', tone=3)
steak.form
# => 'สเต๊ก'

# silent character
shin = Kham(onset='ฌ', vowel='อิ', coda='น', silent_after='สก')
shin.form
# => 'ฌินสก์'

# can be customised (ex. add phinthu)
sia = Kham(onset='ซย', vowel='อา', onset_style='phinthu')
sia.all_tone()
# => ['ซฺยา', 'สฺย่า', 'ซฺย่า', 'ซฺย้า', 'สฺยา']

# use short length for vowel
pai = Kham(onset='ป', vowel='อาย', vowel_length='short')
pai.form
# => 'ไป'
```

`SpellWord` was deprecated but not removed.

### Getting information

```python
from khanaa import Kham

kwang = Kham(onset='กว', vowel='อา', coda='ง', tone=2)
kwang.form
# => 'กว้าง'

# get main onset to derive the tone from
kwang.onset_main
# => 'ก'

# get onset class
kwang.onset_class
# => 'mid'

# get vowel length
kwang.vowel_length
# => 'long'

# get coda class
kwang.coda_class
# => 'alive'

# is it checked syllable? (คำตายหรือเปล่า?)
kwang.is_checked
# => False

# get realized tone
# (different from the input if the input is -1 or not possible)
kwang.tone_realized
# => 2

# is it using ห นำ?
kwang.use_leading_h
# => False

# has it changed to its pair consonant to convey the tone?
kwang.use_pair_onset
# => False

# get naive, rule-based IPA
kwang.ipa()
# => 'k w aː ŋ ˥˩'

# get everything
kwang.data
""" =>
{'all_tone': ['กวาง', 'กว่าง', 'กว้าง', 'กว๊าง', 'กว๋าง'],
 'coda': 'ง',
 'coda_class': 'alive',
 'form': 'กว้าง',
 'homophone': ['กว้าง'],
 'ipa': 'k w aː ŋ ˥˩',
 'is_checked': False,
 'is_donee_end': False,
 'is_donor_end': True,
 'is_donor_start': True,
 'is_possible_tone': True,
 'onset': 'กว',
 'onset_class': 'mid',
 'onset_index': -2,
 'onset_main': 'ก',
 'silent_after': '',
 'silent_before': '',
 'tone': 2,
 'tone_mark': '้',
 'tone_realized': 2,
 'use_leading_h': False,
 'use_pair_onset': False,
 'vowel': 'อา',
 'vowel_length': 'long'}
"""
```

### Ambiguity

As Thai orthography can be ambiguous, we can use these methods to detect if the spelled word's boundary is ambiguous (so that we can do something such as putting dash between ambiguous syllables to clarify the pronunciation).

```python
from khanaa import Kham

kwang = Kham(onset='กว', vowel='อา', coda='ง', tone=2)
kwang.form
# => 'กว้าง'

# Check if onset of the following word can be interpreted
# as this word's coda.
# ex. ตา will return true as ตา + กลม can be read either as
# ตา-กลม or ตาก-ลม
kwang.is_donee_end()
# => False

# Check if coda of this word can be interpreted as the
# following word onset.
# ex. ตาก will return true as ตาก + ลม can be read either as
# ตา-กลม or ตาก-ลม
kwang.is_donor_end()
# => True

# Check if onset of this word can be interpreted as coda
# of the preceding word.
# ex. กลม will return true as ตา + กลม can be read either as
# ตา-กลม or ตาก-ลม
kwang.is_donor_start()
# => True
```

In other words, if a word that returns true on `is_donee_end()` is followed by a word that returns true on `is_donor_start()`, there will be ambiguity (in theory), for example, ตา and กลม.

If a word that returns true on `is_donor_end()` is followed by any word, there will be possible ambiguity.

### Homophone

```python
from khanaa import Kham
khuu = Kham(onset='ค', vowel='อู', tone=2)
khuu.form
# => 'คู่'

khuu.homophone()
# => ['ขู้', 'ฃู้', 'คู่', 'ฅู่', 'ฆู่']
```

### Others

Find all available consonants, vowels and true clusters in khanaa

```python
from khanaa import find_letter_list

find_letter_list()
```

A experimental, basic method to turn text into Kham

```python
from khanaa import Kham, spelling_decompose

sd = spelling_decompose("เขียน")
# the result can be None if the input cannot be parsed
sd
""" =>
{'data': {'coda': 'น',
          'onset': 'ข',
          'silent_after': '',
          'silent_before': '',
          'tone': 4,
          'vowel': 'เอีย'},
 'detail': {'leading_h': False,
            'onset_index': -1,
            'onset_main': 'ข',
            'tone_mark': '',
            'vowel_form': 'เ-ี+ย'},
 'pref': {}}
"""

khian = Kham(**sd['data'])
khian.form
# => 'เขียน'

khian.ipa()
# => 'kʰ iaː n ˩˩˦'
```

## License

MIT