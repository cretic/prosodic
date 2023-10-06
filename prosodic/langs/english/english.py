from prosodic.imports import *
from prosodic.langs.langs import *

class EnglishLanguage(Language):
    pronunciation_dictionary_filename = os.path.join(PATH_DICTS,'en','english.tsv')
    lang_espeak = 'en-us'
    lang = 'en'
    cache_fn = 'english_wordtypes.sqlitedict'
    path_maybestressed = os.path.join(os.path.dirname(__file__), 'maybestressed.txt')
    path_unstressed = os.path.join(os.path.dirname(__file__), 'unstressed.txt')

    @cached_property
    def token2ipa(self):
        d=super().token2ipa
        
        # maybe's and unstressed
        if self.path_maybestressed and os.path.exists(self.path_maybestressed):
            with open(self.path_maybestressed) as f:
                maybewords=set(f.read().strip().split())
                for w in maybewords:
                    if w in d and d[w]:
                        ipa_l = d[w]
                        d[w] = ensure_maybe_stressed(ipa_l)

        if self.path_unstressed and os.path.exists(self.path_unstressed):
            with open(self.path_unstressed) as f:
                unwords=set(f.read().strip().split())
                for w in unwords:
                    if w in d and d[w]:
                        ipa_l = d[w]
                        d[w] = ensure_unstressed(ipa_l)
        
        return d


@cache
def English(): return EnglishLanguage()
LANGS['en'] = English
