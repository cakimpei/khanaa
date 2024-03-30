from itertools import product
from khanaa.thai_script import CONSONANTS, VOWELS

def find_same_sound_consonant(consonant: str, type: str) -> list[str]:
    """Find a list of consonants that have same sound as the input

    Args:
        consonant: a consonant character
        type: "onset" or "coda"

    Returns:
        List of consonants (including the input)
    """
    result = []
    if len(consonant) != 1:
        return result
    name: str = f"sound_{type}"
    sound: str = CONSONANTS.get(consonant)[name]
    for con in CONSONANTS:
        if CONSONANTS[con][name] == sound:
            result.append(con)
    
    return result

def find_same_sound_vowel(vowel: str) -> list[str]:
    """Find a list of vowels that have same sound as the input

    Args:
        vowel: a vowel with default อ

    Returns:
        List of vowels (including the input)
    """
    result = []
    data: str = VOWELS.get(vowel)
    for v in VOWELS:
        v_data = VOWELS[v]
        same_length: bool = data["length"] == v_data["length"]
        same_sound_vowel: bool = data["sound_vowel"] == v_data["sound_vowel"]
        same_sound_coda: bool = data["sound_coda"] == v_data["sound_coda"]
        if same_length and same_sound_vowel and same_sound_coda:
            result.append(v)
    
    return result

def find_homophone_product(onset: str, vowel: str, coda: str):
    """Find a product of inputs' homophone

    Args:
        onset: initial consonant (one or more character)
        vowel: a vowel with default อ
        coda: final consonant

    Returns:
        Product of possible tuples (onset, vowel, coda)
    """
    if len(onset) == 1:
        onsets = find_same_sound_consonant(onset, "onset")
    else:
        onsets = [onset]
    vowels = find_same_sound_vowel(vowel)
    codas = find_same_sound_consonant(coda, "coda")
    if not coda:
        codas.append("")
        if "อรร" in vowels:
            vowels.remove("อรร")
    elif "อรร" in vowels and "ร" in codas:
        codas.remove("ร")
        codas.append("")
    
    possibles = list(product(onsets, vowels, codas))
    
    if "อำ" in vowels:
        a_vowels = find_same_sound_vowel("อะ")
        m_codas = find_same_sound_consonant("ม", "coda")
        new_possibles = list(product(onsets, a_vowels, m_codas))
        possibles.extend(new_possibles)

    elif "อะ" in vowels and coda == "ม":
        possibles.append((onset, "อำ", ""))
    
    return possibles