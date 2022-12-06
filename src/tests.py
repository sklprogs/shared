#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import io
import random

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


ICON = sh.objs.get_pdir().add('..','resources','icon_64x64_cpt.gif')
ICON2 = '/home/pete/bin/mclient/resources/icon_64x64_mclient.gif'
FILE = '/home/pete/base/[unmusic] corrupted tags.txt'
SILENT = False


class Scrollable:

    def __init__ (self,mode='img',image_path='',ScrollX=True
                 ,title=_('Scrollable widget'),icon=''
                 ,width=800,height=600,xborder=5,yborder=0
                 ,Maximize=False
                 ):
        self.modes = ('lbl','img')
        self.label_no = 1
        self.mode = mode
        self.image_path = image_path
        self.title = title
        self.icon = icon
        self.width = width
        self.height = height
        self.xborder = xborder
        self.yborder = yborder
        self.ScrollX = ScrollX
        self.Maximize = Maximize
    
    def run(self):
        self.iscroll = sh.ScrollableC (ScrollX = self.ScrollX
                                      ,title = self.title
                                      ,icon = self.icon
                                      ,width = self.width
                                      ,height = self.height
                                      ,xborder = self.xborder
                                      ,yborder = self.yborder
                                      ,Maximize = self.Maximize
                                      )
        self.set_widgets()
        # Do this only after filling the widget with a content
        self.iscroll.adjust_by_content()
        self.iscroll.show()
    
    def add_row(self):
        sub = []
        for i in range(30):
            sub.append('hello {}'.format(i+1))
        sub = _('Label {}').format(self.label_no) + ' ' + ' '.join(sub)
        self.label_no += 1
        frm_row = sh.Frame (parent = self.iscroll.get_content_frame()
                           ,expand = False
                           ,fill = 'x'
                           ,side = 'top'
                           )
        cbx_row = sh.CheckBox (parent = frm_row
                              ,side = 'left'
                              )
        lbl_row = sh.Label (parent = frm_row
                           ,side = 'left'
                           ,text = sub
                           )
    
    def set_image(self):
        f = '[shared] tests.Scrollable.set_image'
        if self.image_path:
            if sh.File(self.image_path).Success:
                iimage = im.Image()
                iimage.open(self.image_path)
                self.lbl_img.widget.config(image=iimage.image)
                ''' This prevents the garbage collector from deleting
                    the image.
                '''
                self.lbl_img.widget.image = iimage.image
            else:
                mes = _('Wrong input data!')
                sh.objs.get_mes(f,mes,True).show_warning()
        else:
            sh.com.rep_empty(f)
    
    def set_labels(self):
        for i in range(50):
            self.add_row()
    
    def set_image_label(self):
        self.lbl_img = sh.Label (parent = self.iscroll.get_content_frame()
                                ,text = _('Image')
                                )
    
    def set_widgets(self):
        f = '[shared] tests.Scrollable.set_widgets'
        if self.mode == 'lbl':
            self.set_labels()
        elif self.mode == 'img':
            self.set_image_label()
            self.set_image()
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(self.mode,'; '.join(self.modes))
            sh.objs.get_mes(f,mes).show_error()



