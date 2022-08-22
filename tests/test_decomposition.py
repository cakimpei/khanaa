import unittest
from khanaa import spelling_decompose

GENERAL = {
    'เขียน': {
        'data': {
            'onset': 'ข',
            'vowel': 'เอีย',
            'silent_before': '',
            'coda': 'น',
            'silent_after': '',
            'tone': 4
            },
        'detail': {
            'tone_mark': '',
            'leading_h': False,
            'vowel_form': 'เ-ี+ย',
            'onset_index': -1,
            'onset_main': 'ข'
            },
        'pref': {}
        },
    'สมุทร': {
        'data': {
            'onset': 'สม',
            'vowel': 'อุ',
            'silent_before': '',
            'coda': 'ท',
            'silent_after': 'ร',
            'tone': 1
            },
        'detail': {
            'tone_mark': '',
            'leading_h': False,
            'vowel_form': '-ุ+',
            'onset_index': -2,
            'onset_main': 'ส'
            },
        'pref': {
            'silent_after_style': 'plain',
            'clear_vowel': False,
            'clear_vowel_onset': 'not_true_cluster',
            'clear_vowel_tone_mark': False
            }
        },
    'แถลง': {
        'data': {
            'onset': 'ถล',
            'vowel': 'แอ',
            'silent_before': '',
            'coda': 'ง',
            'silent_after': '',
            'tone': 4
            },
        'detail': {
            'tone_mark': '',
            'leading_h': False,
            'vowel_form': 'แ-+',
            'onset_index': -2,
            'onset_main': 'ถ'
            },
        'pref': {
            'clear_vowel': False,
            'clear_vowel_onset': 'not_true_cluster',
            'clear_vowel_tone_mark': False
            }
        }
}

class TestSpellingDecompose(unittest.TestCase):

    def test_general(self):
        for case in GENERAL:
            result = spelling_decompose(case)
            self.assertEqual(result, GENERAL[case])

if __name__ == '__main__':
    unittest.main()