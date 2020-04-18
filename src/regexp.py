#!/usr/bin/python3

import re
import sre_constants
import skl_shared2.shared as sh
from skl_shared2.localize import _


class Record:
    ''' - This class is for both checking a regular expression and
          replacing matches through text (these actions require
          different arguments and are not necessarily interconnected).
        - Example:
          # Expressions must be raw strings, otherwise, there will be
            no match
          orig:       r'(\d+)[\s]{0,1}[–-][\s]{0,1}(\d+)'
          final:      r'\1-\2'
          what1:      'Figures 1 - 2 show that...'
          with1:      'Figures 1-2 show that...'
    '''
    def __init__(self,orig,final,what1=None
                ,with1=None,what2=None,with2=None
                ,what3=None,with3=None,what4=None
                ,with4=None,what5=None,with5=None
                ,id_='Unknown id'
                ):
        f = '[shared] regexp.Record.__init__'
        self.Success = True
        self.orig    = orig
        self.final   = final
        self.what1   = what1
        self.with1   = with1
        self.what2   = what2
        self.with2   = with2
        self.what3   = what3
        self.with3   = with3
        self.what4   = what4
        self.with4   = with4
        self.what5   = what5
        self.with5   = with5
        self.id      = id_
        self.what    = self.with_ = ''
        if not self.orig or not self.final:
            self.Success = False
            mes = _('Not enough input data!')
            sh.objs.get_mes(f,mes).show_warning()
    
    def apply(self,text):
        f = '[shared] regexp.Record.apply'
        if self.Success:
            try:
                result = re.sub(self.orig,self.final,text)
            except sre_constants.error:
                result = ''
                self.Success = False
                mes = _('A syntax error in the regular expression (id: {})!')
                mes = mes.format(self.id_)
                sh.objs.get_mes(f,mes).show_warning()
            return result
        else:
            sh.com.cancel(f)
    
    def _check(self):
        f = '[shared] regexp.Record._check'
        if self.Success:
            result = self.apply(text=self.what)
            if self.Success and result != self.with_:
                self.Success = False
                mes = _('Regular expression {} has failed: we were expecting\n"{}",\nbut received\n"{}".')
                mes = mes.format(self.id_,self.with_,result)
                sh.objs.mes(f,mes).warning()
        else:
            sh.com.cancel(f)
        return self.Success
    
    def check(self):
        f = '[shared] regexp.Record.check'
        if self.Success:
            cond1 = self.what1 and self.with1
            cond2 = self.what2 and self.with2
            cond3 = self.what3 and self.with3
            cond4 = self.what4 and self.with4
            cond5 = self.what5 and self.with5
            if cond1 or cond2 or cond3 or cond4 or cond5:
                if cond1:
                    self.what  = self.what1
                    self.with_ = self.with1
                    self._check()
                if self.Success and cond2:
                    self.what  = self.what2
                    self.with_ = self.with2
                    self._check()
                if self.Success and cond3:
                    self.what  = self.what3
                    self.with_ = self.with3
                    self._check()
                if self.Success and cond4:
                    self.what  = self.what4
                    self.with_ = self.with4
                    self._check()
                if self.Success and cond5:
                    self.what  = self.what5
                    self.with_ = self.with5
                    self._check()
            else:
                self.Success = False
                mes = _('Not enough input data!')
                sh.objs.get_mes(f,mes).show_warning()
        else:
            sh.com.cancel(f)
        return self.Success



if __name__ == '__main__':
    orig = r'([Cc]laim|[Cc]olumn|[Pp]age|[Ss]heet|[Pp]aragraph|[Ll]ine)[s]{0,1}[\s]{0,1}(\d+[,-][\s]{0,1}\d+)'
    final = r'\1s \2'
    #text = 'Records 200 - 300 have undergone a regular procedure...'
    what1 = 'pages 1-2'
    with1 = 'pages 1-2'
    rec = Record (orig  = orig
                 ,final = final
                 ,what1 = what1
                 ,with1 = with1
                 )
    print(rec.check())
    #print(rec.apply(text=what1))
