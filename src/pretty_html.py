#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import html
import lxml.etree

from skl_shared_qt.localize import _
import skl_shared_qt.message.controller as ms


def make_pretty(code):
    f = '[SharedQt] pretty_html.make_pretty'
    if not code:
        ms.rep.empty(f)
        return ''
    try:
        bytes_ = lxml.etree.tostring (lxml.etree.XML(code)
                                     ,pretty_print = True
                                     )
        result = bytes_.decode('utf-8')
        return html.unescape(result)
    except Exception as e:
        mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
        # Almost all tested webpages were invalid, so this should be silent
        ms.Message(f, mes).show_error()
        return code
    return ''
