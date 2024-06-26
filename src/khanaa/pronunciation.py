"""This module contains class used to derive word pronunciation."""

from typing import Any, Dict, List

from khanaa.thai_script import (CLUSTERS, CONSONANTS, FALSE_CLUSTERS, VOWELS,
    TONE_IPA)
from khanaa.thai_spelling import find_vowel_length
from khanaa.utils import find_tone

class ThaiToIPA:
    """Convert Thai spelling data to IPA."""
    def __init__(
            self,
            onset: str,
            vowel: str,
            silent_before: str = '',
            coda: str = '',
            silent_after: str = '',
            tone: int = -1,
            **pref: Any) -> None:
        """Input should be already cleaned from Word and tone should
        be realized tone instead of the input tone.
        """
        self.onset = onset
        self.vowel = vowel
        self.silent_before = silent_before
        self.coda = coda
        self.silent_after = silent_after
        self.tone = tone
        
        self.pref = pref

    def convert(self) -> str:
        """Return basic IPA pronunciation from data provided."""
        joined_vowel = ''.join([self.vowel_ipa, self.length_ipa])
        return ' '.join(filter(None, [self.onset_ipa, joined_vowel,
            self.vowel_coda_ipa, self.coda_ipa, self.tone_ipa]))
    
    @property
    def is_true_cluster(self) -> bool:
        true_cluster = False
        if (self.pref['split_true_cluster'] == False
                and len(self.onset) > 1
                and self.onset[-2:] in CLUSTERS):
            true_cluster = True
        return true_cluster
    
    @property
    def is_false_cluster(self) -> bool:
        false_cluster = False
        if (self.pref['split_false_cluster'] == False
                and len(self.onset) > 1
                and self.onset[-2:] in FALSE_CLUSTERS):
            false_cluster = True
        return false_cluster
    
    @property
    def onset_ipa_list(self) -> List[Dict[str, str]]:
        onset_ipa_chars: List[Dict[str, str]] = []
        convert_onset = self.onset
        if self.is_false_cluster:
            # because false clusters have ซ sound
            convert_onset = convert_onset[:-2] + 'ซ'
        for index, char in enumerate(convert_onset):

            # if it is a glide, put it with the preceding group
            if index == len(convert_onset) - 1 and self.is_true_cluster:
                onset_ipa_chars[-1].update({
                    'glide': CONSONANTS[char]['sound_onset'],
                    'cat': 'cluster'
                })
                continue

            inner_cat: str = "consonant"
            inner_vowel: str = ""
            inner_tone: str = ""

            # if the onset should be separately pronounced
            if not (index == len(convert_onset) - 1
                    or (index == len(convert_onset) - 2 and self.is_true_cluster)):
                inner_cat = "sub"
                inner_vowel = 'a'
                inner_tone = self.find_tone_onset(char)
            inner_onset: str = CONSONANTS[char]['sound_onset']
            onset_ipa_chars.append({
                'cat': inner_cat,
                'onset': inner_onset,
                'glide': "",
                'vowel': inner_vowel,
                'tone': inner_tone
            })
        return onset_ipa_chars

    @property
    def onset_ipa(self) -> str:
        result_list: List[str] = []
        onset_list = self.onset_ipa_list
        for part in onset_list:
            if part['cat'] == 'consonant':
                result_list.append(part['onset'])
            else:
                subtext: str = " ".join(filter(None, [
                    part['onset'],
                    part['glide'],
                    part['vowel'],
                    part['tone']
                ]))
                result_list.append(subtext)
        return ' . '.join(result_list)
    
    @staticmethod
    def find_tone_onset(onset_char) -> str:
        """Find IPA tone for syllabic onset character."""
        tone_num = find_tone(onset_char, 'อะ', '', '', False)
        return TONE_IPA[tone_num]

    @property
    def vowel_ipa(self) -> str:
        return VOWELS[self.vowel]['sound_vowel']
    
    @property
    def vowel_coda_ipa(self) -> str:
        return VOWELS[self.vowel]['sound_coda']
    
    @property
    def length_ipa(self) -> str:
        """Return IPA symbol according to vowel length."""
        length_char = ''
        if (find_vowel_length(self.vowel) == 'long'
                or self.pref['vowel_length'] == 'long'):
            length_char = 'ː'
        elif ((not self.coda and not self.vowel_coda_ipa)
                or self.pref['vowel_length'] == 'short'):
            length_char = 'ʔ'
        return length_char
    
    @property
    def coda_ipa(self) -> str:
        coda_char = ''
        if self.coda:
            coda_char = CONSONANTS[self.coda]['sound_coda']
        return coda_char
    
    @property
    def tone_ipa(self) -> str:
        tone_char = ''
        if self.tone in range(5):
            tone_char = TONE_IPA[self.tone]
        return tone_char