#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.message.controller as ms


class Root:
    
    def __init__(self):
        from skl_shared.graphics.root.controller import ROOT
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
        from skl_shared.graphics.label.controller import Label
        self.ilabel = Label(text=_('Close this window to quit'), font_family='Mono', font_size=13)
        self.win.setCentralWidget(self.ilabel.widget)



class Font(Label):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_font()
    
    def create_font(self):
        from skl_shared.graphics.font.controller import Font
        self.ifont = Font(self.ilabel.widget, 'Mono', 14)
        self.ifont.run()



class Entry(Label):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_entry()
    
    def create_entry(self):
        from skl_shared.graphics.entry.controller import Entry
        ientry = Entry()
        ientry.set_text('This is an entry')
        self.win.setCentralWidget(ientry.widget)



class Color(Label):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color_name = 'cyan'
        self.create_color()
    
    def create_color(self):
        from skl_shared.graphics.color.controller import Color
        self.icolor = Color(self.color_name)
    
    def get_hex(self):
        f = '[shared] test.Color.get_hex'
        Message(f, _('Start test')).show_info()
        hex_ = self.icolor.get_hex()
        mes = f'HEX value of color "{self.color_name}" is {hex_}'
        Message(f, mes).show_debug()
    
    def modify(self):
        f = '[shared] test.Color.modify'
        Message(f, _('Start test')).show_info()
        darker, lighter = self.icolor.modify()
    
    def run_all(self):
        f = '[shared] test.Color.run_all'
        self.get_hex()
        self.modify()
        Message(f, _('Testing is complete')).show_info()



class Button(Root):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_button()
    
    def click(self, event=None):
        f = '[shared] test.Button.click'
        Message(f, _('Operation is complete.'), True).show_info()
    
    def create_button(self):
        from skl_shared.graphics.button.controller import Button
        from PyQt6.QtWidgets import QWidget, QVBoxLayout
        # .gif images from skl_shared/resources are not supported
        path = '/home/pete/bin/mclient/resources/buttons/go_search.png'
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)
        ibutton = Button(text=_('Click me'), action=self.click
                        ,hint=_('This is a button'), active=path
                        ,inactive=path)
        layout.addWidget(ibutton.widget)
        self.win.setCentralWidget(panel)