class Commands:
    
    def __init__(self):
        pass
    
    def run_password(self):
        ipass = pw.Password()
        ipass.show()
        login = ipass.get_login()
        password = ipass.get_password()
        mes = _('Login: "{}"').format(login)
        sh.objs.get_mes(f,mes,True).show_info()
        mes = _('Password: "{}"').format(password)
        sh.objs.get_mes(f,mes,True).show_info()
    
    def run_scrollable(self):
        iscroll = Scrollable (mode = 'lbl'
                             ,image_path = '/home/pete/bin/ImageViewer/resources/Gnu_(PSF).png'
                             ,ScrollX = 1
                             ,title = _('Hello!')
                             ,icon = ICON
                             ,width = 1024
                             ,height = 800
                             ,xborder = 10
                             ,yborder = 10
                             ,Maximize = 0
                             )
        iscroll.run()
        iscroll.mode = 'img'
        iscroll.run()
    
    def check_spelling(self):
        f = '[shared] tests.Commands.check_spelling'
        import skl_shared.spelling as sp
        text = sh.ReadTextFile('/home/pete/tmp/check_spelling.txt').get()
        itop = sh.Top(title=_('Spellchecker'))
        itxt = sp.TextBoxTk(itop)
        itxt.reset(text)
        timer = sh.Timer(f)
        timer.start()
        itxt.check_spell()
        timer.end()
        itop.show()
    
    def run_panes4(self):
        #text1 = '1. Ничего (10) еще не предрешено (α) заранее (b10).'
        #text2 = '1. Nothing (10) has been determined (α) earlier (b10).'
        text1 = sh.ReadTextFile('/home/pete/tmp/large_file.txt').get()
        text2 = sh.ReadTextFile('/home/pete/tmp/large_file2.txt').get()
        text3 = text1
        text4 = text2
        ipanes = sh.Panes4 (text1 = text1
                           ,text2 = text2
                           ,text3 = text3
                           ,text4 = text4
                           )
        ipanes.show()
    
    def run_panes2(self):
        #text1 = '1. Ничего (10) еще не предрешено (α) заранее (b10).'
        #text2 = '1. Nothing (10) has been determined (α) earlier (b10).'
        text1 = sh.ReadTextFile('/home/pete/tmp/large_file.txt').get()
        text2 = sh.ReadTextFile('/home/pete/tmp/large_file2.txt').get()
        ipanes = sh.Panes2 (text1 = text1
                           ,text2 = text2
                           )
        ipanes.show()
    
    def create_button(self):
        self.btn = sh.Button (parent = sh.Top()
                             ,inactive = '/home/pete/bin/mclient/resources/buttons/icon_36x36_block_off.gif'
                             ,active = '/home/pete/bin/mclient/resources/buttons/icon_36x36_block_on.gif'
                             ,Focus = True
                             )
    
    def run_all(self):
        '''
        self.get_free_space()
        self.get_size()
        self.get_size_range()
        self.test_button(self.run_button_trigger)
        self.run_canvas()
        self.run_checkbox()
        self.run_clipboard()
        self.run_entry()
        self.run_entryc()
        self.run_fast_table()
        self.run_frameless()
        self.run_geometry()
        '''
        self.run_listbox()
        self.run_listboxc()
        self.run_messages()
        self.run_multcboxes()
        self.run_multcboxesc()
        self.run_optionmenu()
        self.run_optionmenu_trigger()
        self.run_progressbar()
        self.run_progressbar0()
        self.run_progressbaritem()
        self.run_scrollbar()
        self.run_simple_top()
        self.run_symbol_map()
        self.run_textbox()
        self.run_textboxc()
        self.run_textboxro()
        self.run_textboxrw()
        self.run_top()
        self.run_waitbox()
        self.set_button()
        self.set_figure_commas()
        self.set_font()
        self.set_frame()
        self.set_label()
        self.set_panes()
        self.set_random_coor()
        self.trigger_cbox()
    
    def _fast_table1(self):
        mes = _('Variant #{}').format(1)
        self.iwrite.write(mes)
        self.iwrite.write('\n')
        mes = _('Description: no settings')
        self.iwrite.write(mes)
        self.iwrite.write('\n')
        
        iterable = [[0,1,2]
                   ,['/home/pete','/home','/']
                   ,['notes.txt','Trash.info','bash']
                   ]
        mes = sh.FastTable(iterable).run()
        
        self.iwrite.write(mes)
        self.iwrite.write('\n\n')
    
    def _fast_table2(self):
        mes = _('Variant #{}').format(2)
        self.iwrite.write(mes)
        self.iwrite.write('\n')
        mes = _('Description: headers')
        self.iwrite.write(mes)
        self.iwrite.write('\n')
        
        iterable = ([0,1,2]
                   ,['/home/pete','/home','/']
                   ,['notes.txt','Trash.info','bash']
                   )
        headers = ('NO','DIRECTORY','FILE')
        mes = sh.FastTable (iterable = iterable
                           ,headers = headers
                           ).run()
        
        self.iwrite.write(mes)
        self.iwrite.write('\n\n')
    
    def _fast_table3(self):
        mes = _('Variant #{}').format(3)
        self.iwrite.write(mes)
        self.iwrite.write('\n')
        mes = _('Description: transposition')
        self.iwrite.write(mes)
        self.iwrite.write('\n')
        
        iterable = ((0,'/home/pete','notes.txt')
                   ,(1,'/home','Trash.info')
                   ,(2,'/','bash')
                   )
        mes = sh.FastTable (iterable = iterable
                           ,Transpose = True
                           ).run()
        
        self.iwrite.write(mes)
        self.iwrite.write('\n\n')
    
    def _fast_table4(self):
        mes = _('Variant #{}').format(4)
        self.iwrite.write(mes)
        self.iwrite.write('\n')
        mes = _('Description: transposition and headers')
        self.iwrite.write(mes)
        self.iwrite.write('\n')
        
        iterable = [(0,'/home/pete','notes.txt')
                   ,(1,'/home','Trash.info')
                   ,(2,'/','bash')
                   ]
        headers = ['NO','DIRECTORY','FILE']
        mes = sh.FastTable (iterable = iterable
                           ,headers = headers
                           ,Transpose = True
                           ).run()
        
        self.iwrite.write(mes)
        self.iwrite.write('\n\n')
    
    def run_fast_table(self):
        f = '[shared] tests.Commands.run_fast_table'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        self.iwrite = io.StringIO()
        self._fast_table1()
        self._fast_table2()
        self._fast_table3()
        self._fast_table4()
        mes = self.iwrite.getvalue()
        self.iwrite.close()
        sh.com.run_fast_txt (text = mes
                            ,font = 'Mono 12'
                            )
    
    def set_figure_commas(self):
        f = '[shared] tests.Commands.set_figure_commas'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        vals = [None,'',0,-1,-123456,-1234567,-12.34,123456,1234567
               ,56874867845678456845678456845,'hello'
               ]
        for old in vals:
            new = sh.com.set_figure_commas(old)
            mes = '"{}" -> "{}"'.format(old,new)
            sh.objs.get_mes(f,mes,SILENT).show_debug()
    
    def run_textboxro(self):
        f = '[shared] tests.Commands.run_textboxro'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        text = sh.ReadTextFile(FILE).get()
        itxt = sh.TextBoxRO (Maximize = False
                            ,title = 'TextBoxRO with Selection and Search'
                            ,icon = ICON
                            )
        itxt.insert(text)
        itxt.focus()
        itxt.show()
        result = sh.Text(itxt.get()).shorten(max_len=20)
        mes = _('Output: "{}"').format(result)
        sh.objs.get_mes(f,mes,SILENT).show_debug()
    
    def run_textboxrw(self):
        f = '[shared] tests.Commands.run_textboxrw'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        text = sh.ReadTextFile(FILE).get()
        text = text.strip()
        text = sh.Text (text = text
                       ,Auto = True
                       ).text
        itxt = sh.TextBoxRW (Maximize = False
                            ,title = 'TextBoxRW with Selection and Search'
                            ,icon = ICON
                            )
        itxt.insert(text)
        itxt.focus()
        itxt.show()
        result = sh.Text(itxt.get()).shorten(max_len=20)
        mes = _('Output: "{}"').format(result)
        sh.objs.get_mes(f,mes,SILENT).show_debug()
    
    def run_textboxc(self):
        f = '[shared] tests.Commands.run_textboxc'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        text = sh.ReadTextFile(FILE).get()
        text = sh.Text (text = text
                       ,Auto = True
                       ).text
        itxt = sh.TextBoxC (Maximize = False
                           ,title = 'TextBoxC with Selection and Search'
                           ,icon = ICON
                           )
        itxt.insert(text)
        itxt.check_spell()
        itxt.focus()
        itxt.show()
        result = sh.Text(itxt.get()).shorten(max_len=20)
        mes = _('Output: "{}"').format(result)
        sh.objs.get_mes(f,mes,SILENT).show_debug()
    
    def set_panes(self):
        f = '[shared] tests.Commands.set_panes'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        text = sh.ReadTextFile(FILE).get()
        text = sh.Text (text = text
                       ,Auto = True
                       ).text
        ipanes = sh.Panes4 (bg = 'old lace'
                           ,Extend = True
                           )
        ipanes.reset(text,text,text,text)
        ipanes.show()
    
    def run_textbox(self):
        f = '[shared] tests.Commands.run_textbox'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        text = sh.ReadTextFile(FILE).get()
        text = sh.Text (text = text
                       ,Auto = True
                       ).text
        parent = sh.Top (title = 'TextBox with Selection and Search'
                        ,icon = ICON
                        ,AutoCr = False
                        )
        itxt = sh.TextBox (parent = parent
                          ,expand = 1
                          ,side = None
                          ,fill = 'both'
                          ,font = 'Serif 14'
                          ,ScrollX = True
                          ,ScrollY = True
                          ,wrap = 'word'
                          ,icon = ICON
                          )
        itxt.insert(text)
        itxt.focus()
        parent.show()
        result = sh.Text(itxt.get()).shorten(max_len=20)
        mes = _('Output: "{}"').format(result)
        sh.objs.get_mes(f,mes,SILENT).show_debug()
    
    def run_entryc(self):
        f = '[shared] tests.Commands.run_entryc'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        ient = sh.EntryC (title = 'This is an Entry'
                         ,icon = ICON
                         )
        ient.show()
        mes = _('Output: "{}"').format(ient.get())
        sh.objs.get_mes(f,mes,SILENT).show_debug()
    
    def run_entry(self):
        f = '[shared] tests.Commands.run_entry'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        parent = sh.Top()
        ient = sh.Entry (parent = parent
                        ,side = 'left'
                        ,ipadx = 5
                        ,ipady = 5
                        ,fill = 'x'
                        ,width = 10
                        ,expand = None
                        ,font = 'Sans 11'
                        ,bg = 'blue'
                        ,fg = 'red'
                        ,justify = 'right'
                        )
        ient.focus()
        ient.insert('Anything')
        ient.disable()
        parent.show()
    
    def run_multcboxesc(self):
        f = '[shared] tests.Commands.run_multcboxesc'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        text = '\n'.join([str(i+1) for i in range(100)])
        imult = sh.MultCBoxesC (text = text
                               ,width = 550
                               ,height = 400
                               ,font = 'Sans 11'
                               ,MarkAll = False
                               ,icon = ICON
                               )
        imult.show()
        mes = imult.get_selected()
        sh.objs.get_mes(f,mes,SILENT).show_debug()
    
    def run_multcboxes(self):
        f = '[shared] tests.Commands.run_multcboxes'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        parent = sh.Top()
        imult = sh.MultCBoxes (parent = parent
                              ,text = 'Hello\nBye\nHello again'
                              ,font = 'Sans 11'
                              ,MarkAll = False
                              )
        parent.show()
    
    def trigger_cbox(self,event=None):
        f = '[shared] tests.Commands.trigger_cbox'
        mes = _('Output: "{}"').format(self.cbx.get())
        sh.objs.get_mes(f,mes,SILENT).show_debug()
    
    def run_checkbox(self):
        f = '[shared] tests.Commands.run_checkbox'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        parent = sh.Top()
        sh.Geometry(parent).set('100x100')
        parent.set_title('CheckBox')
        self.cbx = sh.CheckBox (parent = parent
                               ,Active = False
                               ,side = 'left'
                               ,action = self.trigger_cbox
                               )
        self.lbl = sh.Label (parent = parent
                            ,text = 'Label'
                            ,side = 'left'
                            )
        sh.com.bind (obj = self.lbl
                    ,bindings = '<ButtonRelease-1>'
                    ,action = self.trigger_cbox
                    )
        parent.show()
    
    def run_progressbar(self):
        f = '[shared] tests.Commands.run_progressbar'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        top = sh.Top(AutoCr=False)
        iprog = sh.ProgressBar (width = 750
                               ,height = 200
                               ,YScroll = True
                               ,title = 'Load dictionaries'
                               ,icon = ICON
                               )
        for i in range(10):
            iprog.add()
        iprog.show()
        top.show()
    
    def run_progressbaritem(self):
        f = '[shared] tests.Commands.run_progressbaritem'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        parent = sh.Top()
        iprog = sh.ProgressBarItem (parent = parent
                                   ,orient = 'horizontal'
                                   ,length = 100
                                   ,mode = 'determinate'
                                   )
        parent.show()
    
    def run_canvas(self):
        f = '[shared] tests.Commands.run_canvas'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        parent = sh.Top()
        parent.set_title('Canvas')
        icanvas = sh.Canvas (parent = parent
                            ,expand = True
                            ,side = None
                            ,region = None
                            ,width = None
                            ,height = None
                            ,fill = 'both'
                            )
        sh.Geometry(parent=parent).set('1024x768')
        frame = sh.Frame (parent = parent)
        # This frame must be created after the bottom frame
        frame1 = sh.Frame (parent = frame)
        canvas = sh.Canvas(parent = frame1)

        label = sh.Label (parent = frame1
                         ,expand = True
                         ,fill = 'both'
                         ,text = 'Hello, Canvas!'
                         ,fg = 'white'
                         ,bg = 'blue'
                         )

        icanvas.embed(frame)
        icanvas.focus()
        icanvas.set_top_bindings(top=parent)
        parent.show()
    
    def run_clipboard(self):
        ''' #NOTE: Clipboard actions should be tested in Tkinter GUI
            since it may freeze when using pyperclip.
        '''
        f = '[shared] tests.Commands.run_clipboard'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        mes = _('Copy something to clipboard')
        sh.objs.get_mes(f,mes).show_info()
        sub = sh.Clipboard().paste()
        mes = _('Clipboard contents: "{}"').format(sub)
        sh.objs.get_mes(f,mes).show_debug()
        input(_('Press any key to continue'))
        sub = 'Hello! Это тест! αβàáҖҚŸ'
        mes = _('The following will be copied: "{}"').format(sub)
        sh.objs.get_mes(f,mes).show_info()
        input(_('Press any key to continue'))
        sh.Clipboard().copy(sub)
        sub = sh.Clipboard().paste()
        mes = _('Clipboard contents: "{}"').format(sub)
        sh.objs.get_mes(f,mes).show_debug()
    
    def run_symbol_map(self):
        f = '[shared] tests.Commands.run_symbol_map'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        imap = sh.SymbolMap (items = 'àáâäāãæßćĉçèéêēёëəғĝģĥìíîïīĵķļñņòóôõöōœøšùúûūŭũüýÿžжҗқңәөүұÀÁÂÄĀÃÆSSĆĈÇÈÉÊĒЁËƏҒĜĢĤÌÍÎÏĪĴĶĻÑŅÒÓÔÕÖŌŒØŠÙÚÛŪŬŨÜÝŸŽЖҖҚҢӘӨҮҰ'
                            ,title = ''
                            ,icon = '/home/pete/bin/mclient/resources/icon_64x64_mclient.gif'
                            )
        imap.show()
        mes = _('Your input: "{}"').format(imap.get())
        sh.objs.get_mes(f,mes,SILENT).info()
    
    def run_optionmenu_trigger(self,event=None):
        f = '[shared] tests.Commands.run_optionmenu_trigger'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        mes = _('Your input: "{}"').format(self.opt_prm.choice)
        sh.objs.get_mes(f,mes,SILENT).show_debug()
    
    def run_optionmenu(self):
        f = '[shared] tests.Commands.run_optionmenu'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        parent = sh.Top()
        sh.Geometry(parent).set('300x40')
        parent.set_title('OptionMenu')
        self.opt_prm = sh.OptionMenu (parent = parent
                                     ,items = None
                                     ,side = 'left'
                                     ,anchor = 'center'
                                     ,action = self.optionmenu_trigger
                                     ,tfocus = 1
                                     ,default = None
                                     ,Combo = True
                                     ,expand = False
                                     ,fill = None
                                     ,font = 'Sans 11'
                                     )
        parent.show()
        parent.set_title(_('New settings'))
        self.opt_prm.reset (items = (33,34,345,345)
                           ,default = 345
                           ,action = self.optionmenu_trigger
                           )
        parent.show()
    
    def run_listboxc(self):
        f = '[shared] tests.Commands.run_listboxc'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        #lst = [i for i in range(15)]
        lst = sh.Directory(sh.Home().get_home()).get_files()
        self.lbx_prm = sh.ListBoxC (Multiple = False
                                   ,lst = lst
                                   ,action = None
                                   ,side = None
                                   ,expand = True
                                   ,fill = 'both'
                                   ,title = 'ListBox (All)'
                                   ,icon = '/home/pete/bin/mclient/resources/icon_64x64_mclient.gif'
                                   ,ScrollX = True
                                   ,ScrollY = True
                                   )
        self.lbx_prm.show()
        mes = _('Your final selection: "{}"').format(self.lbx_prm.get())
        sh.objs.get_mes(f,mes,SILENT).show_debug()
        '''
        self.lbx_prm.reset (lst = (_('Mexico'),_('Canada'),_('Russia'))
                           ,title = _('New settings')
                           ,icon = ICON
                           )
        self.lbx_prm.show()
        print('Your final selection: "{}"'.format(self.lbx_prm.get()))
        '''
    
    def _trigger_lbx(self,event=None):
        f = '[shared] tests.Commands._trigger_lbx'
        text = self.lbx_prm.get()
        mes = _('Your input: "{}"').format(text)
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def run_listbox(self):
        f = '[shared] tests.Commands.run_listbox'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        parent = sh.Top()
        parent.title('ListBox')
        lst = [i for i in range(15)]
        self.lbx_prm = sh.ListBox (parent = parent
                                  ,Multiple = False
                                  ,lst = lst
                                  ,action = self._trigger_lbx
                                  ,side = None
                                  ,expand = True
                                  ,fill = 'both'
                                  )
        self.lbx_prm.focus()
        parent.show()
    
    def run_scrollbar(self):
        f = '[shared] tests.Commands.run_scrollbar'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        text = '\n'.join([('('+str(i)+')'+f+' ')*(i+1) for i in range(100)])
        parent = sh.Top()
        parent.title('Y Scrollbar')
        ''' #NOTE: when the widget width is <580, the scrollbar will not
            be visible.
        '''
        sh.Geometry(parent).set('600x400')
        
        frm_prm = sh.Frame (parent = parent
                           ,side = 'left'
                           )
        frm_ver = sh.Frame (parent = parent
                           ,side = 'right'
                           ,expand = False
                           ,fill = 'y'
                           )
        frm_txt = sh.Frame (parent = frm_prm
                           ,side = 'top'
                           )
        frm_hor = sh.Frame (parent = frm_prm
                           ,side = 'bottom'
                           ,expand = False
                           ,fill = 'x'
                           )
        
        #TODO: use 'TextBox'
        import tkinter as tk
        widget = tk.Text(frm_txt.widget,wrap='none')
        widget.pack(expand=True,fill='both')
        widget.insert('1.0',text)
        txt = sh.gi.WidgetObject(widget)
        txt.widget.focus_set()
        
        sh.Scrollbar (parent = frm_hor
                     ,scroll = txt
                     ,Horiz = True
                     )
        sh.Scrollbar (parent = frm_ver
                     ,scroll = txt
                     ,Horiz = False
                     )
        parent.show()
    
    def run_waitbox(self):
        f = '[shared] tests.Commands.run_waitbox'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        import time
        icon1 = ICON
        icon2 = ICON2
        sh.objs.get_waitbox().set_icon(icon1)
        sh.objs.waitbox.reset (func = f
                              ,message = None
                              )
        sh.objs.waitbox.show()
        time.sleep(3)
        sh.objs.waitbox.close()
        
        sh.objs.waitbox.set_icon(icon2)
        sh.objs.waitbox.reset (func = f
                              ,message = 'Hello! I\'m still here!'
                              )
        sh.objs.waitbox.show()
        time.sleep(3)
        sh.objs.waitbox.close()
    
    def test_button(self,action=None):
        self.create_button()
        if action:
            self.btn.action = action
        self.btn.show()
        self.btn.parent.kill()
    
    def run_button_trigger(self,event=None):
        f = '[shared] tests.Commands.run_button_trigger'
        ''' #TODO: this works partially: silent messages do not pass
            here, label colors are changed when the mouse pointer is not
            over them (when using mouse).
        '''
        mes = _('The event has been triggered!')
        sh.objs.get_mes(f,mes,True).show_debug()
        if self.btn.Status:
            self.btn.widget.config (bg = 'green'
                                   ,fg = 'black'
                                   )
            self.btn.inactivate()
        else:
            self.btn.widget.config (bg = 'yellow'
                                   ,fg = 'red'
                                   )
            self.btn.activate()
    
    def set_button(self):
        f = '[shared] tests.Commands.set_button'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        parent = sh.Top()
        parent.title(_('Button'))
        self.btn_trg = sh.Button (parent = parent
                                 ,side = 'top'
                                 ,action = self.button_trigger
                                 ,text = _('Trigger an event')
                                 ,font = 'Sans 14 bold'
                                 ,hint = 'A sample hint'
                                 ,bindings = ('<Control-s>','<F2>')
                                 )
        self.btn_img = sh.Button (parent = parent
                                 ,action = None
                                 ,hint = 'This is a hint'
                                 ,inactive = '/home/pete/bin/mclient/resources/buttons/icon_36x36_watch_clipboard_off.gif'
                                 ,active = '/home/pete/bin/mclient/resources/buttons/icon_36x36_watch_clipboard_on.gif'
                                 ,text = 'Press me'
                                 ,height = 36
                                 ,width = 36
                                 ,side = 'top'
                                 ,expand = 0
                                 ,bg = None
                                 ,bg_focus = None
                                 ,fg = None
                                 ,fg_focus = None
                                 ,bd = 0
                                 ,hdelay = 800
                                 ,hbg = '#ffffe0'
                                 ,hdir = 'top'
                                 ,hbwidth = 1
                                 ,hbcolor = 'navy'
                                 ,fill = 'both'
                                 ,Focus = True
                                 ,font = None
                                 )
        parent.show()
    
    def set_frame(self):
        f = '[shared] tests.Commands.set_frame'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        iframe = sh.Frame (parent = sh.Top()
                          ,expand = 1
                          ,fill = 'both'
                          ,side = None
                          ,padx = 10
                          ,pady = 10
                          ,ipadx = None
                          ,ipady = None
                          ,bd = 2
                          ,bg = 'blue'
                          ,width = 200
                          ,height = 200
                          ,propag = False
                          )
        iframe.set_title('Frame')
        sh.Label (parent = iframe
                 ,text = 'Label'
                 ,bg = 'red'
                 ,fg = 'orange'
                 )
        iframe.show()
    
    def _set_random_coor(self,w,h):
        f = '[shared] tests.Commands._set_random_coor'
        x = 0
        y = 0
        max_x, max_y = sh.objs.get_root().get_resolution()
        x = random.randint(0,max_x)
        y = random.randint(0,max_y)
        if w + x > max_x:
            x = max_x - w
        if h + y > max_y:
            y = max_y - h
        messages = []
        mes = _('Screen resolution: {}x{}').format(max_x,max_y)
        messages.append(mes)
        mes = _('Random coordinates: x: {}; y: {}').format(x,y)
        messages.append(mes)
        mes = '\n'.join(messages)
        sh.objs.mes(f,mes,True).show_debug()
        return(x,y)
    
    def _get_size_range(self,event=None):
        f = '[shared] tests.Commands._get_size_range'
        v1 = 0
        v2 = 0
        while abs(v1-v2) <= 40:
            v1 = random.randint(90,250)
            v2 = random.randint(90,250)
        sh.objs.get_mes(f,(v1,v2),True).show_debug()
        return(v1,v2)
    
    def run_frameless(self):
        f = '[shared] tests.Commands.run_frameless'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        top = sh.Top()
        top1 = sh.Top (AutoCr = False
                      ,Lock = False
                      )
        top2 = sh.Top (AutoCr = False
                      ,Lock = False
                      )
        top.set_title('Host')
        sh.Geometry(top).set('150x150')
        
        top1.widget.wm_overrideredirect(1)
        top2.widget.wm_overrideredirect(1)
        
        sh.Label (parent = top
                 ,text = 'HOST'
                 ,bg = 'black'
                 ,fg = 'red'
                 ,expand = True
                 ,fill = 'both'
                 )
        sh.Label (parent = top1
                 ,text = 'TOP1'
                 ,bg = 'green'
                 ,fg = 'orange'
                 ,expand = True
                 ,fill = 'both'
                 )
        sh.Label (parent = top2
                 ,text = 'TOP2'
                 ,bg = 'red'
                 ,fg = 'orange'
                 ,expand = True
                 ,fill = 'both'
                 )
        
        w1, w2 = com._get_size_range()
        h1, h2 = com._get_size_range()
        
        x1, y1 = com._set_random_coor(h1,w1)
        x2, y2 = com._set_random_coor(h2,w2)
        
        geom = sh.Geometry(parent=top1)
        geom.geom = '%dx%d+%d+%d' % (w1,h1,x1,y1)
        geom.restore()
        
        geom = sh.Geometry(parent=top2)
        geom.geom = '%dx%d+%d+%d' % (w2,h2,x2,y2)
        geom.restore()
        
        top1.show()
        top2.show()
        top.show()
        top.kill()
        top1.kill()
        top2.kill()
    
    def set_label(self):
        f = '[shared] tests.Commands.set_label'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        lbl = sh.Label (parent = sh.Top()
                       ,text = 'Hello! It\'s me again'
                       ,font = 'Sans 14'
                       ,side = 'right'
                       ,fill = 'both'
                       ,expand = False
                       ,ipadx = 30
                       ,ipady = 10
                       ,image = None
                       ,fg = 'orange'
                       ,bg = 'green'
                       ,anchor = None
                       ,width = None
                       ,height = None
                       ,justify = 'left'
                       )
        lbl.set_title('Label test')
        lbl.show()
    
    def run_simple_top(self):
        f = '[shared] tests.Commands.run_simple_top'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        icon_path = '/home/pete/bin/mclient/resources/icon_64x64_mclient.gif'
        itop = sh.Top(Lock=False)
        itop.set_title('Welcome to shared')
        itop.set_icon(icon_path)
        itop.show()
        itop.center()
        import time
        time.sleep(2)
    
    def run_geometry(self):
        f = '[shared] tests.Commands.run_geometry'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        import time
        parent = sh.Top(Lock=False)
        igeo = sh.Geometry(parent)
        igeo.set('340x250')
        parent.update_idle()
        time.sleep(3)
        igeo.minimize()
        parent.update_idle()
        time.sleep(3)
        igeo.focus()
        igeo.set_foreground()
        igeo.lift()
        igeo.activate()
        igeo.restore()
        igeo.maximize()
        igeo.update()
        igeo.save()
        mes = _('Window handle (Windows-only): {}')
        mes = mes.format(igeo.get_hwnd())
        sh.objs.mes(f,mes,SILENT).show_debug()
        parent.show()
        parent.kill()
    
    def run_top(self):
        f = '[shared] tests.Commands.run_top'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        icon_path = '/home/pete/bin/mclient/resources/icon_64x64_mclient.gif'
        itop = sh.Top (Maximize = False
                      ,AutoCr = True
                      ,Lock = True
                      ,icon = icon_path
                      ,title = 'Welcome to shared'
                      )
        itop.show()
    
    def run_messages(self):
        f = '[shared] tests.Commands.run_messages'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        mes = 'This is a GUI DEBUG message'
        sh.objs.get_mes(f,mes).show_debug()
        mes = 'This is a GUI INFO message'
        sh.objs.get_mes(f,mes).show_info()
        mes = 'This is a GUI QUESTION message'
        answer = sh.objs.get_mes(f,mes).show_question()
        if answer:
            mes = _('You answered Yes')
        else:
            mes = _('You answered No')
        sh.objs.get_mes(f,mes,True).show_debug()
        mes = 'This is a GUI WARNING message'
        sh.objs.get_mes(f,mes).show_warning()
        mes = 'This is a GUI ERROR message'
        sh.objs.get_mes(f,mes).show_error()
        mes = 'This is a CLI DEBUG message'
        sh.objs.get_mes(f,mes,True).show_debug()
        mes = 'This is a CLI INFO message'
        sh.objs.get_mes(f,mes,True).show_info()
        mes = 'This is a CLI QUESTION message'
        answer = sh.objs.get_mes(f,mes,True).show_question()
        if answer:
            mes = _('You answered Yes')
        else:
            mes = _('You answered No')
        sh.objs.get_mes(f,mes,True).show_debug()
        mes = 'This is a CLI WARNING message'
        sh.objs.get_mes(f,mes,True).show_warning()
        mes = 'This is a CLI ERROR message'
        sh.objs.get_mes(f,mes,True).show_error()
    
    def set_font(self):
        f = '[shared] tests.Commands.set_font'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        ifont = sh.Font('Serif 11')
        ifont.set_text('Hello, I am here and here!')
        ifont.gui.set_font('Sans',11)
        width = ifont.width()
        height = ifont.height()
        mes = _('Font size: {}x{}').format(width,height)
        sh.objs.get_mes(f,mes,SILENT).show_debug()
    
    def get_free_space(self):
        f = '[shared] tests.Commands.get_free_space'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        messages = []
        # Test #1
        mes = _('Test #{}').format(1)
        messages.append(mes)
        path = None
        size = sh.Path(path).get_free_space()
        size = sh.com.get_human_size(size)
        mes = _('Path: "{}"; free space: {}').format(path,size)
        messages.append(mes)
        messages.append('')
        # Test #2
        mes = _('Test #{}').format(2)
        messages.append(mes)
        path = '/'
        size = sh.Path(path).get_free_space()
        size = sh.com.get_human_size(size,LargeOnly=1)
        mes = _('Path: "{}"; free space: {}').format(path,size)
        messages.append(mes)
        messages.append('')
        # Test #3
        mes = _('Test #{}').format(3)
        messages.append(mes)
        path = '/home/pete'
        size = sh.Path(path).get_free_space()
        size = sh.com.get_human_size(size,LargeOnly=1)
        mes = _('Path: "{}"; free space: {}').format(path,size)
        messages.append(mes)
        messages.append('')
        # Test #4
        mes = _('Test #{}').format(4)
        messages.append(mes)
        path = '/tmp'
        size = sh.Path(path).get_free_space()
        size = sh.com.get_human_size(size,LargeOnly=1)
        mes = _('Path: "{}"; free space: {}').format(path,size)
        messages.append(mes)
        messages.append('')
        mes = '\n'.join(messages)
        sh.objs.get_mes(f,mes,SILENT).show_debug()
    
    def get_size(self):
        f = '[shared] tests.Commands.get_size'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        messages = []
        # Test #1
        mes = _('Test #{}').format(1)
        messages.append(mes)
        my_dir = '/home/pete/base/docs/Изображения'
        size = sh.Directory(my_dir).get_size(Follow=1)
        size = sh.com.get_human_size(size,LargeOnly=0)
        mes = _('Object: "{}"; size: {}').format(my_dir,size)
        messages.append(mes)
        messages.append('')
        # Test #2
        mes = _('Test #{}').format(2)
        messages.append(mes)
        my_dir = '/home/pete/base/docs'
        size = sh.Directory(my_dir).get_size(Follow=1)
        size = sh.com.get_human_size(size,LargeOnly=0)
        mes = _('Object: "{}"; size: {}').format(my_dir,size)
        messages.append(mes)
        messages.append('')
        # Test #3
        mes = _('Test #{}').format(3)
        messages.append(mes)
        file = '/boot/initrd.img-4.19.0-6-686'
        size = sh.File(file).get_size()
        size = sh.com.get_human_size(size,LargeOnly=0)
        mes = _('Object: "{}"; size: {}').format(file,size)
        messages.append(mes)
        messages.append('')
        # Test #4
        mes = _('Test #{}').format(4)
        messages.append(mes)
        file = '/home/pete/main/dist/manjaro-xfce-15.12-i686.iso'
        size = sh.File(file).get_size()
        size = sh.com.get_human_size(size,LargeOnly=1)
        mes = _('Object: "{}"; size: {}').format(file,size)
        messages.append(mes)
        messages.append('')
        # Test #5
        mes = _('Test #{}').format(5)
        messages.append(mes)
        file = '/home/pete/bin/examples/python/gettext_windows.py'
        size = sh.File(file).get_size(Follow=0)
        size = sh.com.get_human_size(size,LargeOnly=1)
        mes = _('Object: "{}"; size: {}').format(file,size)
        messages.append(mes)
        mes = '\n'.join(messages)
        sh.objs.get_mes(f,mes,SILENT).show_debug()

    def run_progressbar0(self):
        f = '[shared] tests.Commands.run_progressbar0'
        mes = _('Run "{}". Press any key to continue').format(f)
        input(mes)
        pb = sh.ProgressBar()
        for i in range(100):
            item = pb.add()
            file = 'File #%d' % i
            total = random.randint(1,100)
            cur_size = random.randint(0,total)
            rate = random.randint(1,5000)
            eta = int((total*1000)/rate)
            item.text (file = file
                      ,cur_size = cur_size
                      ,total = total
                      ,rate = rate
                      ,eta = eta
                      )
        pb.show()



