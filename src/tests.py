#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import shared    as sh
import sharedGUI as sg

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('shared','../resources/locale')


def progressbar():
    import random
    pb = sg.ProgressBar()
    for i in range(100):
        item     = pb.add()
        file     = 'File #%d' % i
        total    = random.randint(1,100)
        cur_size = random.randint(0,total)
        rate     = random.randint(1,5000)
        eta      = int((total*1000)/rate)
        item.text (file     = file
                  ,cur_size = cur_size
                  ,total    = total
                  ,rate     = rate
                  ,eta      = eta
                  )
    pb.show()


if __name__ == '__main__':
    sg.objs.start()
    progressbar()
    sg.objs.end()
    