class Clipboard(Label):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from skl_shared.graphics.clipboard.controller import Clipboard
        self.clipboard = Clipboard(False)
        self.clipboard_gui = Clipboard(True)
    
    def _copy(self, text='икепцукапвр ваырвар', CopyEmpty=False, Graphical=False):
        f = '[shared] test.Clipboard._copy'
        mes = _('Copy "{}" to clipboard').format(text)
        ms.Message(f, mes).show_debug()
        if Graphical:
            self.clipboard_gui.copy(text, CopyEmpty)
        else:
            self.clipboard.copy(text, CopyEmpty)
    
    def _paste(self):
        f = '[shared] test.Clipboard._paste'
        mes = _('Paste from clipboard')
        ms.Message(f, mes).show_debug()
        mes = _('Pasted text: "{}"').format(self.clipboard.paste())
        ms.Message(f, mes).show_debug()
    
    def copy_paste(self):
        f = '[shared] test.Clipboard.copy_paste'
        input(_('Start {}').format(f))
        self._copy()
        self._paste()
    
    def paste_empty_allowed(self):
        f = '[shared] test.Clipboard.paste_empty_allowed'
        input(_('Start {}').format(f))
        self._copy('', True)
        self._paste()
    
    def paste_empty_not_allowed(self):
        f = '[shared] test.Clipboard.paste_empty_not_allowed'
        input(_('Start {}').format(f))
        self._copy('', False)
        self._paste()
    
    def paste_empty_not_allowed_gui(self):
        f = '[shared] test.Clipboard.paste_empty_not_allowed_gui'
        input(_('Start {}').format(f))
        self._copy('', False, True)
        self._paste()
    
    def paste_error(self):
        f = '[shared] test.Clipboard.paste_error'
        input(_('Start {}').format(f))
        self._copy(b'\x01')
    
    def paste_error_gui(self):
        f = '[shared] test.Clipboard.paste_error_gui'
        input(_('Start {}').format(f))
        self._copy(b'\x01', Graphical=True)
    
    def run_all(self):
        f = '[shared] test.Clipboard.run_all'
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
        f = '[shared] test.Message.console'
        from text_file import Read
        ms.Message(f, _('Start test')).show_info()
        old = ms.GRAPHICAL
        ms.GRAPHICAL = False
        Read('/tmp/aaa').get()
        ms.GRAPHICAL = old
    
    def run_all(self):
        f = '[shared] test.Message.run_all'
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
        f = '[shared] test.Message.show_debug'
        input(_('Start {}').format(f))
        mes = _('This is {}').format(_('DEBUG'))
        ms.Message(f, mes).show_debug()
    
    def show_debug_gui(self):
        f = '[shared] test.Message.show_debug_gui'
        input(_('Start {}').format(f))
        mes = _('This is {}').format(_('DEBUG'))
        ms.Message(f, mes, True).show_debug()
    
    def show_info(self):
        f = '[shared] test.Message.show_info'
        input(_('Start {}').format(f))
        mes = _('This is {}').format(_('INFO'))
        ms.Message(f, mes).show_info()
    
    def show_info_gui(self):
        f = '[shared] test.Message.show_info_gui'
        input(_('Start {}').format(f))
        mes = _('This is {}').format(_('INFO'))
        ms.Message(f, mes, True).show_info()
    
    def show_warning(self):
        f = '[shared] test.Message.show_warning'
        input(_('Start {}').format(f))
        mes = _('This is {}').format(_('WARNING'))
        ms.Message(f, mes).show_warning()
    
    def show_warning_gui(self):
        f = '[shared] test.Message.show_warning_gui'
        input(_('Start {}').format(f))
        mes = _('This is {}').format(_('WARNING'))
        ms.Message(f, mes, True).show_warning()
    
    def show_error(self):
        f = '[shared] test.Message.show_error'
        input(_('Start {}').format(f))
        mes = _('This is {}').format(_('ERROR'))
        ms.Message(f, mes).show_error()
    
    def show_error_gui(self):
        f = '[shared] test.Message.show_error_gui'
        input(_('Start {}').format(f))
        mes = _('This is {}').format(_('ERROR'))
        ms.Message(f, mes, True).show_error()
    
    def show_question(self):
        f = '[shared] test.Message.show_question'
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
        f = '[shared] test.Message.show_question_gui'
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
        ms.rep.cancel('[shared] test.Report.cancel')
    
    def wrong_input(self):
        ms.rep.wrong_input('[shared] test.Report.wrong_input')
    
    def empty(self):
        ms.rep.empty('[shared] test.Report.empty')
    
    def not_ready(self):
        ms.rep.not_ready('[shared] test.Report.not_ready')
    
    def empty_output(self):
        ms.rep.empty_output('[shared] test.Report.empty_output')
    
    def deleted(self):
        ms.rep.deleted('[shared] test.Report.deleted', 50)
    
    def matches(self):
        ms.rep.matches('[shared] test.Report.matches', 50)
    
    def third_party(self):
        mes = _('Something went horribly wrong.')
        ms.rep.third_party('[shared] test.Report.third_party', mes)
    
    def condition(self):
        ms.rep.condition('[shared] test.Report.condition', '2 + 2 = 4')
    
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



class Panel(Root):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_panel()
    
    def create_panel(self):
        from PyQt6.QtWidgets import QWidget, QVBoxLayout
        self.panel = QWidget()
        self.layout = QVBoxLayout()
        self.panel.setLayout(self.layout)
        self.win.setCentralWidget(self.panel)



