# Changelog
All notable changes to this project will be documented in this file.

## [0.1.0] - 2024-03-30

### Added

- Kham, replacing SpellWord, with Kham.form replacing SpellWord.spell_out() and Kham.all_tone() replacing SpellWord.all_tone().
- Kham.ipa(), returning basic IPA pronunction data of the input.
- Kham.is_donee_end(), Kham.is_donor_end(), Kham.is_donor_start(), returning syllable boundary ambiguity data of the input.
- Kham.homophone(), returning a list of homophone
- Kham.data, returning all data
- New pref kwargs: split_true_cluster, split_false_cluster, split_leading_con, low_single_h_thoo.
- spelling_decompose(), returning spelling data of the input Thai syllable.

### Changed

- Checked syllable with 4/Jattawaa/rising tone will be spelled with Jattawaa tone mark, instead of previous -1 form.

### Deprecated

- SpellWord (replaced by Kham).

## [0.0.6] - 2022-05-30

### Added

- Option to select character that onset style will be applied (onset_style_apply in pref kwargs).

## [0.0.5] - 2022-05-26

### Added

- Option to make ฮ-single low onset cluster less ambiguous (obvious_h_low_single in pref kwargs).

## [0.0.4] - 2022-05-25

First release.