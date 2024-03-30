import unittest
from khanaa import Kham

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
    ['', 'กาบ', 'ก้าบ', 'ก๊าบ', 'ก๋าบ']),
    ({'onset': 'ข', 'vowel': 'อา', 'coda': 'บ'},
    ['', 'ขาบ', 'ข้าบ', 'ค้าบ', 'ค๋าบ']),
    ({'onset': 'ค', 'vowel': 'อา', 'coda': 'บ'},
    ['', 'ขาบ', 'คาบ', 'ค้าบ', 'ค๋าบ']),
    ({'onset': 'ง', 'vowel': 'อา', 'coda': 'บ'},
    ['', 'หงาบ', 'งาบ', 'ง้าบ', 'ง๋าบ']),
    # dead mid, high, paired low, single low onsets (short)
    ({'onset': 'ก', 'vowel': 'อะ', 'coda': 'บ'},
    ['', 'กับ', 'กั้บ', 'กั๊บ', 'กั๋บ']),
    ({'onset': 'ข', 'vowel': 'อะ', 'coda': 'บ'},
    ['', 'ขับ', 'ขั้บ', 'คับ', 'คั๋บ']),
    ({'onset': 'ค', 'vowel': 'อะ', 'coda': 'บ'},
    ['', 'ขับ', 'คั่บ', 'คับ', 'คั๋บ']),
    ({'onset': 'ง', 'vowel': 'อะ', 'coda': 'บ'},
    ['', 'หงับ', 'งั่บ', 'งับ', 'งั๋บ'])]

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

SETTING_SPLIT = [
    ({'split_true_cluster': False},
    {'onset': 'กร', 'vowel': 'อุ', 'coda': 'น', 'tone': 1},
    'กรุ่น'),
    ({'split_true_cluster': True},
    {'onset': 'กร', 'vowel': 'อุ', 'coda': 'น', 'tone': 1},
    'กหรุ่น'),
    ({'split_false_cluster': False},
    {'onset': 'ศร', 'vowel': 'อี', 'tone': 4},
    'ศรี'),
    ({'split_false_cluster': True},
    {'onset': 'ศร', 'vowel': 'อี', 'tone': 4},
    'ศหรี'),
    ({'split_leading_con': False},
    {'onset': 'สล', 'vowel': 'โอ', 'silent_before': 'ว', 'tone': 4},
    'สโลว์'),
    ({'split_leading_con': True},
    {'onset': 'สล', 'vowel': 'โอ', 'silent_before': 'ว', 'tone': 0},
    'สโลว์')
]

SETTING_H_THOO = [
    ({'low_single_h_thoo': False},
    {'onset': 'ม', 'vowel': 'อะ', 'coda': 'น', 'tone': 2},
    'มั่น'),
    ({'low_single_h_thoo': True},
    {'onset': 'ม', 'vowel': 'อะ', 'coda': 'น', 'tone': 2},
    'หมั้น')
]

TO_IPA = (
    ({},
    {'onset': 'ส', 'vowel': 'เอีย', 'coda': 'ง', 'tone': -1},
    's iaː ŋ ˩˩˦'),
    ({},
    {'onset': 'ต', 'vowel': 'อะ', 'coda': 'ง', 'tone': 2},
    't a ŋ ˥˩'),
    ({'split_leading_con': False},
    {'onset': 'สล', 'vowel': 'โอ', 'silent_before': 'ว', 'tone': 4},
    's a ˨˩ . l oː ˩˩˦'),
    ({'split_leading_con': True},
    {'onset': 'สล', 'vowel': 'โอ', 'silent_before': 'ว', 'tone': 0},
    's a ˨˩ . l oː ˧'),
    ({},
    {'onset': 'ป', 'vowel': 'อะ', 'tone': -1},
    'p aʔ ˨˩'),
)

TO_RTGS = (
    ({},
    {'onset': 'น', 'vowel': 'โอะ', 'coda': 'ก', 'tone': -1},
    'nok'),
    ({},
    {'onset': 'ส', 'vowel': 'อุ', 'coda': 'ข', 'tone': 1},
    'suk'),
    ({},
    {'onset': 'ล', 'vowel': 'อะ', 'coda': 'พ', 'silent_after': 'ธ'},
    'lap'),
    ({},
    {'onset': 'สล', 'vowel': 'โอ', 'silent_before': 'ว', 'tone': 0},
    'salo'),
    ({},
    {'onset': 'ปร', 'vowel': 'อา', 'tone': 0},
    'pra'),
)

