#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os

from skl_shared.localize import _
from skl_shared.message.controller import Message


def rewrite(file):
    f = '[SharedQt] rewrite.rewrite'
    if not os.path.isfile(file):
        # Return True to proceed with writing if the file has not been found
        return True
    # We actually don't need to rewrite or delete the file before rewriting
    mes = _('ATTENTION: Do yo really want to rewrite file "{}"?').format(file)
    answer = Message(f, mes, True).show_question()
    Message(f, answer).show_debug()
    return answer
