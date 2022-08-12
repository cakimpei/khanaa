"""This module contains class that combine word data with methods."""

from typing import List

from khanaa.ambiguity import find_donee_end, find_donor_end, find_donor_start
from khanaa.pronunciation import ThaiToIPA
from khanaa.speller import combine
from khanaa.word import Word

class Combination(Word):
    """Combine finding word data part from Word with methods.
    
    For information for each methods, see Kham.
    """
    
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
    def reading(self) -> str:
        # it's _tone_realized not _tone
        # because we want spelled word sound, not the input one.
        thai_to_ipa = ThaiToIPA(self._onset, self._vowel, self._silent_before,
            self._coda, self._silent_after, self._tone_realized, **self.pref)
        return thai_to_ipa.convert()
    
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