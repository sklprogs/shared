#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.logic as lg
import skl_shared_qt.gui as gi

GUI_MES = True
STOP_MES = False
FONT1 = 'Serif 14'
FONT2 = 'Sans 11'


class Debug:
    
    def __init__(self, func='__main__', mes=''):
        self.set_gui()
        if mes:
            self.reset(func, mes)
    
    def reset(self, func, mes):
        self.set_title(func)
        self.fill(mes)
    
    def set_gui(self):
        self.gui = gi.Debug()
        self.gui.set_icon()
        self.set_bindings()
    
    def set_bindings(self):
        self.gui.bind(('Escape',), self.close)
    
    def fill(self, text):
        self.gui.fill(text)
    
    def set_title(self, title):
        self.gui.set_title(title)
    
    def show(self):
        self.gui.show_maximized()
    
    def close(self):
        self.gui.close()



class Color:
    # Accepts a color name (/usr/share/X11/rgb.txt) or a hex value
    def __init__(self, color):
        self.color = color
        self.gui = gi.Color(color)
    
    def get_hex(self):
        f = '[SharedQt] shared.Color.get_hex'
        # Both None and '' are accepted by Qt, but we need transparency here
        if not self.color:
            com.rep_empty(f)
        return self.gui.get_hex()
    
    def modify(self, factor=150):
        ''' Make a color (a color name (/usr/share/X11/rgb.txt) or a hex value)
            brighter and darker.
        '''
        f = '[SharedQt] shared.Color.modify'
        # Qt does not throw errors on empty input
        darker = lighter = ''
        if not self.color:
            com.rep_empty(f)
            return(darker, lighter)
        if factor <= 0:
            mes = f'{factor} > 0'
            com.rep_condition(f, mes)
            return(darker, lighter)
        try:
            darker, lighter = self.gui.modify(factor)
        except Exception as e:
            com.rep_third_party(f, e)
            return(darker, lighter)
        mes = _('Color: {}, darker: {}, lighter: {}')
        mes = mes.format(self.color, darker, lighter)
        objs.get_mes(f, mes, True).show_debug()
        return(darker, lighter)



class FileDialog:
    
    def __init__(self, parent=None, filter_='', folder='', caption=''):
        self.parent = parent
        self.filter = filter_
        self.folder = folder
        self.caption = caption
        self.set_folder()
        self.set_filter()
        self.gui = gi.FileDialog(self.parent)
        self.gui.set_parent()
        self.gui.set_icon()
    
    def set_folder(self):
        if not self.folder or not Directory(self.folder).Success:
            self.folder = Home().get_home()
    
    def set_filter(self):
        if not self.filter:
            self.filter = _('All files (*.*)')
    
    def save(self):
        if not self.caption:
            self.caption = _('Save File As:')
        try:
            file = self.gui.save (caption = self.caption
                                 ,folder = self.folder
                                 ,filter_ = self.filter
                                 )
        except Exception as e:
            com.rep_third_party(f, e)
        return file



class ProgressBar:
    
    def __init__(self, *args, **kwargs):
        pass
    
    def set_text(self, text=None):
        pass
    
    def set_title(self, text=''):
        pass
    
    def add(self):
        pass
    
    def show(self):
        pass
    
    def close(self):
        pass
    
    def update(self, count, limit):
        #f = '[SharedQt] shared.ProgressBar.update'
        pass



class Font:
    
    def __init__(self, widget, family, size):
        self.Success = True
        self.font = None
        self.family = ''
        self.gui = gi.Font()
        self.widget = widget
        self.family = family
        self.size = size
        self.check()
    
    def fail(self, f, e):
        self.Success = False
        mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
        objs.get_mes(f, mes).show_error()
    
    def set_parent(self):
        f = '[SharedQt] shared.Font.set_parent'
        if not self.Success:
            com.cancel(f)
            return
        try:
            self.gui.set_parent(self.widget, self.font)
        except Exception as e:
            self.fail(f, e)
    
    def set_family(self):
        f = '[SharedQt] shared.Font.set_family'
        if not self.Success:
            com.cancel(f)
            return
        try:
            self.gui.set_family(self.font, self.family)
        except Exception as e:
            self.fail(f, e)
    
    def set_size(self):
        f = '[SharedQt] shared.Font.set_size'
        if not self.Success:
            com.cancel(f)
            return
        try:
            self.gui.set_size(self.font, self.size)
        except Exception as e:
            self.fail(f, e)
    
    def set_font(self):
        f = '[SharedQt] shared.Font.set_font'
        if not self.Success:
            com.cancel(f)
            return
        try:
            self.font = self.gui.get_font()
        except Exception as e:
            self.fail(f, e)
        
    def check(self):
        f = '[SharedQt] shared.Font.check'
        if not self.widget:
            com.rep_empty(f)
            self.Success = False
            return
        if not self.family:
            com.rep_empty(f)
            self.Success = False
            return
        if not self.size:
            com.rep_empty(f)
            self.Success = False
            return
    
    def run(self):
        self.set_font()
        self.set_family()
        self.set_size()
        self.set_parent()



