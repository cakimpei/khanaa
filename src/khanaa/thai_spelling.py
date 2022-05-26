"""Thai spelling"""

from typing import Any, List, Dict
from .thai_script import (CLUSTERS, CONSONANTS, VOWELS, TONES,
    TONE_MARKERS, DIACRITICS)

_DEFAULT_PREF = {
    'clear_vowel': True,
    'clear_vowel_onset': 'not_true_cluster',
    'clear_vowel_tone_mark': False,
    'obvious_low_singles': True,
    'obvious_h_low_single': True,
    'onset_style': 'plain',
    'silent_before_style': 'kaaran',
    'coda_style': 'plain',
    'silent_after_style': 'kaaran',
    'vowel_no_coda': 'pair',
    'vowel_coda_form': {},
    'vowel_length': 'input',
    'vowel_pair_form': {}
}

class SpellWord:
    def __init__(self, **pref: Any) -> None:
        """Init SpellWord with setting.

        None of the keyword arguments here are required.

        :key bool clear_vowel: Turn on/off option to put the first
            consonant in front of vowel to make the pronunciation
            less ambiguous.
            Option: False/off (ex. เชว), True/on (ex. ชเว).
            Default: True
        :key str clear_vowel_onset: If clear_vowel is turned on,
            select onset cluster type that clear_vowel will be
            used with.
            Option: 'not_true_cluster' (true cluster คำควบกล้ำแท้
            won't be separated ex. เกวน ชเวน), 'all' (ex. กเวน ชเวน)
            Default: 'not_true_cluster'
        :key bool clear_vowel_tone_mark: If clear_vowel is turned on,
            select if clean_vowel will be used with the word with
            tone marker or not.
            Option: False/not use (ex. คเว เคว่), True/use
            (ex. คเว คเว่).
            Default: False
        :key bool obvious_low_singles: Turn on/off option to make
            single low-single low onset cluster less ambiguous.
            Option: False/off (ex. หนวี่), True/on (ex. นหวี่).
            Default: True
        :key bool obvious_h_low_single: Turn on/off option to make
            ฮ-single low onset cluster less ambiguous.
            Option: False/off (ex. หว่า), True/on (ex. ฮหว่า).
            Default: True
        :key str onset_style: Select onset style.
            Option: 'plain' (no diacritic), 'phinthu' (ใส่พินทุ),
            'yaamakkaan' (ใส่ยามักการ), 'kaaran' (ใส่การันต์)
            Default: 'plain'
        :key str silent_before_style: Select style of the silent
            consonant that comes before the coda.
            Option: 'plain', 'phinthu', 'yaamakkaan', 'kaaran', 'hide'
            Default: 'kaaran'
        :key str coda_style: Select coda style.
            Option: 'plain', 'phinthu', 'yaamakkaan', 'kaaran'
            Default: 'plain'
        :key str silent_after_style: Select style of the silent
            consonant that comes after the coda.
            Option: 'plain', 'phinthu', 'yaamakkaan', 'kaaran', 'hide'
            Default: 'kaaran'
        :key str vowel_no_coda: Select what we should do when vowels (เออะ,
            เอียะ, เอือะ, อัวะ) without its own coda form have coda.
            Option: 'pair' (use its pair form ex. เอียะ + น => เอียน),
            'silent_after' (push the coda to silent_after ex. เอียะ + น
            => เอียะน์)
            Default: 'pair'
        :key dict[str, str] vowel_coda_form: Select specific vowel form
            to use when coda is present. Put vowel in dict key and
            put vowel form in its value. In vowel form, - is
            the consonant position and + is the tone marker position.
            Example: vowel_coda_form={'เออ': 'เ-+อ'} (the result
            will be, for example, เดอน instead of the default เดิน)
        :key str vowel_length: Select vowel length.
            Option: 'input' (same as input), 'short' (if long vowel
            is in the input, the result will be with a short vowel),
            'long' (vice versa)
            Default: 'input'
        :key dict[str, str] vowel_pair_form: Select specific vowel pair
            form to use when the length is specified.
            Example: vowel_length='short',
            vowel_pair_form={'อาย': 'อัย'}
            (อาย will be shorten to อัย instead of the default ไอ)
        """
        self.option = {**_DEFAULT_PREF, **pref}

    def spell_out(
            self,
            onset: str,
            vowel: str,
            silent_before: str = '',
            coda: str = '',
            silent_after: str = '',
            tone: int = -1) -> str:
        """Return the word from the information provided.

        Example:

        spell = SpellWord()

        result = spell.spell_out(onset='ข', vowel='เอีย', coda='น')
        
        result should be 'เขียน'

        Find all available Thai consonants, vowels, and true clusters
        from find_letter_list()
        
        :param onset: Onset (can be one or more) พยัญชนะต้น
        :param vowel: A vowel.
            Write the vowel with อ as a placeholder.
            If vowel has ย, ว or j, w coda, please put
            them here. (Don't put ย, ว in coda section).
            Ex. อา, ไอ, อาว, อํ
        :param silent_before: Silent consonant(s) before coda
        :param coda: A coda, not including j, w ตัวสะกด
        :param silent_after: Silent consonant(s) after coda
        :param tone: Tone number -1 not specified, 0 mid สามัญ,
            1 low เอก, 2 falling โท, 3 high ตรี, 4 rising จัตวา
        """
        self.onset = {'used': onset, 'input': onset, 'used_index': -1}
        self.vowel = {'used': vowel}
        self.silent_before = silent_before
        self.coda = coda
        self.silent_after = silent_after
        self.tone = tone

        self._find_data()
        self._delete_taikhuu()
        combined = self._combine()
        combined = combined.replace('+', self.tone_mark)
        combined_coda = self._combine_coda()

        result = ''.join([combined, combined_coda])
        return result

    def _find_data(self) -> None:
        """Check and collect data for the word"""
        self._check_vowel_coda()
        self._check_multiple_coda()
        self._select_onset()
        self._check_low_singles()
        self._check_h_low_single()
        self._find_vowel()
        self._find_tone()

    def _check_vowel_coda(self) -> None:
        """If the vowel already coda, change coda to silent after.
        
        Ex. อัย เอา already have j, w coda. They can't have coda.
        """
        if VOWELS[self.vowel['used']]['sound_coda']:
            self._coda_to_silent()

    def _coda_to_silent(self) -> None:
        """Change coda to silent after."""
        new_silent_after = ''.join([
            self.coda,
            self.silent_after
        ])
        self.silent_after = new_silent_after
        self.coda = ''

    def _check_multiple_coda(self) -> None:
        """Change all but the first coda to silent after.
        
        If coda has more than one consonants,
        insert every consonant after the first one to silent after."""
        if len(self.coda) > 1:
            new_silent_after = ''.join([
                self.coda[1:],
                self.silent_after
            ])
            self.silent_after = new_silent_after
            self.coda = self.coda[0]

    def _select_onset(self) -> None:
        """Select the main onset to determine tone from it.
        
        According to general rule of Thai onset cluster:

        - If the latter consonant is in single low class,
        tone of the word follows the prior consonant
        (อักษรควบแท้ อักษรควบไม่แท้ อักษรนำที่ตามด้วยอักษรต่ำเดี่ยว)
        - If not, tone follows the latter consonant
        (อักษรนำที่ไม่ได้ตามด้วยอักษรต่ำเดี่ยว)

        All of single low consonants are sonorants.

        "used" is the consonant used to derive the tone of the word.
        """
        if len(self.onset['used']) > 1:
            if CONSONANTS[self.onset['used'][-1]]['class'] == 'low_single':
                used_index = -2
            else:
                used_index = -1
            onset_used = self.onset['used'][used_index]
            self.onset.update({
                'used': onset_used,
                'used_index': used_index
            })

    def _check_low_singles(self) -> None:
        """Check for low single-low single onset cluster ambiguity.
        
        If true, we'll use the latter consonant as the main consonant
        to determine tone.
        Ex. นวี นหวี่ นวี่ นวี้ นหวี
        instead of นวี หนวี่ นวี่ นวี้ หนวี
        """
        if (self.option['obvious_low_singles'] == True
                and len(self.onset['input']) > 1
                and CONSONANTS[self.onset['input'][-1]]['class'] == 'low_single'
                and CONSONANTS[self.onset['input'][-2]]['class'] == 'low_single'
            ):
            self.onset.update({
                'used_index': -1,
                'used': self.onset['input'][-1],
            })
            self.low_single_is_ambiguous = True
        else:
            self.low_single_is_ambiguous = False

    def _check_h_low_single(self) -> None:
        """Check for ฮ and single low onset cluster ambiguity.
        
        If true, we'll use the latter consonant as the main consonant
        to determine tone. (ฮ is paired low and will have the same tone marker
        with single low vowel).
        Ex. ฮวา ฮหว่า ฮว่า ฮว้า ฮหวา
        instead of ฮวา หว่า ฮว่า ฮว้า หวา
        """
        if (self.option['obvious_h_low_single'] == True
                and len(self.onset['input']) > 1
                and self.onset['input'][-2] == 'ฮ'
                and CONSONANTS[self.onset['input'][-1]]['class'] == 'low_single'):
            self.onset.update({
                'used_index': -1,
                'used': self.onset['input'][-1],
            })
            self.h_is_ambiguous = True
        else:
            self.h_is_ambiguous = False

    def _find_vowel(self) -> None:
        """Find vowel to use from VOWELS"""
        vowel_used = self.vowel['used']
        vowel_used = self._select_vowel_length(vowel_used)
        if not self.coda:
            vowel_form = VOWELS[vowel_used]['form_no_coda']
        else:
            if (self.option['vowel_coda_form']
                and vowel_used in self.option['vowel_coda_form']):
                vowel_form = self.option['vowel_coda_form'][vowel_used]
            else:
                vowel_form = VOWELS[vowel_used]['form_with_coda']
        self.vowel.update({
            'used': vowel_used,
            'form': vowel_form
        })
        if not self.vowel['form']:
            self._deal_empty_vowel()

    def _select_vowel_length(self, vowel_used: str) -> str:
        """Select vowel length according to the preference."""
        if self.option['vowel_length'] not in ['short', 'long']:
            return vowel_used
        current_length = find_vowel_length(vowel_used)
        if self.option['vowel_length'] != current_length:
            if (self.option['vowel_pair_form']
                    and vowel_used in self.option['vowel_pair_form']):
                vowel_used = self.option['vowel_pair_form'][vowel_used]
            else:
                vowel_used = find_vowel_pair(vowel_used)
        return vowel_used

    def _deal_empty_vowel(self) -> None:
        """Find vowel to use if vowel from VOWEL is empty.
        
        Some vowels don't have coda form, so there are two choices:
        - Use coda form from its pair
        - Change coda to silent letter
        The choice is up to the setting.
        """
        if self.option['vowel_no_coda'] == 'pair':
            vowel_used = VOWELS[self.vowel['used']]['pair']
            vowel_form = VOWELS[vowel_used]['form_with_coda']
        else:
            vowel_used = self.vowel['used']
            vowel_form = VOWELS[vowel_used]['form_no_coda']
            self._coda_to_silent()
        self.vowel.update({
            'used': vowel_used,
            'form': vowel_form
        })

    def _find_tone(self) -> None:
        """Find consonant form and tone marker according to tone."""

        self.onset.update({'form': self.onset['used']})
        self.tone_mark = ''

        if self.tone not in range(5):
            return
        
        tone_info = self._find_tone_info()

        if tone_info[0] == 'pair':
            if CONSONANTS[self.onset['used']]['class'] == 'high':
                self._use_pair_onset()
            elif CONSONANTS[self.onset['used']]['class'] == 'low_pair':
                self._use_pair_onset()
            if CONSONANTS[self.onset['used']]['class'] == 'low_single':
                self._use_h_onset()

        if tone_info[1]:
            self.tone_mark = TONE_MARKERS[tone_info[1]]

    def _find_tone_info(self) -> List[str]:
        """Find tone information from TONES"""
        onset_class = CONSONANTS[self.onset['used']]['class']
        if onset_class in ['low_pair', 'low_single']:
            onset_class = 'low'
        alive_dead = 'dead' if self._is_checked() else 'alive'
        length = VOWELS[self.vowel['used']]['length']

        if onset_class in ['high', 'low'] and alive_dead == 'dead':
            word_detail = f'{onset_class} {length} {alive_dead}'
        else:
            word_detail = f'{onset_class} {alive_dead}'
            
        tone_info = TONES[self.tone][word_detail]
        return tone_info

    def _is_checked(self) -> bool:
        """Check if the word is checked (dead) or not.
        
        Checked word in Thai:
        - Has no coda, short length (and no hidden coda like ไอ)
        - Has dead class coda"""
        checked = False
        if (not self.coda
                and VOWELS[self.vowel['used']]['length'] == 'short'
                and not VOWELS[self.vowel['used']]['sound_coda']
            ):
            checked = True
        elif (self.coda
                and CONSONANTS[self.coda]['coda_class'] == 'dead'
            ):
            checked = True
        return checked

    def _use_pair_onset(self) -> None:
        """Change onset to its class pair ex. ข => ค or ค => ข"""
        self.onset.update({'form': CONSONANTS[self.onset['used']]['pair']})
    
    def _use_h_onset(self) -> None:
        """Add ห to the onset."""
        self.onset.update({'form': ''.join(['ห', self.onset['used']])})

    def _delete_taikhuu(self) -> None:
        """Delete mai taikhuu if there's also a tone marker."""
        mai_taikhuu = DIACRITICS['mai_taikhuu']
        if self.tone_mark and self.vowel['form'].find(mai_taikhuu) != -1:
            self.vowel['form'] = self.vowel['form'].replace(mai_taikhuu, '')

    def _combine(self) -> str:
        """Return joined onset and vowel.
        
        index_after_vowel is the index of consonant that
        should be after the vowel. Note that ห นำ is still not
        being calculated in this index yet.

        If the amount of onsets are more than two,
        just put the vowel in front of the penultimate onset.

        Then, for onsets with the amount of two,
        check for some Thai vowels that create ambiguity in
        pronunciation of the word with onset cluster.
        We might put these vowels in front of the last consonant
        to clarify the pronunciation.
        Ex. เชว, แชว, โชว > ชเว, ชแว, ชโว

        If the word is already mark for being ambiguous single low-
        single low cluster and has ห นำ, just put the vowel in front of the
        last consonant.

        Same case with ambiguous ฮ and single low cluster.

        Otherwise use general case: Every onset is after the vowel."""
        if len(self.onset['input']) > 2:
            index_after_vowel = -2
        elif self._is_vowel_ambiguous():
            index_after_vowel = -1
        elif self.low_single_is_ambiguous and len(self.onset['form']) == 2:
            index_after_vowel = -1
        elif self.h_is_ambiguous and len(self.onset['form']) == 2:
            index_after_vowel = -1
        else:
            index_after_vowel = 0
        combined = self._join_onset_vowel(index_after_vowel)
        
        return combined
    
    def _is_vowel_ambiguous(self) -> bool:
        """Check if we should put initial onset in front of vowel.
        
        As some Thai vowels create ambiguity in pronunciation
        of the word with onset cluster, we might put the prior onset
        in front of these vowels to clarify it.

        Ex. เชว, แชว, โชว > ชเว, ชแว, ชโว
        """
        if (self.option['clear_vowel']
                and len(self.onset['input']) == 2
                and (self.option['clear_vowel_onset'] == 'all'
                or (self.option['clear_vowel_onset'] == 'not_true_cluster'
                and self.onset['input'] not in CLUSTERS))
                and (self.option['clear_vowel_tone_mark']
                or (not self.option['clear_vowel_tone_mark']
                and not self.tone_mark))
                ):
            return True
        else:
            return False

    def _join_onset_vowel(self, index_after_vowel: int) -> str:
        """Join onsets and vowel according to the index provided."""
        combined_onset = self._join_onset()
        index_after_vowel = self._find_new_index(index_after_vowel)

        before_vowel = self._combine_diacritic(
            combined_onset[:index_after_vowel]
        )
        after_vowel = combined_onset[index_after_vowel:]
        if len(after_vowel) > 1:
            after_vowel = ''.join([
                self._combine_diacritic(after_vowel[:-1]),
                after_vowel[-1]
            ])
        
        combined = ''.join([
            before_vowel,
            self.vowel['form'].replace('-', after_vowel)
        ])
        return combined

    def _join_onset(self) -> str:
        """Join the form of main onset with other onsets."""
        prior = self.onset['input'][:self.onset['used_index']]
        latter = self.onset['input'][self.onset['used_index'] + 1:]
        if self.onset['used_index'] == -1:
            latter = ''
        combined_onset = ''.join([
            prior,
            self.onset['form'],
            latter])
        return combined_onset

    def _find_new_index(self, index_after_vowel: int) -> int:
        """Shift index leftward if ห นำ is used."""
        if (len(self.onset['form']) == 2
                and self.onset['used_index'] >= index_after_vowel
                ):
            index_after_vowel -= 1
        return index_after_vowel

    def _combine_diacritic(self, content: str) -> str:
        """Combine diacritic to the onset.
        
        If option specifies that we should add diacritic to onset,
        add diacritic to every character in onset except the last one.
        """
        if self.option['onset_style'] in ['plain']:
            return content
        if self.option['onset_style'] in ['phinthu', 'yaamakkaan', 'kaaran']:
            diacritic = DIACRITICS[f"{self.option['onset_style']}"]
            return self._add_diacritic(content, diacritic)

    @staticmethod
    def _add_diacritic(chars: str, diacritic: str) -> str:
        """Add diacritic to every character."""
        if chars:
            chars = ''.join([''.join([x, diacritic]) for x in chars])
        return chars

    @staticmethod
    def _add_diacritic_last(chars: str, diacritic: str) -> str:
        """Add diacritic to the last character."""
        if chars:
            chars = ''.join([chars, diacritic])
        return chars

    def _combine_coda(self) -> str:
        """Combine coda section: silent before, coda, silent after."""
        self.silent_before = self._combine_diacritic_coda(
            self.silent_before, 'silent_before')
        self.coda = self._combine_diacritic_coda(
            self.coda, 'coda')
        self.silent_after = self._combine_diacritic_coda(
            self.silent_after, 'silent_after')
        combined_coda = ''.join([
            self.silent_before,
            self.coda,
            self.silent_after
        ])
        return combined_coda

    def _combine_diacritic_coda(self, content: str, name: str) -> str:
        """Combine coda section with diacritic, depending on option."""
        style = f'{name}_style'
        if self.option[style] in ['plain']:
            return content
        elif self.option[style] in ['hide'] and name != 'coda':
            return ''
        elif self.option[style] in [
                'phinthu', 'yaamakkaan', 'kaaran']:
            diacritic = DIACRITICS[f'{self.option[style]}']
            if self.option[style] in ['phinthu', 'yaamakkaan']:
                add_method = self._add_diacritic
            elif self.option[style] in ['kaaran']:
                add_method = self._add_diacritic_last
            return add_method(content, diacritic)

    def all_tone(self, **word: Any) -> List[str]:
        """Return all five tone versions of the word.
        
        See parameters from spell_out."""
        result = []
        for tone_num in range(0, 5):
            word['tone'] = tone_num
            result.append(self.spell_out(**word))
        return result

def find_vowel_pair(vowel: str) -> str:
    """Return vowel length pair."""
    pair = VOWELS[vowel]['pair']
    if not pair:
        pair = vowel
    return pair

def find_vowel_length(vowel: str) -> str:
    """Return vowel length ('short' or 'long')."""
    return VOWELS[vowel]['length']

def find_letter_list() -> Dict[str, List[str]]:
    """Return all consonants, vowels and true clusters."""
    result = {
        'consonants': list(CONSONANTS.keys()),
        'vowels': list(VOWELS.keys()),
        'true clusters': list(CLUSTERS)}
    return result

def _consonant_by_property(property: str, property_name: str) -> List[str]:
    """Return list of consonant with provided properties.
    
    Ex. _consonant_by_property('coda_class', 'alive')
    """
    return [x for x in CONSONANTS if CONSONANTS[x][property] == property_name]