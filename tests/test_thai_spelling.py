import unittest
from khanaa import SpellWord

GENERAL = [
    ({'onset': 'ส', 'vowel': 'เอีย', 'coda': 'ง', 'tone': -1},
    'เสียง'),
    ({'onset': 'ต', 'vowel': 'อะ', 'coda': 'ง', 'tone': 2},
    'ตั้ง'),
    ({'onset': 'ย', 'vowel': 'อะ', 'coda': 'ก', 'silent_after': 'ษ'},
    'ยักษ์'),
    ({'onset': 'บ', 'vowel': 'เออ', 'silent_before': 'ร', 'coda': 'น'},
    'เบิร์น'),
    ({'onset': 'พฤ', 'vowel': 'อ', 'coda': 'ก', 'silent_after': 'ษ'},
    'พฤกษ์'),
    ({'onset': 'ม', 'vowel': 'อิ', 'coda': 'น', 'silent_after': 'สก'},
    'มินสก์'),
    ({'onset': 'สก', 'vowel': 'เอะ', 'coda': 'ต'},
    'สเก็ต'),
    ({'onset': 'คว', 'vowel': 'เอ', 'coda': 'น'},
    'เควน'),
    ({'onset': 'สตร', 'vowel': 'เอ', 'coda': 'ส'},
    'สเตรส')
]

ONSET_TONE = [
    # alive mid, high, paired low, single low onsets
    ({'onset': 'ก', 'vowel': 'อา'},
    ['กา', 'ก่า', 'ก้า', 'ก๊า', 'ก๋า']),
    ({'onset': 'ข', 'vowel': 'อา'},
    ['คา', 'ข่า', 'ข้า', 'ค้า', 'ขา']),
    ({'onset': 'ค', 'vowel': 'อา'},
    ['คา', 'ข่า', 'ค่า', 'ค้า', 'ขา']),
    ({'onset': 'ง', 'vowel': 'อา'},
    ['งา', 'หง่า', 'ง่า', 'ง้า', 'หงา']),
    # dead mid, high, paired low, single low onsets (long)
    ({'onset': 'ก', 'vowel': 'อา', 'coda': 'บ'},
    ['กาบ', 'กาบ', 'ก้าบ', 'ก๊าบ', 'กาบ']),
    ({'onset': 'ข', 'vowel': 'อา', 'coda': 'บ'},
    ['ขาบ', 'ขาบ', 'ข้าบ', 'ค้าบ', 'ขาบ']),
    ({'onset': 'ค', 'vowel': 'อา', 'coda': 'บ'},
    ['คาบ', 'ขาบ', 'คาบ', 'ค้าบ', 'คาบ']),
    ({'onset': 'ง', 'vowel': 'อา', 'coda': 'บ'},
    ['งาบ', 'หงาบ', 'งาบ', 'ง้าบ', 'งาบ']),
    # dead mid, high, paired low, single low onsets (short)
    ({'onset': 'ก', 'vowel': 'อะ', 'coda': 'บ'},
    ['กับ', 'กับ', 'กั้บ', 'กั๊บ', 'กับ']),
    ({'onset': 'ข', 'vowel': 'อะ', 'coda': 'บ'},
    ['ขับ', 'ขับ', 'ขั้บ', 'คับ', 'ขับ']),
    ({'onset': 'ค', 'vowel': 'อะ', 'coda': 'บ'},
    ['คับ', 'ขับ', 'คั่บ', 'คับ', 'คับ']),
    ({'onset': 'ง', 'vowel': 'อะ', 'coda': 'บ'},
    ['งับ', 'หงับ', 'งั่บ', 'งับ', 'งับ'])]

ONSET_CLUSTER = [
    # mid & single low
    ({'onset': 'กว', 'vowel': 'อา'},
    ['กวา', 'กว่า', 'กว้า', 'กว๊า', 'กว๋า']),
    # pair low & single low
    ({'onset': 'ซย', 'vowel': 'อา'},
    ['ซยา', 'สย่า', 'ซย่า', 'ซย้า', 'สยา']),
    # high & high
    ({'onset': 'ผส', 'vowel': 'โอะ', 'coda': 'ม'},
    ['ผซม', 'ผส่ม', 'ผส้ม', 'ผซ้ม', 'ผสม']),
    # single low & single low
    ({'onset': 'ลว', 'vowel': 'อี'},
    ['ลวี', 'ลหวี่', 'ลวี่', 'ลวี้', 'ลหวี']),
    # three consonants
    ({'onset': 'สตร', 'vowel': 'อา'},
    ['สตรา', 'สตร่า', 'สตร้า', 'สตร๊า', 'สตร๋า'])
]

