"""This module contains class that combine word data with methods."""

from typing import List

from khanaa.ambiguity import find_donee_end, find_donor_end, find_donor_start
from khanaa.homophone import find_homophone_product
from khanaa.pronunciation import ThaiToIPA
from khanaa.romanization import ipa_to_rtgs
from khanaa.speller import combine
from khanaa.word import Word

class Combination(Word):
    """Combine finding word data part from Word with methods.
    
    For information for each methods, see Kham.
    """
    _ipa_data: ThaiToIPA = None
    
    @property
    def form(self) -> str:
        """Return spelled form of the word."""
        return combine(self, self.pref)
    
    @property
    def all_tone(self) -> List[str]:
        all_tone = []
        for n in range(5):
            spell = Combination(self._onset, self._vowel, self._silent_before,
                self._coda, self._silent_after, n, **self.pref)
            if not spell._is_possible_tone:
                all_tone.append('')
                continue
            all_tone.append(spell.form)
        return all_tone
    
    @property
    def ipa_data(self) -> ThaiToIPA:
        if not self._ipa_data:
            # it's _tone_realized not _tone
            # because we want spelled word sound, not the input one.
            self._ipa_data = ThaiToIPA(self._onset, self._vowel, self._silent_before,
                self._coda, self._silent_after, self._tone_realized, **self.pref)
        return self._ipa_data

    @property
    def reading(self) -> str:
        return self.ipa_data.convert()
    
    @property
    def rtgs(self) -> str:
        return ipa_to_rtgs(self.ipa_data)
    
    @property
    def is_donee_end(self) -> bool:
        return find_donee_end(self._vowel, self._silent_before, self._coda,
            self._silent_after, self.pref['silent_before_style'],
            self.pref['silent_after_style'])
    
    @property
    def is_donor_end(self) -> bool:
        return find_donor_end(self._vowel, self._silent_before, self._coda,
            self._silent_after, self.pref['silent_before_style'],
            self.pref['silent_after_style'], self._tone_mark,
            self._vowel_form)
    
    @property
    def is_donor_start(self) -> bool:
        return find_donor_start(self._onset, self.form)
    
    @property
    def homophone(self) -> list:
        product = find_homophone_product(self._onset, self._vowel, self._coda)
        result = []
        for possible in product:
            kham = Combination(
                onset=possible[0],
                vowel=possible[1],
                coda=possible[2],
                tone=self._tone_realized
            )
            result.append(kham.form)
        return list(dict.fromkeys(result))