class CheckBox(Panel):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_checkbox()
    
    def click(self, event=None):
        f = '[shared] test.CheckBox.click'
        ms.Message(f, _('Operation is complete.'), True).show_info()
    
    def create_checkbox(self):
        from skl_shared.graphics.checkbox.controller import CheckBox
        icheckbox = CheckBox(text=_('Select me'), font_family='Mono'
                            ,font_size=12)
        self.layout.addWidget(icheckbox.widget)



class Icon(Label):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon = None
        self.set_icon()
    
    def run_win(self):
        self.win.setWindowIcon(self.icon)
    
    def run_root(self):
        self.root.get_root().setWindowIcon(self.icon)
    
    def run_info(self):
        f = '[shared] test.Icon.run_info'
        ms.Message(f, _('Operation is complete.'), True).show_info()
    
    def run_all(self):
        f = '[shared] test.Icon.run_all'
        if not self.icon:
            ms.rep.empty(f)
            return
        ''' Setting an icon for QWidget (for example, when based on Panel) has
            no effect because we need QMainWindow or QApplication. There is no
            need to set the icon individually for QMessageBox if this icon is
            already set for QApplication.
        '''
        self.run_root()
        #self.run_win()
        self.run_info()
    
    def set_icon(self):
        from skl_shared.graphics.icon.controller import ICON
        ICON.set('/home/pete/bin/mclient/resources/mclient.png')
        self.icon = ICON.get()



class Debug(Label):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_debug()
    
    def create_debug(self):
        f = '[shared] test.Debug.create_debug'
        from skl_shared.graphics.debug.controller import DEBUG
        DEBUG.reset(f, _('Operation is complete.'))
        self.win.setCentralWidget(DEBUG.gui)



class FileDialog(Label):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def run_save_custom(self):
        f = '[shared] test.FileDialog.run_save_custom'
        input(_('Start {}').format(f))
        from skl_shared.graphics.file_dialog.controller import FILE_DIALOG
        filter_ = _('Web-pages (*.htm, *.html)')
        FILE_DIALOG.reset('/tmp', filter_, f)
        file = FILE_DIALOG.save()
        ms.Message(f, f'"{file}"').show_debug()
    
    def run_save_default(self):
        f = '[shared] test.FileDialog.run_save_default'
        input(_('Start {}').format(f))
        from skl_shared.graphics.file_dialog.controller import FILE_DIALOG
        file = FILE_DIALOG.save()
        ms.Message(f, f'"{file}"').show_debug()
    
    def run_save_invalid_dir(self):
        f = '[shared] test.FileDialog.run_save_invalid_dir'
        input(_('Start {}').format(f))
        from skl_shared.graphics.file_dialog.controller import FILE_DIALOG
        FILE_DIALOG.reset('/tmp/456345645645645')
        file = FILE_DIALOG.save()
        ms.Message(f, f'"{file}"').show_debug()
    
    def run_all(self):
        self.run_save_default()
        self.run_save_invalid_dir()
        self.run_save_custom()



class OptionMenu(Label):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_menu()
    
    def get_current(self):
        f = '[shared] test.OptionMenu.get_current'
        ms.Message(f, f'"{self.menu.get()}"').show_debug()
    
    def create_menu(self):
        from skl_shared.graphics.option_menu.controller import OptionMenu
        self.menu = OptionMenu([0, 1, 2, 3, 4], 4, self.get_current)
        self.win.setCentralWidget(self.menu.widget)
        self.show()
    
    def run_common(self):
        ''' Root.run_all is called before Root.show, so we need to show
            the OptionMenu before each test of this class.
        '''
        f = '[shared] test.OptionMenu.run_common'
        input(_('Start {}').format(f))
        lst = ('China', 'Great Britain', 'Island', 'India')
        self.menu.reset(lst, 'India')
        self.show()
    
    def run_digits(self):
        # Non-string tuples and lists must be supported
        f = '[shared] test.OptionMenu.run_digits'
        input(_('Start {}').format(f))
        lst = [0, 1, 2.3, -3, 4, 5, None, __name__, self.__init__]
        self.menu.reset(lst)
        self.show()
    
    def run_get(self):
        f = '[shared] test.OptionMenu.run_get'
        input(_('Start {}').format(f))
        option = self.menu.get()
        ms.Message(f, f'"{option}"').show_debug()
    
    def run_set(self):
        f = '[shared] test.OptionMenu.run_set'
        input(_('Start {}').format(f))
        self.menu.set('Great Britain')
    
    def run_set_invalid(self):
        f = '[shared] test.OptionMenu.run_set_invalid'
        input(_('Start {}').format(f))
        self.menu.set('колбаса')
    
    def run_all(self):
        self.run_common()
        self.run_get()
        self.run_set()
        self.run_set_invalid()
        self.run_digits()



