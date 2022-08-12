"""This module contains class that find word data."""

from typing import Any, Dict, List

from khanaa.setting import _DEFAULT_PREF
from khanaa.thai_script import (CLUSTERS, CONSONANTS, FALSE_CLUSTERS,
    LOW_SINGLE_ALT, TONE_MARKERS, TONE_NOT_AVAILABLE, TONES, VOWELS)
from khanaa.utils import (check_checked, find_tone, find_tone_phrase,
    find_vowel_length, find_vowel_pair)

class Word:
    """Find word/syllable data from input."""
    def __init__(
            self,
            onset: str,
            vowel: str,
            silent_before: str = '',
            coda: str = '',
            silent_after: str = '',
            tone: int = -1,
            **pref: Any) -> None:
        """See input information from Kham.
        
        Every attribute is usable and completely calculated except
        self._vowel_check and self._coda_check which are just
        calculation stage for self._vowel and self._coda.
        All attribute here won't be changed after it is defined and
        all calculation steps for them are in static methods began
        with _find + its name.
        """
        self.onset = onset
        self.vowel = vowel
        self.silent_before = silent_before
        self.coda = coda
        self.silent_after = silent_after
        self.tone = tone
        
        self.pref: Dict[str, Any] = {**_DEFAULT_PREF, **pref}

        self._onset: str = self._find_onset(self.onset)
        self._is_low_single_vague: bool = self._find_is_low_single_vague(
            self.pref['obvious_low_singles'], self._onset)
        self._is_h_vague: bool = self._find_is_h_vague(
            self.pref['obvious_h_low_single'], self._onset)
        self._onset_index: int = self._find_onset_index(
            self._is_low_single_vague, self._is_h_vague, self._onset,
            self.pref['split_true_cluster'], self.pref['split_false_cluster'],
            self.pref['split_leading_con'])
        self._onset_main: str = self._find_onset_main(self._onset,
            self._onset_index)
        self._onset_class: str = self._find_onset_class(self._onset_main)

        # _vowel_check and _coda_check are just calculation stages.
        self._vowel_check: str = self._find_vowel_check(self.vowel,
            self.pref['vowel_length'], self.pref['vowel_pair_form'])
        self._coda_check: str = self._find_coda_check(self._vowel_check,
            self.coda)
        self._is_vowel_empty_form: bool = self._find_is_vowel_empty_form(
            self.pref['vowel_coda_form'], self._vowel_check,
            self._coda_check)

        self._vowel: str = self._find_vowel(self._vowel_check,
            self._is_vowel_empty_form, self.pref['vowel_no_coda'])
        self._vowel_length: str = self._find_vowel_length(self._vowel)

        self._silent_before: str = self._find_silent_before(
            self.silent_before)

        self._coda: str = self._find_coda(self._coda_check,
            self._is_vowel_empty_form, self.pref['vowel_no_coda'])
        self._coda_class: str = self._find_coda_class(self._coda)
        
        self._vowel_form: str = self._find_vowel_form(self._vowel, self._coda,
            self._is_vowel_empty_form, self.pref['vowel_no_coda'],
            self.pref['vowel_coda_form'])
        self._is_checked: bool = self._find_is_checked(self._vowel,
            self._coda)

        self._silent_after: str = self._find_silent_after(self._vowel,
            self.coda, self.silent_after, self._is_vowel_empty_form,
            self.pref['vowel_no_coda'])
        
        self._tone: int = self._find_tone(self.tone)

        self._tone_phrase: str = self._find_tone_phrase(self._onset_class,
            self._is_checked, self._vowel_length)
        self._tone_detail: List[str] = self._find_tone_detail(self._tone,
            self._tone_phrase, self.pref['low_single_h_thoo'])
        self._is_possible_tone: bool = self._find_is_possible_tone(self._tone,
            self._tone_phrase)
        self._tone_realized: int = self._find_tone_realized(self._tone,
            self._onset_main, self._vowel, self._coda, self._is_possible_tone)
        self._use_pair_onset: bool = self._find_use_pair_onset(self._tone,
            self._tone_detail, self._onset_class)
        self._use_leading_h: bool = self._find_use_leading_h(self._tone,
            self._tone_detail, self._onset_class)
        self._tone_mark: str = self._find_tone_mark(self._tone,
            self._tone_detail)

        self._is_vowel_vague = self._find_is_vowel_vague(self._onset,
            self.pref['clear_vowel'], self.pref['clear_vowel_onset'],
            self.pref['clear_vowel_tone_mark'], self._tone_mark)

    @staticmethod
    def _find_onset(onset: str) -> str:
        return onset
    
    @staticmethod
    def _find_is_low_single_vague(obvious_low_singles: bool,
            onset: str) -> bool:
        """Check for low single-low single onset cluster ambiguity.
        
        If true, we'll use the latter consonant as the main consonant
        to determine tone.
        Ex. นวี นหวี่ นวี่ นวี้ นหวี
        instead of นวี หนวี่ นวี่ นวี้ หนวี
        """
        return (obvious_low_singles
            and len(onset) > 1
            and CONSONANTS[onset[-2]]['class'] == 'low_single'
            and CONSONANTS[onset[-1]]['class'] == 'low_single')

    @staticmethod
    def _find_is_h_vague(obvious_h_low_single: bool, onset: str) -> bool:
        """Check for ฮ and single low onset cluster ambiguity.
        
        If true, we'll use the latter consonant as the main consonant
        to determine tone. (ฮ is paired low and will have the same tone marker
        with single low vowel).
        Ex. ฮวา ฮหว่า ฮว่า ฮว้า ฮหวา
        instead of ฮวา หว่า ฮว่า ฮว้า หวา
        """
        return (obvious_h_low_single
            and len(onset) > 1
            and onset[-2] == 'ฮ'
            and CONSONANTS[onset[-1]]['class'] == 'low_single')

    @staticmethod
    def _find_onset_index(is_low_single_vague: bool,
            is_h_vague: bool, onset: str, split_true_cluster: bool,
            split_false_cluster: bool, split_leading_con: bool) -> int:
        """Select the index of main onset to determine tone from it.
        
        According to general rule of Thai onset cluster:

        - If the latter consonant is in single low class,
        tone of the word follows the prior consonant
        (อักษรควบแท้ อักษรควบไม่แท้ อักษรนำที่ตามด้วยอักษรต่ำเดี่ยว)
        - If not, tone follows the latter consonant
        (อักษรนำที่ไม่ได้ตามด้วยอักษรต่ำเดี่ยว)

        All of single low consonants are sonorants.
        """
        index: int = -1
        if is_low_single_vague or is_h_vague:
            pass
        elif split_true_cluster and onset[-2:] in CLUSTERS:
            pass
        elif split_false_cluster and onset[-2:] in FALSE_CLUSTERS:
            pass
        elif (len(onset) > 1
                and CONSONANTS[onset[-1]]['class'] == 'low_single'
                and not split_leading_con):
            index = -2
        return index

    @staticmethod
    def _find_onset_main(onset: str, onset_index: int) -> str:
        """Find main onset to be used when calculating tone."""
        return onset[onset_index]

    @staticmethod
    def _find_onset_class(onset_main: str) -> str:
        """หมวดหมู่ของพยัญชนะต้น"""
        return CONSONANTS[onset_main]['class']

    @staticmethod
    def _find_vowel_check(vowel_input: str, vowel_length_pref: str,
            vowel_pair_form_pref: Dict[str, str]) -> str:
        """Change length of input vowel according to the setting."""
        vowel: str = vowel_input
        if vowel_length_pref not in ['short', 'long']:
            pass
        elif vowel_length_pref != find_vowel_length(vowel_input):
            if vowel_input in vowel_pair_form_pref:
                vowel = vowel_pair_form_pref[vowel_input]
            else:
                vowel = find_vowel_pair(vowel_input)
        return vowel

    @staticmethod    
    def _find_is_vowel_empty_form(vowel_coda_form: Dict[str, str],
            vowel: str, coda: str) -> bool:
        """Check if vowel coda form is empty.
        
        Some vowels don't have coda form, so there are two choices:
        - Use coda form from its pair
        - Change coda to silent letter
        The choice is up to the setting.
        """
        if vowel_coda_form.get(vowel):
            return False
        elif (coda
                and not VOWELS[vowel]['form_with_coda']):
            return True
        else:
            return False

    @staticmethod
    def _find_vowel(vowel_input: str, is_vowel_empty_form: bool,
            vowel_no_coda_pref: str) -> str:
        """Find vowel.

        This step check if vowel coda form is empty and has to be
        change to its pair form according to the setting. The vowel
        should be already converted according to length from
        _find_vowel_check.
        """
        vowel: str = vowel_input
        if is_vowel_empty_form and vowel_no_coda_pref == 'pair':
            vowel = VOWELS[vowel]['pair']
        return vowel

    @staticmethod
    def _find_vowel_form(vowel: str, coda: str, is_vowel_empty_form: bool,
            vowel_no_coda_pref: str, vowel_coda_form: Dict[str, str]) -> str:
        """Find vowel form to use from VOWELS"""
        vowel_form: str = VOWELS[vowel]['form_no_coda']
        if coda:
            if vowel_coda_form.get(vowel):
                vowel_form = vowel_coda_form[vowel]
            elif (is_vowel_empty_form
                    and vowel_no_coda_pref == 'silent_after'):
                vowel_form = VOWELS[vowel]['form_no_coda']
            else:
                vowel_form = VOWELS[vowel]['form_with_coda']
        return vowel_form

    @staticmethod
    def _find_vowel_length(vowel: str) -> str:
        """Find ultimate vowel length."""
        return VOWELS[vowel]['length']

    @staticmethod
    def _find_silent_before(silent_before) -> str:
        return silent_before

    @staticmethod
    def _find_coda_check(vowel_check: str, coda_input: str) -> str:
        """Check vowel.
        
        If the vowel already coda, change coda to silent after.        
        Ex. อัย เอา already have j, w coda. They can't have coda.
        And change all but the first coda to silent after.
        """
        if VOWELS[vowel_check]['sound_coda']:
            return ''
        else:
            return coda_input[:1]

    @staticmethod
    def _find_coda(coda: str, is_vowel_empty_form: bool,
            vowel_no_coda_pref: str) -> str:
        """Return empty coda in case of vowel without coda form."""
        if (is_vowel_empty_form
                and vowel_no_coda_pref == 'silent_after'):
            return ''
        else:
            return coda

    @staticmethod
    def _find_coda_class(coda: str) -> str:
        """Return coda class (dead or alive)."""
        if coda:
            return CONSONANTS[coda]['coda_class']
        else:
            return ''

    @staticmethod
    def _find_is_checked(vowel: str, coda: str) -> bool:
        return check_checked(vowel, coda)

    @staticmethod
    def _find_silent_after(vowel: str, coda: str, silent_after: str,
            is_vowel_empty_form: bool, vowel_no_coda_pref: str) -> str:
        """Return silent after.
        
        If the vowel already has coda or coda should be changed to
        silent after because vowel coda is empty, index is zero.
        Otherwise index is one for multiple coda case.
        """
        index: int = 1
        if (VOWELS[vowel]['sound_coda']
                or (is_vowel_empty_form
                    and vowel_no_coda_pref == 'silent_after')):
            index = 0
        return ''.join([coda[index:], silent_after])

    @staticmethod
    def _find_tone(tone) -> int:
        return tone

    @staticmethod
    def _find_tone_realized(tone: int, onset_main: str, vowel: str,
            coda: str, is_possible_tone: bool) -> int:
        if tone == -1 or not is_possible_tone:
            return find_tone(onset_main, vowel, coda)
        else:
            return tone

    @staticmethod
    def _find_tone_phrase(onset_class: str, is_checked: bool,
            vowel_length) -> str:
        """Tone phrase is used when searching tone detail in TONES."""
        if onset_class in ['low_pair', 'low_single']:
            onset_class = 'low'
        alive_dead: str =  'dead' if is_checked else 'alive'
        return find_tone_phrase(onset_class,
            alive_dead, vowel_length)

    @staticmethod
    def _find_tone_detail(tone: int, tone_phrase: str,
            low_single_h_thoo: bool) -> List[str]:
        """Tone detail is whether onset has to be changed to pair
        and what tone mark it is.
        """
        if tone == -1:
            return ['', '']
        elif low_single_h_thoo and tone == 2:
            return LOW_SINGLE_ALT
        else:
            return TONES[tone][tone_phrase]
    
    @staticmethod
    def _find_use_pair_onset(tone: int, tone_detail: List[str],
            onset_class: str) -> bool:
        if tone == -1:
            return False
        else:
            return (tone_detail[0] == 'pair'
                and onset_class in ['high', 'low_pair'])

    @staticmethod
    def _find_use_leading_h(tone: int, tone_detail: List[str],
            onset_class: str) -> bool:
        """ห นำ"""
        if tone == -1:
            return False
        else:
            return (tone_detail[0] == 'pair'
                and onset_class == 'low_single')
    
    @staticmethod
    def _find_tone_mark(tone: int, tone_detail: List[str]) -> str:
        if tone == -1 or not tone_detail[1]:
            return ''
        else:
            return TONE_MARKERS[tone_detail[1]]
    
    @staticmethod
    def _find_is_possible_tone(tone: int, tone_phrase: str) -> bool:
        """As some words can't be pronounced with some tones
        such as 0 tone with checked syllable.
        """
        return not (tone in TONE_NOT_AVAILABLE
            and tone_phrase in TONE_NOT_AVAILABLE[tone])

    @staticmethod
    def _find_is_vowel_vague(onset: str, clear_vowel: bool,
            clear_vowel_onset: str, clear_vowel_tone_mark: bool,
            tone_mark: str) -> bool:
        """Check if we should put initial onset in front of vowel.
        
        As some Thai vowels create ambiguity in pronunciation
        of the word with onset cluster, we might put the prior onset
        in front of these vowels to clarify it.

        Ex. เชว, แชว, โชว > ชเว, ชแว, ชโว
        """
        return (clear_vowel
            and len(onset) == 2
            and (clear_vowel_onset == 'all'
                or (clear_vowel_onset == 'not_true_cluster'
                    and onset not in CLUSTERS))
            and (clear_vowel_tone_mark
                or (not clear_vowel_tone_mark
                    and not tone_mark)))