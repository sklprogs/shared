#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# Low-level functions that cannot use logging


class Enclose:
    
    def __init__(self, text, opening='"'):
        self.text = str(text)
        self.opening = str(opening)
        
    def get_closing(self):
        match self.opening:
            case '(':
                return ')'
            case '[':
                return ']'
            case '{':
                return '}'
            case '“':
                return '”'
            case '«':
                return '»'
        return self.opening
    
    def run(self):
        return self.opening + self.text + self.get_closing()



class Shorten:

    def __init__(self, text, limit=10, CutStart=False, ShowGap=True, encloser=''):
        self.gap = ''
        self.text = str(text)
        self.limit = limit
        self.CutStart = CutStart
        self.ShowGap = ShowGap
        self.encloser = str(encloser)
    
    def enclose(self):
        ''' Currently, 'Enclose' works with empty strings, but we want to
            eliminate potential gotchas if it becomes more complex.
        '''
        if self.encloser:
            self.text = Enclose(self.text, self.encloser).run()
    
    def set_gap(self):
        if not self.ShowGap or self.limit < 4:
            return
        # I am aware of the ellipsis, but it reads poorly in terminal
        self.gap = '...'
        self.limit -= 3
    
    def add_gap(self):
        if self.CutStart:
            self.text = self.gap + self.text[len(self.text) - self.limit:]
        else:
            self.text = self.text[0:self.limit] + self.gap
    
    def shorten(self):
        if len(self.text) <= self.limit:
            return
        if self.encloser:
            enc_len = 2 * len(self.encloser)
            if self.limit > enc_len:
                self.limit -= enc_len
        self.set_gap()
        self.add_gap()
    
    def run(self):
        if self.limit == 0:
            return self.text
        self.shorten()
        self.enclose()
        return self.text


if __name__ == '__main__':
    text = 'hello there!'
    limit = 10
    CutStart = False
    ShowGap = True
    encloser = '«'
    text = Shorten(text, limit, CutStart, ShowGap, encloser).run()
    print(f'[{text}]')
