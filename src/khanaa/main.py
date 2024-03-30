from typing import Any, List

from khanaa.combination import Combination
from khanaa.thai_script import DIACRITICS

class Kham:
    """Spell Thai word from information provided.
    
    Attributes:
        form (str): Spelled form of the word.
        data (dict[str, Any]): All information about this word.
        onset (str): พยัญชนะต้น
        onset_index (int): Index of onset used when calculating tone.
        onset_main (str): Main onset used when calculating tone.
        onset_class (str): high, mid, low_pair, low_single
        vowel (str): สระ
        vowel_length (str): short, long
        silent_before (str): ตัวการันต์ก่อนตัวสะกด
        coda (str): ตัวสะกด
        coda_class (str): dead (ก, บ, ด) or alive (the rest).
        silent_after (str): ตัวการันต์หลังตัวสะกด
        tone (int): เสียงวรรณยุกต์
        is_possible_tone (bool): Check if the input tone is possible
            with this word.
        tone_realized (int): Tone in spelled word, different from tone
            if tone is -1 or not possible with the word.
        use_leading_h (bool): Check if ห นำ is used.
        use_pair_onset (bool): Check if onset is changed to
            its pair onset.
        tone_mark (str): รูปวรรณยุกต์
        is_checked (bool): Check if the word is checked (คำตาย).
    
    Methods:
        ipa (str): Return basic IPA pronunciation of the word.
        is_donee_end (bool): Check if onset of the following word
            can be interpreted as this word's coda.
        is_donor_end (bool): Check if coda of this word can be
            interpreted as the following word onset.
        is_donor_start (bool): Check if onset of this word can be
            interpreted as coda of the preceding word.
        all_tone (list[str]): Return 0-4 tone version of the word.
        homophone (list[str]): Return a list of homophone
    """

    def __init__(
            self,
            onset: str,
            vowel: str,
            silent_before: str = '',
            coda: str = '',
            silent_after: str = '',
            tone: int = -1,
            **pref: Any) -> None:
        """Init Kham.

        None of the keyword arguments here are required.

        Find all available Thai consonants, vowels, and true clusters
        from find_letter_list()

        Examples:

            spell = Kham(onset='ข', vowel='เอีย', coda='น')

            result = spell.form

            result should be 'เขียน'

            spell = Kham('สม', 'อุ', '', 'ท', 'ร', -1,
                silent_after_style='plain')

            result = spell.form

            result should be 'สมุทร'

        Args:
            onset: Initial consonant(s), can be one or more.
                (พยัญชนะต้น)
            vowel: Vowel (สระ). Write the vowel with อ as
                a placeholder. If vowel has ตัวสะกด ย, ว or j, w coda,
                put them here together with vowel. Ex. อา, ไอ, อาว, อัย
            silent_before: Silent consonant(s) before coda.
                Defaults to ''.
            coda: Final consonant, excluding j, w (ตัวสะกด
                ไม่รวม ย, ว). Defaults to ''.
            silent_after: Silent consonant(s) after coda.
                Defaults to ''.
            tone: Tone (เสียงวรรณยุกต์). -1 not specified,
                0 mid สามัญ, 1 low เอก, 2 falling โท, 3 high ตรี,
                4 rising จัตวา. Defaults to -1.

        Keyword Args:
            clear_vowel (bool): Turn on/off option to put the first
                consonant in front of vowel to make the pronunciation
                less ambiguous.
                Option: False/off (ex. เชว), True/on (ex. ชเว).
                Default: True
            clear_vowel_onset (str): If clear_vowel is turned on,
                select onset cluster type that clear_vowel will be
                used with.
                Option: 'not_true_cluster' (true cluster คำควบกล้ำแท้
                won't be separated ex. เกวน ชเวน), 'all' (ex. กเวน ชเวน)
                Default: 'not_true_cluster'
            clear_vowel_tone_mark (bool): If clear_vowel is turned on,
                select if clean_vowel will be used with the word with
                tone marker or not.
                Option: False/not use (ex. คเว เคว่), True/use
                (ex. คเว คเว่).
                Default: False
            split_true_cluster (bool): Turn on/off option to treat
                true cluster onset as separate syllables. (เลือกว่า
                จะให้คำควบกล้ำแท้ออกเสียง/ผันวรรณยุกต์ควบกัน หรือว่า
                ออกเสียง/ผันวรรณยุกต์แบบเรียงพยางค์)
                Option: False/off (ex. กร+อุ+น+1 = กรุ่น = กฺรุ่น),
                True/on (ex. กร+อุ+น+1 = กหรุ่น = กะ-หฺรุ่น)
                Default: False
            split_false_cluster (bool): Turn on/off option to treat
                false cluster onset as separate syllables.
                Option: False/off (ex. ศร+อี = ศรี = สี,
                ศร+อา = ศรา = สา), True/on (ex. ศร+อี = ศรี = สะ-รี,
                ศร+อา = ศรา = สะ-รา)
                Default: False
            split_leading_con (bool): Turn on/off option to treat
                leading consonant cluster (อักษรนำ) as separate
                syllable.
                Option: False/off (ex. สล+อัว = สลัว = สะ-หฺลัว,
                สล+โอ+ว์ = สโลว์ = สะ-โหฺล), True/on (ex. สล+อัว = สลัว
                = สะ-ลัว, สล+โอ+ว์ = สโลว์ = สะ-โล
                Default: False
            obvious_low_singles (bool): Turn on/off option to make
                single low-single low onset cluster less ambiguous.
                Option: False/off (ex. หนวี่), True/on (ex. นหวี่).
                Default: True
            obvious_h_low_single (bool): Turn on/off option to make
                ฮ-single low onset cluster less ambiguous.
                Option: False/off (ex. หว่า), True/on (ex. ฮหว่า).
                Default: True
            onset_style (str): Select onset style.
                Option: 'plain' (no diacritic), 'phinthu' (ใส่พินทุ),
                'yaamakkaan' (ใส่ยามักการ), 'kaaran' (ใส่การันต์)
                Default: 'plain'
            onset_style_apply (str): Select character that onset style
                will be applied.
                Option: 'not_h' (ห นำ won't have diacritic), 'h' (ห นำ
                will have diacritic)
                Default: 'not_h'
            silent_before_style (str): Select style of the silent
                consonant that comes before the coda.
                Option: 'plain', 'phinthu', 'yaamakkaan', 'kaaran',
                'hide'
                Default: 'kaaran'
            coda_style (str): Select coda style.
                Option: 'plain', 'phinthu', 'yaamakkaan', 'kaaran'
                Default: 'plain'
            silent_after_style (str): Select style of the silent
                consonant that comes after the coda.
                Option: 'plain', 'phinthu', 'yaamakkaan', 'kaaran',
                'hide'
                Default: 'kaaran'
            vowel_no_coda (str): Select what we should do when vowels
                (เออะ, เอียะ, เอือะ, อัวะ) without its own coda form
                have coda.
                Option: 'pair' (use its pair form ex. เอียะ + น
                => เอียน), 'silent_after' (push the coda to
                silent_after ex. เอียะ + น => เอียะน์)
                Default: 'pair'
            vowel_coda_form (dict[str, str]): Select specific
                vowel form to use when coda is present. Put vowel in
                dict key and put vowel form in its value.
                In vowel form, - is the consonant position and + is
                the tone marker position.
                Example: vowel_coda_form={'เออ': 'เ-+อ'} (the result
                will be, for example, เดอน instead of the default เดิน)
            vowel_length (str): Select vowel length.
                Option: 'input' (same as input), 'short' (if long vowel
                is in the input, the result will be with
                a short vowel), 'long' (vice versa)
                Default: 'input'
            vowel_pair_form (dict[str, str]): Select specific
                vowel pair form to use when the length is specified.
                Example: vowel_length='short',
                vowel_pair_form={'อาย': 'อัย'}
                (อาย will be shorten to อัย instead of the default ไอ)
            low_single_h_thoo (bool): Turn on/off option to use
                leading h + mai thoo for word with low single onset and
                falling tone.
                Option: False/off (ex. ม+อะ+น+2=มั่น), True/on
                (ex. ม+อะ+น+2=หมั้น)
                Default: False
        """
        self._spell = Combination(onset, vowel, silent_before, coda,
            silent_after, tone, **pref)
        self.onset: str = self._spell._onset
        self.onset_index: int = self._spell._onset_index
        self.onset_main: str = self._spell._onset_main
        self.onset_class: str = self._spell._onset_class
        self.vowel: str = self._spell._vowel
        self.vowel_length: str = self._spell._vowel_length
        self.silent_before: str = self._spell._silent_before
        self.coda: str = self._spell._coda
        self.coda_class: str = self._spell._coda_class
        self.silent_after: str = self._spell._silent_after
        self.tone: int = self._spell._tone
        self.is_possible_tone: bool = self._spell._is_possible_tone
        self.tone_realized: int = self._spell._tone_realized
        self.use_leading_h: bool = self._spell._use_leading_h
        self.use_pair_onset: bool = self._spell._use_pair_onset
        self.tone_mark: str = self._spell._tone_mark
        self.is_checked: bool = self._spell._is_checked

        self.form = self._spell.form

    def __repr__(self) -> str:
        letters = [self.onset, self.vowel]
        if self.silent_before:
            letters.append(self.silent_before + DIACRITICS['kaaran'])
        if self.coda:
            letters.append(self.coda)
        if self.silent_after:
            letters.append(self.silent_after + DIACRITICS['kaaran'])

        letters.append(str(self.tone))
        letter_phrase = '+'.join(letters)

        return repr(' '.join([self.form, '=', letter_phrase]))

    def ipa(self) -> str:
        """Return basic IPA pronunciation of the spelled syllable.
        
        Ex. เขียน kʰ iaː n ˩˩˦, วลี w aʔ ˦˥ . l iː ˧

        Things not supported:
            - Stress: It depends on word level rather than syllable
            level. Also no vowel and tone reduction.
            - Irregular reading: ม+ไอ+3=ไม้=maj˦˥ (short vowel)
            instead of maːj˦˥ (long vowel) as in real world.
            - Yaamakkaan pronunciation
        
        Notes:
            - In the default setting, onsets being คำควบกล้ำแท้
            คำควบกล้ำไม่แท้ อักษรนำ are taken into account for tone
            calculation. So สล+อัว+-1=สลัว=saʔ˨˩.luaː˩˩˦ and
            สล+โอ+ว์+-1=สโลว์=saʔ˨˩.loː˩˩˦. But we can change this in
            split_leading_con so that สล+โอ+ว์+-1=สโลว์=saʔ˨˩.loː˧.
        """
        return self._spell.reading

    def is_donee_end(self) -> bool:
        """Return True if onset after this word can be seen as its coda.
        
        This function will return True if this word doesn't have coda,
        but if it is followed by word with more than one onset,
        the beginning onset of the following word can be interpreted
        as a coda of this word.
        
        Ex. ตา will return True. If ตา is followed by กลม, it will
        be ambiguous if the words ตากลม is ตา+กลม or ตาก+ลม.
        """
        return self._spell.is_donee_end

    def is_donor_end(self) -> bool:
        """Return True if coda can be seen as following word's onset.
        
        This function will return True if this word has coda (or
        some kind of unmarked silent_before or silent_after) and
        if this word is followed by another word, this coda can be
        interpreted as one of the onsets of the following word.

        Ex. ตาก will return True. If ตาก is followed by ลม, it will
        be ambiguous if the words ตากลม is ตา+กลม or ตาก+ลม.
        """
        return self._spell.is_donor_end

    def is_donor_start(self) -> bool:
        """Return True if onsets can be seen as precede word's coda.
        
        This function will return True if this word has more than
        one onsets, and if this word follows 'open end' word, the first
        onset of this word can be interpreted as coda of the word
        that comes before.

        Ex. กลม will return True. If the word ตา is followed by กลม,
        it will be ambiguous if the words ตากลม is ตา+กลม or ตาก+ลม.
        """
        return self._spell.is_donor_start
    
    def all_tone(self) -> List[str]:
        """Return 0-4 tone version of the word.
        
        Notes:
            - Now empty string will be the result if the word is not
            possible with that tone.
            Ex. ['', 'กะ', 'ก้ะ', 'ก๊ะ', 'ก๋ะ']
        """
        return self._spell.all_tone
    
    def homophone(self) -> List[str]:
        """Return a list of the word's homophone
        
        Notes:
            - The list also includes the original word
            - Silent characters are not included
        """
        return self._spell.homophone
    
    @property
    def data(self) -> dict[str, Any]:
        result = {attr: self.__dict__[attr] for attr in self.__dict__}
        result.pop("_spell")
        result.update({
            'ipa': self.ipa(),
            'is_donee_end': self.is_donee_end(),
            'is_donor_end': self.is_donor_end(),
            'is_donor_start': self.is_donor_start(),
            'all_tone': self.all_tone(),
            'homophone': self.homophone(),
        })
        return result