class TempFile:
    
    def __init__(self):
        import temp_file as tf
        self.tf = tf
        ms.GRAPHICAL = False
    
    def create(self):
        f = '[shared] test.TempFile.create'
        input(_('Start {}').format(f))
        path = self.tf.get_file()
        ms.Message(f, f'"{path}"').show_debug()
    
    def create_custom(self):
        f = '[shared] test.TempFile.create_custom'
        input(_('Start {}').format(f))
        path = self.tf.get_file('.dat', True)
        ms.Message(f, f'"{path}"').show_debug()
    
    def run(self):
        self.create()
        self.create_custom()



class PrettyHtml(Label):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = ''
        self.Success = True
        self.file = '/home/pete/tmp/example.html'
        # Almost all tested webpages were invalid
        self.file_invalid = '/home/pete/docs/mclient_tests/multitrancom (saved in browser)/teeth in (2024-10-27).html'
        self.create_debug()
    
    def create_debug(self):
        f = '[shared] test.PrettyHtml.create_debug'
        from skl_shared.graphics.debug.controller import DEBUG
        self.debug = DEBUG
        self.win.setCentralWidget(self.debug.gui)
    
    def load(self):
        from skl_shared.text_file import Read
        f = '[shared] test.PrettyHtml.load'
        if not self.Success:
            ms.rep.cancel(f)
            return
        self.code = Read(self.file).get()
        if not self.code:
            self.Success = False
    
    def make_pretty(self):
        from skl_shared.pretty_html import make_pretty
        f = '[shared] test.PrettyHtml.make_pretty'
        if not self.Success:
            ms.rep.cancel(f)
            return
        return make_pretty(self.code)
    
    def run_pretty(self):
        f = '[shared] test.PrettyHtml.run_pretty'
        input(_('Start {}').format(f))
        self.load()
        self.debug.reset(f, self.make_pretty())
        self.show()    
    
    def run_pretty_errors(self):
        f = '[shared] test.PrettyHtml.run_pretty_errors'
        input(_('Start {}').format(f))
        old = self.file
        self.file = self.file_invalid
        self.load()
        self.debug.reset(f, self.make_pretty())
        self.file = old
    
    def run_all(self):
        self.run_pretty()
        self.run_pretty_errors()



class Online:

    def __init__(self):
        from skl_shared.online import ONLINE
        ms.GRAPHICAL = False
        self.online = ONLINE
    
    def browse_url(self):
        self.base = 'https://ya.ru/search/?text=%s'
        self.pattern = 'Как у нас сегодня дела?'
        self.online.reset(self.base, self.pattern)
        self.online.get_url()
        self.online.browse()
    
    def run_all(self):
        self.browse_url()
    
    def run(self):
        self.run_all()



class Email:

    def __init__(self):
        import skl_shared.logic as lg
        from skl_shared.online import EMAIL
        ms.GRAPHICAL = False
        # Display the entire mailto
        ms.MAX_LEN = 0
        self.iemail = EMAIL
        self.email = lg.email
        self.subject = _('Message Subject')
        self.message = _('Message Body')
        self.file = '/tmp/attach.txt'
    
    def attach(self):
        f = '[shared] test.Email.attach'
        input(_('Start {}').format(f))
        self.iemail.reset(self.email, self.subject, self.message, self.file)
        self.iemail.create()
    
    def create(self):
        f = '[shared] test.Email.create'
        input(_('Start {}').format(f))
        self.iemail.reset(self.email, self.subject, self.message)
        self.iemail.create()
    
    def run_all(self):
        self.create()
        self.attach()
    
    def run(self):
        self.run_all()



