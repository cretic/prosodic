from .imports import *
SYLL_SEP='.'

class SyllableList(EntityList): pass
class WordTypeList(EntityList): pass

@total_ordering
class WordFormList(EntityList):
    def __repr__(self):
        return ' '.join(wf.token_stress for wf in self.data)
    
    @cached_property
    def slots(self):
        return [
            syll
            for wordform in self.data
            for syll in wordform.children
        ]

    @cached_property
    def df(self):
        l=[
            {
                k:('.'.join(v) if type(v)==list else v)
                for k,v in px.attrs.items()
            }
            for px in self.data
            if px is not None
        ]
        return setindex(pd.DataFrame(l))

    @cached_property
    def num_stressed_sylls(self):
        return sum(
            int(syll.is_stressed)
            for wordform in self.data
            for syll in wordform.children
        )
    
    @cached_property
    def num_sylls(self):
        return sum(
            1
            for wordform in self.data
            for syll in wordform.children
        )
    
    @cached_property
    def first_syll(self):
        for wordform in self.data:
            for syll in wordform.children:
                return syll
    
    @cached_property
    def sort_key(self):
        sylls_is_odd = int(bool(self.num_sylls % 2))
        first_syll_stressed = 2 if self.first_syll is None else int(self.first_syll.is_stressed)
        return (sylls_is_odd, self.num_sylls, self.num_stressed_sylls, first_syll_stressed)

    def __lt__(self, other): return self.sort_key<other.sort_key
    def __eq__(self, other): 
        # return self.sort_key==other.sort_key
        return self is other
        





@cache
@profile
def Word(token, lang=DEFAULT_LANG):
    if lang not in LANGS: 
        raise Exception(f'Language {lang} not recognized')
    lang_obj = LANGS[lang]()
    return lang_obj.get(token)

class WordToken(Entity):
    child_type='WordType'
    list_type=WordTypeList

    prefix='wordtoken'
    @profile
    def __init__(self, token, lang=DEFAULT_LANG, parent=None, **kwargs):
        self.word = word = Word(token, lang=lang)
        super().__init__(
            children=[word],
            parent=parent,
            txt=token,
            **kwargs
        )


class WordType(Entity):
    child_type: str = 'WordForm'
    list_type=list
    
    prefix='word'
    @profile
    def __init__(self, token:str, children:list, parent=None, **kwargs):
        super().__init__(
            children=children, 
            parent=parent,
            txt=token,
            **kwargs
        )

    @property
    def forms(self): return self.children
    @property
    def form(self): return self.children[0] if self.children else None
    @property
    def num_forms(self): return len(self.children)
    @property
    def is_punc(self): 
        return True if not any([x.isalpha() for x in self.txt]) else None

    @cached_property
    def num_sylls(self): 
        x=np.median([form.num_sylls for form in self.forms])
        return None if np.isnan(x) else int(round(x))

    @cached_property
    def num_stressed_sylls(self): 
        x=np.median([form.num_stressed_sylls for form in self.forms])
        return None if np.isnan(x) else int(round(x))

    @cached_property
    def attrs(self):
        return {
            **super().attrs,
            'num_forms':self.num_forms,
            # 'num_sylls':self.num_sylls,
            # 'num_stressed_sylls':self.num_stressed_sylls,
            'is_punc':self.is_punc,
        }
    


class WordForm(Entity):
    prefix='wordform'
    child_type: str = 'Syllable'
    list_type = SyllableList

    @profile
    def __init__(self, txt:str, sylls_ipa=[], sylls_text=[], syll_sep='.'):
        from .syllables import Syllable
        sylls_ipa=(
            sylls_ipa.split(syll_sep) 
            if type(sylls_ipa)==str 
            else sylls_ipa
        )
        sylls_text=(
            sylls_text.split(syll_sep) 
            if type(sylls_text)==str 
            else (
                sylls_text
                if sylls_text
                else sylls_ipa
            )
        )
        children=[]
        if sylls_text and sylls_ipa:
            for syll_str,syll_ipa in zip(sylls_text, sylls_ipa):
                syll = Syllable(
                    syll_str, 
                    ipa=syll_ipa, 
                    parent=self
                )
                children.append(syll)
        super().__init__(
            # sylls_ipa=sylls_ipa, 
            # sylls_text=sylls_text, 
            txt=txt,
            children=children
        )

    @cached_property
    def token_stress(self):
        return SYLL_SEP.join(
            syll.txt.upper() if syll.is_stressed else syll.txt.lower()
            for syll in self.children
        )

    
    @cached_property
    def is_functionword(self):
        return len(self.children)==1 and not self.children[0].is_stressed
    @cached_property
    def num_sylls(self): return len(self.children)
    @cached_property
    def num_stressed_sylls(self): return len([syll for syll in self.children if syll.is_stressed])







def get_stress(ipa):
    if not ipa: return ''
    if ipa[0]=='`': return 'S'
    if ipa[0]=="'": return 'P'
    return 'U'



def unstress(ipa):
    if not ipa: return ''
    if ipa[0] in {'`', "'"}: ipa=ipa[1:]
    return ipa

def stress(ipa, primary=True):
    if not ipa: return ''
    ipa = unstress(ipa)
    sstr = "'" if primary else '`'
    return sstr+ipa


def ensure_maybe_stressed(ipa_l):
    if any(any(get_stress(syllipa)!='U') for ipa in ipa_l for syllipa in ipa):
        ipa_l.append([unstress(syllipa) for syllipa in ipa_l[0]])
    else:
        ipa_l.append([stress(syllipa,primary=not i) for i,syllipa in enumerate(ipa_l[0])])

def ensure_unstressed(ipa_l):
    return [
        [unstress(syllipa) for syllipa in ipa_l[0]]
    ]