class Entry:
    
    def __init__(self):
        self.gui = gi.Entry()
        self.widget = self.gui.widget
    
    def change_font_size(self, delta=1):
        f = '[SharedQt] shared.Entry.change_font_size'
        size = self.gui.get_font_size()
        if not size:
            com.rep_empty(f)
            return
        if size + delta <= 0:
            mes = f'{size} + {delta} > 0'
            com.rep_condition(f, mes)
            return
        self.gui.set_font_size(size + delta)
    
    def disable(self):
        self.gui.disable()
    
    def enable(self):
        self.gui.enable()
    
    def get_width(self):
        return self.gui.get_width()
    
    def get_root_y(self):
        return self.gui.get_root_y()
    
    def get_x(self):
        return self.gui.get_x()
    
    def set_min_width(self, width):
        self.gui.set_min_width(width)
    
    def set_max_width(self, width):
        self.gui.set_max_width(width)
    
    def bind(self, hotkeys, action):
        self.gui.bind(hotkeys, action)
    
    def reset(self):
        self.clear()
    
    def clear(self):
        self.gui.clear()
    
    def get(self):
        return self.gui.get()
    
    def insert(self, text):
        self.gui.insert(str(text))
    
    def set_text(self, text):
        # Unlike with 'insert', no need to clear the entry first
        self.gui.set_text(str(text))
    
    def focus(self):
        self.gui.focus()



class Top:

    def __init__(self, title='', icon=''):
        self.gui = gi.Top()
        self.widget = self.gui.widget
        self.title = title
        self.icon = icon
    
    def add_widget(self, item):
        f = '[SharedQt] shared.Top.add_widget'
        if hasattr(item, 'widget'):
            self.gui.add_widget(item.widget)
        else:
            mes = _('Wrong input data!')
            objs.get_mes(f, mes, True).show_error()
    
    def show(self):
        self.gui.show()
    
    def close(self):
        self.gui.close()
    
    def bind(self, hotkeys, action):
        self.gui.bind(hotkeys, action)



class TestTop(Top):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_bindings()
    
    def set_bindings(self):
        self.bind(('Ctrl+Q',), self.close)
        self.bind(('Esc',), self.close)



class OptionMenu:
    
    def __init__ (self, items=[], default=None, font_family=None
                 ,font_size=None, action=None):
        self.items = []
        self.action = action
        self.gui = gi.OptionMenu()
        self.widget = self.gui.widget
        # Qt changes default font family upon receiving None
        if font_family and font_size:
            self.gui.set_font(font_family, font_size)
        if items:
            self.reset(items, default)
        self.set_action()
        
    def set_action(self, action=None):
        if action:
            self.action = action
        if self.action:
            self.widget.activated.connect(self.action)
    
    def change_font_size(self, delta=1):
        f = '[SharedQt] shared.OptionMenu.change_font_size'
        size = self.gui.get_font_size()
        if not size:
            com.rep_empty(f)
            return
        if size + delta <= 0:
            mes = f'{size} + {delta} > 0'
            com.rep_condition(f, mes)
            return
        self.gui.set_font_size(size+delta)
    
    def enable(self):
        self.gui.enable()
    
    def disable(self):
        self.gui.disable()
        
    def set(self, item):
        f = '[SharedQt] shared.OptionMenu.set'
        item = str(item)
        if item in self.items:
            self.gui.set(item)
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(item, '; '.join(self.items))
            objs.get_mes(f, mes).show_error()
    
    def fill(self):
        self.gui.fill(self.items)

    def reset(self, items=[], default=None):
        self.items = [str(item) for item in items]
        self.fill()
        if default is not None:
            self.set(default)
        if len(self.items) < 2:
            self.disable()
        else:
            self.enable()

    def get(self):
        return self.gui.get()
    
    def get_index(self):
        return self.gui.get_index()
    
    def set_index(self, index_):
        return self.gui.set_index(index_)

    def set_prev(self):
        index_ = self.get_index()
        if index_ == 0:
            index_ = len(self.items) - 1
        else:
            index_ -= 1
        self.set_index(index_)

    def set_next(self):
        index_ = self.get_index()
        if index_ == len(self.items) - 1:
            index_ = 0
        else:
            index_ += 1
        self.set_index(index_)



