"""This module stores functions that check syllable's ambiguity."""

from khanaa.thai_script import CONSONANTS, DIACRITICS, VOWELS

def find_donee_end(vowel: str, silent_before: str, coda: str,
        silent_after: str, silent_before_style: str,
        silent_after_style: str) -> bool:
    """See details at Kham."""
    is_donee_end: bool = False
    if (VOWELS[vowel]['form_no_coda'] == VOWELS[vowel]['form_with_coda']
            and not coda
            and (not silent_before or silent_before_style == 'hide')
            and (not silent_after or silent_after_style == 'hide')
            and vowel not in ['อๅ']):
        is_donee_end = True
    return is_donee_end

def find_donor_end(vowel: str, silent_before: str, coda: str,
        silent_after: str, silent_before_style: str,
        silent_after_style: str, tone_mark: str,
        vowel_form: str) -> bool:
    """See details at Kham."""
    is_donor_end: bool = False
    if silent_after and silent_after_style == 'plain':
        is_donor_end = True
    elif silent_after and silent_after_style != 'hide':
        is_donor_end = False
    elif not coda and silent_before and silent_before_style == 'plain':
        is_donor_end = True
    elif coda and find_donor_end_coda(vowel, vowel_form, tone_mark):
        is_donor_end = True
    elif find_donor_end_jw(vowel, silent_before, silent_before_style,
            tone_mark):
        is_donor_end = True
    return is_donor_end

def find_donor_end_coda(vowel: str, vowel_form: str, tone_mark: str) -> bool:
    return (VOWELS[vowel]['form_no_coda'] == VOWELS[vowel]['form_with_coda']
        or (DIACRITICS['mai_taikhuu'] in VOWELS[vowel]['form_with_coda']
            and VOWELS[VOWELS[vowel]['pair']]['form_no_coda']
                == VOWELS[vowel]['form_with_coda'].replace(
                    DIACRITICS['mai_taikhuu'], '')
            and tone_mark)
        or vowel_form == '-+')

def find_donor_end_jw(vowel: str, silent_before: str,
        silent_before_style: str, tone_mark: str):
    return ((not silent_before or silent_before_style in ['plain', 'hide'])
        and VOWELS[vowel]['sound_coda'] in ['j', 'w']
        and vowel[-1] in ['ย', 'ว']
        and (DIACRITICS['mai_taikhuu'] not in vowel
            or tone_mark)
        and vowel[:-1].replace(DIACRITICS['mai_taikhuu'], '')
            in VOWELS
        and (VOWELS[vowel[:-1].replace(
                DIACRITICS['mai_taikhuu'], '')]['form_no_coda']
            == VOWELS[vowel[:-1].replace(
                DIACRITICS['mai_taikhuu'], '')]['form_with_coda']
            or vowel[:-1].replace(DIACRITICS['mai_taikhuu'], '')
                == 'เออ'))

def find_donor_start(onset: str, form: str) -> bool:
    """See details at Kham."""
    is_donor_start: bool = False
    if (len(onset) > 1
            and form[0] in CONSONANTS
            and CONSONANTS[form[0]]['sound_coda']
            and form[0] not in ['ห', 'ฮ']):
        is_donor_start = True
    return is_donor_start