SETTING_STYLE = [
    ({'onset_style': 'kaaran'},
    {'onset': 'ทซ', 'vowel': 'อุ'},
    'ท์ซุ'),
    ({'onset_style': 'phinthu', 'silent_before_style': 'phinthu',
    'coda_style': 'phinthu', 'silent_after_style': 'phinthu'},
    {'onset': 'สว', 'vowel': 'เออ', 'silent_before': 'ร',
    'coda': 'ล', 'silent_after': 'ส'},
    'สฺเวิรฺลฺสฺ'),
    ({'onset_style': 'phinthu'},
    {'onset': 'ยว', 'vowel': 'อิ', 'coda': 'น', 'tone': 4},
    'ยฺหวิน'),
    ({'onset_style': 'yaamakkaan', 'silent_before_style': 'yaamakkaan',
    'coda_style': 'yaamakkaan', 'silent_after_style': 'yaamakkaan'},
    {'onset': 'สว', 'vowel': 'เออ', 'silent_before': 'ร',
    'coda': 'ล', 'silent_after': 'ส'},
    'ส๎เวิร๎ล๎ส๎'),
    ({'silent_before_style': 'plain',
    'silent_after_style': 'plain'},
    {'onset': 'สว', 'vowel': 'เออ', 'silent_before': 'ร',
    'coda': 'ล', 'silent_after': 'ส'},
    'สเวิรลส'),
    ({'silent_before_style': 'hide',
    'silent_after_style': 'hide'},
    {'onset': 'สว', 'vowel': 'เออ', 'silent_before': 'ร',
    'coda': 'ล', 'silent_after': 'ส'},
    'สเวิล'),
    ({'vowel_length': 'short'},
    {'onset': 'ม', 'vowel': 'อา', 'coda': 'น'},
    'มัน')]

SETTING_FORM = [
    ({'vowel_no_coda': 'pair'},
    {'onset': 'อ', 'vowel': 'เอียะ', 'coda': 'น'},
    'เอียน'),
    ({'vowel_no_coda': 'silent_after'},
    {'onset': 'อ', 'vowel': 'เอียะ', 'coda': 'น'},
    'เอียะน์'),
    ({'vowel_coda_form': {'เออ': 'เ-ิ+'}},
    {'onset': 'น', 'vowel': 'เออ', 'coda': 'ส'},
    'เนิส'),
    ({'vowel_coda_form': {'เออ': 'เ-+อ'}},
    {'onset': 'น', 'vowel': 'เออ', 'coda': 'ส'},
    'เนอส'),
    ({'vowel_length': 'long'},
    {'onset': 'ม', 'vowel': 'อะ', 'coda': 'น'},
    'มาน'),
    ({'vowel_length': 'short', 'vowel_pair_form': {'อาย': 'อัย'}},
    {'onset': 'อ', 'vowel': 'อาย'},
    'อัย'),
    ({'vowel_length': 'short', 'vowel_pair_form': {'อาย': 'ไอ'}},
    {'onset': 'อ', 'vowel': 'อาย'},
    'ไอ')
]

SETTING_PLACING = [
    ({'clear_vowel_onset': 'not_true_cluster'},
    {'onset': 'คว', 'vowel': 'เอ'},
    'เคว'),
    ({'clear_vowel_onset': 'all'},
    {'onset': 'คว', 'vowel': 'เอ'},
    'คเว'),
    ({'clear_vowel_onset': 'all', 'clear_vowel_tone_mark': False},
    {'onset': 'คว', 'vowel': 'เอ', 'tone': 2},
    'เคว่'),
    ({'clear_vowel_onset': 'all', 'clear_vowel_tone_mark': True},
    {'onset': 'คว', 'vowel': 'เอ', 'tone': 2},
    'คเว่')
]

SETTING_LS = [
    ({'obvious_low_singles': False},
    {'onset': 'ลว', 'vowel': 'อี'},
    ['ลวี', 'หลวี่', 'ลวี่', 'ลวี้', 'หลวี']),
    ({'obvious_low_singles': True},
    {'onset': 'ลว', 'vowel': 'อี'},
    ['ลวี', 'ลหวี่', 'ลวี่', 'ลวี้', 'ลหวี'])
]

SETTING_HLS = [
    ({'obvious_h_low_single': False},
    {'onset': 'ฮว', 'vowel': 'เอีย', 'coda': 'น'},
    ['ฮเวียน', 'เหวี่ยน', 'เฮวี่ยน', 'เฮวี้ยน', 'หเวียน']),
    ({'obvious_h_low_single': True},
    {'onset': 'ฮว', 'vowel': 'เอีย', 'coda': 'น'},
    ['ฮเวียน', 'ฮเหวี่ยน', 'เฮวี่ยน', 'เฮวี้ยน', 'ฮเหวียน'])
]

class TestSpellWord(unittest.TestCase):

    def test_general(self):
        spell = SpellWord()
        for case in GENERAL:
            self.assertEqual(spell.spell_out(**case[0]), case[1])

    def test_onset_tone(self):
        spell = SpellWord()
        for case in ONSET_TONE:
            self.assertEqual(spell.all_tone(**case[0]), case[1])

    def test_onset_cluster(self):
        spell = SpellWord()
        for case in ONSET_CLUSTER:
            self.assertEqual(spell.all_tone(**case[0]), case[1])

    def test_setting_style(self):
        for case in SETTING_STYLE:
            spell = SpellWord(**case[0])
            self.assertEqual(spell.spell_out(**case[1]), case[2])

    def test_setting_form(self):
        for case in SETTING_FORM:
            spell = SpellWord(**case[0])
            self.assertEqual(spell.spell_out(**case[1]), case[2])

    def test_setting_placing(self):
        for case in SETTING_PLACING:
            spell = SpellWord(**case[0])
            self.assertEqual(spell.spell_out(**case[1]), case[2])

    def test_setting_ls(self):
        for case in SETTING_LS:
            spell = SpellWord(**case[0])
            self.assertEqual(spell.all_tone(**case[1]), case[2])

    def test_setting_ls(self):
        for case in SETTING_HLS:
            spell = SpellWord(**case[0])
            self.assertEqual(spell.all_tone(**case[1]), case[2])

if __name__ == '__main__':
    unittest.main()