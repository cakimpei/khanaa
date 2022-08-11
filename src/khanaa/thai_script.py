"""
This module stores Thai script information.

CONSONANTS

ฤ ฦ are traditionally considered as vowels,
but they're included here.

Thai consonants: กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤลฦวศษสหฬอฮ

By onset class
High: ขฃฉฐถผฝศษสห
Mid: กจฎฏดตบปอ
Low with high pair: คฅฆชซฌฑฒทธพฟภฮ
Low without high pair: งญณนมยรฤลฦวฬ

Consonants without coda sound: ฉผฝฤฦอ

CLUSTERS

บร, ฟร, ทร are used in loanwords and not conventional.
ผร (not included here) is rarely used for onomatopoeic effect.

VOWELS

All vowels here:
'อะ', 'อ', 'อา', 'อิ', 'อี', 'อุ', 'อู', 'อึ', 'อือ', 'อๅ', 'เอะ', 'เอ',
'แอะ', 'แอ', 'โอะ', 'โอ', 'เอาะ', 'ออ', 'เออะ', 'เออ',
'เอียะ', 'เอีย', 'เอือะ', 'เอือ', 'อัวะ', 'อัว',
'อัย', 'ใอ', 'ไอ', 'ไอย', 'อาย', 'เอา', 'อาว',
'อิย', 'อีย', 'อิว', 'อีว', 'อึย', 'อืย', 'อึว', 'อืว',
'อุย', 'อูย', 'อุว', 'อูว', 'เอ็ว', 'เอว', 'แอ็ย', 'แอย', 'แอ็ว', 'แอว',
'อย', 'โอย', 'โอว', 'อ็อย', 'ออย', 'อ็อว', 'ออว', 'เอ็ย', 'เอย', 'เอิว', 'เออว',
'เอียว', 'เอือย', 'เอือว', 'อวย', 'อรร', 'อำ', 'อาม', 'อํ'

Order: monothongs, diphthongs, +j and +w forms

Vowels that don't have +j or +w forms:
เอะ + ย, เอ + ย, โอะ + ว (อว?), เออะ + ว
เอียะ + ย, เอีย + ย, อัวะ + ว, อัว + ว (maybe more)

Some vowels might
- have more than one form
- have more than one coda form
- be without pair (ex. อๅ)

Ex. Short form of อาย can be ไอ or อัย. (It's ไอ here).

Vowels without coda form:
'เออะ', 'เอียะ', 'เอือะ', 'อัวะ', and all vowels with +j, +w, +m coda
เอิ็น เอี็ยน เอื็อน อ็วน?

Vowel form not in this:
ออ (with ร as coda) appearing as -+ (กร ศร)
อ็ (ก็)
เออ (with coda) appearing as เ-+อ (เทอม เทอญ)
"""

