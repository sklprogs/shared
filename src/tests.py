#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('shared','../resources/locale')

import random
import shared    as sh
import sharedGUI as sg


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

def far_range(event=None):
    v1 = 0
    v2 = 0
    while abs(v1-v2) <= 40:
        v1 = random.randint(90,250)
        v2 = random.randint(90,250)
    return(v1,v2)

def test_anchors(event=None):
    anchors = ('N','NE','NW','E','EN','ES','S','SE','SW','W','WN','WS')
    sg.objs.root().widget.wm_attributes('-topmost',1)
    top = sg.objs.new_top(Maximize=0,AutoCenter=0)
    top.title('TOP')
    for anchor in anchors:
        sh.log.append ('test_anchors'
                      ,_('INFO')
                      ,'Anchor: %s' % anchor
                      )
        
        w1, w2 = far_range()
        h1, h2 = far_range()
        
        top1 = sg.SimpleTop(parent=sg.objs._root)
        top2 = sg.SimpleTop(parent=sg.objs._root)
        
        top_lbl = sg.Label (parent = top
                           ,text   = 'Anchor: %s\nPress return to adjust Widget 2.'\
                                     % anchor
                           ,expand = True
                           ,fill   = 'both'
                           )
        sg.Label (parent = top1
                 ,text   = 'WIDGET1'
                 ,bg     = 'blue'
                 ,fg     = 'yellow'
                 ,expand = True
                 ,fill   = 'both'
                 )
        sg.Label (parent = top2
                 ,text   = 'WIDGET2'
                 ,bg     = 'red'
                 ,fg     = 'yellow'
                 ,expand = True
                 ,fill   = 'both'
                 )
        top1.title('WIDGET1')
        top2.title('WIDGET2')
        
        # Strict order: 'wm_overrideredirect' -> 'show' -> 'center'
        top1.widget.wm_overrideredirect(1)
        top1.show()
        top2.widget.wm_overrideredirect(1)
        top2.show()
        
        geom = sg.Geometry(parent=top1)
        geom._geom = '%dx%d' % (w1,h1)
        geom.restore()
        
        geom = sg.Geometry(parent=top2)
        geom._geom = '%dx%d' % (w2,h2)
        geom.restore()
        
        top1.center()
        
        attach = sg.AttachWidget (obj1   = top1
                                 ,obj2   = top2
                                 ,anchor = anchor
                                 )
        sg.bind (obj      = top
                ,bindings = '<Return>'
                ,action   = attach.run
                )
        sg.bind (obj      = top1
                ,bindings = '<Return>'
                ,action   = attach.run
                )
        sg.bind (obj      = top2
                ,bindings = '<Return>'
                ,action   = attach.run
                )
        top.show()
        top_lbl.widget.destroy()
        top1.widget.destroy()
        top2.widget.destroy()


if __name__ == '__main__':
    sg.objs.start()
    test_anchors()
    sg.objs.end()
    