class Get(Label):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = ''
        self.create_debug()
    
    def create_debug(self):
        f = '[shared] test.Get.create_debug'
        from skl_shared.graphics.debug.controller import DEBUG
        self.debug = DEBUG
        self.win.setCentralWidget(self.debug.gui)
    
    def get(self):
        f = '[shared] test.Get.get'
        import skl_shared.get_url as gu
        code = gu.Get('https://www.google.com').run()
        self.debug.reset(f, code)
    
    def run_all(self):
        self.get()



class Launch:

    def __init__(self):
        ms.GRAPHICAL = False
    
    def open_file_default(self):
        from skl_shared.launch import Launch
        Launch('/home/pete/tmp/buffer').launch_default()
    
    def run_all(self):
        self.open_file_default()
    
    def run(self):
        self.run_all()



class Time:

    def __init__(self):
        ms.GRAPHICAL = False
        from skl_shared.time import TIME
        self.time = TIME
    
    def get_current_month(self):
        f = '[shared] test.Time.get_current_month'
        month = _(self.time.get_month_name())
        mes = _('Current month: {}').format(month)
        ms.Message(f, mes).show_debug()
    
    def get_current_date(self):
        f = '[shared] test.Time.get_current_date'
        self.time.get_todays_date()
        mes = _('Current date: {}').format(self.time.get_date())
        ms.Message(f, mes).show_debug()
    
    def get_tomorrow(self):
        f = '[shared] test.Time.get_tomorrow'
        self.time.get_todays_date()
        self.time.add_days(1)
        mes = _('Tomorrow’s date: {}').format(self.time.get_date())
        ms.Message(f, mes).show_debug()
    
    def run_all(self):
        self.get_current_date()
        self.get_tomorrow()
        self.get_current_month()
    
    def run(self):
        self.run_all()



class Table:

    def __init__(self):
        ms.GRAPHICAL = False
        
    def run_table(self):
        f = '[shared] test.Table.run_table'
        from skl_shared.table import Table
        from skl_shared.paths import Directory
        from skl_shared.time import Timer
        files = Directory('/home/pete/tmp').get_subfiles()
        headers = (_('#'), _('FILE'))
        nos = []
        for i in range(len(files)):
            nos.append(i + 1)
        timer = Timer(f)
        timer.start()
        print(Table([nos, files], headers, maxrow=50, CutStart=True).run())
        timer.end()
    
    def run_all(self):
        self.run_table()
    
    def run(self):
        self.run_all()



class List:

    def __init__(self):
        ms.GRAPHICAL = False
        
    def get_diff(self):
        f = '[shared] test.List.get_diff'
        import skl_shared.list as ls
        lst1 = [0, 8, 3, 2, 3, 5, 6, 7, 7, 8]
        lst2 = [0, 9, 1, 2, 3, 4, 5, 6, 7, 8]
        ilist = ls.List(lst1, lst2)
        print(ilist.get_diff())
    
    def run_all(self):
        self.get_diff()
    
    def run(self):
        self.run_all()



