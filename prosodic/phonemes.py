from .imports import *


class PhonemeClass(Entity):
    prefix = 'phon'

    @profile
    def __init__(self, txt, **kwargs):
        super().__init__(txt, **kwargs)

    @cached_property
    def is_vowel(self):
        if hasattr(self, 'cons') and self.cons > 0:
            return False
        if hasattr(self, 'cons') and self.cons < 1:
            return True
        return None

    def to_json(self):
        resd = super().to_json()
        resd['_class'] = 'Phoneme'
        resd.pop('children')
        return resd


@cache
@profile
def get_phoneme_featuretable():
    import panphon
    ft = panphon.FeatureTable()
    return ft


@cache
@profile
def Phoneme(txt, **kwargs):
    phon = txt
    ft = get_phoneme_featuretable()
    phonl = ft.word_fts(phon)
    if not phonl:
        # logger.error(f'What is this phoneme? {phon}')
        if phon in get_ipa_info():
            phond = get_ipa_info().get(phon, {})
        else:
            logger.error(
                f'What is this phoneme? No features found for it: {phon}')
            phond = {}
    else:
        phond = phonl[0].data
    phonobj = PhonemeClass(phon, **phond)
    return phonobj


@cache
def get_ipa_info():
    ipa = {}
    ipakey = ['approx', 'cons', 'son', 'syll', 'constr', 'spread', 'voice', 'long', 'cont_acoust', 'cont_artic', 'delrel', 'lat', 'nas',
              'strid', 'tap', 'trill', 'coronal', 'dorsal', 'labial', 'labiodental', 'ant', 'dist', 'back', 'front', 'high', 'low', 'tense', 'round']
    ipa['p'] = [False, True, False, False, False, False, False, None, False, False, False, False, False,
                False, False, False, False, False, True, False, True, False, False, None, False, False, None, False]
    ipa['m'] = [False, True, True, False, False, False, True, None, True, False, False, False, True,
                False, False, False, False, False, True, False, True, False, False, None, False, False, None, False]
    ipa['pʰ'] = [False, True, False, False, False, True, False, None, False, False, False, False, False,
                 False, False, False, False, False, True, False, True, False, False, None, False, False, None, False]
    ipa['t'] = [False, True, False, False, False, False, False, None, False, False, False, False, False,
                False, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
    ipa['b'] = [False, True, False, False, False, False, True, None, False, False, False, False, False,
                False, False, False, False, False, True, False, True, False, False, None, False, False, None, False]
    ipa['d'] = [False, True, False, False, False, False, True, None, False, False, False, False, False,
                False, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
    ipa['k'] = [False, True, False, False, False, False, False, None, False, False, False, False, False,
                False, False, False, False, True, False, False, False, False, True, None, True, False, None, False]
    ipa['d̪'] = [False, True, False, False, False, False, True, None, False, False, False, False, False,
                 False, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
    ipa['t̪'] = [False, True, False, False, False, False, False, None, False, False, False, False, False,
                 False, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
    ipa['n'] = [False, True, True, False, False, False, True, None, True, False, False, False, True,
                False, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
    ipa['ɳ'] = [False, True, True, False, False, False, True, None, True, False, False, False, True,
                False, False, False, True, False, False, False, False, False, False, None, False, False, None, False]
    ipa['ɲ'] = [False, True, True, False, False, False, True, None, True, False, False, False, True,
                False, False, False, True, True, False, False, False, True, False, None, True, False, None, False]
    ipa['ɡ'] = [False, True, False, False, False, False, True, None, False, False, False, False, False,
                False, False, False, False, True, False, False, False, False, True, None, True, False, None, False]
    ipa['f'] = [False, True, False, False, False, False, False, None, True, True, False, False, False,
                False, False, False, False, False, True, True, True, False, False, None, False, False, None, False]
    ipa['v'] = [False, True, False, False, False, False, True, None, True, True, False, False, False,
                False, False, False, False, False, True, True, True, False, False, None, False, False, None, False]
    ipa['ʃ'] = [False, True, False, False, False, False, False, None, True, True, False, False, False,
                True, False, False, True, False, False, False, False, True, False, None, False, False, None, False]
    ipa['s'] = [False, True, False, False, False, False, False, None, True, True, False, False, False,
                True, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
    ipa['z'] = [False, True, False, False, False, False, True, None, True, True, False, False, False,
                True, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
    ipa['ʒ'] = [False, True, False, False, False, False, True, None, True, True, False, False, False,
                True, False, False, True, False, False, False, False, True, False, None, False, False, None, False]
    ipa['j'] = [True, False, True, False, False, False, True, None, True, True, False, False, False,
                False, False, False, True, True, False, False, False, False, False, None, True, False, None, False]
    ipa['ɦ'] = [False, True, False, False, False, True, True, None, True, True, False, False, False, False,
                False, False, False, False, False, False, False, False, False, None, False, False, None, False]
    ipa['h'] = [False, True, False, False, False, True, False, None, True, True, False, False, False,
                False, False, False, False, False, False, False, False, False, False, None, False, False, None, False]
    ipa['q'] = [False, True, False, False, False, False, False, None, False, False, False, False, False,
                False, False, False, False, True, False, False, False, False, True, None, False, False, None, False]
    ipa['ɸ'] = [False, True, False, False, False, False, False, None, True, True, False, False, False,
                False, False, False, False, False, True, False, True, False, False, None, False, False, None, False]
    ipa['ʀ'] = [True, True, True, False, False, False, True, None, True, True, False, False, False,
                False, False, True, False, True, False, False, False, False, True, None, False, False, None, False]
    ipa['ʁ'] = [False, True, False, False, False, False, True, None, True, True, False, False, False,
                False, False, False, False, True, False, False, False, False, True, None, False, False, None, False]
    ipa['ɣ'] = [False, True, False, False, False, False, True, None, True, True, False, False, False,
                False, False, False, False, True, False, False, False, False, True, None, True, False, None, False]
    ipa['ɬ'] = [False, True, False, False, False, False, False, None, True, True, False, True, False,
                False, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
    ipa['ɮ'] = [False, True, False, False, False, False, True, None, True, True, False, True, False,
                False, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
    ipa['x'] = [False, True, False, False, False, False, False, None, True, True, False, False, False,
                False, False, False, False, True, False, False, False, False, True, None, True, False, None, False]
    ipa['ʤ'] = [False, True, False, False, False, False, True, None, False, False, True, False, False,
                True, False, False, True, False, False, False, False, True, False, None, False, False, None, False]
    ipa['ʧ'] = [False, True, False, False, False, False, False, None, False, False, True, False, False,
                True, False, False, True, False, False, False, False, True, False, None, False, False, None, False]
    ipa['ð'] = [False, True, False, False, False, False, True, None, True, True, False, False, False,
                False, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
    ipa['θ'] = [False, True, False, False, False, False, False, None, True, True, False, False, False,
                False, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
    ipa['β'] = [False, True, False, False, False, False, True, None, True, True, False, False, False,
                False, False, False, False, False, True, False, True, False, False, None, False, False, None, False]
    ipa['ç'] = [False, True, False, False, False, False, False, None, True, True, False, False, False,
                False, False, False, True, True, False, False, False, True, False, None, True, False, None, False]
    ipa['ʂ'] = [False, True, False, False, False, False, False, None, True, True, False, False, False,
                True, False, False, True, False, False, False, False, False, False, None, False, False, None, False]
    ipa['ʐ'] = [False, True, False, False, False, False, True, None, True, True, False, False, False,
                True, False, False, True, False, False, False, False, False, False, None, False, False, None, False]
    ipa['l'] = [True, True, True, False, False, False, True, None, True, True, False, True, False, False,
                False, False, True, False, False, False, True, False, False, None, False, False, None, False]
    ipa['r'] = [True, True, True, False, False, False, True, None, True, True, False, False, False,
                False, False, True, True, False, False, False, True, False, False, None, False, False, None, False]
    ipa['ɾ'] = [True, True, True, False, False, False, True, None, True, True, False, False, False,
                False, True, False, True, False, False, False, True, False, False, None, False, False, None, False]
    ipa['ɥ'] = [True, False, True, False, False, False, True, None, True, True, False, False, False,
                False, False, False, True, True, True, False, False, False, False, None, True, False, None, True]
    ipa['ʔ'] = [False, True, False, False, True, False, False, None, False, False, False, False, False,
                False, False, False, False, False, False, False, False, False, False, None, False, False, None, False]
    ipa['ŋ'] = [False, True, True, False, False, False, True, None, True, False, False, False, True,
                False, False, False, False, True, False, False, False, False, True, None, True, False, None, False]
    ipa['ɻ'] = [True, True, True, False, False, False, True, None, True, True, False, False, False,
                False, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
    ipa['ħ'] = [False, True, False, False, False, False, False, None, True, True, False, False, False,
                False, False, False, False, True, False, False, False, False, True, None, False, True, None, False]
    ipa['χ'] = [False, True, False, False, False, False, False, None, True, True, False, False, False,
                False, False, False, False, True, False, False, False, False, True, None, False, False, None, False]
    ipa['n̪'] = [False, True, True, False, False, False, True, None, True, False, False, False, True,
                 False, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
    ipa['kʰ'] = [False, True, False, False, False, True, False, None, False, False, False, False, False,
                 False, False, False, False, True, False, False, False, False, True, None, True, False, None, False]
    ipa['tʰ'] = [False, True, False, False, False, True, False, None, False, False, False, False, False,
                 False, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
    ipa['ʈ'] = [False, True, False, False, False, False, False, None, False, False, False, False, False,
                False, False, False, True, False, False, False, False, False, False, None, False, False, None, False]
    ipa['ʈʰ'] = [False, True, False, False, False, True, False, None, False, False, False, False, False,
                 False, False, False, True, False, False, False, False, False, False, None, False, False, None, False]
    ipa['ɖ'] = [False, True, False, False, False, False, True, None, False, False, False, False, False,
                False, False, False, True, False, False, False, False, False, False, None, False, False, None, False]
    ipa['ɖʰ'] = [False, True, False, False, False, True, True, None, False, False, False, False, False,
                 False, False, False, True, False, False, False, False, False, False, None, False, False, None, False]
    ipa['ʝ'] = [False, True, False, False, False, False, True, None, True, True, False, False, False,
                False, False, False, False, True, False, False, False, True, False, None, True, False, None, False]
    ipa['kʷ'] = [False, True, False, False, False, False, False, None, False, False, False, False, False,
                 False, False, False, False, True, True, False, False, False, True, None, True, False, None, True]
    ipa['gʷ'] = [False, True, False, False, False, False, True, None, False, False, False, False, False,
                 False, False, False, False, True, True, False, False, False, True, None, True, False, None, True]
    ipa['ɢ'] = [False, True, False, False, False, False, True, None, False, False, False, False, False,
                False, False, False, False, True, False, False, False, False, True, None, False, False, None, False]
    ipa['kʲ'] = [False, True, False, False, False, False, False, None, False, False, False, False, False,
                 False, False, False, True, True, False, False, False, False, False, None, True, False, None, False]
    ipa['gʲ'] = [False, True, False, False, False, False, True, None, False, False, False, False, False,
                 False, False, False, True, True, False, False, False, False, False, None, True, False, None, False]
    ipa['ɱ'] = [False, True, True, False, False, False, True, None, True, False, False, False, True,
                False, False, False, False, False, True, True, True, False, False, None, False, False, None, False]
    ipa['ʋ'] = [True, True, True, False, False, False, True, None, True, True, False, False, False,
                False, False, False, False, False, True, True, True, False, False, None, False, False, None, False]
    ipa['c'] = [False, True, False, False, False, False, False, None, False, False, False, False, False,
                False, False, False, True, True, False, False, False, True, False, None, True, False, None, False]
    ipa['ʝ'] = [False, True, False, False, False, False, True, None, False, False, False, False, False,
                False, False, False, True, True, False, False, False, True, False, None, True, False, None, False]
    ipa['n̥'] = [False, True, True, False, False, False, False, None, True, False, False, False, True,
                 False, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
    ipa['m̥'] = [False, True, True, False, False, False, False, None, True, False, False, False, True,
                 False, False, False, True, False, True, False, False, False, False, None, False, False, None, False]
    ipa['pʷ'] = [False, True, False, False, False, False, False, None, False, False, False, False, False,
                 False, False, False, False, False, True, False, True, False, False, None, False, False, None, True]
    ipa['bʷ'] = [False, True, False, False, False, False, True, None, False, False, False, False, False,
                 False, False, False, False, False, True, False, True, False, False, None, False, False, None, True]
    ipa['ɬ̪'] = [False, True, False, False, False, False, False, None, True, True, False, True, False,
                 False, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
    ipa['ɮ̪'] = [False, True, False, False, False, False, True, None, True, True, False, True, False,
                 False, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
    ipa['r̪'] = [True, True, True, False, False, False, True, None, True, True, False, False, False,
                 False, False, True, True, False, False, False, True, True, False, None, False, False, None, False]
    ipa['ɾ̪'] = [True, True, True, False, False, False, True, None, True, True, False, False, False,
                 False, True, False, True, False, False, False, True, True, False, None, False, False, None, False]
    ipa['ɹ̪'] = [True, True, True, False, False, False, True, None, True, True, False, False, False,
                 False, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
    ipa['w̃'] = [True, True, True, False, False, False, True, None, True, True, False, False, True,
                 False, False, False, False, True, True, False, True, False, True, None, True, False, None, True]
    ipa['cʰ'] = [False, True, False, False, False, True, False, None, False, False, False, False, False,
                 False, False, False, True, True, False, False, False, True, False, None, True, False, None, False]
    ipa['t̪ʰ'] = [False, True, False, False, False, True, False, None, False, False, False, False, False,
                  False, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
    ipa['s̪'] = [False, True, False, False, False, False, False, None, True, True, False, False, False,
                 True, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
    ipa['l̪'] = [True, True, True, False, False, False, True, None, True, True, False, True, False,
                 False, False, False, True, False, False, False, True, True, False, None, False, False, None, False]
    ipa['ʟ'] = [True, True, True, False, False, False, True, None, True, True, False, False, False,
                False, False, False, False, True, False, False, False, False, False, None, True, True, None, False]
    ipa['ɭ'] = [True, True, True, False, False, False, True, None, True, True, False, False, False, False,
                False, False, True, False, False, False, False, False, False, None, False, False, None, False]
    ipa['ʎ'] = [True, True, True, False, False, False, True, None, True, True, False, False, False,
                False, False, False, True, True, False, False, False, True, False, None, True, False, None, False]
    ipa['ʦ'] = [False, True, False, False, False, False, False, None, False, False, True, False, False,
                True, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
    ipa['ʣ'] = [False, True, False, False, False, False, True, None, False, False, True, False, False,
                True, False, False, True, False, False, False, True, False, False, None, False, False, None, False]
    ipa['ɽ'] = [True, True, True, False, False, False, True, None, True, True, False, False, False,
                False, True, False, True, False, False, False, False, False, False, None, False, False, None, False]
    ipa['o'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, True, False, False, False, True, True]
    ipa['ɔ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, True, False, False, False, False, True]
    ipa['ɐ'] = [None, False, True, False, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, False, False, False, True, True, False]
    ipa['w'] = [None, False, True, False, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, False, False, False, False, False, False]
    ipa['ɤ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, True, False, False, False, True, False]
    ipa['ɨ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, False, False, True, False, True, False]
    ipa['ə'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, False, False, False, False, False, False]
    ipa['i'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, False, True, True, False, True, False]
    ipa['iː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, False, True, True, False, True, False]
    ipa['y'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, False, True, True, False, True, True]
    ipa['yː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, False, True, True, False, True, True]
    ipa['ɪ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, False, True, True, False, False, False]
    ipa['ɪː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, False, True, True, False, False, False]
    ipa['ʏ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, False, True, True, False, False, True]
    ipa['ʏː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, False, True, True, False, False, True]
    ipa['e'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, False, True, False, False, True, False]
    ipa['eː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, False, True, False, False, True, False]
    ipa['ø'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, False, True, False, False, True, True]
    ipa['øː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, False, True, False, False, True, True]
    ipa['ɛ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, False, True, False, False, False, False]
    ipa['ɛː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, False, True, False, False, False, False]
    ipa['œ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, False, True, False, False, False, True]
    ipa['œː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, False, True, False, False, False, True]
    ipa['æ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, False, True, False, True, True, False]
    ipa['æː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, False, True, False, True, True, False]
    ipa['ɶ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, False, True, False, True, False, True]
    ipa['ʉ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, False, False, True, False, True, True]
    ipa['ʉː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, False, False, True, False, True, True]
    ipa['a'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, False, False, False, True, False, False]
    ipa['aː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, False, False, False, True, False, False]
    ipa['ɯ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, True, False, True, False, True, False]
    ipa['ɯː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, True, False, True, False, True, False]
    ipa['u'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, True, False, True, False, True, True]
    ipa['uː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, True, False, True, False, True, True]
    ipa['ʊ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, True, False, True, False, False, True]
    ipa['ʊː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, True, False, True, False, False, True]
    ipa['oː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, True, False, False, False, True, True]
    ipa['ʌ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, True, False, False, False, False, False]
    ipa['ʌː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, True, False, False, False, False, False]
    ipa['ɔː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, True, False, False, False, False, True]
    ipa['ɑ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, True, False, False, True, False, False]
    ipa['ɑː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, True, False, False, True, False, False]
    ipa['ɒ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, True, False, False, True, False, True]
    ipa['ɒː'] = [None, False, True, True, None, None, None, True, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, True, False, False, True, False, True]
    ipa['œ̃'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, False, True, False, False, False, True]
    ipa['ɵ'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                None, None, None, None, None, None, None, None, None, False, False, False, False, False, True]
    ipa['ʉ̞'] = [None, False, True, True, None, None, None, False, None, None, None, None, False,
                 None, None, None, None, None, None, None, None, None, False, True, True, False, True, True]
    ipa['ẽ'] = [None, False, True, True, None, None, None, True, None, None, None, None, True,
                 None, None, None, None, None, None, None, None, None, False, True, False, False, True, False]
    ipa['ɛ̃'] = [None, False, True, True, None, None, None, False, None, None, None, None, True,
                 None, None, None, None, None, None, None, None, None, False, True, False, False, False, False]
    ipa['ɔ̃'] = [None, False, True, True, None, None, None, False, None, None, None, None, True,
                 None, None, None, None, None, None, None, None, None, True, False, False, False, False, True]
    ipa['ɑ̃'] = [None, False, True, True, None, None, None, False, None, None, None, None, True,
                 None, None, None, None, None, None, None, None, None, True, False, False, True, False, False]
    ipa['ɑ̃ː'] = [None, False, True, True, None, None, None, False, None, None, None, None, True,
                  None, None, None, None, None, None, None, None, None, True, False, False, True, False, False]
    ipa['ã'] = [None, False, True, True, None, None, None, False, None, None, None, None, True,
                 None, None, None, None, None, None, None, None, None, False, False, False, True, False, None]
  
    return {
        key: dict(zip(ipakey, vals))
        for key, vals in ipa.items()
    }
