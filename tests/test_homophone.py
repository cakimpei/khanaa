import unittest
from khanaa import Kham

GENERAL = [
    ({'onset': 'ค', 'vowel': 'โอะ', 'coda': 'น'},
        ['คญ', 'คณ', 'คน', 'คร', 'คล', 'คฬ', 'ฅญ', 'ฅณ', 'ฅน', 'ฅร', 'ฅล',
            'ฅฬ', 'ฆญ', 'ฆณ', 'ฆน', 'ฆร', 'ฆล', 'ฆฬ']),
    ({'onset': 'กว', 'vowel': 'อา', 'coda': 'ง', 'tone': 2},
        ['กว้าง']),
    ({'onset': 'สว', 'vowel': 'อิ', 'coda': 'ต', 'silent_after': 'ช'},
        ['สวิจ', 'สวิช', 'สวิซ', 'สวิฌ', 'สวิฎ', 'สวิฏ', 'สวิฐ', 'สวิฑ', 'สวิฒ', 'สวิด',
            'สวิต', 'สวิถ', 'สวิท', 'สวิธ', 'สวิศ', 'สวิษ', 'สวิส'])
]

class TestHomophone(unittest.TestCase):

    def test_general(self):
        for case in GENERAL:
            kham = Kham(**case[0])
            result = kham.homophone()
            self.assertEqual(result, case[1])

if __name__ == '__main__':
    unittest.main()