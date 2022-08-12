from typing import Dict, List, Tuple

from khanaa.thai_script import (CLUSTERS, CONSONANTS, TONE_NOT_AVAILABLE,
    VOWELS, TONES)

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
    result: Dict[str, List[str]] = {
        'consonants': list(CONSONANTS.keys()),
        'vowels': list(VOWELS.keys()),
        'true clusters': list(CLUSTERS)}
    return result

def letter_by_property(letter_dict: Dict[str, Dict[str, str]],
        property: str, property_name: str) -> List[str]:
    """Return list of letters with provided properties.
    
    Ex. letter_by_property(CONSONANTS, 'coda_class', 'alive')
    """
    return [letter for letter in letter_dict
        if letter_dict[letter][property] == property_name]

def check_checked(vowel: str, coda: str) -> bool:
    """Check if the word is checked (dead) or not.
    
    Checked word in Thai:
    - Has no coda, short length (and no hidden coda like ไอ)
    - Has dead class coda"""
    checked: bool = False
    if (not coda
            and VOWELS[vowel]['length'] == 'short'
            and not VOWELS[vowel]['sound_coda']
        ):
        checked = True
    elif (coda
            and CONSONANTS[coda]['coda_class'] == 'dead'
        ):
        checked = True
    return checked

def find_tone_data(onset: str, vowel: str,
        coda: str) -> Tuple[str, str, str]:
    """Return onset_class, alive_dead, length.
    
    onset accepts only one character."""
    onset_class: str = CONSONANTS[onset]['class']
    if onset_class in ['low_pair', 'low_single']:
        onset_class = 'low'
    alive_dead: str = 'dead' if check_checked(
        vowel, coda) else 'alive'
    length: str = VOWELS[vowel]['length']
    return onset_class, alive_dead, length

def find_tone_phrase(onset_class: str, alive_dead: str, length: str):
    """Return word detail in format that is used in TONES."""
    word_detail: str
    if onset_class in ['high', 'low'] and alive_dead == 'dead':
        word_detail = f'{onset_class} {length} {alive_dead}'
    else:
        word_detail = f'{onset_class} {alive_dead}'
    return word_detail

def find_tone(onset: str, vowel: str, coda: str = '',
        tone_marker: str = '', h_present: bool = False):
    """Find what tone (เสียงวรรณยุกต์) this syllable has.
    
    onset accepts only one character.
    tone_marker can be '' (not present), 'mai_eek', 'mai_thoo',
        'mai_trii', 'mai_jattawaa'
    h_present can be True (ห นำ is present) or False

    return -1 (not valid), 0 (สามัญ), 1 (เอก), 2 (โท), 3 (ตรี), 4 (จัตวา)
    """
    tone_num: int = -1
    onset_class, alive_dead, length = find_tone_data(onset, vowel, coda)
    if h_present and onset_class == 'low':
        onset_class = 'high'
    tone_info: str = find_tone_phrase(onset_class, alive_dead, length)

    for tone in TONES:
        if (tone_info in TONES[tone]
                and not (tone in TONE_NOT_AVAILABLE
                    and tone_info in TONE_NOT_AVAILABLE[tone])
                and TONES[tone][tone_info] == ['', tone_marker]):
            tone_num = tone
            break

    return tone_num