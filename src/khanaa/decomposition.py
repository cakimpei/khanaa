"""This module stores function that decompose word's components.

This function uses basic rule to decompose syllable,
so it won't cover some cases:
- เทอม (เอ) No เออ as เออ coda form yet
- ก็ will be None. (Don't have อ็ vowel in dict yet)
- มารถ will be มา+ร+ถ์
- ฤทธิ์ will have โอะ vowel
- Overall ฤ won't have correct sound ex. ทฤษ(ฎี)
- โพล will be พ+โอ+ล although it can be both this and พล+โอ when
judged from the writing
- Some short vowel use ไม้ไต่คู้ when it has coda, but when it also
has tone mark, ไม้ไต่คู้ will be delete so its form will look like
its long vowel pair.
- Some stylistic data are not saved such as if silent_before doesn't
have kaaran, so if we use the data with Kham, it might have
different form.
- Not covering phinthu, yamakkaan
"""

import re
from typing import Any, Dict, List, Tuple, Union

from khanaa.thai_script import (CLUSTERS, CONSONANTS, DIACRITICS,
    TONE_MARKERS, VOWEL_CHAR, VOWELS)
from khanaa.word import Word
from khanaa.utils import find_tone

TONE_MARK: str = ''.join([TONE_MARKERS[tone] for tone in TONE_MARKERS])
CODA_LIST: str = ''.join([char for char in CONSONANTS
    if CONSONANTS[char]['sound_coda']
    and char not in ['ย', 'ว']])

vowel_re = None
# should be created once by create_vowel_re()
# and after that its value won't be changed

def spelling_decompose(text: str) -> Union[Dict[str, Any], None]:
    """Find each part of the spelled word.

    Args:
        text: A Thai syllable such as เขียน (Also fine in case of
            multiple onsets such as มหา, แถลง, สมุทร)

    Returns:
        Syllable data in this structure:
            - 'data': onset, vowel, silent_before, coda, silent_after,
            tone
            - 'detail': tone_mark, leading_h, vowel_form, onset_index,
            onset_main
            - 'pref': (in some case)
                - vowel_coda_form
                - low_single_h_thoo
                - clear_vowel
                - clear_vowel_onset
                - clear_vowel_tone_mark
                - silent_after_style
            
        Or None if it can't be analyzed.
    """
    if not text:
        return

    global vowel_re
    if vowel_re == None:
        vowel_re = create_vowel_re()
    pref = {}

    tone_mark = analyze_tone_mark(text)
    no_sa, silent_after_last = split_silent_after(text)
    # no_sa is from no_silent_after

    vowel, silent_after, no_sa, vowel_type, vowel_form = analyze_vowel(no_sa)
    if not vowel:
        return

    if silent_after and not silent_after_last:
        pref.update({'silent_after_style': 'plain'})
    silent_after = ''.join([silent_after, silent_after_last])
    # remove tone mark after find vowel
    # because sometimes tone mark can help disambiguate the word
    # ex. สวน=ส+อัว+น or สว+โอะ+น? but ส่วน is only ส+อัว+น
    # but we don't want it while finding onset and coda
    no_sa = remove_tone(no_sa)
    
    coda, no_coda = analyze_coda(no_sa, vowel_type)
    onset, leading_h, onset_f, onset_b = analyze_onset(no_coda, vowel_form)
    # onset_f is onset char(s) that comes before front vowel such as
    # ส in สเตย์ while onset_b is onset char(s) that comes after it
    # such as ต
    if len(onset_f) + len(onset_b) == 2:
        pref.update(find_onset_pref(onset_f, onset_b, tone_mark))
    silent_before = analyze_silent_before(no_coda)

    # โอะ+ร > ออ+ร
    new_vowel, new_form = change_o_r(vowel, coda)
    if new_form:
        vowel = new_vowel
        vowel_form = new_form
        pref.update({'vowel_coda_form': {new_vowel: new_form}})

    # find tone number
    is_low_single_vague = Word._find_is_low_single_vague(True, onset)
    is_h_vague = Word._find_is_h_vague(True, onset)
    onset_index = Word._find_onset_index(is_low_single_vague,
        is_h_vague, onset, False, False, False)
    onset_main = Word._find_onset_main(onset, onset_index)
    tone = find_tone(onset_main, vowel, coda, tone_mark, leading_h)

    # ห+ต่ำเดี่ยว+ไม้โท
    if save_h_thoo(tone, leading_h):
        pref.update({'low_single_h_thoo': True})

    return {'data': {'onset': onset, 'vowel': vowel,
            'silent_before': silent_before, 'coda': coda,
            'silent_after': silent_after, 'tone': tone},
        'detail': {'tone_mark': tone_mark, 'leading_h': leading_h,
            'vowel_form': vowel_form, 'onset_index': onset_index,
            'onset_main': onset_main},
        'pref': pref}