CONSONANTS = {
    'ก': {
        'class': 'mid',
        'pair': '',
        'coda_class': 'dead',
        'sound_onset': 'k',
        'sound_coda': 'k̚'
    },
    'ข': {
        'class': 'high',
        'pair': 'ค',
        'coda_class': 'dead',
        'sound_onset': 'kʰ',
        'sound_coda': 'k̚'
    },
    'ฃ': {
        'class': 'high',
        'pair': 'ฅ',
        'coda_class': 'dead',
        'sound_onset': 'kʰ',
        'sound_coda': 'k̚'
    },
    'ค': {
        'class': 'low_pair',
        'pair': 'ข',
        'coda_class': 'dead',
        'sound_onset': 'kʰ',
        'sound_coda': 'k̚'
    },
    'ฅ': {
        'class': 'low_pair',
        'pair': 'ฃ',
        'coda_class': 'dead',
        'sound_onset': 'kʰ',
        'sound_coda': 'k̚'
    },
    'ฆ': {
        'class': 'low_pair',
        'pair': 'ข',
        'coda_class': 'dead',
        'sound_onset': 'kʰ',
        'sound_coda': 'k̚'
    },
    'ง': {
        'class': 'low_single',
        'pair': '',
        'coda_class': 'alive',
        'sound_onset': 'ŋ',
        'sound_coda': 'ŋ'
    },
    'จ': {
        'class': 'mid',
        'pair': '',
        'coda_class': 'dead',
        'sound_onset': 't͡ɕ',
        'sound_coda': 't̚'
    },
    'ฉ': {
        'class': 'high',
        'pair': 'ช',
        'coda_class': '',
        'sound_onset': 't͡ɕʰ',
        'sound_coda': ''
    },
    'ช': {
        'class': 'low_pair',
        'pair': 'ฉ',
        'coda_class': 'dead',
        'sound_onset': 't͡ɕʰ',
        'sound_coda': 't̚'
    },
    'ซ': {
        'class': 'low_pair',
        'pair': 'ส',
        'coda_class': 'dead',
        'sound_onset': 's',
        'sound_coda': 't̚'
    },
    'ฌ': {
        'class': 'low_pair',
        'pair': 'ฉ',
        'coda_class': 'dead',
        'sound_onset': 't͡ɕʰ',
        'sound_coda': 't̚'
    },
    'ญ': {
        'class': 'low_single',
        'pair': '',
        'coda_class': 'alive',
        'sound_onset': 'j',
        'sound_coda': 'n'
    },
    'ฎ': {
        'class': 'mid',
        'pair': '',
        'coda_class': 'dead',
        'sound_onset': 'd',
        'sound_coda': 't̚'
    },
    'ฏ': {
        'class': 'mid',
        'pair': '',
        'coda_class': 'dead',
        'sound_onset': 't',
        'sound_coda': 't̚'
    },
    'ฐ': {
        'class': 'high',
        'pair': 'ฑ',
        'coda_class': 'dead',
        'sound_onset': 'tʰ',
        'sound_coda': 't̚'
    },
    'ฑ': {
        'class': 'low_pair',
        'pair': 'ฐ',
        'coda_class': 'dead',
        'sound_onset': 'tʰ',
        'sound_coda': 't̚'
    },
    'ฒ': {
        'class': 'low_pair',
        'pair': 'ฐ',
        'coda_class': 'dead',
        'sound_onset': 'tʰ',
        'sound_coda': 't̚'
    },
    'ณ': {
        'class': 'low_single',
        'pair': '',
        'coda_class': 'alive',
        'sound_onset': 'n',
        'sound_coda': 'n'
    },
    'ด': {
        'class': 'mid',
        'pair': '',
        'coda_class': 'dead',
        'sound_onset': 'd',
        'sound_coda': 't̚'
    },
    'ต': {
        'class': 'mid',
        'pair': '',
        'coda_class': 'dead',
        'sound_onset': 't',
        'sound_coda': 't̚'
    },
    'ถ': {
        'class': 'high',
        'pair': 'ท',
        'coda_class': 'dead',
        'sound_onset': 'tʰ',
        'sound_coda': 't̚'
    },
    'ท': {
        'class': 'low_pair',
        'pair': 'ถ',
        'coda_class': 'dead',
        'sound_onset': 'tʰ',
        'sound_coda': 't̚'
    },
    'ธ': {
        'class': 'low_pair',
        'pair': 'ถ',
        'coda_class': 'dead',
        'sound_onset': 'tʰ',
        'sound_coda': 't̚'
    },
    'น': {
        'class': 'low_single',
        'pair': '',
        'coda_class': 'alive',
        'sound_onset': 'n',
        'sound_coda': 'n'
    },
    'บ': {
        'class': 'mid',
        'pair': '',
        'coda_class': 'dead',
        'sound_onset': 'b',
        'sound_coda': 'p̚'
    },
    'ป': {
        'class': 'mid',
        'pair': '',
        'coda_class': 'dead',
        'sound_onset': 'p',
        'sound_coda': 'p̚'
    },
    'ผ': {
        'class': 'high',
        'pair': 'พ',
        'coda_class': 'dead',
        'sound_onset': 'pʰ',
        'sound_coda': ''
    },
    'ฝ': {
        'class': 'high',
        'pair': 'ฟ',
        'coda_class': '',
        'sound_onset': 'f',
        'sound_coda': ''
    },
    'พ': {
        'class': 'low_pair',
        'pair': 'ผ',
        'coda_class': 'dead',
        'sound_onset': 'pʰ',
        'sound_coda': 'p̚'
    },
    'ฟ': {
        'class': 'low_pair',
        'pair': 'ฝ',
        'coda_class': 'dead',
        'sound_onset': 'f',
        'sound_coda': 'p̚'
    },
    'ภ': {
        'class': 'low_pair',
        'pair': 'ผ',
        'coda_class': 'dead',
        'sound_onset': 'pʰ',
        'sound_coda': 'p̚'
    },
    'ม': {
        'class': 'low_single',
        'pair': '',
        'coda_class': 'alive',
        'sound_onset': 'm',
        'sound_coda': 'm'
    },
    'ย': {
        'class': 'low_single',
        'pair': '',
        'coda_class': 'alive',
        'sound_onset': 'j',
        'sound_coda': 'j'
    },
    'ร': {
        'class': 'low_single',
        'pair': '',
        'coda_class': 'alive',
        'sound_onset': 'r',
        'sound_coda': 'n'
    },
    'ฤ': {
        'class': 'low_single',
        'pair': '',
        'coda_class': '',
        'sound_onset': 'r',
        'sound_coda': ''
    },
    'ล': {
        'class': 'low_single',
        'pair': '',
        'coda_class': 'alive',
        'sound_onset': 'l',
        'sound_coda': 'n'
    },
    'ฦ': {
        'class': 'low_single',
        'pair': '',
        'coda_class': '',
        'sound_onset': 'l',
        'sound_coda': ''
    },
    'ว': {
        'class': 'low_single',
        'pair': '',
        'coda_class': 'alive',
        'sound_onset': 'w',
        'sound_coda': 'w'
    },
    'ศ': {
        'class': 'high',
        'pair': 'ซ',
        'coda_class': 'dead',
        'sound_onset': 's',
        'sound_coda': 't̚'
    },
    'ษ': {
        'class': 'high',
        'pair': 'ซ',
        'coda_class': 'dead',
        'sound_onset': 's',
        'sound_coda': 't̚'
    },
    'ส': {
        'class': 'high',
        'pair': 'ซ',
        'coda_class': 'dead',
        'sound_onset': 's',
        'sound_coda': 't̚'
    },
    'ห': {
        'class': 'high',
        'pair': 'ฮ',
        'coda_class': 'alive',
        'sound_onset': 'h',
        'sound_coda': 'h'
    },
    'ฬ': {
        'class': 'low_single',
        'pair': '',
        'coda_class': 'alive',
        'sound_onset': 'l',
        'sound_coda': 'n'
    },
    'อ': {
        'class': 'mid',
        'pair': '',
        'coda_class': '',
        'sound_onset': 'ʔ',
        'sound_coda': ''
    },
    'ฮ': {
        'class': 'low_pair',
        'pair': 'ห',
        'coda_class': 'alive',
        'sound_onset': 'h',
        'sound_coda': 'h'
    }
}

