from khanaa.pronunciation import ThaiToIPA

IPA_RTGS = {
    "initial": {
        "ŋ": "ng",
        "t͡ɕ": "ch",
        "t͡ɕʰ": "ch",
        "j": "y"
    },
    "final": {
        "ŋ": "ng",
        "j": "i",
        "w": "o",
    },
    "vowel": {
        "ɯ": "ue",
        "ɛ": "ae",
        "ɔ": "o",
        "ɤ": "oe",
    }
}

def ipa_to_rtgs(ipa: ThaiToIPA) -> str:
    result = []
    for part in ipa.onset_ipa_list:
        # initial
        initial: str = part["onset"]
        if initial in IPA_RTGS['initial']:
            initial = IPA_RTGS['initial'][initial]
        initial = initial.replace("ʰ", "h")
        if initial == 'ʔ':
            initial = None
        result.append("".join(filter(None, [initial, part["glide"], part["vowel"]])))

    vowel = ipa.vowel_ipa
    if ipa.vowel_ipa[0] in IPA_RTGS["vowel"]:
        vowel = IPA_RTGS["vowel"][vowel[0]] + vowel[1:]
    result.append(vowel)
    
    if ipa.vowel_coda_ipa:
        vowel_coda = ipa.vowel_coda_ipa
        if vowel_coda in IPA_RTGS["final"]:
            vowel_coda = IPA_RTGS["final"][vowel_coda]
        result.append(vowel_coda)

    if ipa.coda_ipa:
        final = ipa.coda_ipa
        if ipa.coda_ipa in IPA_RTGS["final"]:
            final = IPA_RTGS["final"][ipa.coda_ipa]
        final = final.replace(u"\u031a", "")
        result.append(final)

    return "".join(result)