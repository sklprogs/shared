#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared_qt.message.controller as ms
import skl_shared_qt.shared as sh


class Root:
    
    def __init__(self):
        from skl_shared_qt.graphics.root.controller import ROOT
        self.root = ROOT
    
    def show(self):
        from PyQt6.QtWidgets import QMainWindow
        win = QMainWindow()
        win.show()
        self.root.end()
    
    def run(self):
        self.show()



class Messages:
    
    def console(self):
        ms.GRAPHICAL = False
        #sh.com.start()
        sh.ReadTextFile('/tmp/aaa').get()
        #sh.com.end()



class Report:
    
    def cancel(self):
        ms.rep.cancel('[SharedQt] test.Report.cancel')
    
    def wrong_input(self):
        ms.rep.wrong_input('[SharedQt] test.Report.wrong_input')
    
    def empty(self):
        ms.rep.empty('[SharedQt] test.Report.empty')
    
    def not_ready(self):
        ms.rep.not_ready('[SharedQt] test.Report.not_ready')
    
    def empty_output(self):
        ms.rep.empty_output('[SharedQt] test.Report.empty_output')
    
    def deleted(self):
        ms.rep.deleted('[SharedQt] test.Report.deleted', 50)
    
    def matches(self):
        ms.rep.matches('[SharedQt] test.Report.matches', 50)
    
    def third_party(self):
        mes = 'Something went horribly wrong'
        ms.rep.third_party('[SharedQt] test.Report.third_party', mes)
    
    def condition(self):
        ms.rep.condition('[SharedQt] test.Report.condition', '2 + 2 = 4')
    
    def test_all(self):
        self.cancel()
        self.wrong_input()
        self.empty()
        self.not_ready()
        self.empty_output()
        self.deleted()
        self.matches()
        sh.com.start()
        self.third_party()
        self.condition()
        sh.com.end()


if __name__ == '__main__':
    #Report().test_all()
    Root().show()