CLUSTERS = {
    'กร', 'กล', 'กว',
    'ขร', 'คร', 'ขล', 'คล', 'ขว', 'คว',
    'บร', 'บล',
    'ปร', 'ปล',
    'พร', 'ผล', 'พล',
    'ฟร', 'ฟล',
    'ตร',
    'ทร',
    'ดร'
}

FALSE_CLUSTERS = {
    'จร', 'ซร', 'ศร', 'สร'
}

VOWELS = {
    # MONOPHTHONGS
    'อะ': {
        'form_no_coda': '-+ะ',
        'form_with_coda': '-ั+',
        'length': 'short',
        'pair': 'อา',
        'sound_vowel': 'a',
        'sound_coda': ''
    },
    'อ': {
        'form_no_coda': '-+',
        'form_with_coda': '-+',
        'length': 'short',
        'pair': 'อา',
        'sound_vowel': 'a',
        'sound_coda': ''
    },
    'อา': {
        'form_no_coda': '-+า',
        'form_with_coda': '-+า',
        'length': 'long',
        'pair': 'อะ',
        'sound_vowel': 'a',
        'sound_coda': ''
    },
    'อิ': {
        'form_no_coda': '-ิ+',
        'form_with_coda': '-ิ+',
        'length': 'short',
        'pair': 'อี',
        'sound_vowel': 'i',
        'sound_coda': ''
    },
    'อี': {
        'form_no_coda': '-ี+',
        'form_with_coda': '-ี+',
        'length': 'long',
        'pair': 'อิ',
        'sound_vowel': 'i',
        'sound_coda': ''
    },
    'อุ': {
        'form_no_coda': '-ุ+',
        'form_with_coda': '-ุ+',
        'length': 'short',
        'pair': 'อู',
        'sound_vowel': 'u',
        'sound_coda': ''
    },
    'อู': {
        'form_no_coda': '-ู+',
        'form_with_coda': '-ู+',
        'length': 'long',
        'pair': 'อุ',
        'sound_vowel': 'u',
        'sound_coda': ''
    },
    'อึ': {
        'form_no_coda': '-ึ+',
        'form_with_coda': '-ึ+',
        'length': 'short',
        'pair': 'อือ',
        'sound_vowel': 'ɯ',
        'sound_coda': ''
    },
    'อือ': {
        'form_no_coda': '-ื+อ',
        'form_with_coda': '-ื+',
        'length': 'long',
        'pair': 'อึ',
        'sound_vowel': 'ɯ',
        'sound_coda': ''
    },
    'อๅ': {
        'form_no_coda': '-+ๅ',
        'form_with_coda': '-+ๅ',
        'length': 'long',
        'pair': '',
        'sound_vowel': 'ɯ',
        'sound_coda': ''
    },
    'เอะ': {
        'form_no_coda': 'เ-+ะ',
        'form_with_coda': 'เ-็+',
        'length': 'short',
        'pair': 'เอ',
        'sound_vowel': 'e',
        'sound_coda': ''
    },
    'เอ': {
        'form_no_coda': 'เ-+',
        'form_with_coda': 'เ-+',
        'length': 'long',
        'pair': 'เอะ',
        'sound_vowel': 'e',
        'sound_coda': ''
    },
    'แอะ': {
        'form_no_coda': 'แ-+ะ',
        'form_with_coda': 'แ-็+',
        'length': 'short',
        'pair': 'แอ',
        'sound_vowel': 'ɛ',
        'sound_coda': ''
    },
    'แอ': {
        'form_no_coda': 'แ-+',
        'form_with_coda': 'แ-+',
        'length': 'long',
        'pair': 'แอะ',
        'sound_vowel': 'ɛ',
        'sound_coda': ''
    },
    'โอะ': {
        'form_no_coda': 'โ-+ะ',
        'form_with_coda': '-+',
        'length': 'short',
        'pair': 'โอ',
        'sound_vowel': 'o',
        'sound_coda': ''
    },
    'โอ': {
        'form_no_coda': 'โ-+',
        'form_with_coda': 'โ-+',
        'length': 'long',
        'pair': 'โอะ',
        'sound_vowel': 'o',
        'sound_coda': ''
    },
    'เอาะ': {
        'form_no_coda': 'เ-+าะ',
        'form_with_coda': '-็+อ',
        'length': 'short',
        'pair': 'ออ',
        'sound_vowel': 'ɔ',
        'sound_coda': ''
    },
    'ออ': {
        'form_no_coda': '-+อ',
        'form_with_coda': '-+อ',
        'length': 'long',
        'pair': 'เอาะ',
        'sound_vowel': 'ɔ',
        'sound_coda': ''
    },
    'เออะ': {
        'form_no_coda': 'เ-+อะ',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'เออ',
        'sound_vowel': 'ɤ',
        'sound_coda': ''
    },
    'เออ': {
        'form_no_coda': 'เ-+อ',
        'form_with_coda': 'เ-ิ+',
        'length': 'long',
        'pair': 'เออะ',
        'sound_vowel': 'ɤ',
        'sound_coda': ''
    },

    # DIPHTHONGS
    'เอียะ': {
        'form_no_coda': 'เ-ี+ยะ',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'เอีย',
        'sound_vowel': 'ia',
        'sound_coda': ''
    },
    'เอีย': {
        'form_no_coda': 'เ-ี+ย',
        'form_with_coda': 'เ-ี+ย',
        'length': 'long',
        'pair': 'เอียะ',
        'sound_vowel': 'ia',
        'sound_coda': ''
    },
    'เอือะ': {
        'form_no_coda': 'เ-ื+อะ',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'เอือ',
        'sound_vowel': 'ɯa',
        'sound_coda': ''
    },
    'เอือ': {
        'form_no_coda': 'เ-ื+อ',
        'form_with_coda': 'เ-ื+อ',
        'length': 'long',
        'pair': 'เอือะ',
        'sound_vowel': 'ɯa',
        'sound_coda': ''
    },
    'อัวะ': {
        'form_no_coda': '-ั+วะ',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'อัว',
        'sound_vowel': 'ua',
        'sound_coda': ''
    },
    'อัว': {
        'form_no_coda': '-ั+ว',
        'form_with_coda': '-+ว',
        'length': 'long',
        'pair': 'อัวะ',
        'sound_vowel': 'ua',
        'sound_coda': ''
    },

    # PHONETIC DIPHTHONGS
    'อัย': {
        'form_no_coda': '-ั+ย',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'อาย',
        'sound_vowel': 'a',
        'sound_coda': 'j'
    },
    'ใอ': {
        'form_no_coda': 'ใ-+',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'อาย',
        'sound_vowel': 'a',
        'sound_coda': 'j'
    },
    'ไอ': {
        'form_no_coda': 'ไ-+',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'อาย',
        'sound_vowel': 'a',
        'sound_coda': 'j'
    },
    'ไอย': {
        'form_no_coda': 'ไ-+ย',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'อาย',
        'sound_vowel': 'a',
        'sound_coda': 'j'
    },
    'อาย': {
        'form_no_coda': '-+าย',
        'form_with_coda': '',
        'length': 'long',
        'pair': 'ไอ',
        'sound_vowel': 'a',
        'sound_coda': 'j'
    },
    'เอา': {
        'form_no_coda': 'เ-+า',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'อาว',
        'sound_vowel': 'a',
        'sound_coda': 'w'
    },
    'อาว': {
        'form_no_coda': '-+าว',
        'form_with_coda': '',
        'length': 'long',
        'pair': 'เอา',
        'sound_vowel': 'a',
        'sound_coda': 'w'
    },
    'อิย': {
        'form_no_coda': '-ิ+ย',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'อีย',
        'sound_vowel': 'i',
        'sound_coda': 'j'
    },
    'อีย': {
        'form_no_coda': '-ี+ย',
        'form_with_coda': '',
        'length': 'long',
        'pair': 'อิย',
        'sound_vowel': 'i',
        'sound_coda': 'j'
    },
    'อิว': {
        'form_no_coda': '-ิ+ว',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'อีว',
        'sound_vowel': 'i',
        'sound_coda': 'w'
    },
    'อีว': {
        'form_no_coda': '-ี+ว',
        'form_with_coda': '',
        'length': 'long',
        'pair': 'อิว',
        'sound_vowel': 'i',
        'sound_coda': 'w'
    },
    'อึย': {
        'form_no_coda': '-ึ+ย',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'อืย',
        'sound_vowel': 'ɯ',
        'sound_coda': 'j'
    },
    'อืย': {
        'form_no_coda': '-ื+ย',
        'form_with_coda': '',
        'length': 'long',
        'pair': 'อึย',
        'sound_vowel': 'ɯ',
        'sound_coda': 'j'
    },
    'อึว': {
        'form_no_coda': '-ึ+ว',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'อืว',
        'sound_vowel': 'ɯ',
        'sound_coda': 'w'
    },
    'อืว': {
        'form_no_coda': '-ื+ว',
        'form_with_coda': '',
        'length': 'long',
        'pair': 'อึว',
        'sound_vowel': 'ɯ',
        'sound_coda': 'w'
    },
    'อุย': {
        'form_no_coda': '-ุ+ย',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'อูย',
        'sound_vowel': 'u',
        'sound_coda': 'j'
    },
    'อูย': {
        'form_no_coda': '-ู+ย',
        'form_with_coda': '',
        'length': 'long',
        'pair': 'อุย',
        'sound_vowel': 'u',
        'sound_coda': 'j'
    },
    'อุว': {
        'form_no_coda': '-ุ+ว',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'อูว',
        'sound_vowel': 'u',
        'sound_coda': 'w'
    },
    'อูว': {
        'form_no_coda': '-ู+ว',
        'form_with_coda': '',
        'length': 'long',
        'pair': 'อูว',
        'sound_vowel': 'u',
        'sound_coda': 'w'
    },
    'เอ็ว': {
        'form_no_coda': 'เ-็+ว',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'เอว',
        'sound_vowel': 'e',
        'sound_coda': 'w'
    },
    'เอว': {
        'form_no_coda': 'เ-+ว',
        'form_with_coda': '',
        'length': 'long',
        'pair': 'เอ็ว',
        'sound_vowel': 'e',
        'sound_coda': 'w'
    },
    'แอ็ย': {
        'form_no_coda': 'แ-็+ย',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'แอย',
        'sound_vowel': 'ɛ',
        'sound_coda': 'j'
    },
    'แอย': {
        'form_no_coda': 'แ-+ย',
        'form_with_coda': '',
        'length': 'long',
        'pair': 'แอ็ย',
        'sound_vowel': 'ɛ',
        'sound_coda': 'j'
    },
    'แอ็ว': {
        'form_no_coda': 'แ-็+ว',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'แอว',
        'sound_vowel': 'ɛ',
        'sound_coda': 'w'
    },
    'แอว': {
        'form_no_coda': 'แ-+ว',
        'form_with_coda': '',
        'length': 'long',
        'pair': 'แอ็ว',
        'sound_vowel': 'ɛ',
        'sound_coda': 'w'
    },
    'อย': {
        'form_no_coda': '-+ย',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'โอย',
        'sound_vowel': 'o',
        'sound_coda': 'j'
    },
    'โอย': {
        'form_no_coda': 'โ-+ย',
        'form_with_coda': '',
        'length': 'long',
        'pair': 'อย',
        'sound_vowel': 'o',
        'sound_coda': 'j'
    },
    'โอว': {
        'form_no_coda': 'โ-+ว',
        'form_with_coda': '',
        'length': 'long',
        'pair': '',
        'sound_vowel': 'o',
        'sound_coda': 'w'
    },
    'อ็อย': {
        'form_no_coda': '-็+อย',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'ออย',
        'sound_vowel': 'ɔ',
        'sound_coda': 'j'
    },
    'ออย': {
        'form_no_coda': '-+อย',
        'form_with_coda': '',
        'length': 'long',
        'pair': 'อ็อย',
        'sound_vowel': 'ɔ',
        'sound_coda': 'j'
    },
    'อ็อว': {
        'form_no_coda': '-็+อว',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'ออว',
        'sound_vowel': 'ɔ',
        'sound_coda': 'w'
    },
    'ออว': {
        'form_no_coda': '-+อว',
        'form_with_coda': '',
        'length': 'long',
        'pair': 'อ็อว',
        'sound_vowel': 'ɔ',
        'sound_coda': 'w'
    },
    'เอ็ย': {
        'form_no_coda': 'เ-็+ย',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'เอย',
        'sound_vowel': 'ɤ',
        'sound_coda': 'j'
    },
    'เอย': {
        'form_no_coda': 'เ-+ย',
        'form_with_coda': '',
        'length': 'long',
        'pair': 'เอ็ย',
        'sound_vowel': 'ɤ',
        'sound_coda': 'j'
    },
    'เอิว': {
        'form_no_coda': 'เ-ิ+ว',
        'form_with_coda': '',
        'length': 'long',
        'pair': '',
        'sound_vowel': 'ɤ',
        'sound_coda': 'w'
    },
    'เออว': {
        'form_no_coda': 'เ-+อว',
        'form_with_coda': '',
        'length': 'long',
        'pair': '',
        'sound_vowel': 'ɤ',
        'sound_coda': 'w'
    },
    'เอียว': {
        'form_no_coda': 'เ-ี+ยว',
        'form_with_coda': '',
        'length': 'long',
        'pair': '',
        'sound_vowel': 'ia',
        'sound_coda': 'w'
    },
    'เอือย': {
        'form_no_coda': 'เ-ื+อย',
        'form_with_coda': '',
        'length': 'long',
        'pair': '',
        'sound_vowel': 'ɯa',
        'sound_coda': 'j'
    },
    'เอือว': {
        'form_no_coda': 'เ-ื+อว',
        'form_with_coda': '',
        'length': 'long',
        'pair': '',
        'sound_vowel': 'ɯa',
        'sound_coda': 'w'
    },
    'อวย': {
        'form_no_coda': '-+วย',
        'form_with_coda': '',
        'length': 'long',
        'pair': '',
        'sound_vowel': 'ua',
        'sound_coda': 'j'
    },

    # EXTRAS
    'อรร': {
        'form_no_coda': '-+รร',
        'form_with_coda': '-+รร',
        'length': 'short',
        'pair': '',
        'sound_vowel': 'a',
        'sound_coda': '' # or n
    },    
    'อำ': {
        'form_no_coda': '-+ำ',
        'form_with_coda': '',
        'length': 'short',
        'pair': 'อาม',
        'sound_vowel': 'a',
        'sound_coda': 'm'
    },
    'อาม': {
        'form_no_coda': '-+าม',
        'form_with_coda': '',
        'length': 'long',
        'pair': 'อำ',
        'sound_vowel': 'a',
        'sound_coda': 'm'
    },
    'อํ': {
        'form_no_coda': '-ํ+',
        'form_with_coda': '',
        'length': 'short',
        'pair': '',
        'sound_vowel': 'a',
        'sound_coda': 'm' # or ŋ
    }
}