def replace_vowel_re(form: str) -> str:
    """Add regular expression to vowel form.

    Args:
        form: Vowel form

    Returns:
        Regular expression string for the vowel form.
    """
    form: str = form.replace('+', f'[{TONE_MARK}]?')
    form = form.replace('-', '[ก-ฮ]+')
    form = ''.join(['^[ก-ฮ]*', form])
    return form

def create_vowel_re():
    """Create vowel regular expression dict to be used.

    Returns:
        Vowel dict in this structure:
            - 'vowel_jw' for vowel with ย, ว coda
            - 'vowel_coda' for vowel with coda
            - 'vowel_no_coda' for vowel without coda
            - 'ex_coda' for vowel with coda that should come after
            vowel_no_coda
            - 'ex_no_coda' for vowel without coda that should come
            after ex_no_coda
            
        Each vowel type contains vowels sorted by vowel form length
        and each vowel contains:
            - 'form' for vowel form
            - 're' for vowel regex
    """
    # find vowels for each vowel type because each vowel type will use
    # different regex
    vowel_re = {'vowel_jw': {}, 'vowel_coda': {}, 'vowel_no_coda': {}}
    for vowel in VOWELS:
        if (VOWELS[vowel]['form_no_coda']
                and VOWELS[vowel]['sound_coda'] in ['j', 'w']):
            vowel_re['vowel_jw'].update({vowel: VOWELS[vowel]['form_no_coda']})
        if VOWELS[vowel]['form_with_coda']:
            vowel_re['vowel_coda'].update({vowel: VOWELS[vowel]['form_with_coda']})
        if (VOWELS[vowel]['form_no_coda']
                and VOWELS[vowel]['sound_coda'] not in ['j', 'w']):
            vowel_re['vowel_no_coda'].update({vowel: VOWELS[vowel]['form_no_coda']})
    
    # these vowels should come last because they're invisible
    vowel_re['vowel_coda'].pop('อ')
    vowel_re['vowel_coda'].pop('โอะ')
    vowel_re['vowel_no_coda'].pop('อ')
    vowel_re.update({'ex_coda': {'โอะ': VOWELS['โอะ']['form_with_coda']}})
    vowel_re.update({'ex_no_coda': {'อ': VOWELS['อ']['form_no_coda']}})

    # sort vowels and create regex for each vowel
    for vowel_type, vowel_data in vowel_re.items():
        sorted_vowel = sorted(vowel_re[vowel_type],
            key=lambda vowel: len(vowel_re[vowel_type][vowel]), reverse=True)
        additional = ''
        if vowel_type == 'vowel_jw':
            additional = f'(?![์{TONE_MARK}])'
        elif vowel_type in ['vowel_coda', 'ex_coda']:
            additional = f'([ก-ฮ]+์)?[{CODA_LIST}](?![์{TONE_MARK}])'
        new_vowel_data = {}
        for vowel in sorted_vowel:
            pattern = re.compile(
                replace_vowel_re(vowel_data[vowel]) + additional)
            new_vowel_data.update({
                vowel: {
                    'form': vowel_data[vowel],
                    're': pattern}})
        vowel_re[vowel_type] = new_vowel_data
    return vowel_re

