"""This module contains functions that are used for spelling word."""

from typing import Any, Dict
from khanaa.thai_script import CONSONANTS, DIACRITICS

def combine(word: Dict[str, Any], pref: Dict[str, Any]) -> str:
    """Main function for combining word data and spelling word.

    Args:
        word: Word data.
        pref: Preference data.

    Returns:
        Spelled form of the word.
    """
    index_after_vowel: int = find_index_after_vowel(word._onset,
        word._is_vowel_vague, word._is_low_single_vague,
        word._is_h_vague, word._use_leading_h)
    onset_convert: str = convert_onset(word._onset_main,
        word._use_pair_onset, word._use_leading_h)
    combined_onset_vowel: str = join_onset_vowel(index_after_vowel,
        word._use_leading_h, pref['onset_style'], pref['onset_style_apply'],
        word._vowel_form, word._onset, word._onset_index,
        onset_convert)
    combined_coda: str = combine_coda(word._silent_before,
        word._coda, word._silent_after, pref)
    combined: str = ''.join([combined_onset_vowel, combined_coda])
    combined = delete_taikhuu(combined, word._tone_mark)

    return combined.replace('+', word._tone_mark)

def find_index_after_vowel(onset: str, is_vowel_vague: bool,
        is_low_single_vague: bool, is_h_vague: bool,
        use_leading_h: bool) -> int:
    """Return index_after_vowel.
    
    index_after_vowel is the index of onset that
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
    index_after_vowel: int = 0
    if len(onset) > 2:
        index_after_vowel = -2
    elif is_vowel_vague:
        index_after_vowel = -1
    elif is_low_single_vague and use_leading_h:
        index_after_vowel = -1
    elif is_h_vague and use_leading_h:
        index_after_vowel = -1
    
    return index_after_vowel

def convert_onset(onset_main, use_pair_onset, use_leading_h):
    """Convert onset to its pair or add ห นำ if it's needed."""
    onset_convert: str = onset_main
    if use_pair_onset:
        onset_convert = CONSONANTS[onset_main]['pair']
    elif use_leading_h:
        onset_convert = ''.join(['ห', onset_main])
    return onset_convert

def join_onset_vowel(index_after_vowel: int, use_leading_h: bool,
        onset_style: str, onset_style_apply: str, vowel_form: str,
        onset: str, onset_index: int, onset_main: str) -> str:
    """Join onsets and vowel according to the index provided."""
    combined_onset: str = join_onset(onset, onset_index, onset_main)
    index_after_vowel: int = find_new_index(use_leading_h, onset_index,
        index_after_vowel)

    before_vowel: str = combine_diacritic(onset_style,
        combined_onset[:index_after_vowel])
    after_vowel: str = combined_onset[index_after_vowel:]
    if len(after_vowel) > 1:
        diacritic_index: int = -1
        if (use_leading_h and onset_style_apply == 'not_h'):
            diacritic_index: int = -2
        after_vowel = ''.join([
            combine_diacritic(onset_style, after_vowel[:diacritic_index]),
            after_vowel[diacritic_index:]
        ])
    
    combined: str = ''.join([
        before_vowel,
        vowel_form.replace('-', after_vowel)
    ])
    return combined

def join_onset(onset: str, onset_index: int, onset_convert: str) -> str:
    """Join the form of main onset with other onsets."""
    prior: str = onset[:onset_index]
    latter: str = onset[onset_index+1:]
    if onset_index == -1:
        latter = ''
    combined_onset: str = ''.join([prior, onset_convert, latter])
    return combined_onset

def find_new_index(use_leading_h: bool, onset_index: int, index_after_vowel: int) -> int:
    """Shift index leftward if ห นำ is used."""
    if use_leading_h and onset_index >= index_after_vowel:
        index_after_vowel -= 1
    return index_after_vowel

def combine_diacritic(onset_style: str, content: str) -> str:
    """Combine diacritic to the onset.
    
    If option specifies that we should add diacritic to onset,
    add diacritic to every character in onset except the last one.
    """
    if onset_style in ['plain']:
        return content
    if onset_style in ['phinthu', 'yaamakkaan', 'kaaran']:
        diacritic = DIACRITICS[f"{onset_style}"]
        return add_diacritic(content, diacritic)
    raise ValueError('onset_style not recognized')

def add_diacritic(chars: str, diacritic: str) -> str:
    """Add diacritic to every character."""
    if chars:
        chars = ''.join([''.join([x, diacritic]) for x in chars])
    return chars

def add_diacritic_last(chars: str, diacritic: str) -> str:
    """Add diacritic to the last character."""
    if chars:
        chars = ''.join([chars, diacritic])
    return chars

def combine_coda(silent_before: str, coda: str, silent_after: str,
        pref: Dict[str, Any]) -> str:
    """Combine coda section: silent before, coda, silent after."""
    silent_before = combine_diacritic_coda(pref,
        silent_before, 'silent_before')
    coda = combine_diacritic_coda(pref, coda, 'coda')
    silent_after = combine_diacritic_coda(pref,
        silent_after, 'silent_after')

    combined_coda: str = ''.join([silent_before, coda, silent_after])
    return combined_coda

def combine_diacritic_coda(pref: Dict[str, Any], content: str,
        name: str) -> str:
    """Combine coda section with diacritic, depending on option."""
    style: str = f'{name}_style'
    if pref[style] in ['plain']:
        return content
    elif pref[style] in ['hide'] and name != 'coda':
        return ''
    elif pref[style] in [
            'phinthu', 'yaamakkaan', 'kaaran']:
        diacritic = DIACRITICS[f'{pref[style]}']
        if pref[style] in ['phinthu', 'yaamakkaan']:
            add_method = add_diacritic
        elif pref[style] in ['kaaran']:
            add_method = add_diacritic_last
        return add_method(content, diacritic)
    else:
        raise ValueError(f'{style} not recognized')

def delete_taikhuu(combined: str, tone_mark: str) -> str:
    """Delete mai taikhuu if there's also a tone marker."""
    mai_taikhuu: str = DIACRITICS['mai_taikhuu']
    if tone_mark and combined.find(mai_taikhuu) != -1:
        combined = combined.replace(mai_taikhuu, '')
    return combined