class Paths:

    def __init__(self):
        ms.GRAPHICAL = False
        import paths
        self.paths = paths
        
    def get_resources(self):
        f = '[shared] test.Paths.get_resources'
        # May be non-existent
        path = self.paths.PDIR.add('..', 'resources')
        path = self.paths.Path(path).get_absolute()
        Message(f, f'"{path}"').show_debug()
    
    def get_path_report(self):
        f = '[shared] test.Paths.get_path_report'
        ipath = self.paths.Path('/home/pete/tmp/Смартфон (конвертировано)/2024-10-11/WP_20241011_09_41_41_Pro.jpg')
        # Does not follow symbolic links
        path = ipath.get_absolute()
        mes = _('Full path: {}').format(f'"{path}"')
        Message(f, mes).show_debug()
        dirname = ipath.get_dirname()
        mes = _('Directory: {}').format(f'"{dirname}"')
        Message(f, mes).show_debug()
        filename = ipath.get_filename()
        mes = _('File name: {}').format(f'"{filename}"')
        Message(f, mes).show_debug()
        basename = ipath.get_basename()
        mes = _('File name without extension: {}').format(f'"{basename}"')
        Message(f, mes).show_debug()
    
    def create(self):
        f = '[shared] test.Paths.create'
        input(_('Start {}').format(f))
        # Recursive by design
        self.paths.Path('/tmp/path0/1/2/3/4/5/6/7/8/9/0').create()
    
    def create_invalid(self):
        f = '[shared] test.Paths.create_invalid'
        input(_('Start {}').format(f))
        # Recursive by design
        self.paths.Path('/tmp/hello/\0').create()
    
    def create_error(self):
        f = '[shared] test.Paths.create_error'
        input(_('Start {}').format(f))
        # Recursive by design
        self.paths.Path('/root/test').create()
    
    def run_all(self):
        self.get_resources()
        self.get_path_report()
        self.create()
        self.create_invalid()
        self.create_error()
    
    def run(self):
        self.run_all()



class Directory:

    def __init__(self):
        ms.GRAPHICAL = False
        import paths
        self.paths = paths
        
    def delete_empty(self):
        f = '[shared] test.Directory.delete_empty'
        input(_('Start {}').format(f))
        # Recursive by design
        path = '/tmp/path0/1/2/3/4/5/6/7/8/9/0'
        self.paths.Path(path).create()
        self.paths.Directory(path).delete_empty()
    
    def delete_empty_error(self):
        f = '[shared] test.Directory.delete_empty_error'
        input(_('Start {}').format(f))
        # Recursive by design
        self.paths.Path('/tmp/path0/1/2/3/4/5/6/7/8/9/0').create()
        self.paths.Directory('/tmp/path0').delete_empty()
    
    def run_all(self):
        self.delete_empty()
        self.delete_empty_error()
    
    def run(self):
        self.run_all()



class Timer:

    def __init__(self):
        ms.GRAPHICAL = False
        from skl_shared.time import Timer
        self.timer = Timer
        
    def run_timer(self):
        f = '[shared] test.Timer.run_timer'
        input(_('Start {}').format(f))
        import time
        timer = self.timer(f)
        timer.start()
        time.sleep(2.5)
        timer.end()
    
    def run_all(self):
        self.run_timer()
    
    def run(self):
        self.run_all()



class TextFile(Label):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from skl_shared.text_file import Read, Write
        self.iread = Read
        self.iwrite = Write
        self.create_debug()
    
    def create_debug(self):
        f = '[shared] test.TextFile.create_debug'
        from skl_shared.graphics.debug.controller import DEBUG
        self.debug = DEBUG
        self.win.setCentralWidget(self.debug.gui)
    
    def load(self):
        f = '[shared] test.TextFile.load'
        input(_('Start {}').format(f))
        file = '/home/pete/tmp/buffer'
        self.debug.reset(f, self.iread(file).get())
        self.show()
    
    def load_non_existent(self):
        f = '[shared] test.TextFile.load_non_existent'
        input(_('Start {}').format(f))
        self.iread('/tmp/ZERO').get()
    
    def load_no_permissions(self):
        f = '[shared] test.TextFile.load_no_permissions'
        input(_('Start {}').format(f))
        self.iread('/etc/shadow').get()
    
    def write(self):
        f = '[shared] test.TextFile.write'
        input(_('Start {}').format(f))
        self.iwrite('/tmp/test').write('test')
    
    def force_rewrite(self):
        f = '[shared] test.TextFile.force_rewrite'
        input(_('Start {}').format(f))
        self.iwrite('/tmp/test', True).write('test')
    
    def rewrite_cancel(self):
        f = '[shared] test.TextFile.rewrite_cancel'
        input(_('Start {}').format(f))
        mes = _('Please answer No here.')
        Message(f, mes, True, True).show_info()
        self.iwrite('/tmp/test').write('test')
    
    def rewrite(self):
        f = '[shared] test.TextFile.rewrite'
        input(_('Start {}').format(f))
        mes = _('Please answer Yes here.')
        Message(f, mes, True, True).show_info()
        self.iwrite('/tmp/test').write('test')
    
    def run_all(self):
        self.load()
        self.load_non_existent()
        self.load_no_permissions()
        self.write()
        self.force_rewrite()
        self.rewrite_cancel()
        self.rewrite()



