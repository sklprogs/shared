#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.message.controller as ms
import skl_shared_qt.shared as sh


class Root:
    
    def __init__(self):
        from skl_shared_qt.graphics.root.controller import ROOT
        from PyQt6.QtWidgets import QMainWindow
        self.root = ROOT
        self.win = QMainWindow()
        self.set_bindings()
    
    def bind(self, hotkeys, action):
        from PyQt6.QtGui import QShortcut, QKeySequence
        for hotkey in hotkeys:
            QShortcut(QKeySequence(hotkey), self.win).activated.connect(action)
    
    def set_bindings(self):
        self.bind(('Esc',), self.win.close)
    
    def show(self):
        # Must be on a separate line
        self.win.show()
    
    def run_all(self):
        # Override this procedure in inherited classes
        pass
    
    def run(self):
        self.run_all()
        # Main window can be shown either before or after creating other widgets
        self.show()
        self.root.end()



class Label(Root):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_label()
    
    def create_label(self):
        from skl_shared_qt.graphics.label.controller import Label
        self.ilabel = Label(text=_('Close this window to quit'), font_family='Mono', font_size=13)
        self.win.setCentralWidget(self.ilabel.widget)



class Font(Label):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_font()
    
    def create_font(self):
        from skl_shared_qt.graphics.font.controller import Font
        self.ifont = Font(self.ilabel.widget, 'Mono', 14)
        self.ifont.run()



class Entry(Label):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_entry()
    
    def create_entry(self):
        from skl_shared_qt.graphics.entry.controller import Entry
        ientry = Entry()
        ientry.set_text('This is an entry')
        self.win.setCentralWidget(ientry.widget)



class Color(Label):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color_name = 'cyan'
        self.create_color()
    
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
        f = '[SharedQt] test.Color.run_all'
        self.get_hex()
        self.modify()
        ms.Message(f, _('Testing is complete')).show_info()



class Button(Root):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_button()
    
    def click(self, event=None):
        f = '[SharedQt] test.Button.click'
        ms.Message(f, _('Operation is complete.'), True).show_info()
    
    def create_button(self):
        from skl_shared_qt.graphics.button.controller import Button
        from PyQt6.QtWidgets import QWidget, QVBoxLayout
        path = '/home/pete/bin/mclient/resources/buttons/go_search.png'
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)
        ibutton = Button (text=_('Click me'), action=self.click
                         ,hint=_('This is a button'), active=path
                         ,inactive=path
                         )
        layout.addWidget(ibutton.widget)
        self.win.setCentralWidget(panel)



class Clipboard(Label):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        input(_('Start {}').format(f))
        self._copy()
        self._paste()
    
    def paste_empty_allowed(self):
        f = '[SharedQt] test.Clipboard.paste_empty_allowed'
        input(_('Start {}').format(f))
        self._copy('', True)
        self._paste()
    
    def paste_empty_not_allowed(self):
        f = '[SharedQt] test.Clipboard.paste_empty_not_allowed'
        input(_('Start {}').format(f))
        self._copy('', False)
        self._paste()
    
    def paste_empty_not_allowed_gui(self):
        f = '[SharedQt] test.Clipboard.paste_empty_not_allowed_gui'
        input(_('Start {}').format(f))
        self._copy('', False, True)
        self._paste()
    
    def paste_error(self):
        f = '[SharedQt] test.Clipboard.paste_error'
        input(_('Start {}').format(f))
        self._copy(b'\x01')
    
    def paste_error_gui(self):
        f = '[SharedQt] test.Clipboard.paste_error_gui'
        input(_('Start {}').format(f))
        self._copy(b'\x01', Graphical=True)
    
    def run_all(self):
        f = '[SharedQt] test.Clipboard.run_all'
        self.copy_paste()
        self.paste_empty_allowed()
        self.paste_empty_not_allowed()
        self.paste_empty_not_allowed_gui()
        self.paste_error()
        self.paste_error_gui()
        ms.Message(f, _('Testing is complete')).show_info()