class Anchors:
    
    def __init__(self):
        self.count = 0
        self.anchors = ('N' ,'NE','NW','E' 
                       ,'EN','ES','S' ,'SE'
                       ,'SW','W','WN','WS'
                       )
        self.anchor = self.anchors[0]
    
    def adjust(self,event=None):
        if self.count % 2:
            self.set_next_anchor()
            self.attach()
            mes = _('Press Return to place widgets randomly')
            self.lbl_top.set_text(mes)
        else:
            self.place_widgets()
            mes = _('Anchor: {}\nPress Return to adjust Widget 2')
            mes = mes.format(self.anchor)
            self.lbl_top.set_text(mes)
        self.count += 1
    
    def set_next_anchor(self):
        ind = self.anchors.index(self.anchor)
        if ind + 1 == len(self.anchors):
            self.anchor = self.anchors[0]
        else:
            self.anchor = self.anchors[ind+1]
    
    def run(self,event=None):
        f = '[shared] tests.Anchors.run'

        self.top = sh.Top()
        self.top1 = sh.Top (AutoCr = False
                           ,Lock = False
                           )
        self.top2 = sh.Top (AutoCr = False
                           ,Lock = False
                           )
        self.top.set_title('HOST')
        sh.Geometry(self.top).set('550x150')
        
        # Strict order: 'wm_overrideredirect' -> 'show' -> 'center'
        self.top1.widget.wm_overrideredirect(1)
        self.top2.widget.wm_overrideredirect(1)
        
        mes = _('Press Return to place widgets randomly')
        self.lbl_top = sh.Label (parent = self.top
                                ,text = mes
                                ,expand = True
                                ,fill = 'both'
                                )
        sh.Label (parent = self.top1
                 ,text = 'WIDGET1'
                 ,bg = 'green'
                 ,fg = 'orange'
                 ,expand = True
                 ,fill = 'both'
                 )
        sh.Label (parent = self.top2
                 ,text = 'WIDGET2'
                 ,bg = 'red'
                 ,fg = 'orange'
                 ,expand = True
                 ,fill = 'both'
                 )
        
        self.place_widgets()
        
        mes = _('Anchor: {}').format(self.anchor)
        sh.Message(f,mes,True).show_info()
        
        sh.com.bind (obj = self.top
                    ,bindings = '<Return>'
                    ,action = self.adjust
                    )
        sh.com.bind (obj = self.top1
                    ,bindings = '<Return>'
                    ,action = self.adjust
                    )
        sh.com.bind (obj = self.top2
                    ,bindings = '<Return>'
                    ,action = self.adjust
                    )
        
        self.top1.show()
        self.top2.show()
        self.top.show()
    
    def place_widgets(self,event=None):
        w1, w2 = com.get_size_range()
        h1, h2 = com.get_size_range()
        
        x1, y1 = com.set_random_coor(h1,w1)
        x2, y2 = com.set_random_coor(h2,w2)
        
        geom = sh.Geometry(parent=self.top1)
        geom.geom = '%dx%d+%d+%d' % (w1,h1,x1,y1)
        geom.restore()
        
        geom = sh.Geometry(parent=self.top2)
        geom.geom = '%dx%d+%d+%d' % (w2,h2,x2,y2)
        geom.restore()
    
    def attach(self,event=None):
        sh.AttachWidget (obj1 = self.top1
                        ,obj2 = self.top2
                        ,anchor = self.anchor
                        ).run()



