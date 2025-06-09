#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import html
import lxml.etree

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep


def make_pretty(code):
    f = '[shared] pretty_html.make_pretty'
    if not code:
        rep.empty(f)
        return ''
    try:
        bytes_ = lxml.etree.tostring(lxml.etree.XML(code)
                                    ,pretty_print = True)
        result = bytes_.decode('utf-8')
        return html.unescape(result)
    except Exception as e:
        mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
        # Almost all tested webpages were invalid, so this should be silent
        Message(f, mes).show_error()
        return code
    return ''
