#!/usr/bin/python3
# -*- coding: UTF-8 -*-

''' Separating this code to an individual module allows to make
    'enchant' optional and not to bundle binaries not requiring 
    a spellchecker with 'enchant' dictionaries.
'''

import enchant

from skl_shared_qt.localize import _
import skl_shared_qt.logic as lg
import skl_shared_qt.shared as sh


class TextBoxTk(sh.TextBoxTk):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def check_spell(self):
        f = '[shared] spelling.TextBox.check_spell'
        self.set_word('1.0')
        while not self.is_last_word():
            pos = self.set_next_word()
            # Stripping is done here
            word = self.get_word_text (pos = pos
                                      ,Strip = False
                                      )
            objs.get_spell().reset(word)
            if not objs.spell.check():
                # Spelling returns True on an empty input
                if word[0] in lg.punc_array \
                or word[0] in lg.punc_ext_array:
                    pos = '{}+1c'.format(pos)
                pos2 = '{}+{}c'.format(pos,len(objs.spell.word))
                self.tag_add (tag = 'misspell'
                             ,pos1 = pos
                             ,pos2 = pos2
                             ,DelPrev = False
                             )
        self.tag_config (tag = 'misspell'
                        ,bg = 'red'
                        )



class Spelling:
    
    def __init__(self):
        ''' Enchant:
            
            Does not accept:
            - an empty input (raises an exception)
            - mixed case
            - punctuation
            
            Accepts:
            - lower-case, upper-case and words where the first letter
               is capital
            - 'ё' and 'е' (new versions)
            - non-nominative cases (new versions)
        '''
        self.ru = enchant.Dict('ru_RU')
        self.gb = enchant.Dict('en_GB')
        self.us = enchant.Dict('en_US')
    
    def check(self):
        f = '[shared] spelling.Spelling.check'
        ''' We do not warn about empty input/output since this happens
            quite often. Moreover, we return True in such cases since
            this is actually not a spelling error.
        '''
        if self.word:
            self.word = self.word.strip()
            itext = sh.Text(self.word)
            self.word = itext.delete_punctuation()
            if self.word and not itext.has_digits():
                if len(self.word) == 1:
                    return True
                elif itext.has_cyrillic():
                    return self.ru.check(self.word)
                elif itext.has_latin():
                    return self.gb.check(self.word) \
                    or self.us.check(self.word)
            else:
                # Ignore an empty input and words with digits
                return True
        else:
            return True
    
    def reset(self,word):
        self.word = word



class SearchBox(sh.SearchBox,TextBoxTk):
    
    def __init__(self,*args,**kwargs):
        super(SearchBox,self).__init__(*args,**kwargs)



class TextBoxC(sh.TextBoxC):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    def set_gui(self):
        self.parent = sh.Top (Maximize = self.Maximize
                             ,title = self.title
                             ,icon = self.icon
                             )
        self.widget = self.parent.widget
        self.gui = sh.gi.TextBoxC(self.parent)
        self.obj = SearchBox (parent = self.parent
                             ,ScrollX = False
                             ,ScrollY = True
                             ,icon = self.icon
                             ,font = self.font
                             )
        self.set_bindings()



class TextBoxRW(sh.TextBoxRW,TextBoxC):
    
    def __init__(self,*args,**kwargs):
        ''' Inheriting both instances allows to keep old bindings that
            run in 'sh.TextBoxRW.__init__' and, at the same time, to
            override procedures.
        '''
        super(TextBoxRW,self).__init__(*args,**kwargs)



class Objects:
    
    def __init__(self):
        self.spell = None
    
    def get_spell(self):
        ''' Importing 'enchant' is fast, but dictionary loading takes
            some time.
        '''
        if self.spell is None:
            self.spell = Spelling()
        return self.spell


objs = Objects()