def split_silent_after(text: str) -> Tuple[str, str]:
    """Split silent after from the last position.

    This cannot find more than one silent_after char, so if the word
    has more than one, we'll catch it when we find the vowel.
    Because sometimes silent_after range can be ambiguous.
    (สเตย์=สต+เอ+ย์ we shouldn't include ต because เอ char but
    จันทร์ we should include ท but not น because อั char needs coda).

    As for why we don't find all silent_after only after find vowel,
    because this way we can still catch words like ฤทธิ์
    which has silent vowel char under silent mark.

    Args:
        text: Thai syllable

    Returns:
        text without silent_after, silent_after
    """
    no_silent_after: str = text
    silent_after: str = ''
    if text[-1] == DIACRITICS['kaaran']:
        result: List[str] = re.split(f'([ก-ฮ][{VOWEL_CHAR}]?์$)', text)
        if len(result) > 1:
            no_silent_after = result[0]
            silent_after = result[1].replace('์', '')
    return no_silent_after, silent_after

def analyze_tone_mark(text: str):
    """Find tone mark used.

    Args:
        text: The word

    Returns:
        Tone mark name
    """
    tone_mark = ''
    for char in TONE_MARK:
        if char in text:
            tone_mark = char
            break
    # because tone marks are difficult to see
    # we'll return their names instead
    for name, tone_char in TONE_MARKERS.items():
        if tone_mark == tone_char:
            tone_mark = name
            break
    return tone_mark

def analyze_vowel(text: str) -> Tuple[str, str, str, str, str]:
    """Find vowel in the word.

    Args:
        text: Thai syllable.

    Returns:
        vowel, silent_after, word without silent_after, vowel_type
    """
    all_vowels: List[str] = [char for char in text if char in VOWEL_CHAR]
    vowel, silent_after, no_silent_after, vowel_form = '', '', '', ''
    for vowel_type in vowel_re:
        result = analyze_vowel_form(text, all_vowels, vowel_type)
        if result[0]:
            vowel, silent_after, no_silent_after, vowel_form = result
            break
    return vowel, silent_after, no_silent_after, vowel_type, vowel_form

def analyze_vowel_form(text: str, all_vowels: List[str],
        vowel_type: str) -> Tuple[str, str, str, str]:
    """Find vowel in the word from one vowel type.

    Args:
        text: One Thai syllable/word
        vowel_type: From vowel_re

    Returns:
        Vowel form if vowel is found. Empty string if not found.
    """
    for vowel in vowel_re[vowel_type]:
        form = vowel_re[vowel_type][vowel]['form']
        pattern = vowel_re[vowel_type][vowel]['re']
        result = re.search(pattern, text)
        if result:
            # To make sure every vowel char is taken into account.
            # Even if we order our search by vowel form length,
            # because we search vowel with ย, ว before other type
            # of vowel, the word like เปลี่ยน will be matched with
            # อีย before เอีย.
            leftover = [char for char in all_vowels if char not in form]
            if leftover:
                # for ญาติ, เหตุ
                if (len(leftover) == 1
                        and leftover[0] in ['ิ', 'ุ']
                        and text[-1] in ['ิ', 'ุ']):
                    pass
                else:
                    continue
            split = re.split(pattern, text)
            silent_after = ''
            if split[-1]:
                # แสวง should be สว+แอ+ง not ส+แอว+(ง)
                if (vowel_type == 'vowel_jw'
                        and split[-1].find(DIACRITICS['kaaran']) == -1):
                    continue
                silent_after = split[-1].replace(DIACRITICS['kaaran'], '')
            return vowel, silent_after, result[0], form
    return '', '', '', ''

def analyze_coda(text: str, vowel_type: str) -> Tuple[str, str]:
    """Find coda. This assumes that there's no silent_after left.

    Args:
        text: Syllable without silent_after
        vowel_type: From vowel_re

    Returns:
        coda, text without coda
    """
    coda = ''
    if vowel_type in ['vowel_coda', 'ex_coda']:
        coda = text[-1]
        text = text[:-1]
    return coda, text

def remove_tone(text: str) -> str:
    """Remove tone mark.

    Args:
        text: Thai syllable.

    Returns:
        Thai syllable without tone mark.
    """
    for char in TONE_MARK:
        text = text.replace(char, '')
    return text

