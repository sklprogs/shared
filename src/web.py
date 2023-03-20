#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import html
import lxml.etree

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class WebPage:
    
    def __init__(self,code):
        self.code = code
    
    def make_pretty(self):
        f = '[shared] web.WebPage.make_pretty'
        if not self.code:
            sh.com.rep_empty(f)
            return ''
        try:
            bytes_ = lxml.etree.tostring (lxml.etree.XML(self.code)
                                         ,pretty_print = True
                                         )
            result = bytes_.decode('utf-8')
            return html.unescape(result)
        except Exception as e:
            mes = _('Third-party module has failed!\n\nDetails: {}')
            mes = mes.format(e)
            sh.objs.get_mes(f,mes).show_error()
            return self.code
        return ''
