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
        self.ilabel = Label(text='Hello there!', font_family='Mono', font_size=13)
        self.win.setCentralWidget(self.ilabel.widget)
    
    def run(self):
        self.create_main()
        self.create_label()
        self.win.show()
        self.root.end()



class Font(Label):
    
    def __init__(self):
        super().__init__()
    
    def create_font(self):
        from skl_shared_qt.graphics.font.controller import Font
        self.ifont = Font(self.ilabel.widget, 'Mono', 14)
        self.ifont.run()
    
    def run(self):
        self.create_main()
        self.create_label()
        self.create_font()
        self.win.show()
        self.root.end()



class Entry:
    
    def __init__(self):
        from skl_shared_qt.graphics.root.controller import ROOT
        self.root = ROOT
    
    def create_main(self):
        from PyQt6.QtWidgets import QMainWindow
        self.win = QMainWindow()
    
    def create_entry(self):
        from skl_shared_qt.graphics.entry.controller import Entry
        ientry = Entry()
        ientry.set_text('Hello there!')
        self.win.setCentralWidget(ientry.widget)
    
    def run(self):
        self.create_main()
        self.create_entry()
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
    
    def run(self):
        self.show()
        self.root.end()



class MainWindow:
    
    def __init__(self):
        from skl_shared_qt.graphics.root.controller import ROOT
        self.root = ROOT
        self.create_main()
    
    def create_main(self):
        from PyQt6.QtWidgets import QMainWindow
        self.win = QMainWindow()
    
    def show(self):
        self.win.show()
    
    def run(self):
        self.show()
        self.root.end()



class Color(MainWindow):
    
    def __init__(self):
        super().__init__()
        self.color_name = 'cyan'
    
    def create_color(self):
        from skl_shared_qt.graphics.color.controller import Color
        self.icolor = Color(self.color_name)
    
    def get_hex(self):
        f = '[SharedQt] test.Color.get_hex'
        ms.Message(f, _('Start test')).show_info()
        hex_ = self.icolor.get_hex()
        mes = f'HEX value of color "{self.color_name}" is {hex_}'
        ms.Message(f, mes).show_debug()
    
    def modify(self):
        f = '[SharedQt] test.Color.modify'
        ms.Message(f, _('Start test')).show_info()
        darker, lighter = self.icolor.modify()
    
    def run_all(self):
        self.get_hex()
        self.modify()
    
    def run(self):
        self.show()
        self.create_color()
        self.run_all()
        self.root.end()



class Clipboard(MainWindow):
    
    def __init__(self):
        super().__init__()
        from skl_shared_qt.graphics.clipboard.controller import Clipboard
        self.clipboard = Clipboard(False)
        self.clipboard_gui = Clipboard(True)
    
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
        self.show()
        self.run_all()
        self.root.end()



class Message(MainWindow):
    
    def __init__(self):
        super().__init__()
    
    def console(self):
        f = '[SharedQt] test.Message.console'
        ms.Message(f, f'Start {f}').show_info()
        old = ms.GRAPHICAL
        ms.GRAPHICAL = False
        sh.ReadTextFile('/tmp/aaa').get()
        ms.GRAPHICAL = old
    
    def run_all(self):
        self.console()
        self.show_debug()
        self.show_debug_gui()
        self.show_info()
        self.show_info_gui()
        self.show_warning()
        self.show_warning_gui()
        self.show_error()
        self.show_error_gui()
        self.show_question()
        self.show_question_gui()
    
    def show_debug(self):
        f = '[SharedQt] test.Message.show_debug'
        input(f'Start {f}')
        mes = 'This is Debug'
        ms.Message(f, mes).show_debug()
    
    def show_debug_gui(self):
        f = '[SharedQt] test.Message.show_debug_gui'
        input(f'Start {f}')
        mes = 'This is Debug'
        ms.Message(f, mes, True).show_debug()
    
    def show_info(self):
        f = '[SharedQt] test.Message.show_info'
        input(f'Start {f}')
        mes = 'This is Info'
        ms.Message(f, mes).show_info()
    
    def show_info_gui(self):
        f = '[SharedQt] test.Message.show_info_gui'
        input(f'Start {f}')
        mes = 'This is Info'
        ms.Message(f, mes, True).show_info()
    
    def show_warning(self):
        f = '[SharedQt] test.Message.show_warning'
        input(f'Start {f}')
        mes = 'This is Warning'
        ms.Message(f, mes).show_warning()
    
    def show_warning_gui(self):
        f = '[SharedQt] test.Message.show_warning_gui'
        input(f'Start {f}')
        mes = 'This is Warning'
        ms.Message(f, mes, True).show_warning()
    
    def show_error(self):
        f = '[SharedQt] test.Message.show_error'
        input(f'Start {f}')
        mes = 'This is Error'
        ms.Message(f, mes).show_error()
    
    def show_error_gui(self):
        f = '[SharedQt] test.Message.show_error_gui'
        input(f'Start {f}')
        mes = 'This is Error'
        ms.Message(f, mes, True).show_error()
    
    def show_question(self):
        f = '[SharedQt] test.Message.show_question'
        input(f'Start {f}')
        mes = 'This is Question'
        answer = ms.Message(f, mes).show_question()
        if answer:
            answer = 'Yes'
        else:
            answer = 'No'
        ms.Message(f, f'You answer is {answer}').show_debug()
    
    def show_question_gui(self):
        f = '[SharedQt] test.Message.show_question_gui'
        input(f'Start {f}')
        mes = 'This is Question'
        answer = ms.Message(f, mes, True).show_question()
        if answer:
            answer = 'Yes'
        else:
            answer = 'No'
        ms.Message(f, f'You answer is {answer}', True).show_debug()
    
    def run(self):
        self.show()
        self.run_all()
        self.root.end()



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
    #Message().run()
    #Clipboard().run()
    #Label().run()
    #Entry().run()
    #Font().run()
    Color().run()