class Config:

    def __init__(self):
        ms.GRAPHICAL = False
        from skl_shared.config import Config
        self.config = Config
        
    def run_config(self):
        f = '[shared] test.Timer.run_config'
        input(_('Start {}').format(f))
        default = '/home/pete/bin/mclient/resources/config/default.json'
        schema = '/home/pete/bin/mclient/resources/config/schema.json'
        local = '/home/pete/.config/mclient/mclient.json'
        self.config(default, schema, local).run()
    
    def run_all(self):
        self.run_config()
    
    def run(self):
        self.run_all()



class ProgressBar:
    
    def __init__(self):
        from skl_shared.graphics.root.controller import ROOT
        from skl_shared.graphics.progress_bar.controller import ProgressBar
        ROOT.get_root()
        self.root = ROOT
        self.bar = ProgressBar()
    
    def run_basic(self):
        f = '[shared] test.ProgressBar.run_basic'
        input(_('Start {}').format(f))
        self.bar.set_info('Copying files, please wait...')
        self.bar.show()
    
    def run_long_text(self):
        f = '[shared] test.ProgressBar.run_long_text'
        input(_('Start {}').format(f))
        mes = ''
        for i in range(1000):
            mes += str(i)
        self.bar.set_info(mes)
        mes = 'Title ' * 50
        self.bar.set_title(mes)
        self.bar.show()
    
    def run_progress(self):
        f = '[shared] test.ProgressBar.run_progress'
        input(_('Start {}').format(f))
        # time.sleep() will freeze GUI
        from skl_shared.paths import Path, Directory, File
        #path = '/home/pete/tmp'
        path = '/home/pete/.local/share/unmusic/локальная коллекция/10000'
        files = Directory(path).get_subfiles()
        #files = files[:10]
        self.bar.set_max(len(files))
        self.bar.show()
        Path('/tmp/10000').create()
        for file in files:
            # Must be put within the loop
            self.bar.update()
            mes = _('Copy {}').format(file)
            self.bar.set_info(mes)
            filename = Path(file).get_filename()
            dest = f'/tmp/10000/{filename}'
            File(file, dest).copy()
            self.bar.inc()
        self.bar.close()
        from skl_shared.message.controller import Message
        Message(f, 'Goodbye!', 1).show_debug()
    
    def run_all(self):
        self.run_basic()
        self.run_long_text()
        self.run_progress()
    
    def run(self):
        self.run_all()
        self.root.end()


if __name__ == '__main__':
    #Report().run()
    #Root().run()
    #Message().run()
    #Clipboard().run()
    #Label().run()
    #Entry().run()
    #Font().run()
    #Color().run()
    #Button().run()
    #CheckBox().run()
    #Icon().run()
    #Debug().run()
    #FileDialog().run()
    #OptionMenu().run()
    #TempFile().run()
    #PrettyHtml().run()
    #Online().run()
    #Email().run()
    #Get().run()
    #Launch().run()
    #Time().run()
    #Table().run()
    #List().run()
    #Paths().run()
    #Directory().run()
    #Timer().run()
    #TextFile().run()
    #Config().run()
    ProgressBar().run()