TONES = {
    0: {
        'mid alive': ['', ''],
        'mid dead': ['', ''], # cannot
        'high alive': ['pair', ''],
        'high short dead': ['', ''], # cannot
        'high long dead': ['', ''], # cannot
        'low alive': ['', ''],
        'low short dead': ['', ''], # cannot
        'low long dead': ['', ''] # cannot
    },
    1: {
        'mid alive': ['', 'mai_eek'],
        'mid dead': ['', ''],
        'high alive': ['', 'mai_eek'],
        'high short dead': ['', ''],
        'high long dead': ['', ''],
        'low alive': ['pair', 'mai_eek'],
        'low short dead': ['pair', ''],
        'low long dead': ['pair', '']
    },
    2: {
        'mid alive': ['', 'mai_thoo'],
        'mid dead': ['', 'mai_thoo'],
        'high alive': ['', 'mai_thoo'],
        'high short dead': ['', 'mai_thoo'],
        'high long dead': ['', 'mai_thoo'],
        'low alive': ['', 'mai_eek'],
        'low short dead': ['', 'mai_eek'],
        'low long dead': ['', '']
    },
    3: {
        'mid alive': ['', 'mai_trii'],
        'mid dead': ['', 'mai_trii'],
        'high alive': ['pair', 'mai_thoo'],
        'high short dead': ['pair', ''],
        'high long dead': ['pair', 'mai_thoo'],
        'low alive': ['', 'mai_thoo'],
        'low short dead': ['', ''],
        'low long dead': ['', 'mai_thoo']
    },
    4: {
        'mid alive': ['', 'mai_jattawaa'],
        'mid dead': ['', 'mai_jattawaa'], # can but no usage
        'high alive': ['', ''],
        'high short dead': ['pair', 'mai_jattawaa'], # can but no usage
        'high long dead': ['pair', 'mai_jattawaa'], # can but no usage
        'low alive': ['pair', ''],
        'low short dead': ['', 'mai_jattawaa'], # can but no usage
        'low long dead': ['', 'mai_jattawaa'] # can but no usage
    }
}

LOW_SINGLE_ALT = ['pair', 'mai_thoo'] # for falling tone เสียงโท

TONE_NOT_AVAILABLE = {
    0: {
        'mid dead': ['', ''], # cannot
        'high short dead': ['', ''], # cannot
        'high long dead': ['', ''], # cannot
        'low short dead': ['', ''], # cannot
        'low long dead': ['', ''] # cannot
    }
}

TONE_MARKERS = {
    'mai_eek': u'\u0e48',
    'mai_thoo': u'\u0e49',
    'mai_trii': u'\u0e4a',
    'mai_jattawaa': u'\u0e4b'
}

DIACRITICS = {
    'mai_taikhuu': u'\u0e47',
    'kaaran': u'\u0e4c',
    'phinthu': u'\u0e3a',
    'yaamakkaan': u'\u0e4e'
}

TONE_IPA = {
    0: '˧',
    1: '˨˩',
    2: '˥˩',
    3: '˦˥',
    4: '˩˩˦',
}