class TestBox:

    def __init__(self):
        self.text = 'Здесь был вася, Васян, переВася, Вася и еще раз Вася.'
        self.pattern = 'Вася'
        #self.text = sh.ReadTextFile('/home/pete/tmp/large_file.txt').get()
        self.top = sh.Top (icon = ICON
                          ,title = _('Text:')
                          )
        self.itxt = sh.SearchBox(parent=self.top)
        self.itxt.insert (text = self.text
                         ,mode = 'top'
                         )
    
    def select_all_search(self):
        self.itxt.select_all_search (pattern = self.pattern
                                    ,Case = False
                                    ,WordsOnly = True
                                    )
        self.top.show()
    
    def is_last_word(self,event=None):
        f = '[shared] tests.TestBox.is_last_word'
        pos = self.itxt.get_pointer()
        pos = self.itxt.get_word_start(pos)
        self.itxt.set_word(pos)
        res = self.itxt.is_end(pos)
        mes = 'IsEnd: {}'.format(res)
        sh.objs.get_mes(f,mes,True).show_debug()
        res = self.itxt.is_last_word()
        mes = 'IsLastWord: {}'.format(res)
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def bind_last_word(self):
        sh.com.bind (obj = self.top
                    ,bindings = '<ButtonRelease-1>'
                    ,action = self.is_last_word
                    )
        self.top.show()
    
    def print_word(self,event=None):
        pos = self.itxt.get_pointer()
        self.itxt.get_word_text(pos)
    
    def bind_print_word(self):
        sh.com.bind (obj = self.top
                    ,bindings = '<ButtonRelease-1>'
                    ,action = self.print_word
                    )
        self.top.show()
    
    def select_prev_word(self,event=None):
        self.itxt.set_prev_word()
        self.itxt.select_word()
    
    def select_next_word(self,event=None):
        self.itxt.set_next_word()
        self.itxt.select_word()
    
    def navigate_words(self):
        self.itxt.set_word()
        sh.com.bind (obj = self.top
                    ,bindings = '<Left>'
                    ,action = self.select_prev_word
                    )
        sh.com.bind (obj = self.top
                    ,bindings = '<Right>'
                    ,action = self.select_next_word
                    )
        self.top.show()
    
    def bind_select_word(self):
        sh.com.bind (obj = self.top
                    ,bindings = '<ButtonRelease-1>'
                    ,action = self.select_word
                    )
        self.top.show()
    
    def select_word(self,event=None):
        f = '[SearchBox] tests.TestBox.select_word'
        pos = self.itxt.obj.get_pointer()
        borders = self.itxt.get_word_borders(pos)
        if borders:
            pos1, pos2 = borders[0], borders[1]
            self.itxt.tag_add (tag = 'word'
                              ,pos1 = pos1
                              ,pos2 = pos2
                              )
            self.itxt.tag_config (tag = 'word'
                                 ,bg = 'MediumOrchid1'
                                 )
        else:
            sh.com.rep_empty(f)
    
    def print_pointer(self,event=None):
        f = '[SearchBox] tests.TestBox.print_pointer'
        if event:
            pos = self.itxt.obj.get_pointer()
            mes = '"{}"'.format(pos)
            sh.objs.get_mes(f,mes,True).show_debug()
        else:
            sh.com.rep_empty(f)
    
    def print_cursor(self,event=None):
        f = '[SearchBox] tests.TestBox.print_cursor'
        mes = '"{}"'.format(self.itxt.obj.get_cursor())
        sh.objs.get_mes(f,mes,True).show_debug()
    
    def get_cursor(self):
        sh.com.bind (obj = self.itxt.gui.parent
                    ,bindings = '<ButtonRelease-1>'
                    ,action = self.print_cursor
                    )
        self.top.show()
    
    def get_pointer(self):
        sh.com.bind (obj = self.itxt.gui.parent
                    ,bindings = '<ButtonRelease-1>'
                    ,action = self.print_pointer
                    )
        self.top.show()
    
    def run_select_all(self):
        self.itxt.select_all (pattern = self.pattern
                             ,Case = False
                             ,tag = 'select_all'
                             ,bg = 'MediumOrchid1'
                             )
        self.top.show()
    
    def run_select_by_count(self):
        self.itxt.select_by_count (pattern = self.pattern
                                  ,start = '1.0'
                                  ,end = 'end'
                                  ,Case = True
                                  ,count = 4
                                  ,tag = 'count'
                                  ,bg = 'red'
                                  )
        self.top.show()
    
    def run_search_box(self):
        self.itxt.reset_src (Case = False
                            ,Loop = True
                            )
        self.itxt.focus()
        self.top.show()



com = Commands()


if __name__ == '__main__':
    f = '[shared] tests.__main__'
    sh.com.start()
    com.run_clipboard()
    sh.com.end()
