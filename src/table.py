#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import io

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.basic_text import Shorten, Enclose


class Table:
    
    def __init__(self, iterable=[], headers=[], sep=' ', Transpose=False
                ,maxrow=0, CutStart=False, maxrows=0, encloser='', ShowGap=True):
        # #NOTE: In case of tuple, do not forget to add commas, e.g.: ((1,),)
        self.Success = True
        self.lens = []
        self.encloser = encloser
        self.CutStart = CutStart
        self.headers = headers
        self.lst = iterable
        self.maxrow = maxrow
        self.maxrows = maxrows
        self.sep = sep
        self.Transpose = Transpose
        self.ShowGap = ShowGap
    
    def set_max_rows(self):
        f = '[SharedQt] table.Table.set_max_rows'
        if not self.Success:
            rep.cancel(f)
            return
        if self.maxrows <= 0:
            return
        mes = _('Set the max number of rows to {}').format(self.maxrows)
        Message(f, mes).show_debug()
        for i in range(len(self.lst)):
            # +1 for a header
            self.lst[i] = self.lst[i][0:self.maxrows+1]
    
    def set_max_width(self):
        f = '[SharedQt] table.Table.set_max_width'
        if not self.Success:
            rep.cancel(f)
            return
        if self.maxrow <= 0:
            return
        mes = _('Set the max column width to {} symbols').format(self.maxrow)
        Message(f, mes).show_debug()
        if self.encloser:
            max_len = self.maxrow - len(self.encloser)
            if max_len < 0:
                max_len = 0
        else:
            max_len = self.maxrow
        for i in range(len(self.lst)):
            for j in range(len(self.lst[i])):
                text = str(self.lst[i][j])
                self.lst[i][j] = Shorten(text, max_len, self.CutStart, self.ShowGap).run()
    
    def enclose(self):
        ''' Passing 'encloser' in 'Text.shorten' is not enough since it
            does not enclose items shorter than 'max_len'.
        '''
        f = '[SharedQt] table.Table.enclose'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.enclose:
            return
        for i in range(len(self.lst)):
            j = 1
            while j < len(self.lst[i]):
                self.lst[i][j] = Enclose(self.lst[i][j], self.encloser).run()
                j += 1
    
    def transpose(self):
        f = '[SharedQt] table.Table.transpose'
        if not self.Success:
            rep.cancel(f)
            return
        if self.Transpose:
            self.lst = [*zip(*self.lst)]
            # 'zip' produces tuples
            self.lst = [list(item) for item in self.lst]
    
    def set_headers(self):
        f = '[SharedQt] table.Table.set_headers'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.headers:
            rep.lazy(f)
            return
        ''' If there is a condition mismatch when everything is seemingly
            correct, check that headers are provided in the form of
            ('NO1', 'NO2') instead of ('NO1, NO2').
        '''
        if len(self.headers) == len(self.lst):
            for i in range(len(self.lst)):
                self.lst[i].insert(0, self.headers[i])
        else:
            sub = f'{len(self.headers)} == {len(self.lst)}'
            mes = _('The condition "{}" is not observed!').format(sub)
            Message(f, mes, True).show_warning()
    
    def report(self):
        f = '[SharedQt] table.Table.report'
        result = ''
        if not self.Success:
            rep.cancel(f)
            return
        iwrite = io.StringIO()
        for j in range(len(self.lst[0])):
            for i in range(len(self.lst)):
                delta = self.lens[i] - len(self.lst[i][j])
                iwrite.write(self.lst[i][j])
                iwrite.write(' ' * delta)
                if i + 1 < len(self.lst):
                    iwrite.write(self.sep)
            iwrite.write('\n')
        result = iwrite.getvalue()
        iwrite.close()
        return result
    
    def add_gap(self):
        f = '[SharedQt] table.Table.add_gap'
        if not self.Success:
            rep.cancel(f)
            return
        lst = [len(item) for item in self.lst]
        if not lst:
            self.Success = False
            rep.empty(f)
            return
        maxl = max(lst)
        for i in range(len(self.lst)):
            delta = maxl - len(self.lst[i])
            for j in range(delta):
                self.lst[i].append('')
    
    def get_lens(self):
        f = '[SharedQt] table.Table.get_lens'
        if not self.Success:
            rep.cancel(f)
            return
        for item in self.lst:
            tmp = sorted(item, key=len, reverse=True)
            self.lens.append(len(tmp[0]))
    
    def make_list(self):
        f = '[SharedQt] table.Table.make_list'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.lst:
            self.Success = False
            rep.empty(f)
            return
        try:
            self.lst = list(self.lst)
            for i in range(len(self.lst)):
                self.lst[i] = [str(item) for item in self.lst[i]]
        except TypeError:
            self.Success = False
            mes = _('Only iterable objects are supported!')
            Message(f, mes, True).show_warning()
    
    def run(self):
        self.make_list()
        self.transpose()
        self.set_headers()
        self.set_max_rows()
        self.set_max_width()
        self.enclose()
        self.add_gap()
        self.get_lens()
        return self.report()
