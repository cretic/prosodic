from .imports import *



class Stanza(entity):
    sep: str = ''
    child_type: str = 'Line'
    prefix='stanza'

    @profile
    def __init__(self, txt:str='', children=[], parent=None, tokens_df=None, lang=DEFAULT_LANG, **kwargs):
        if not txt and not children and tokens_df is None:
            raise Exception('Must provide either txt, children, or tokens_df')
        self._txt=txt
        if not children:
            if tokens_df is None: tokens_df = pd.DataFrame(tokenize_sentwords_iter(txt))
            children = [
                Line(parent=self, tokens_df=line_df)                
                for line_i,line_df in tokens_df.groupby('line_i')
            ]
        super().__init__(children=children, parent=parent, **kwargs)
    

class Line(entity):
    line_sep = '\n'
    sep: str = ''
    child_type: str = 'Word'
    is_parseable = True
    prefix='line'

    @profile
    def __init__(self, txt:str='', children=[], parent=None, tokens_df=None, lang=DEFAULT_LANG, **kwargs):
        from .words import WordToken
        if not txt and not children and tokens_df is None:
            raise Exception('Must provide either txt, children, or tokens_df')
        self._txt=txt
        if not children:
            if tokens_df is None: tokens_df = pd.DataFrame(tokenize_sentwords_iter(txt))
            children=[
                WordToken(
                    token=word_d.get('word_str',''),
                    lang=lang,
                    parent=self,
                    # is_punc=word_d.get('word_ispunc'),
                    sent_num=word_d.get('sent_i'),
                    sentpart_num=word_d.get('sent_i'),
                )
                for word_d in tokens_df.to_dict('records')
                if 'word_str' in word_d and 'word_ispunc'
            ]
        
        super().__init__(children=children, parent=parent, **kwargs)