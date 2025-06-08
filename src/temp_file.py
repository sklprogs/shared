#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import tempfile

from skl_shared.localize import _
from skl_shared.message.controller import Message


def get_file(suffix='.htm', Delete=False):
    f = '[SharedQt] temp_file.get_file'
    try:
        # Delete=True deletes the file as soon as it is closed
        return tempfile.NamedTemporaryFile (mode = 'w', encoding = 'UTF-8'
                                           ,suffix = suffix
                                           ,delete = Delete).name
    except Exception as e:
        mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
        Message(f, mes).show_error()