DONEE_END = [
    ({},
    {'onset': 'ต', 'vowel': 'อา'},
    True),
    ({},
    {'onset': 'ปล', 'vowel': 'อิว'},
    False),
    ({'silent_before_style': 'kaaran'},
    {'onset': 'อ', 'vowel': 'อา', 'silent_before': 'ร'},
    False),
    ({'silent_before_style': 'plain'},
    {'onset': 'อ', 'vowel': 'อา', 'silent_before': 'ร'},
    False)
]

DONOR_END = [
    ({},
    {'onset': 'ต', 'vowel': 'อา', 'coda': 'ก'},
    True),
    ({},
    {'onset': 'ค', 'vowel': 'อือ'},
    False),
    ({'silent_before_style': 'kaaran'},
    {'onset': 'อ', 'vowel': 'อา', 'silent_before': 'ร'},
    False),
    ({'silent_before_style': 'plain'},
    {'onset': 'อ', 'vowel': 'อา', 'silent_before': 'ร'},
    True)
]

DONOR_START = [
    ({},
    {'onset': 'กล', 'vowel': 'โอะ', 'coda': 'ม'},
    True),
    ({'clear_vowel': False},
    {'onset': 'คว', 'vowel': 'เอ'},
    False)
]

class TestSpellWord(unittest.TestCase):

    def test_general(self):
        for case in GENERAL:
            spell = Kham(**case[0])
            self.assertEqual(spell.form, case[1])

    def test_onset_tone(self):
        for case in ONSET_TONE:
            spell = Kham(**case[0])
            self.assertEqual(spell.all_tone(), case[1])

    def test_onset_cluster(self):
        for case in ONSET_CLUSTER:
            spell = Kham(**case[0])
            self.assertEqual(spell.all_tone(), case[1])

    def test_setting_style(self):
        for case in SETTING_STYLE:
            spell = Kham(**case[0], **case[1])
            self.assertEqual(spell.form, case[2])

    def test_setting_form(self):
        for case in SETTING_FORM:
            spell = Kham(**case[0], **case[1])
            self.assertEqual(spell.form, case[2])

    def test_setting_placing(self):
        for case in SETTING_PLACING:
            spell = Kham(**case[0], **case[1])
            self.assertEqual(spell.form, case[2])

    def test_setting_ls(self):
        for case in SETTING_LS:
            spell = Kham(**case[0], **case[1])
            self.assertEqual(spell.all_tone(), case[2])

    def test_setting_ls(self):
        for case in SETTING_HLS:
            spell = Kham(**case[0], **case[1])
            self.assertEqual(spell.all_tone(), case[2])

    def test_setting_split(self):
        for case in SETTING_SPLIT:
            spell = Kham(**case[0], **case[1])
            self.assertEqual(spell.form, case[2])

    def test_setting_h_thoo(self):
        for case in SETTING_H_THOO:
            spell = Kham(**case[0], **case[1])
            self.assertEqual(spell.form, case[2])

    def test_to_ipa(self):
        for case in TO_IPA:
            spell = Kham(**case[0], **case[1])
            self.assertEqual(spell.ipa(), case[2])

    def test_to_rtgs(self):
        for case in TO_RTGS:
            spell = Kham(**case[0], **case[1])
            self.assertEqual(spell.rtgs(), case[2])

    def test_donee_end(self):
        for case in DONEE_END:
            spell = Kham(**case[0], **case[1])
            self.assertEqual(spell.is_donee_end(), case[2])

    def test_donor_end(self):
        for case in DONOR_END:
            spell = Kham(**case[0], **case[1])
            self.assertEqual(spell.is_donor_end(), case[2])

    def test_donor_start(self):
        for case in DONOR_START:
            spell = Kham(**case[0], **case[1])
            self.assertEqual(spell.is_donor_start(), case[2])

if __name__ == '__main__':
    unittest.main()