class Button(gi.Button):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class DummyMessage:

    def __init__(self, *args):
        pass

    def show_debug(self):
        pass
    
    def show_error(self):
        pass

    def show_info(self):
        pass
                       
    def show_warning(self):
        pass

    def show_question(self):
        pass



class Directory(lg.Directory):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Email(lg.Email):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class FastTable(lg.FastTable):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class File(lg.File):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Get(lg.Get):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Home(lg.Home):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Input(lg.Input):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Launch(lg.Launch):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class List(lg.List):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Log(lg.Log):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class OSSpecific(lg.OSSpecific):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Online(lg.Online):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class ProgramDir(lg.ProgramDir):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Path(lg.Path):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class ReadTextFile(lg.ReadTextFile):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Search(lg.Search):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Text(lg.Text):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Time(lg.Time):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Timer(lg.Timer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class WriteTextFile(lg.WriteTextFile):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Clipboard:

    def __init__(self, Silent=False):
        self.Silent = Silent
        self.gui = gi.Clipboard()

    def copy(self, text, CopyEmpty=True):
        f = '[SharedQt] shared.Clipboard.copy'
        if not (text or CopyEmpty):
            com.rep_empty(f)
            return
        try:
            self.gui.copy(text)
        except Exception as e:
            com.rep_failed(f, e, self.Silent)

    def paste(self):
        f = '[SharedQt] shared.Clipboard.paste'
        try:
            text = self.gui.paste()
        except Exception as e:
            text = ''
            com.rep_failed(f, e, self.Silent)
        # Further possible actions: strip, delete double line breaks
        return text



class Objects(lg.Objects):
    
    def __init__(self):
        ''' #NOTE: Since we use 'super' here, attributes of 'lg.Objects'
            set directly in the controller will not be reflected in
            'logic'. Use 'logic' methods to set attributes.
        '''
        super().__init__()
        self.question = self.info = self.warning = self.debug = self.error \
                      = self.mes = self.waitbox = None
    
    def get_mes(self, func='Logic error', message='Logic error', Silent=False):
        if STOP_MES:
            return DummyMessage()
        if self.mes is None:
            self.mes = Message
        return self.mes(func, message, Silent)
    
    def get_waitbox(self, icon=''):
        if self.waitbox is None:
            if not icon:
                icon = self.icon
            #TODO: Implement
            self.waitbox = None
            #self.waitbox = WaitBox(icon)
        return self.waitbox
    
    def get_root(self):
        return gi.objs.get_root()
    
    def get_error(self):
        if self.error is None:
            self.error = gi.Message().get_error()
        return self.error
    
    def get_warning(self):
        if self.warning is None:
            self.warning = gi.Message().get_warning()
        return self.warning
    
    def get_debug(self):
        # Reusing the same 'info' object may result in GUI glitches
        if self.debug is None:
            self.debug = gi.Message().get_debug()
        return self.debug
    
    def get_info(self):
        if self.info is None:
            self.info = gi.Message().get_info()
        return self.info
    
    def get_question(self):
        if self.question is None:
            self.question = gi.Message().get_question()
        return self.question



class Message:

    def __init__(self, func, message, Silent=False, Block=True):
        self.func = func
        self.message = str(message)
        self.Silent = Silent
        self.Block = Block
        self.set_detailed()

    def set_detailed(self):
        sub = _('Code block: {}').format(self.func)
        self.detailed = f'{self.message}\n\n{sub}'
    
    def show_debug(self):
        if GUI_MES and not self.Silent:
            objs.get_debug().set_text(self.detailed)
            if self.Block:
                objs.debug.exec()
            else:
                objs.debug.show()
        # Duplicate the message to the console
        lg.Message (func = self.func
                   ,message = self.message
                   ).show_debug()
    
    def show_error(self):
        if GUI_MES and not self.Silent:
            objs.get_error().set_text(self.detailed)
            if self.Block:
                objs.error.exec()
            else:
                objs.error.show()
        # Duplicate the message to the console
        lg.Message (func = self.func
                   ,message = self.message
                   ).show_error()

    def show_info(self):
        if GUI_MES and not self.Silent:
            objs.get_info().set_text(self.detailed)
            if self.Block:
                objs.info.exec()
            else:
                objs.info.show()
        # Duplicate the message to the console
        lg.Message (func = self.func
                   ,message = self.message
                   ).show_info()
                       
    def show_warning(self):
        if GUI_MES and not self.Silent:
            objs.get_warning().set_text(self.detailed)
            if self.Block:
                objs.warning.exec()
            else:
                objs.warning.show()
        # Duplicate the message to the console
        lg.Message (func = self.func
                   ,message = self.message
                   ).show_warning()

    def show_question(self):
        if GUI_MES and not self.Silent:
            objs.get_question().set_text(self.detailed)
            # There is not reason in showing non-blocking question dialogs
            objs.question.exec()
            lg.log.append(self.func, 'question', self.message)
            #cur
            '''
            answer = objs.question.ask()
            lg.Message (func = self.func
                       ,message = str(answer)
                       ).show_debug()
            return answer
            '''
        else:
            return lg.Message (func = self.func
                              ,message = self.message
                              ).show_question()



class Commands(lg.Commands):
    
    def __init__(self):
        super().__init__()
        
    def get_image(self, path, width, height):
        f = '[SharedQt] shared.Commands.get_image'
        try:
            return gi.com.get_image (path = path
                                    ,width = width
                                    ,height = height
                                    )
        except Exception as e:
            mes = _('Third-party module has failed!\n\nDetails: {}').format(e)
            objs.get_mes(f, mes, True).show_warning()
    
    def start(self):
        gi.objs.start()
    
    def end(self):
        gi.objs.end()



class CheckBox:
    
    def __init__(self, text='', font_family=None, font_size=None):
        self.gui = gi.CheckBox()
        self.widget = self.gui.widget
        self.gui.set_text(text)
        # Qt changes default font family upon receiving None
        if font_family and font_size:
            self.gui.set_font(font_family, font_size)
    
    def change_font_size(self, delta=1):
        f = '[SharedQt] shared.CheckBox.change_font_size'
        size = self.gui.get_font_size()
        if not size:
            com.rep_empty(f)
            return
        if size + delta <= 0:
            mes = f'{size} + {delta} > 0'
            com.rep_condition(f, mes)
            return
        self.gui.set_font_size(size+delta)
    
    def get(self):
        return self.gui.get()
    
    def set(self, value):
        if value:
            self.enable()
        else:
            self.disable()
    
    def enable(self):
        self.gui.enable()
    
    def disable(self):
        self.gui.disable()
    
    def toggle(self):
        self.gui.toggle()



class Label:
    
    def __init__(self, text='', font_family=None, font_size=None):
        self.gui = gi.Label()
        self.widget = self.gui.widget
        self.set_text(text)
        # Qt changes default font family upon receiving None
        if font_family and font_size:
            self.gui.set_font(font_family, font_size)
    
    def set_action(self, action=None):
        self.gui.set_action(action)
    
    def change_font_size(self, delta=1):
        f = '[SharedQt] shared.Label.change_font_size'
        size = self.gui.get_font_size()
        if not size:
            com.rep_empty(f)
            return
        if size + delta <= 0:
            mes = f'{size} + {delta} > 0'
            com.rep_condition(f, mes)
            return
        self.gui.set_font_size(size + delta)
    
    def set_text(self, text):
        if not text:
            text = '[SharedQt] shared.Label.set_text'
        self.gui.set_text(text)



com = Commands()
objs = Objects()
# Use GUI dialogs for logic-only modules
lg.objs.mes = Message


if __name__ == '__main__':
    f = '[SharedQt] shared.__main__'
    com.start()
    #lg.ReadTextFile('/tmp/aaa').get()
    #Geometry(Top()).activate()
    idebug = Debug(f, 'Here should be some debug info')
    # This MUST be on a separate line, the widget will not be shown otherwise
    idebug.show()
    com.end()