def analyze_onset(matched_text: str, vowel_form: str) -> Tuple[
        str, bool, str, str]:
    """Find onset.

    Args:
        matched_text: Word without coda and silent_after
        vowel_form: Form of the vowel ex. -+า

    Returns:
        Onset, leading_h, onset_front, onset_back
    """
    vowel_form = vowel_form.replace('+', '') # + is tone mark place
    char_before, char_after = vowel_form.split('-') # - is onset place
    pattern = f'(?<={char_before})[ก-ฮ]+(?={char_after})(?!์)'
    onset_back = re.search(re.compile(pattern), matched_text)[0]
    onset_back, leading_h = analyze_leading_h(onset_back)

    # check for onset before vowel such as ส from สเต็ก
    onset_front = ''
    if char_before:
        pattern_front = f'^[ก-ฮ]+(?={char_before})'
        found_onset = re.search(re.compile(pattern_front), matched_text)
        if found_onset:
            onset_front = found_onset[0]
    onset = ''.join([onset_front, onset_back])
    return onset, leading_h, onset_front, onset_back

def analyze_leading_h(onset: str) -> Tuple[str, bool]:
    """Find and separate ห นำ from onset.

    Args:
        onset: Onset characters

    Returns:
        Onset (without leading h), If this word has ห นำ
    """
    leading_h: bool = False
    if ('ห' in onset
            and len(onset) > onset.index('ห')+1
            and CONSONANTS[onset[onset.index('ห')+1]]['class']
                == 'low_single'):
        leading_h = True
        onset = onset.replace('ห', '')
    return onset, leading_h

def find_onset_pref(onset_front: str, onset_back: str,
        tone_mark: str) -> Dict[str, bool]:
    """Find preference data for onset chars.

    This function is used when we have two onset chars (ห นำ
    not included).

    Args:
        onset_front: Onset before of front vowel such as ส in สเตย์
        onset_back: Onset after front vowel such as ต in สเตย์
        tone_mark: Tone mark of the word.

    Returns:
        Onset preference data.
    """
    clear_vowel = True
    clear_vowel_onset = 'not_true_cluster'
    clear_vowel_tone_mark = False
    if tone_mark:
        if len(onset_back) == 2:
            clear_vowel_tone_mark = False
        elif len(onset_front) == 1:
            clear_vowel_tone_mark = True
    if onset_front + onset_back in CLUSTERS:
        if len(onset_back) == 2:
            clear_vowel_onset = 'not_true_cluster'
        elif len(onset_front) == 1:
            clear_vowel_onset = 'all'
    else:
        if len(onset_back) == 2:
            clear_vowel = False
        elif len(onset_front) == 1:
            clear_vowel = True
    return {'clear_vowel': clear_vowel,
        'clear_vowel_onset': clear_vowel_onset,
        'clear_vowel_tone_mark': clear_vowel_tone_mark}

def analyze_silent_before(text: str) -> str:
    """Find silent_before. This assumes text doesn't have coda.

    Args:
        text: Syllable without coda.

    Returns:
        silent_before
    """
    silent_before: str = ''
    if text[-1] == DIACRITICS['kaaran']:
        silent_before = text[-2]
    return silent_before

def change_o_r(vowel: str, coda: str) -> Tuple[str, str]:
    """Change vowel for อร as it's usually pronounced with ออ not โอะ.

    Args:
        vowel: Vowel with อ as placeholder.
        coda: Syllable coda.

    Returns:
        New vowel and new vowel form
    """
    form: str = ''
    if vowel == 'โอะ' and coda == 'ร':
        vowel = 'ออ'
        form = '-+'
    return vowel, form

def save_h_thoo(tone: int, h_present: bool) -> bool:
    """If ห นำ+อักษรต่ำเดี่ยว+ไม้โท is used, save it to pref.

    Args:
        tone: Tone number.
        h_present: If ห นำ is here.

    Returns:
        low_single_h_thoo pref.
    """
    low_single_h_thoo: bool = False
    if tone == 2 and h_present:
        low_single_h_thoo = True
    return low_single_h_thoo