#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.message.controller as ms
import skl_shared_qt.shared as sh


class Label:
    
    def __init__(self):
        from skl_shared_qt.graphics.root.controller import ROOT
        self.root = ROOT
    
    def create_main(self):
        from PyQt6.QtWidgets import QMainWindow
        self.win = QMainWindow()
    
    def create_label(self):
        from skl_shared_qt.graphics.label.controller import Label
        ilabel = Label(text='Hello there!', font_family='Mono', font_size=13)
        self.win.setCentralWidget(ilabel.widget)
    
    def run(self):
        self.create_main()
        self.create_label()
        # Must be on a separate line
        self.win.show()
        self.root.end()



class Root:
    
    def __init__(self):
        from skl_shared_qt.graphics.root.controller import ROOT
        self.root = ROOT
    
    def show(self):
        from PyQt6.QtWidgets import QMainWindow
        win = QMainWindow()
        # Must be on a separate line
        win.show()
        self.root.end()
    
    def run(self):
        self.show()



class Clipboard:
    
    def __init__(self):
        from skl_shared_qt.graphics.root.controller import ROOT
        import skl_shared_qt.graphics.clipboard.controller as cl
        self.root = ROOT
        self.clipboard = cl.Clipboard(False)
        self.clipboard_gui = cl.Clipboard(True)
    
    def _copy(self, text='икепцукапвр ваырвар', CopyEmpty=False, Graphical=False):
        f = '[SharedQt] test.Clipboard._copy'
        mes = _('Copy "{}" to clipboard').format(text)
        ms.Message(f, mes).show_debug()
        if Graphical:
            self.clipboard_gui.copy(text, CopyEmpty)
        else:
            self.clipboard.copy(text, CopyEmpty)
    
    def _paste(self):
        f = '[SharedQt] test.Clipboard._paste'
        mes = _('Paste from clipboard')
        ms.Message(f, mes).show_debug()
        mes = _('Pasted text: "{}"').format(self.clipboard.paste())
        ms.Message(f, mes).show_debug()
    
    def copy_paste(self):
        f = '[SharedQt] test.Clipboard.copy_paste'
        ms.Message(f, _('Start test')).show_info()
        self._copy()
        self._paste()
    
    def set_gui(self):
        from PyQt6.QtWidgets import QMainWindow
        # Must be assigned to self, or will be destroyed by garbage collector
        self.win = QMainWindow()
        # Must be on a separate line
        self.win.show()
    
    def paste_empty_allowed(self):
        f = '[SharedQt] test.Clipboard.paste_empty_allowed'
        ms.Message(f, _('Start test')).show_info()
        self._copy('', True)
        self._paste()
    
    def paste_empty_not_allowed(self):
        f = '[SharedQt] test.Clipboard.paste_empty_not_allowed'
        ms.Message(f, _('Start test')).show_info()
        self._copy('', False)
        self._paste()
    
    def paste_empty_not_allowed_gui(self):
        f = '[SharedQt] test.Clipboard.paste_empty_not_allowed_gui'
        ms.Message(f, _('Start test')).show_info()
        self._copy('', False, True)
        self._paste()
    
    def paste_error(self):
        f = '[SharedQt] test.Clipboard.paste_error'
        ms.Message(f, _('Start test')).show_info()
        self._copy(b'\x01')
    
    def paste_error_gui(self):
        f = '[SharedQt] test.Clipboard.paste_error_gui'
        ms.Message(f, _('Start test')).show_info()
        self._copy(b'\x01', Graphical=True)
    
    def run_all(self):
        self.copy_paste()
        self.paste_empty_allowed()
        self.paste_empty_not_allowed()
        self.paste_empty_not_allowed_gui()
        self.paste_error()
        self.paste_error_gui()
    
    def run(self):
        self.set_gui()
        self.run_all()
        self.root.end()



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
    #Root().run()
    #Clipboard().run()
    Label().run()
