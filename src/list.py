#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import difflib
import itertools

from skl_shared.localize import _
from skl_shared.message.controller import Message
from skl_shared.logic import Text


class List:

    def __init__(self, lst1=[], lst2=[]):
        if lst1 is None:
            self.lst1 = []
        else:
            self.lst1 = list(lst1)
        if lst2 is None:
            self.lst2 = []
        else:
            self.lst2 = list(lst2)
    
    def join_sublists(self):
        return list(itertools.chain(*self.lst1))
    
    def split_by_item(self, item):
        f = '[shared] list.List.split_by_item'
        try:
            index_ = self.lst1.index(item)
            self.lst2 = self.lst1[index_:]
            self.lst1 = self.lst1[:index_]
        except ValueError:
            mes = _('Wrong input data: "{}"!').format(item)
            Message(f, mes).show_warning()
        return(self.lst1, self.lst2)
    
    def split_by_len(self, len_):
        # Get successive len_-sized chunks
        return [self.lst1[i:i+len_] for i in range(0, len(self.lst1), len_)]
    
    def split_by_gaps(self):
        ''' Split an integer sequence where the next item does not
            increment the preceding one.
        '''
        if len(self.lst1) <= 0:
            return self.lst1
        cuts = []
        cut = [self.lst1[0]]
        i = 1
        while i < len(self.lst1):
            if self.lst1[i-1] + 1 == self.lst1[i]:
                cut.append(self.lst1[i])
            else:
                cuts.append(cut)
                cut = [self.lst1[i]]
            i += 1
        if cut:
            cuts.append(cut)
        return cuts

    def find_by_count(self, max_count=1):
        count = 0
        old = list(self.lst1)
        start = 0
        while True:
            self.lst1 = old[start:]
            poses = self.find()
            if not poses:
                break
            count += 1
            poses[0] += start
            poses[1] += start
            start = poses[1] + 1
            if count == max_count:
                break
        self.lst1 = old
        return poses
    
    def find_all(self):
        old = list(self.lst1)
        start = 0
        poses = []
        while True:
            self.lst1 = old[start:]
            res = self.find()
            if not res:
                break
            res[0] += start
            res[1] += start
            start = res[1] + 1
            poses.append(res)
        self.lst1 = old
        return poses
    
    def find(self):
        len_ = len(self.lst2)
        for index_ in (i for i, e in enumerate(self.lst1) if e == self.lst2[0]):
            if self.lst1[index_:index_+len_] == self.lst2:
                return([index_, index_ + len_ - 1])
    
    def get_shared(self):
        return [item for item in self.lst2 if item in self.lst1]
    
    def eats(self):
        # Check if 'lst1' fully comprises 'lst2'
        for item in self.lst2:
            if not item in self.lst1:
                return False
        return True
    
    def get_duplicates_low(self):
        ''' Remove (case-insensitively) duplicate items (positioned after
            original items). Both lists must consist of strings.
        '''
        cilst = [item.lower() for item in self.lst1]
        i = len(cilst) - 1
        while i >= 0:
            ind = cilst.index(cilst[i])
            if ind < i:
                del cilst[i]
                del self.lst1[i]
            i -= 1
        return self.lst1
    
    def delete_duplicates(self):
        # Remove duplicate items (positioned after original items)
        i = len(self.lst1) - 1
        while i >= 0:
            ind = self.lst1.index(self.lst1[i])
            if ind < i:
                del self.lst1[i]
            i -= 1
        return self.lst1
    
    def space_items(self):
        # Add a space where necessary and convert to a string
        lst1 = [str(item) for item in self.lst1]
        lst2 = [str(item) for item in self.lst2]
        lst = lst1 + lst2
        if not lst:
            return ''
        itext = Text(lst[0])
        i = 1
        while i < len(lst):
            itext.join(lst[i])
            i += 1
        return itext.text

    def equalize(self):
        # Adjust the lists at input to have the same length
        max_range = max(len(self.lst1), len(self.lst2))
        if max_range == len(self.lst1):
            for i in range(len(self.lst1)-len(self.lst2)):
                self.lst2.append('')
        else:
            for i in range(len(self.lst2)-len(self.lst1)):
                self.lst1.append('')
        return(self.lst1, self.lst2)

    def get_diff(self):
        # Find different elements (strict order)
        # Based on http://stackoverflow.com/a/788780
        seqm = difflib.SequenceMatcher(a=self.lst1, b=self.lst2)
        output = []
        for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
            if opcode != 'equal':
                output += seqm.a[a0:a1]
        return output