class Message(Label):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def console(self):
        f = '[SharedQt] test.Message.console'
        ms.Message(f, _('Start test')).show_info()
        old = ms.GRAPHICAL
        ms.GRAPHICAL = False
        sh.ReadTextFile('/tmp/aaa').get()
        ms.GRAPHICAL = old
    
    def run_all(self):
        f = '[SharedQt] test.Message.run_all'
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
        ms.Message(f, _('Testing is complete')).show_info()
    
    def show_debug(self):
        f = '[SharedQt] test.Message.show_debug'
        input(_('Start {}').format(f))
        mes = _('This is {}').format(_('DEBUG'))
        ms.Message(f, mes).show_debug()
    
    def show_debug_gui(self):
        f = '[SharedQt] test.Message.show_debug_gui'
        input(_('Start {}').format(f))
        mes = _('This is {}').format(_('DEBUG'))
        ms.Message(f, mes, True).show_debug()
    
    def show_info(self):
        f = '[SharedQt] test.Message.show_info'
        input(_('Start {}').format(f))
        mes = _('This is {}').format(_('INFO'))
        ms.Message(f, mes).show_info()
    
    def show_info_gui(self):
        f = '[SharedQt] test.Message.show_info_gui'
        input(_('Start {}').format(f))
        mes = _('This is {}').format(_('INFO'))
        ms.Message(f, mes, True).show_info()
    
    def show_warning(self):
        f = '[SharedQt] test.Message.show_warning'
        input(_('Start {}').format(f))
        mes = _('This is {}').format(_('WARNING'))
        ms.Message(f, mes).show_warning()
    
    def show_warning_gui(self):
        f = '[SharedQt] test.Message.show_warning_gui'
        input(_('Start {}').format(f))
        mes = _('This is {}').format(_('WARNING'))
        ms.Message(f, mes, True).show_warning()
    
    def show_error(self):
        f = '[SharedQt] test.Message.show_error'
        input(_('Start {}').format(f))
        mes = _('This is {}').format(_('ERROR'))
        ms.Message(f, mes).show_error()
    
    def show_error_gui(self):
        f = '[SharedQt] test.Message.show_error_gui'
        input(_('Start {}').format(f))
        mes = _('This is {}').format(_('ERROR'))
        ms.Message(f, mes, True).show_error()
    
    def show_question(self):
        f = '[SharedQt] test.Message.show_question'
        input(_('Start {}').format(f))
        mes = _('This is {}').format(_('QUESTION'))
        answer = ms.Message(f, mes).show_question()
        if answer:
            answer = _('Yes')
        else:
            answer = _('No')
        mes = _('Your answer is {}').format(answer)
        ms.Message(f, mes).show_debug()
    
    def show_question_gui(self):
        f = '[SharedQt] test.Message.show_question_gui'
        input(_('Start {}').format(f))
        mes = _('This is {}').format(_('QUESTION'))
        answer = ms.Message(f, mes, True).show_question()
        if answer:
            answer = _('Yes')
        else:
            answer = _('No')
        mes = _('Your answer is {}').format(answer)
        ms.Message(f, mes, True).show_debug()



class Report(Label):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
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
        mes = _('Something went horribly wrong.')
        ms.rep.third_party('[SharedQt] test.Report.third_party', mes)
    
    def condition(self):
        ms.rep.condition('[SharedQt] test.Report.condition', '2 + 2 = 4')
    
    def run_all(self):
        self.cancel()
        self.wrong_input()
        self.empty()
        self.not_ready()
        self.empty_output()
        self.deleted()
        self.matches()
        self.third_party()
        self.condition()


if __name__ == '__main__':
    #Report().run()
    #Root().run()
    #Message().run()
    #Clipboard().run()
    #Label().run()
    #Entry().run()
    #Font().run()
    #Color().run()
    Button().run()
