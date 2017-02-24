#!/usr/bin/python3
#coding=UTF-8

import tkinter as tk
import tkinter.filedialog as dialog
import mes_ru as mes
import sys, os

import constants
import shared

h_os = constants.h_os
globs = constants.globs
globs['mes'] = constants.mes_ru
lev_crit = constants.lev_crit
lev_debug = constants.lev_debug
lev_debug_err = constants.lev_debug_err
lev_err = constants.lev_err
lev_info = constants.lev_info
lev_ques = constants.lev_ques
lev_warn = constants.lev_warn

from shared import Search, Text, timer, Words, log


if h_os.sys() == 'win':
	import win32gui, win32con, ctypes

# Вернуть тип параметра
def get_obj_type(obj,Verbal=True,IgnoreErrors=False):
	obj_type_str = ''
	obj_type_str = str(type(obj))
	obj_type_str = obj_type_str.replace("<class '",'')
	obj_type_str = obj_type_str.replace("'>",'')
	# int, float, str, list, dict, tuple, NoneType
	if Verbal:
		obj_type_str = obj_type_verbal(obj_type_str,IgnoreErrors=IgnoreErrors)
	#log.append('get_obj_type',lev_debug,obj_type_str)
	return obj_type_str
	
# Название типа на русском
def obj_type_verbal(obj_type_str,IgnoreErrors=False):
	obj_type_str = str(obj_type_str)
	if obj_type_str == 'str':
		obj_type_str = globs['mes'].type_str
	elif obj_type_str == 'list':
		obj_type_str = globs['mes'].type_lst
	elif obj_type_str == 'dict':
		obj_type_str = globs['mes'].type_dic
	elif obj_type_str == 'tuple':
		obj_type_str = globs['mes'].type_tuple
	elif obj_type_str == 'set' or obj_type_str == 'frozenset':
		obj_type_str = globs['mes'].type_set
	elif obj_type_str == 'int':
		obj_type_str = globs['mes'].type_int
	elif obj_type_str == 'long':
		obj_type = globs['mes'].type_long_int
	elif obj_type_str == 'float':
		obj_type_str = globs['mes'].type_float
	elif obj_type_str == 'complex':
		obj_type_str = globs['mes'].type_complex
	elif obj_type_str == 'bool':
		obj_type_str = globs['mes'].type_bool
	elif IgnoreErrors:
		pass
	else:
		Message(func='obj_type_verbal',type=lev_err,message=globs['mes'].unknown_mode % (obj_type_str,'str, list, dict, tuple, set, frozenset, int, long, float, complex, bool'))
	#log.append('obj_type_verbal',lev_debug,obj_type_str)
	return obj_type_str
	


# Класс для оформления root как виджета
class Root:

	def __init__(self):
		self.type = 'Root'
		self.widget = tk.Tk()

	def run(self):
		self.widget.mainloop()

	def show(self):
		self.widget.deiconify()

	def close(self):
		self.widget.withdraw()

	def destroy(self):
		self.kill()
	
	def kill(self):
		self.widget.destroy()
		
	def update(self):
		self.widget.update()



# Привязать горячие клавиши или кнопки мыши к действию
def create_binding(widget,bindings,action): # widget, list, function
	bindings_type = get_obj_type(bindings,Verbal=True,IgnoreErrors=True)
	if bindings_type == globs['mes'].type_str or bindings_type == globs['mes'].type_lst:
		if bindings_type == globs['mes'].type_str:
			bindings = [bindings]
		for i in range(len(bindings)):
			try:
				widget.bind(bindings[i],action)
			except tk.TclError:
				Message(func='create_binding',type=lev_err,message=globs['mes'].wrong_keybinding % bindings[i])
	else:
		Message(func='create_binding',type=lev_err,message=globs['mes'].unknown_mode % (str(bindings_type),'%s, %s' % (globs['mes'].type_str,globs['mes'].type_lst)))

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class WidgetShared:
	
	def focus(object,*args):
		object.widget.focus()

	def insert(object,text,pos):
		if text:
			if object.type == 'TextBox' or object.type == 'Entry':
				try:
					object.widget.insert(pos,text)
				except tk.TclError:
					try:
						object.widget.insert(pos,globs['mes'].insert_failure)
					except tk.TclError:
						Message(func='WidgetShared.insert',type=lev_err,message=globs['mes'].insert_failure)
		else:
			log.append('WidgetShared.insert',lev_warn,globs['mes'].empty_input)

	def font(object,font='Sans 11'): # font_style, globs['var']['menu_font']
		if object.type == 'TextBox' or object.type == 'Entry':
			object.widget.config(font=font)

	def set_state(object,ReadOnly=False):
		if object.type == 'TextBox' or object.type == 'Entry':
			if ReadOnly:
				object.widget.config(state='disabled')
				object.state = 'disabled'
			else:
				object.widget.config(state='normal')
				object.state = 'normal'
			
	def title(object,text=globs['mes'].text,my_program_title=''): # Родительский виджет
		if object.type == 'Toplevel' or object.type == 'Root':
			object.widget.title(text + my_program_title)
		
	def custom_buttons(object):
		if not object.Composite:
			if object.parent_obj.type == 'Toplevel' or object.parent_obj.type == 'Root':
				if object.state == 'disabled':
					object.parent_obj.close_button.widget.config(text=globs['mes'].btn_x)
				else:
					object.parent_obj.close_button.widget.config(text=globs['mes'].save_and_close)
				
	def icon(object,file): # Родительский объект
		if object.type == 'Toplevel' or object.type == 'Root':
			if file and os.path.exists(file):
				object.widget.tk.call('wm','iconphoto',object.widget._w,tk.PhotoImage(master=object.widget,file=file))



class Top:

	# todo: del 'trigger_obj'
	def __init__(self,parent_obj,Maximize=False,AutoCenter=True,trigger_obj=None):
		self.type = 'Toplevel'
		# Lock = True - блокировать дальнейшее выполнение программы до попытки закрытия виджета. Lock = False позволяет создать одновременно несколько виджетов на экране. Они будут работать, однако, виджет с Lock = False будет закрыт при закрытии виджета с Lock = True. Кроме того, если ни один из виджетов не имеет Lock = True, то они все будут показаны и тут же закрыты.
		self.Lock = False
		self.parent_obj = parent_obj
		self.AutoCenter = AutoCenter
		self.trigger_obj = trigger_obj
		self.count = 0
		self.widget = tk.Toplevel(self.parent_obj.widget)
		self.widget.protocol("WM_DELETE_WINDOW",self.close)
		if Maximize:
			Geometry(parent_obj=self).maximize()
		if self.trigger_obj:
			self.trigger_obj.add(self)
		else:
			self.tk_trigger = tk.BooleanVar()
	
	def close(self,*args):
		self.widget.withdraw()
		if self.Lock:
			if self.trigger_obj:
				self.trigger_obj.on_close()
			else:
				self.tk_trigger.set(True)
	
	def show(self,Lock=True):
		self.count += 1
		self.widget.deiconify()
		# Changing geometry at a wrong time may prevent frames from autoresizing after 'pack_forget'
		if self.AutoCenter:
			self.center()
		self.Lock = Lock
		if self.Lock:
			if self.trigger_obj:
				self.trigger_obj.on_show()
			else:
				self.tk_trigger = tk.BooleanVar()
				self.widget.wait_variable(self.tk_trigger)
	
	def title(self,text='Title:'):
		WidgetShared.title(self,text=text)
		
	def icon(self,path):
		WidgetShared.icon(self,path)
		
	# todo: not centers without Force=True when Lock=False
	def center(self,Force=False):
		# Make child widget always centered at the first time and up to a user's choice any other time (if the widget is reused).
		if self.count == 1 or Force:
			self.widget.update_idletasks()
			width = self.widget.winfo_screenwidth()
			height = self.widget.winfo_screenheight()
			size = tuple(int(_) for _ in self.widget.geometry().split('+')[0].split('x'))
			x = width/2 - size[0]/2
			y = height/2 - size[1]/2
			self.widget.geometry("%dx%d+%d+%d" % (size + (x, y)))
			
	def focus(self,*args):
		self.widget.focus_set()



class SearchBox:

	def __init__(self,obj):
		self.type = 'SearchBox'
		self.obj = obj
		self.parent_obj = self.obj.parent_obj
		h_top = Top(self.parent_obj)
		self.h_entry = Entry(h_top)
		self.h_entry.title(text='Find:') # todo: mes
		self.h_entry.close()
		self.h_sel = Selection(self.obj)

	def reset_logic(self,words=None,Strict=False): # Strict: case-sensitive, with punctuation
		self.Success = True
		self._prev_loop = self._next_loop = self._search = self._pos1 = self._pos2 = self._text = None
		self.i = 0
		self.words = words
		self.Strict = Strict
		if self.words:
			self.words.sent_nos() # cur
			if self.Strict: # Do not get text from the widget - it's not packed yet
				self._text = self.words._text_p
			else:
				self._text = self.words._text_n
			self.h_sel.reset_logic(words=self.words)
			self.h_search = Search(text=self._text)
		else:
			self.Success = False
			Message(func='SearchBox.reset_logic',type=lev_warn,message=globs['mes'].not_enough_input_data,Silent=True)
	
	def reset_data(self):
		self.Success = True
		self._prev_loop = self._next_loop = self._search = self._pos1 = self._pos2 = None
		self.i = 0
		self.search()
		if self._text and self._search:
			self.h_search.reset(text=self._text,search=self._search)
			self.h_search.next_loop()
			if not self.h_search._next_loop: # Prevents from calling self.search() once again
				Message(func='SearchBox.reset_data',type=lev_info,message='No matches!') # todo: mes
				self.Success = False
		else:
			self.Success = False
			log.append('SearchBox.reset_data',lev_warn,globs['mes'].canceled)
			
	def reset(self,mode='data',words=None,Strict=False):
		if mode == 'data':
			self.reset_data()
		else:
			self.reset_logic(words=words,Strict=Strict)
		
	def loop(self):
		if self.Success:
			if not self.h_search._next_loop:
				self.reset()
		else:
			log.append('SearchBox.loop',lev_warn,globs['mes'].canceled)
		return self.h_search._next_loop
		
	def add(self):
		if self.Success:
			if self.i < len(self.loop()) - 1:
				self.i += 1
		else:
			log.append('SearchBox.add',lev_warn,globs['mes'].canceled)
			
	def subtract(self):
		if self.Success:
			if self.i > 0:
				self.i -= 1
		else:
			log.append('SearchBox.subtract',lev_warn,globs['mes'].canceled)

	def new(self,*args):
		self.reset_data()
		self.next()

	def select(self):
		if self.Success:
			result = self.words.no_by_pos(pos=self.pos1())
			if result is None:
				_pos1tk = _pos2tk = '1.0'
				log.append('SearchBox.select',lev_err,globs['mes'].wrong_input2)
			else:
				_pos1tk = self.words.words[result].tf()
				_pos2tk = self.words.words[result].tl()
			self.h_sel.reset(pos1tk=_pos1tk,pos2tk=_pos2tk,background='green')
			self.h_sel.set()
		else:
			log.append('SearchBox.select',lev_warn,globs['mes'].canceled)

	def search(self):
		if self.Success:
			if self.words and not self._search:
				self.h_entry.focus()
				self.h_entry.select_all()
				self.h_entry.show()
				self._search = self.h_entry.get()
				if self._search and not self.Strict:
					self._search = Text(text=self._search,Auto=False).delete_punctuation()
					self._search = Text(text=self._search,Auto=False).delete_duplicate_spaces()
					self._search = self._search.lower()
			return self._search
		else:
			log.append('SearchBox.search',lev_warn,globs['mes'].canceled)
	
	def next(self,*args):
		if self.Success:
			_loop = self.loop()
			if _loop:
				old_i = self.i
				self.add()
				if old_i == self.i:
					if len(_loop) == 1:
						Message(func='SearchBox.next',type=lev_info,message='Only one match found!') # todo: mes
					else:
						Message(func='SearchBox.next',type=lev_info,message='No more matches, continuing from the top!') # todo: mes
						self.i = 0
				self.select()
			else:
				Message(func='SearchBox.next',type=lev_info,message='No matches!') # todo: mes
		else:
			log.append('SearchBox.next',lev_warn,globs['mes'].canceled)

	def prev(self,*args):
		if self.Success:
			_loop = self.loop()
			if _loop:
				old_i = self.i
				self.subtract()
				if old_i == self.i:
					if len(_loop) == 1:
						Message(func='SearchBox.prev',type=lev_info,message='Only one match found!') # todo: mes
					else:
						Message(func='SearchBox.prev',type=lev_info,message='No more matches, continuing from the bottom!') # todo: mes
						self.i = len(_loop) - 1 # Not just -1
				self.select()
			else:
				Message(func='SearchBox.prev',type=lev_info,message='No matches!') # todo: mes
		else:
			log.append('SearchBox.prev',lev_warn,globs['mes'].canceled)

	def pos1(self):
		if self.Success:
			if self._pos1 is None:
				self.loop()
				self.i = 0
			_loop = self.loop()
			if _loop:
				self._pos1 = _loop[self.i]
			return self._pos1
		else:
			log.append('SearchBox.pos1',lev_warn,globs['mes'].canceled)
		
	def pos2(self):
		if self.Success:
			if self.pos1() is not None:
				self._pos2 = self._pos1 + len(self.search())
			return self._pos2
		else:
			log.append('SearchBox.pos2',lev_warn,globs['mes'].canceled)



class TextBox:
	
	def __init__(self,parent_obj,Composite=False,expand=1,side=None,fill='both',words=None,font='Serif 14',HorizontalScrollbar=False,Spelling=False):
		self.type = 'TextBox'
		self.Composite = Composite
		self.HorizontalScrollbar = HorizontalScrollbar
		self.font = font
		self.state = 'normal' # 'disabled' - отключить редактирование
		self.SpecialReturn = True
		self.Save = False
		self.tags = []
		self.marks = []
		self.parent_obj = parent_obj
		self.expand = expand
		self.side = side
		self.fill = fill
		self.gui()
		self.reset_logic(words=words,Spelling=Spelling)
		
	def _gui_txt(self):
		if self.parent_obj.type == 'Toplevel' or self.parent_obj.type == 'Root':
			self.widget = tk.Text(self.parent_obj.widget,font=self.font,wrap='word',height=1)
		else:
			self.widget = tk.Text(self.parent_obj.widget,font=self.font,wrap='word')
		self.widget.pack(expand=self.expand,fill=self.fill,side=self.side)
	
	def _gui_scroll_hor(self):
		frame = Frame(parent_obj=self.parent_obj,expand=0,fill='x',side='top')
		self.scrollbar_hor = tk.Scrollbar(frame.widget,orient=tk.HORIZONTAL,jump=0,takefocus=False)
		self.widget.config(xscrollcommand=self.scrollbar_hor.set)
		self.scrollbar_hor.config(command=self.widget.xview)
		self.scrollbar_hor.pack(expand=1,fill='x')
	
	def _gui_scroll_ver(self):
		self.scrollbar = tk.Scrollbar(self.widget,jump=0,takefocus=False)
		self.widget.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.widget.yview)
		self.scrollbar.pack(side='right',fill='y')
	
	def gui(self):
		self._gui_txt()
		self._gui_scroll_ver()
		if self.HorizontalScrollbar:
			self._gui_scroll_hor()
		if not self.Composite and not hasattr(self.parent_obj,'close_button'):
			if self.parent_obj.type == 'Toplevel' or self.parent_obj.type == 'Root':
				self.parent_obj.close_button = Button(self.parent_obj,text=globs['mes'].btn_x,hint=globs['mes'].btn_x,action=self.close,expand=0,side='bottom')
		self.search_box = SearchBox(self)
		WidgetShared.custom_buttons(self)
		self.custom_bindings()
		
	def reset(self,mode='data',words=None,Spelling=False):
		if mode == 'data':
			self.reset_data()
		else:
			self.reset_logic(words=words,Spelling=Spelling)
	
	def reset_logic(self,words=None,Spelling=False):
		self.words = words
		self.Spelling = Spelling
		self.search_box.reset_logic(words=self.words)
		self.spelling()
	
	# Delete text, tags, marks
	def reset_data(self,*args):
		self.clear_text()
		self.clear_tags()
		self.clear_marks()

	# Setting ReadOnly state works only after filling text. Only widgets tk.Text, tk.Entry and not tk.Toplevel are supported.
	def read_only(self,ReadOnly=True):
		WidgetShared.set_state(self,ReadOnly=ReadOnly)
		
	def show(self):
		self.parent_obj.show()
	
	def close(self,*args):
		self.Save = True
		self.parent_obj.close()
		return 'break'
	
	def custom_bindings(self):
		create_binding(widget=self.widget,bindings=['<Control-f>','<Control-F3>'],action=self.search_box.new)
		create_binding(widget=self.widget,bindings='<F3>',action=self.search_box.next)
		create_binding(widget=self.widget,bindings='<Shift-F3>',action=self.search_box.prev)
		# Только для несоставных виджетов
		if not self.Composite:
			self.widget.unbind('<Return>')
			if self.state == 'disabled' or self.SpecialReturn:
				# Разрешать считывать текст после нажатия Escape (в Entry запрещено)
				create_binding(widget=self.widget,bindings=['<Return>','<KP_Enter>','<Escape>'],action=self.close)
			else:
				create_binding(widget=self.widget,bindings=['<Escape>'],action=self.close)
		create_binding(widget=self.widget,bindings='<Control-a>',action=self.select_all)
	
	def _get(self):
		try:
			return self.widget.get('1.0','end')
		except tk._tkinter.TclError:
			# Do not use GUI
			log.append('TextBox._get',lev_warn,'The parent has already been destroyed.') # todo: mes
	
	def get(self,Strip=True):
		result = self._get()
		if result:
			if Strip:
				return result.strip()
			else:
				return result.strip('\n')

	def insert(self,text='text',pos='1.0',MoveTop=True):
		WidgetShared.insert(self,text=text,pos=pos)
		if MoveTop:
			self.mark_add() # Move to the beginning

	def select_all(self,*args):
		self.tag_add()
		self.mark_add()
		return 'break'

	def _tag_remove(self,tag_name='sel',pos1tk='1.0',pos2tk='end'):
		try:
			self.widget.tag_remove(tag_name,pos1tk,pos2tk)
		except tk.TclError:
			log.append('TextBox.tag_remove',lev_warn,globs['mes'].tag_remove_failed % (tag_name,str(widget),pos1tk,pos2tk))
	
	def tag_remove(self,tag_name='sel',pos1tk='1.0',pos2tk='end'):
		self._tag_remove(tag_name=tag_name,pos1tk=pos1tk,pos2tk=pos2tk)
		if self.tags:
			try:
				self.tags.remove(tag_name)
			except ValueError:
				# todo: Что тут не работает?
				log.append('TextBox.tag_remove',lev_debug_err,globs['mes'].element_not_found % (tag_name,str(self.tags)))

	# Tk.Entry не поддерживает тэги и метки
	def tag_add(self,tag_name='sel',pos1tk='1.0',pos2tk='end',DeletePrevious=True):
		if DeletePrevious:
			self.tag_remove(tag_name)
		try:
			self.widget.tag_add(tag_name,pos1tk,pos2tk)
		except tk.TclError:
			log.append('TextBox.tag_add',lev_err,globs['mes'].tag_addition_failure % (tag_name,pos1tk,pos2tk))
		self.tags.append(tag_name)
		
	def tag_config(self,tag_name='sel',background=None,foreground=None):
		if background:
			try:
				self.widget.tag_config(tag_name,background=background)
			except tk.TclError:
				log.append('TextBox.tag_config',lev_err,globs['mes'].tag_bg_failure2 % (str(tag_name),str(background)))
		if foreground:
			try:
				self.widget.tag_config(tag_name,foreground=foreground)
			except tk.TclError:
				log.append('TextBox.tag_config',lev_err,globs['mes'].tag_fg_failure2 % (str(tag_name),str(foreground)))
	
	# Tk.Entry не поддерживает тэги и метки
	def mark_add(self,mark_name='insert',postk='1.0'):
		try:
			self.widget.mark_set(mark_name,postk)
			# todo: mes: adding mark
			log.append('TextBox.mark_add',lev_debug,globs['mes'].mark_added % (mark_name,postk))
		except tk.TclError:
			log.append('TextBox.tag_add',lev_err,globs['mes'].mark_addition_failure % (mark_name,postk))
		self.marks.append(mark_name)
	
	def mark_remove(self,mark_name='insert'):
		try:
			self.widget.mark_unset(mark_name)
			# todo: mes: removing mark
			log.append('TextBox.mark_remove',lev_debug,globs['mes'].mark_removed % (mark_name))
		except tk.TclError:
			log.append('TextBox.mark_remove',lev_err,globs['mes'].mark_removal_failure % mark_name)
		try:
			self.marks.remove(mark_name)
		except ValueError:
			log.append('TextBox.mark_remove',lev_err,globs['mes'].element_not_found % (mark_name,str(self.marks)))
			
	def clear_text(self):
		try:
			self.widget.delete('1.0','end')
		except tk._tkinter.TclError:
			# Do not use GUI
			log.append('TextBox.clear_text',lev_warn,'The parent has already been destroyed.') # todo: mes
		
	def clear_tags(self):
		i = len(self.tags) - 1
		while i >= 0:
			self.tag_remove(self.tags[i])
			i -= 1
	
	def clear_marks(self):
		i = len(self.marks) - 1
		while i >= 0:
			self.mark_remove(self.marks[i])
			i -= 1
	
	def goto(self,GoTo=''):
		if GoTo:
			try:
				goto_pos = self.widget.search(GoTo,'1.0','end')
				self.mark_add('goto',goto_pos)
				self.mark_add('insert',goto_pos)
				self.widget.yview('goto')
			except:
				log.append('TextBox.goto',lev_err,globs['mes'].shift_screen_failure % 'goto')
				
	# Сместить экран до позиции tkinter или до метки (тэги не работают)
	def scroll(self,mark):
		try:
			self.widget.yview(mark)
		except tk.TclError:
			log.append('TextBox.scroll',lev_warn,globs['mes'].shift_screen_failure % str(mark))
			
	# Сместить экран до позиции tkinter или до метки, если они не видны (тэги не работают)
	def autoscroll(self,mark):
		if not self.visible(mark):
			self.scroll(mark)
			
	# todo: select either 'see' or 'autoscroll'
	def see(self,mark):
		self.widget.see(mark)
	
	def title(self,text='Title:'):
		WidgetShared.title(self.parent_obj,text)
		
	def icon(self,path):
		WidgetShared.icon(self.parent_obj,path)
	
	# Только для несоставных виджетов (ввиду custom_bindings)
	def update(self,title='Title:',text='',GoTo='',SelectAll=False,ReadOnly=False,CursorPos='1.0',icon='',SpecialReturn=True):
		self.Save = False
		self.SpecialReturn = SpecialReturn
		# Операции над главным виджетом
		self.icon(path=icon)
		self.title(text=title)
		# Иначе обновление текста не сработает. Необходимо делать до любых операций по обновлению текста.
		self.read_only(ReadOnly=False)
		self.reset()
		# Присвоение аргументов
		self.insert(text=text)
		# Перейти в указанное место
		self.mark_add(mark_name='insert',postk=CursorPos)
		self.widget.yview(CursorPos)
		self.read_only(ReadOnly=ReadOnly)
		WidgetShared.custom_buttons(self)
		if SelectAll:
			self.select_all()
		self.goto(GoTo=GoTo)
		# Только для несоставных виджетов
		self.custom_bindings()
		
	def visible(self,tk_pos):
		if self.widget.bbox(tk_pos):
			return True
			
	def cursor(self,*args):
		try:
			self._pos = self.widget.index('insert')
			log.append('TextBox.cursor',lev_debug,'Got position: "%s"' % str(self._pos)) # todo: mes
		except tk.TclError:
			self._pos = '1.0'
			log.append('TextBox.cursor',lev_warn,'Cannot return a cursor position!') # todo: mes
		return self._pos
		
	def focus_set(self,*args):
		self.focus()
	
	def focus(self,*args):
		self.widget.focus_set()
		
	def spelling(self):
		if self.Spelling:
			if self.words:
				self.words.sent_nos() # cur
				result = []
				for i in range(self.words.len()):
					if not self.words.words[i].spell_ru():
						result.append(i)
				if result:
					self.clear_tags()
					for i in range(len(result)):
						no = self.words._no = result[i]
						pos1tk = self.words.words[no].tf()
						pos2tk = self.words.words[no].tl()
						self.tag_add(tag_name='spell',pos1tk=pos1tk,pos2tk=pos2tk,DeletePrevious=False)
					self.tag_config(tag_name='spell',background='red')
				else:
					log.append('TextBox.spelling',lev_info,'Spelling seems to be correct.') # todo: mes
			else:
				Message(func='TextBox.spelling',type=lev_warn,message=globs['mes'].not_enough_input_data,Silent=True)
		
	def zzz(self):
		pass
		
		
		
class Entry:
	
	def __init__(self,parent_obj,Composite=False,side=None,ipadx=None,ipady=None,fill=None,width=None,expand=None):
		self.type = 'Entry'
		self.Composite = Composite
		self.state = 'normal' # 'disabled' - отключить редактирование
		self.Save = False
		self.parent_obj = parent_obj
		self.widget = tk.Entry(self.parent_obj.widget,font='Sans 11',width=width) #globs['var']['menu_font']
		create_binding(widget=self.widget,bindings='<Control-a>',action=self.select_all)
		self.widget.pack(side=side,ipadx=ipadx,ipady=ipady,fill=fill,expand=expand)
		if not self.Composite:
			# Тип родительского виджета может быть любым
			if not hasattr(self.parent_obj,'close_button'):
				self.parent_obj.close_button = Button(self.parent_obj,text=globs['mes'].btn_x,hint=globs['mes'].btn_x,action=self.close,expand=0,side='bottom')
			WidgetShared.custom_buttons(self)
		self.custom_bindings()
	
	# Setting ReadOnly state works only after filling text. Only widgets tk.Text, tk.Entry and not tk.Toplevel are supported.
	def read_only(self,ReadOnly=True):
		WidgetShared.set_state(self,ReadOnly=ReadOnly)
	
	def custom_bindings(self):
		if self.Composite:
			self.clear_text()
		else:
			create_binding(widget=self.widget,bindings=['<Return>','<KP_Enter>'],action=self.close)
			create_binding(widget=self.widget,bindings='<Escape>',action=self.parent_obj.close)

	def show(self,*args):
		self.parent_obj.show()
	
	def close(self,*args):
		self.Save = True
		self.parent_obj.close()
	
	def _get(self):
		try:
			return self.widget.get()
		except tk._tkinter.TclError:
			# Do not use GUI
			log.append('Entry.clear_text',lev_warn,'The parent has already been destroyed.') # todo: mes
			
	def get(self,Strip=False):
		result = self._get()
		if result:
			if Strip:
				return result.strip()
			else:
				return result.strip('\n')

	def insert(self,text='text',pos=0):
		WidgetShared.insert(self,text=text,pos=pos)

	def select_all(self,*args):
		self.widget.select_clear()
		self.widget.select_range(0,'end')
		return 'break'

	def clear_text(self):
		try:
			self.widget.delete(0,'end')
		except tk._tkinter.TclError:
			# Do not use GUI
			log.append('Entry.clear_text',lev_warn,'The parent has already been destroyed.') # todo: mes
		
	# GoTo работает только в tk.Text и оставлено для совместимости с ним (как и SpecialReturn)
	def update(self,title='Title:',text='',SelectAll=True,ReadOnly=False,CursorPos=0,icon='',GoTo='',SpecialReturn=False):
		self.Save = False
		# Операции над главным виджетом
		self.icon(path=icon)
		self.title(text=title)
		# Иначе обновление текста не сработает. Необходимо делать до любых операций по обновлению текста.
		self.read_only(ReadOnly=False)
		# Очистка текста
		self.clear_text()
		# Присвоение аргументов
		self.insert(text=text)
		# Перейти в указанное место
		self.widget.icursor(CursorPos) # int, 'end'
		self.read_only(ReadOnly=ReadOnly)
		WidgetShared.custom_buttons(self)
		if SelectAll:
			self.select_all()
		self.widget.focus_set()
		
	def icon(self,path):
		WidgetShared.icon(self.parent_obj,path)
		
	def title(self,text='Title:'):
		WidgetShared.title(self.parent_obj,text)
		
	def focus_set(self,*args):
		self.focus()
		return 'break' # Manual Tab focus (left to right widget)
	
	def focus(self,*args):
		self.widget.focus_set()
		return 'break' # Manual Tab focus (left to right widget)



class Frame:
	
	def __init__(self,parent_obj,expand=1,fill='both',side=None,padx=None,pady=None,ipadx=None,ipady=None):
		self.type = 'Frame'
		self.parent_obj = parent_obj
		self.widget = tk.Frame(self.parent_obj.widget)
		self.widget.pack(expand=expand,fill=fill,side=side,padx=padx,pady=pady,ipadx=ipadx,ipady=ipady)
			
	def title(self,text=None):
		if text:
			self.parent_obj.title(text)
		else:
			self.parent_obj.title()
			
	def show(self):
		self.parent_obj.show()
		
	def close(self):
		self.parent_obj.close()



# todo: Нужно ли на входе ,bindings=[]?
class Button:
	
	def __init__(self,parent_obj,action,hint='<Hint>',inactive_image_path=None,active_image_path=None,text='Press me',height=36,width=36,side='left',expand=0,fg='black',bd=0,hint_delay=800,hint_width=280,hint_height=40,hint_background='#ffffe0',hint_direction='top',hint_border_width=1,hint_border_color='navy',bindings=[],fill='both',TakeFocus=False):
		self.parent_obj = parent_obj
		self.action = action
		self.Status = False
		self.height = height
		self.width = width
		self.side = side
		self.expand = expand
		self.fill = fill
		self.inactive_image = self.image(inactive_image_path)
		self.active_image = self.image(active_image_path)
		if self.inactive_image:
			self.widget = tk.Button(self.parent_obj.widget,image=self.inactive_image,height=self.height,width=self.width,bd=bd,fg=fg)
		else:
			# В большинстве случаев текстовая кнопка не требует задания высоты и ширины по умолчанию, они определяются автоматически. Также в большинстве случаев для текстовых кнопок следует использовать рамку.
			self.widget = tk.Button(self.parent_obj.widget,bd=1,fg=fg)
		self.title(button_text=text)
		if bindings:
			hint_extended = hint + '\n' + str(bindings).replace('[','').replace(']','').replace('<','').replace('>','').replace("'",'')
		else:
			hint_extended = hint
		ToolTip(self.widget,text=hint_extended,hint_delay=hint_delay,hint_width=hint_width,hint_height=hint_height,hint_background=hint_background,hint_direction=hint_direction,button_side=side)
		self.show()
		create_binding(widget=self.widget,bindings=['<ButtonRelease-1>','<space>','<Return>','<KP_Enter>'],action=self.click)
		if TakeFocus:
			self.widget.focus_set()
	
	def title(self,button_text='Press me'):
		if button_text:
			self.widget.config(text=button_text)
	
	def image(self,button_image_path=None):
		# Без 'file=' не сработает!
		if button_image_path and os.path.exists(button_image_path):
			button_image = tk.PhotoImage(file=button_image_path,master=self.parent_obj.widget,width=self.width,height=self.height)
		else:
			button_image = None
		return button_image
	
	def click(self,*args):
		if len(args) > 0:
			self.action(args)
		else:
			self.action()
	
	def active(self):
		if not self.Status:
			self.Status = True
			if self.active_image:
				self.widget.config(image=self.active_image)
				self.widget.flag_img = self.active_image
			#self.widget.config(text="I'm Active")
	
	def inactive(self):
		if self.Status:
			self.Status = False
			if self.inactive_image:
				self.widget.config(image=self.inactive_image)
				self.widget.flag_img = self.inactive_image
			#self.widget.config(text="I'm Inactive")
			
	def show(self):
		self.widget.pack(expand=self.expand,side=self.side,fill=self.fill)
	
	def close(self):
		self.widget.pack_forget()



def button_test(button):
	if button.Status:
		button.title('I am active')
	else:
		button.title('I am passive')
		


# Всплывающие подсказки для кнопок
# see also 'calltips'
# based on idlelib.ToolTip
class ToolTipBase:
	
	def __init__(self,button):
		self.button = button
		self.tipwindow = None
		self.id = None
		self.x = self.y = 0
		self._id1 = self.button.bind("<Enter>", self.enter)
		self._id2 = self.button.bind("<Leave>", self.leave)
		self._id3 = self.button.bind("<ButtonPress>", self.leave)

	def enter(self, event=None):
		self.schedule()

	def leave(self, event=None):
		self.unschedule()
		self.hidetip()

	def schedule(self):
		self.unschedule()
		self.id = self.button.after(self.hint_delay, self.showtip)

	def unschedule(self):
		id = self.id
		self.id = None
		if id:
			self.button.after_cancel(id)

	def showtip(self):
		if not 'geom_top' in globs or not 'width' in globs['geom_top'] or not 'height' in globs['geom_top']:
			log.append('ToolTipBase.showtip',lev_err,globs['mes'].not_enough_input_data)
		if self.tipwindow:
			return
		# The tip window must be completely outside the button; otherwise when the mouse enters the tip window we get a leave event and it disappears, and then we get an enter event and it reappears, and so on forever :-(
		# Координаты подсказки рассчитываются так, чтобы по горизонтали подсказка и кнопка, несмотря на разные размеры, совпадали бы центрами.
		x = self.button.winfo_rootx() + self.button.winfo_width()/2 - self.hint_width/2
		if self.hint_direction == 'bottom':
			y = self.button.winfo_rooty() + self.button.winfo_height() + 1
		elif self.hint_direction == 'top':
			y = self.button.winfo_rooty() - self.hint_height - 1
		else:
			Message(func='ToolTipBase.showtip',type=lev_err,message=globs['mes'].unknown_mode % (str(self.hint_direction),'top, bottom'))
		if 'geom_top' in globs and 'width' in globs['geom_top'] and 'height' in globs['geom_top']:
			self.tipwindow = tw = tk.Toplevel(self.button)
			tw.wm_overrideredirect(1)
			# "+%d+%d" is not enough!
			log.append('ToolTipBase.showtip',lev_info,globs['mes'].new_geometry % ('tw',self.hint_width,self.hint_height,x,y))
			tw.wm_geometry("%dx%d+%d+%d" % (self.hint_width,self.hint_height,x, y))
			self.showcontents()

	def hidetip(self):
		tw = self.tipwindow
		self.tipwindow = None
		if tw:
			tw.destroy()



class ToolTip(ToolTipBase):

	def __init__(self,button,text='Sample text',hint_delay=None,hint_width=None,hint_height=None,hint_background=None,hint_direction=None,hint_border_width=None,hint_border_color=None,button_side='left'):
		if not hint_delay:
			hint_delay = 800 #globs['int']['default_hint_delay']
		if not hint_width:
			hint_width = 280 #globs['int']['default_hint_width']
		if not hint_height:
			hint_height = 40 #globs['int']['default_hint_height']
		if not hint_background:
			hint_background = '#ffffe0' #globs['var']['default_hint_background']
		if not hint_direction:
			hint_direction = 'top' #globs['var']['default_hint_direction']
		if not hint_border_width:
			hint_border_width = 1 #globs['int']['default_hint_border_width']
		if not hint_border_color:
			hint_border_color = 'navy' #globs['var']['default_hint_border_color']
		self.text = text
		self.hint_delay = hint_delay
		self.hint_direction = hint_direction
		self.hint_background = hint_background
		self.hint_border_color = hint_border_color
		self.hint_height = hint_height
		self.hint_width = hint_width
		self.hint_border_width = hint_border_width
		self.button_side = button_side
		ToolTipBase.__init__(self,button)

	def showcontents(self):
		frame = tk.Frame(self.tipwindow,background=self.hint_border_color,borderwidth=self.hint_border_width)
		frame.pack()
		label = tk.Label(frame,text=self.text,justify='center',background=self.hint_background,width=self.hint_width,height=self.hint_height)
		label.pack() #expand=1,fill='x'
		


class ListBox:
	# todo: fix: Cannot cancel by Escape
	# todo: configure a font
	# todo: SelectFirst is enabled, however, after pressing Save button nothing happens
	def __init__(self,parent_obj,Multiple=False,lst=[],title='Title:',icon=None,SelectionCloses=True,SelectFirst=True,Composite=False,SingleClick=True,user_function=None,side=None,Scrollbar=True,expand=1,fill='both'):
		self.parent_obj = parent_obj
		self.Multiple = Multiple
		self.expand = expand
		self.Composite = Composite
		self.Scrollbar = Scrollbar
		self._fill = fill
		self.side = side
		# A user-defined function that is run when pressing Up/Down arrow keys and LMB. There is a problem binding it externally, so we bind it here.
		self.user_function = user_function
		self._index = 0
		self.state = 'normal'
		self.SelectionCloses = SelectionCloses
		self.SingleClick = SingleClick
		self._icon = icon
		self.gui()
		self.reset(lst=lst,title=title,SelectFirst=SelectFirst)
		
	def bindings(self):
		if self.user_function:
			create_binding(self.widget,'<<ListboxSelect>>',self.user_function) # Binding just to '<Button-1>' does not work. We do not need binding Return/space/etc. because the function will be called each time the selection is changed. However, we still need to bind Up/Down.
		elif self.SelectionCloses:
			# todo: test <KP_Enter> in Windows
			create_binding(self.widget,['<Return>','<KP_Enter>','<Double-Button-1>'],self.close)
			if self.SingleClick and not self.Multiple:
				create_binding(self.widget,'<Button-1>',self.close)
		if not self.Multiple:
			create_binding(self.widget,'<Up>',self.move_up)
			create_binding(self.widget,'<Down>',self.move_down)
		if not self.Composite: # todo: test
			create_binding(self.widget,['<Escape>','<Control-q>','<Control-w>'],self.close)
		
	def gui(self):
		self._scroll()
		if self.Multiple:
			self.widget = tk.Listbox(self.parent_obj.widget,exportselection=0,selectmode=tk.MULTIPLE)
		else:
			self.widget = tk.Listbox(self.parent_obj.widget,exportselection=0,selectmode=tk.SINGLE)
		self.widget.pack(expand=self.expand,fill=self._fill,side=self.side)
		self._resize()
		self._scroll_config()
		self.icon(path=self._icon)
		self.widget.focus_set()
		self.bindings()
		if not self.Composite:
			# Тип родительского виджета может быть любым
			if not hasattr(self.parent_obj,'close_button'):
				self.parent_obj.close_button = Button(self.parent_obj,text=globs['mes'].btn_x,hint=globs['mes'].btn_x,action=self.close,expand=0,side='bottom')
			WidgetShared.custom_buttons(self)

	def _scroll(self):
		if self.Scrollbar:
			self.scrollbar = tk.Scrollbar(self.parent_obj.widget)
			self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
			
	def _scroll_config(self):
		if self.Scrollbar:
			self.scrollbar.config(command=self.widget.yview)
			self.widget.config(yscrollcommand=self.scrollbar.set)
	
	def _resize(self):
		# Autofit to contents
		self.widget.config(width=0)
		self.widget.config(height=0)
	
	def activate(self):
		self.widget.activate(self._index)
	
	def clear(self):
		self.widget.delete(0,tk.END)
		
	def clear_selection(self):
		self.widget.selection_clear(0,tk.END)
	
	def reset(self,lst=[],title=None,SelectFirst=True):
		self.SelectFirst = SelectFirst
		self._title = title
		self.clear()
		self.lst = list(lst)
		self.title(text=self._title)
		self.fill()
		self._resize()
		self._index = 0
		if self.SelectFirst:
			self.select()
		else:
			self.clear_selection()
		self.IQuit = False
	
	def select(self):
		self.clear_selection()
		self.widget.selection_set(self._index)
		self.widget.see(self._index)
	
	def show(self):
		self.parent_obj.show()

	def close(self,*args):
		self.IQuit = True
		self.parent_obj.close()
	
	def fill(self):
		for i in range(len(self.lst)):
			self.widget.insert(tk.END,self.lst[i])
			
	def title(self,text=None):
		if text:
			self.parent_obj.title(text=text)
		
	def icon(self,path=None):
		if path:
			WidgetShared.icon(self.parent_obj,path)
		
	def index(self):
		selection = self.widget.curselection()
		if selection and len(selection) > 0:
			# ATTENTION: selection[0] is a number in Python 3.4, however, in older interpreters and builds based on them it is a string. In order to preserve compatibility, we convert it to a number.
			self._index = int(selection[0])
			return self._index
		else:
			return 0
			
	def index_add(self):
		if self.index() < len(self.lst) - 1:
			self._index += 1
		else:
			self._index = 0
	
	def index_subtract(self):
		if self.index() > 0:
			self._index -= 1
		else:
			self._index = len(self.lst) - 1
	
	def _get(self): # Call this externally to get results *before* closing the widget
		result = [self.widget.get(idx) for idx in self.widget.curselection()]
		if self.Multiple:
			return result
		else:
			if len(result) > 0:
				return result[0]
	
	def get(self):
		if self.SelectionCloses:
			# Return a result if the user has selected anything or None otherwise
			if self.IQuit:
				return self._get()
		else:
			return self._get()
			
	def move_down(self,*args):
		self.index_add()
		self.select()
		if self.user_function:
			self.user_function()
		
	def move_up(self,*args):
		self.index_subtract()
		self.select()
		if self.user_function:
			self.user_function()



def dialog_save_file(filetypes=()):
	file = ''
	if not filetypes:
		filetypes = ((globs['mes'].plain_text,'.txt'),(globs['mes'].webpage,'.htm'),(globs['mes'].webpage,'.html'),(globs['mes'].all_files,'*'))
	options = {}
	options['initialfile'] = ''
	options['filetypes'] = filetypes
	options['title'] = globs['mes'].save_as
	try:
		file = dialog.asksaveasfilename(**options)
	except:
		Message(func='dialog_save_file',type=lev_err,message=globs['mes'].file_sel_failed)
	return file



class OptionMenu:
	
	def __init__(self,parent_obj,items=(1,2,3,4,5),side='left',anchor='center',command=None):
		self.parent_obj = parent_obj
		self.items = items
		self.command = command
		self.choice = None
		self.index = 0
		self.var = tk.StringVar(self.parent_obj.widget)
		self.widget = tk.OptionMenu(self.parent_obj.widget,self.var,*self.items,command=self.trigger)
		self.widget.pack(side=side,anchor=anchor)
		self.default_set()
		
	def trigger(self,*args):
		self._get()
		if self.command:
			self.command()
	
	def default_set(self):
		if len(self.items) > 0:
			self.var.set(self.items[0])
	
	def fill(self):
		self.widget['menu'].delete(0,'end')
		for item in self.items:
			self.widget['menu'].add_command(label=item,command=lambda v=self.var,l=item:v.set(l))
	
	def reset(self,items=(1,2,3,4,5)):
		self.items = items
		self.fill()
		self.default_set()
		
	def _get(self,*args): # Auto updated (after selecting an item)
		self.choice = self.var.get()
		self.index = self.items.index(self.choice)
		
	def set_prev(self,*args):
		if self.index == 0:
			self.index = len(self.items) - 1
		else:
			self.index -= 1
		self.var.set(self.items[self.index])
		
	def set_next(self,*args):
		if self.index == len(self.items) - 1:
			self.index = 0
		else:
			self.index += 1
		self.var.set(self.items[self.index])



'''	Usage:
	create_binding(h_txt.widget,'<ButtonRelease-1>',action)

def action(*args):
	h_selection.get() # Refresh coordinates (or set h_selection._pos1tk, h_selection._pos2tk manually)
	h_selection.set()
'''
class Selection: # Selecting words only
	
	def __init__(self,h_widget,words=None):
		self.h_widget = h_widget
		self.reset_logic(words=words)
		self.reset_data()
		
	def reset(self,mode='data',words=None,pos1tk=None,pos2tk=None,background=None,foreground=None,tag='tag'):
		if mode == 'data':
			self.reset_data(pos1tk=pos1tk,pos2tk=pos2tk,background=background,foreground=foreground,tag=tag)
		else:
			self.reset_logic(words=words)
	
	def reset_logic(self,words):
		self.words = words
		
	def reset_data(self,pos1tk=None,pos2tk=None,background=None,foreground=None,tag='tag'):
		self._pos1tk = pos1tk
		self._pos2tk = pos2tk
		self._text = ''
		self._bg = background
		self._fg = foreground
		if not self._bg and not self._fg:
			self._bg = 'cyan'
		self._tag = tag
		
	def clear(self,tag_name='sel',pos1tk='1.0',pos2tk='end'):
		self.h_widget._tag_remove(tag_name=tag_name,pos1tk=pos1tk,pos2tk=pos2tk)
	
	def pos1tk(self):
		if self._pos1tk is None:
			self.get()
		return self._pos1tk
		
	def pos2tk(self):
		if self._pos2tk is None:
			self.get()
		return self._pos2tk
	
	def get(self,*args):
		try:
			self._pos1tk = self.h_widget.widget.index('sel.first')
			self._pos2tk = self.h_widget.widget.index('sel.last')
		except tk.TclError:
			self._pos1tk, self._pos2tk = None, None
			log.append('Selection.tk_poses',lev_warn,globs['mes'].no_selection2 % 1) # todo: mes
		log.append('Selection.tk_poses',lev_debug,str((self._pos1tk,self._pos2tk)))
		return(self._pos1tk,self._pos2tk)
		
	def text(self):
		try:
			self._text = self.h_widget.widget.get('sel.first','sel.last').replace('\r','').replace('\n','')
		except tk.TclError:
			self._text = ''
			log.append('Selection.text',lev_err,globs['mes'].tk_sel_failure2)
		return self._text
		
	def cursor(self):
		return self.h_widget.cursor()
		
	def select_all(self):
		self.h_widget.select_all()
	
	def set(self,DeletePrevious=True,AutoScroll=True):
		if self.pos1tk() and self.pos2tk():
			mark = self._pos1tk
			self.h_widget.tag_add(pos1tk=self._pos1tk,pos2tk=self._pos2tk,tag_name=self._tag,DeletePrevious=DeletePrevious)
		else:
			# Just need to return something w/o warnings
			_cursor = mark = self.cursor()
			self.h_widget.tag_add(tag_name=self._tag,pos1tk=_cursor,pos2tk=_cursor,DeletePrevious=DeletePrevious)
		if self._bg:
			# This is not necessary for 'sel' tag which is hardcoded for selection and permanently colored with gray. A 'background' attribute cannot be changed for a 'sel' tag.
			self.h_widget.widget.tag_config(tagName=self._tag,background=self._bg)
		elif self._fg:
			self.h_widget.widget.tag_config(tagName=self._tag,foreground=self._fg)
		if AutoScroll: # todo: select either 'see' or 'autoscroll'
			#self.h_widget.see(mark)
			self.h_widget.autoscroll(mark)



class ParallelTexts: # Requires Search
	
	def __init__(self,parent_obj,Extended=True):
		self.parent_obj = parent_obj
		self.obj = Top(self.parent_obj,Maximize=True)
		self.widget = self.obj.widget
		self.title()
		self.frame1 = Frame(parent_obj=self.obj,side='top')
		self.Extended = Extended
		if self.Extended:
			self.frame2 = Frame(parent_obj=self.obj,side='bottom')
		self.txt1 = TextBox(self.frame1,Composite=True,side='left')
		self.txt2 = TextBox(self.frame1,Composite=True,side='right')
		if self.Extended:
			self.txt3 = TextBox(self.frame2,Composite=True,side='left')
			self.txt4 = TextBox(self.frame2,Composite=True,side='right')
		self.h_tk_pos1 = TkPos(h_widget=self.txt1)
		self.h_tk_pos2 = TkPos(h_widget=self.txt2)
		if self.Extended:
			self.h_tk_pos3 = TkPos(h_widget=self.txt3)
			self.h_tk_pos4 = TkPos(h_widget=self.txt4)
		self.custom_bindings()
		self.icon()
		self.close()
		
	def reset(self,words1,words2,words3=None,words4=None):
		log.append('ParallelTexts.reset',lev_info,'Reset widget') # todo: del when optimized
		widgets.waitbox().reset(func_title='ParallelTexts.reset',message='Reset widget')
		widgets._waitbox.show()
		self.words1 = words1
		self.words2 = words2
		self.words3 = words3
		self.words4 = words4
		if self.words3 and self.words4:
			self.Extended = True
		else:
			self.Extended = False
		self.txt1.reset_logic(words=self.words1)
		self.txt1.reset_data()
		self.txt2.reset_logic(words=self.words2)
		self.txt2.reset_data()
		if self.Extended:
			self.txt3.reset_logic(words=self.words3)
			self.txt3.reset_data()
			self.txt4.reset_logic(words=self.words4)
			self.txt4.reset_data()
		self.h_tk_pos1.reset_logic(words=self.words1)
		self.h_tk_pos1.reset_data()
		self.h_tk_pos2.reset_logic(words=self.words2)
		self.h_tk_pos2.reset_data()
		if self.Extended:
			self.h_tk_pos3.reset_logic(words=self.words3)
			self.h_tk_pos3.reset_data()
			self.h_tk_pos4.reset_logic(words=self.words4)
			self.h_tk_pos4.reset_data()
		self.fill()
		# Setting ReadOnly state works only after filling text
		self.txt1.read_only(ReadOnly=True)
		self.txt2.read_only(ReadOnly=True)
		if self.Extended:
			self.txt3.read_only(ReadOnly=True)
			self.txt4.read_only(ReadOnly=True)
		self.txt1.focus()
		self.init_cursor_pos()
		self.select1()
		# todo: del when optimized
		widgets._waitbox.close()
		
	# Set the cursor to the start of the text
	def init_cursor_pos(self):
		self.txt1.mark_add()
		self.txt2.mark_add()
		if self.Extended:
			self.txt3.mark_add()
			self.txt4.mark_add()
		
	def select1(self,*args):
		self.txt1.focus() # Without this the search doesn't work (the pane is inactive)
		self.decolorize()
		self.txt1.widget.config(bg='old lace')
		self.duplicates(self.h_tk_pos1,self.h_tk_pos2)
		self.select11()
		
	def select2(self,*args):
		self.txt2.focus() # Without this the search doesn't work (the pane is inactive)
		self.decolorize()
		self.txt2.widget.config(bg='old lace')
		self.duplicates(self.h_tk_pos1,self.h_tk_pos2)
		self.select22()
		
	def select3(self,*args):
		self.txt3.focus() # Without this the search doesn't work (the pane is inactive)
		self.decolorize()
		self.txt3.widget.config(bg='old lace')
		self.duplicates(self.h_tk_pos3,self.h_tk_pos4)
		self.select11()
		
	def select4(self,*args):
		self.txt4.focus() # Without this the search doesn't work (the pane is inactive)
		self.decolorize()
		self.txt4.widget.config(bg='old lace')
		self.duplicates(self.h_tk_pos3,self.h_tk_pos4)
		self.select22()
	
	def custom_bindings(self):
		create_binding(widget=self.widget,bindings='<Control-q>',action=self.close)
		create_binding(widget=self.widget,bindings='<Escape>',action=Geometry(parent_obj=self.obj).minimize)
		create_binding(widget=self.widget,bindings=['<Alt-Key-1>','<Control-Key-1>'],action=self.select1)
		create_binding(widget=self.widget,bindings=['<Alt-Key-2>','<Control-Key-2>'],action=self.select2)
		if self.Extended:
			create_binding(widget=self.widget,bindings=['<Alt-Key-3>','<Control-Key-3>'],action=self.select3)
			create_binding(widget=self.widget,bindings=['<Alt-Key-4>','<Control-Key-4>'],action=self.select4)
		create_binding(self.txt1.widget,'<ButtonRelease-1>',self.select1)
		create_binding(self.txt2.widget,'<ButtonRelease-1>',self.select2)
		if self.Extended:
			create_binding(self.txt3.widget,'<ButtonRelease-1>',self.select3)
			create_binding(self.txt4.widget,'<ButtonRelease-1>',self.select4)
			
	def decolorize(self):
		self.txt1.widget.config(bg='white')
		self.txt2.widget.config(bg='white')
		if self.Extended:
			self.txt3.widget.config(bg='white')
			self.txt4.widget.config(bg='white')
		
	def show(self):
		self.obj.show()
		
	def close(self,*args):
		self.obj.close()
		
	def title(self,text='Compare texts:'):
		self.obj.title(text)
		
	def fill(self):
		self.txt1.insert(text=self.words1._text)
		self.txt2.insert(text=self.words2._text)
		if self.Extended:
			self.txt3.insert(text=self.words3._text)
			self.txt4.insert(text=self.words4._text)
		
	def update_txt(self,h_widget,words,background='orange'):
		pos1 = words.tk_p_f()
		pos2 = words.tk_p_l()
		if pos1 and pos2:
			h_widget.tag_add(tag_name='tag',pos1tk=pos1,pos2tk=pos2,DeletePrevious=True)
			h_widget.widget.tag_config('tag',background=background)
			# Set the cursor to the first symbol of the selection
			h_widget.mark_add('insert',pos1)
			h_widget.mark_add(mark_name='yview',postk=pos1)
			h_widget.widget.see('yview')
		else:
			Message(func='ParallelTexts.update_txt',type=lev_err,message=globs['mes'].wrong_input2)
			
	def synchronize11(self):
		_search = self.words22.np() # Substring=False
		_loop22 = Search(self.words22._text,_search).next_loop()
		try:
			index22 = _loop22.index(self.words22.f_sym_p())
		except ValueError:
			#Message(func='ParallelTexts.synchronize11',type=lev_err,message=globs['mes'].wrong_input2)
			index22 = 0
		_loop11 = Search(self.words11._text,_search).next_loop()
		if index22 >= len(_loop11):
			''' # Go to the last stone
			words11.change_no(words11.len()-1)
			_no = words11.stone_no()
			'''
			_no = None # Keep old selection
		else:
			_no = self.words11.get_p_no(_loop11[index22])
		if _no is not None:
			self.words11.change_no(_no)
			self.update_txt(self.txt11,self.words11,background='orange')
			
	def synchronize22(self):
		_search = self.words11.np()
		# This helps in case the word has both Cyrillic symbols and digits
		_search = Text(text=_search,Auto=False).delete_cyrillic()
		# cur
		_search = _search.replace(' ','') # Removing the non-breaking space
		_loop11 = Search(self.words11._text,_search).next_loop()
		try:
			index11 = _loop11.index(self.words11.f_sym_p())
		except ValueError:
			#Message(func='ParallelTexts.synchronize22',type=lev_err,message=globs['mes'].wrong_input2)
			index11 = 0
		_loop22 = Search(self.words22._text,_search).next_loop()
		if index11 >= len(_loop22):
			''' # Go to the last stone
			self.words22.change_no(self.words22.len()-1)
			_no = self.words22.stone_no()
			'''
			_no = None # Keep old selection
		else:
			_no = self.words22.get_p_no(_loop22[index11])
		if _no is not None:
			self.words22.change_no(_no)
			self.update_txt(self.txt22,self.words22,background='cyan')
			
	def select11(self,*args):
		self.h_tk_pos11.reset()
		self.words11.change_no(no=self.h_tk_pos11.p_no())
		result = self.words11.stone_no()
		if result == '-2':
			Message(func='ParallelTexts.select11',type=lev_err,message=globs['mes'].wrong_input2)
		else:
			self.words11.change_no(no=result)
			self.update_txt(self.txt11,self.words11)
			self.synchronize22()

	def select22(self,*args):
		self.h_tk_pos22.reset()
		self.words22.change_no(no=self.h_tk_pos22.p_no())
		result = self.words22.stone_no()
		if result == '-2':
			Message(func='ParallelTexts.select22',type=lev_err,message=globs['mes'].wrong_input2)
		else:
			self.words22.change_no(no=result)
			self.update_txt(self.txt22,self.words22,'cyan')
			self.synchronize11()
			
	def duplicates(self,h_tk_pos11,h_tk_pos22):
		self.h_tk_pos11 = h_tk_pos11
		self.h_tk_pos22 = h_tk_pos22
		self.words11 = self.h_tk_pos11.words
		self.words22 = self.h_tk_pos22.words
		self.txt11 = self.h_tk_pos11.h_widget
		self.txt22 = self.h_tk_pos22.h_widget
		
	def icon(self,path=None):
		if path:
			self.obj.icon(path)
		else:
			self.obj.icon('.' + h_os.sep() + 'resources' + h_os.sep() + 'icon_64x64_cpt.gif')



class TkPos:
	
	def __init__(self,h_widget,words=None):
		self.h_widget = h_widget
		self.words = words
		self.reset_data()
	
	def reset(self,mode='data',words=None,pos=None,pos_tk=None,sent_no=None,sents_len=None,p_no=None,First=True):
		if mode == 'data':
			self.reset_data(pos=pos,pos_tk=pos_tk,sent_no=sent_no,sents_len=sents_len,p_no=p_no,First=First)
		else:
			self.reset_logic(words=words)
	
	def reset_logic(self,words):
		self.words = words
	
	def reset_data(self,pos=None,pos_tk=None,sent_no=None,sents_len=None,p_no=None,First=True):
		self._pos = pos
		self._pos_tk = pos_tk
		self._sent_no = sent_no
		self._sents_len = sents_len
		self._p_no = p_no
		self.First = First
		
	def sent_no(self):
		if self._sent_no is None:
			self.split()
		return self._sent_no
		
	def sents_len(self):
		if self._sents_len is None:
			self.split()
		return self._sents_len
		
	def pos_tk(self):
		if self._pos_tk is None:
			self._pos_tk = self.h_widget.cursor()
		return self._pos_tk
		
	def pos(self):
		if self._pos is None:
			self.tk2pos()
		return self._pos
	
	def tk2pos(self):
		self.split()
		return self._pos
		
	def p_no(self):
		if self._p_no is None:
			self._p_no = self.words.get_p_no(pos=self.pos())
		if self._p_no is None:
			Message(func='TkPos.p_no',type=lev_err,message=globs['mes'].wrong_input2)
			self._p_no = 0
		return self._p_no
		
	def pos2tk(self):
		self.words.change_no(no=self.p_no())
		if self.First:
			self._pos_tk = self.words.tk_p_f()
		else:
			self._pos_tk = self.words.tk_p_l()
		return self._pos_tk
			
	def split(self):
		_tuple = self.pos_tk().partition('.')
		if _tuple[2]:
			self._sent_no = Text(_tuple[0],Auto=False).str2int() - 1
			if self._sent_no == 0:
				self._sents_len = 0
			else:
				self._sents_len = self.words.sents_p_len(sent_no=self._sent_no)
				if self._sents_len is None:
					self._sents_len = 0
			self._pos = self._sents_len + Text(_tuple[2],Auto=False).str2int()
		else:
			Message(func='TkPos.split',type=lev_err,message=globs['mes'].wrong_input2)
			self._sent_no = self._sents_len = self._pos = 0



# A modified mclient class
class SymbolMap:
	
	def __init__(self,parent_obj):
		self.symbol = 'EMPTY'
		self.parent_obj = parent_obj
		self.obj = Top(parent_obj)
		self.widget = self.obj.widget
		self.obj.title(globs['mes'].paste_spec_symbol)
		self.frame = Frame(self.obj,expand=1)
		for i in range(len(globs['var']['spec_syms'])):
			if i % 10 == 0:
				self.frame = Frame(self.obj,expand=1)
			# lambda сработает правильно только при моментальной упаковке, которая не поддерживается create_button (моментальная упаковка возвращает None вместо виджета), поэтому не используем эту функцию. По этой же причине нельзя привязать кнопкам '<Return>' и '<KP_Enter>', сработают только встроенные '<space>' и '<ButtonRelease-1>'.
			# width и height нужны для Windows
			self.button = tk.Button(self.frame.widget,text=globs['var']['spec_syms'][i],command=lambda i=i:self.set(globs['var']['spec_syms'][i]),width=2,height=2).pack(side='left',expand=1)
		self.close()
		
	def set(self,sym,*args):
		self.symbol = sym
		self.close()

	def get(self,*args):
		self.show()
		return self.symbol

	def show(self,*args):
		self.obj.show()
		
	def close(self,*args):
		self.obj.close()



# Window behavior is not uniform through different platforms or even through different Windows versions, so we bypass Tkinter's commands here
class Geometry: # Requires h_os, widgets
	
	def __init__(self,parent_obj=None,title=None,hwnd=None):
		self.parent_obj = parent_obj
		self._title = title
		self._hwnd = hwnd
		self._geom = None

	def update(self):
		widgets.root().widget.update_idletasks()
	
	def save(self):
		if self.parent_obj:
			self.update()
			self._geom = self.parent_obj.widget.geometry()
			log.append('Geometry.save',lev_info,'Saved geometry: %s' % self._geom) # todo: mes
		else:
			Message(func='Geometry.save',type=lev_err,message=globs['mes'].wrong_input2)
		
	def restore(self):
		if self.parent_obj:
			if self._geom:
				log.append('Geometry.restore',lev_info,'Restoring geometry: %s' % self._geom) # todo: mes
				self.parent_obj.widget.geometry(self._geom)
			else:
				Message(func='Geometry.update',type=lev_warn,message='Failed to restore geometry!') # todo: mes
		else:
			Message(func='Geometry.restore',type=lev_err,message=globs['mes'].wrong_input2)
	
	def foreground(self,*args):
		if h_os.sys() == 'win':
			if self.hwnd():
				try:
					win32gui.SetForegroundWindow(self._hwnd)
				except: # 'pywintypes.error', but needs to import this for some reason
					# In Windows 'Message' can be raised foreground, so we just log it
					log.append('Geometry.foreground',lev_err,'Failed to change window properties!') # todo: mes
			else:
				Message(func='Geometry.foreground',type=lev_err,message=globs['mes'].wrong_input2)
		elif self.parent_obj:
			self.parent_obj.widget.lift()
		else:
			Message(func='Geometry.foreground',type=lev_err,message=globs['mes'].wrong_input2)

	def minimize(self,*args):
		if self.parent_obj:
			''' # Does not always work
			if h_os.sys() == 'win':
				win32gui.ShowWindow(self.hwnd(),win32con.SW_MINIMIZE)
			else:
			'''
			self.parent_obj.widget.iconify()
		else:
			Message(func='Geometry.minimize',type=lev_err,message=globs['mes'].wrong_input2)

	def maximize(self,*args):
		if h_os.sys() == 'win':
			#win32gui.ShowWindow(self.hwnd(),win32con.SW_MAXIMIZE)
			self.parent_obj.widget.wm_state(newstate='zoomed')
		elif self.parent_obj:
			self.parent_obj.widget.wm_attributes('-zoomed',True)
		else:
			Message(func='Geometry.maximize',type=lev_err,message=globs['mes'].wrong_input2)

	def focus(self,*args):
		if h_os.sys() == 'win':
			win32gui.SetActiveWindow(self.hwnd())
		elif self.parent_obj:
			self.parent_obj.widget.focus_set()
		else:
			Message(func='Geometry.focus',type=lev_err,message=globs['mes'].wrong_input2)

	def lift(self,*args):
		if self.parent_obj:
			self.parent_obj.widget.lift()
		else:
			Message(func='Geometry.list',type=lev_err,message=globs['mes'].wrong_input2)

	def _activate(self):
		if self.parent_obj:
			self.parent_obj.widget.deiconify()
			#self.parent_obj.widget.focus_set()
			self.parent_obj.widget.lift()
		else:
			Message(func='Geometry._activate',type=lev_err,message=globs['mes'].wrong_input2)
	
	def activate(self,MouseClicked=False,*args):
		self._activate()
		if h_os.sys() == 'win':
			self.parent_obj.widget.wm_attributes('-topmost',1)
			self.parent_obj.widget.wm_attributes('-topmost',0)
			# Иначе нажатие кнопки будет вызывать переход по ссылке там, где это не надо
			if MouseClicked:
				# Уродливый хак, но иначе никак не поставить фокус на виджет (в Linux/Windows XP обходимся без этого, в Windows 7/8 - необходимо)
				# Cимулируем нажатие кнопки мыши
				ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0) # left mouse button down
				ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0) # left mouse button up

	def hwnd(self,*args):
		if not self._hwnd:
			if self._title:
				try:
					self._hwnd = win32gui.FindWindow(None,self._title)
				except win32ui.error:
					Message(func='Geometry.hwnd',type=lev_err,message='Failed to get the window handle!') # todo: mes
			else:
				Message(func='Geometry.hwnd',type=lev_err,message=globs['mes'].not_enough_input_data)
		return self._hwnd
		
	def set(self,arg='800x600'):
		self._geom = arg
		self.restore()



class WaitBox:
	
	def __init__(self,parent_obj):
		self.type = 'WaitBox'
		self.parent_obj = parent_obj
		self._func = self._title = self._args = self._message = None
		self.obj = Top(parent_obj=self.parent_obj,Maximize=False)
		self.widget = self.obj.widget
		self.widget.geometry('300x150')
		self.label = tk.Label(self.widget,text=globs['mes'].wait)
		self.label.pack(expand=True)
		self.close()
		
	def reset(self,func_title=None,func=None,args=None,message=None): # Use tuple for 'args' to pass multiple arguments
		self._func = func
		self._title = func_title
		self._args = args
		self._message = message
		self.title()
		self.message()
	
	def run(self):
		self.show()
		if self._func:
			if self._args:
				func_res = self._func(self._args)
			else:
				func_res = self._func()
		else:
			Message(func='WaitBox.run',type=lev_err,message=globs['mes'].wrong_input2)
		self.close()
		return func_res
	
	def show(self):
		self.obj.show(Lock=False)
		# todo: fix centering in Top.center() when Lock=False
		self.obj.center(Force=True)
	
	def close(self):
		self.obj.close()
		
	def title(self,text=None):
		if text:
			self._title = text
		if self._title:
			self.obj.title(self._title)
			
	def message(self,message=None):
		if message:
			self._message = message
		if self._message:
			self.label.config(text=self._message + '\n\n' + globs['mes'].wait)
		else:
			self.label.config(text=globs['mes'].wait)



class Label:
	
	def __init__(self,parent_obj,text='Text:',font='Sans 11',side=None,fill=None,expand=False,ipadx=None,ipady=None,image=None): # 'Top' and 'Root' (the last only with 'wait_window()')
		self.type = 'Label'
		self.parent_obj = parent_obj
		self.side = side
		self.fill = fill
		self.expand = expand
		self._text = text
		self._font = font
		self.ipadx = ipadx
		self.ipady = ipady
		self.image = image
		self.gui()
		self.close()
		
	def gui(self):
		self.widget = tk.Label(self.parent_obj.widget,image=self.image)
		self.text()
		self.font()
		self.widget.pack(side=self.side,fill=self.fill,expand=self.expand,ipadx=self.ipadx,ipady=self.ipady)
		
	def text(self,arg=None):
		if arg:
			self._text = arg
		self.widget.config(text=self._text)
		
	def font(self,arg=None):
		if arg:
			self._font = arg
		try:
			self.widget.config(font=self._font)
		except tk.TclError:
			Message(func='Label.font',type=lev_err,message='Wrong font: "%s"!' % str(self._font)) # todo: mes
			self._font = 'Sans 11'
		
	def show(self):
		self.parent_obj.show()
		
	def close(self):
		self.parent_obj.close()
		
	def title(self,text='Title:'):
		self.parent_obj.title(text=text)



class CheckBox:
	
	def __init__(self,parent_obj,Active=False):
		self.parent_obj = parent_obj
		self.status = tk.IntVar()
		self.gui()
		self.reset(Active=Active)
			
	def reset(self,Active=False):
		if Active:
			self.enable()
		else:
			self.disable()
		
	def gui(self):
		self.widget = tk.Checkbutton(self.parent_obj.widget,variable=self.status)
		self.widget.pack()
		self.obj = self
		
	def show(self):
		self.parent_obj.show()
		
	def close(self):
		self.parent_obj.close()
		
	def focus(self,*args):
		self.widget.focus_set()
		
	def enable(self):
		self.widget.select()
		
	def disable(self):
		self.widget.deselect()
		
	def get(self,*args):
		return self.status.get()
		
	def toggle(self,*args):
		self.widget.toggle()
		
		
		
class Message:
	
	def __init__(self,func='MAIN',type=lev_warn,message='Message',Silent=False):
		self.Success = True
		self.Yes = False
		self.func = func
		self.message = message
		self.type = type
		self.Silent = Silent
		if not self.func or not self.message:
			self.Success = False
			log.append('Message.__init__',lev_err,globs['mes'].not_enough_input_data)
		if self.type == lev_info:
			self.info()
		elif self.type == lev_warn:
			self.warning()
		elif self.type == lev_err:
			self.error()
		elif self.type == lev_ques:
			self.question()
		else:
			log.append('Message.__init__',lev_err,globs['mes'].unknown_mode % (str(self.type),lev_info + ', ' + lev_warn + ', ' + lev_err + ', ' + lev_ques))
			
	def error(self):
		if self.Success:
			if not self.Silent:
				widgets.error().reset(title=self.func+':',text=self.message).show()
			log.append(self.func,lev_err,self.message)
		else:
			log.append('Message.error',lev_err,globs['mes'].canceled)
			
	def info(self):
		if self.Success:
			if not self.Silent:
				widgets.info().reset(title=self.func+':',text=self.message).show()
			log.append(self.func,lev_info,self.message)
		else:
			log.append('Message.info',lev_info,globs['mes'].canceled)
	
	def question(self):
		if self.Success:
			widgets.question().reset(title=self.func+':',text=self.message).show()
			self.Yes = widgets._question.Yes
			log.append(self.func,lev_ques,self.message)
		else:
			log.append('Message.question',lev_ques,globs['mes'].canceled)
	
	def warning(self):
		if self.Success:
			if not self.Silent:
				widgets.warning().reset(title=self.func+':',text=self.message).show()
			log.append(self.func,lev_warn,self.message)
		else:
			log.append('Message.warning',lev_warn,globs['mes'].canceled)



# Not using tkinter.messagebox because it blocks main GUI (even if we specify a non-root parent)
class MessageBuilder: # Requires 'constants'
	
	def __init__(self,parent_obj,type,Single=True,YesNo=False): # Most often: 'root'
		self.Yes = False
		self.YesNo = YesNo
		self.Single = Single
		self.type = type
		self.Lock = False
		self.paths()
		self.parent_obj = parent_obj
		self.obj = Top(parent_obj=self.parent_obj)
		self.widget = self.obj.widget
		self.frames()
		self.picture()
		self.txt = TextBox(parent_obj=self.top_right,Composite=True)
		self.buttons()
		self.bindings()
		Geometry(parent_obj=self.obj).set('400x300')
		self.close()
		
	def bindings(self):
		create_binding(widget=self.widget,bindings=['<Control-q>','<Control-w>','<Escape>'],action=self.close_no)
		self.widget.protocol("WM_DELETE_WINDOW",self.close)
		
	def paths(self):
		if self.type == lev_warn:
			self.path = '.' + h_os.sep() + 'resources' + h_os.sep() + 'warning.gif'
		elif self.type == lev_info:
			self.path = '.' + h_os.sep() + 'resources' + h_os.sep() + 'info.gif'
		elif self.type == lev_ques:
			self.path = '.' + h_os.sep() + 'resources' + h_os.sep() + 'question.gif'
		elif self.type == lev_err:
			self.path = '.' + h_os.sep() + 'resources' + h_os.sep() + 'error.gif'
		else:
			log.append('MessageBuilder.paths',lev_err,globs['mes'].unknown_mode % (str(self.path),', '.join([lev_warn,lev_err,lev_ques,lev_info])))
		
	def frames(self):
		frame = Frame(parent_obj=self.obj,expand=1)
		top = Frame(parent_obj=frame,expand=1,side='top')
		bottom = Frame(parent_obj=frame,expand=0,side='bottom')
		self.top_left = Frame(parent_obj=top,expand=0,side='left')
		self.top_right = Frame(parent_obj=top,expand=1,side='right')
		self.bottom_left = Frame(parent_obj=bottom,expand=1,side='left')
		self.bottom_right = Frame(parent_obj=bottom,expand=1,side='right')
		
	def buttons(self):
		if self.YesNo or self.type == lev_ques:
			YesName = 'Yes'
			NoName = 'No'
		else:
			YesName = 'OK'
			NoName = 'Cancel'
		if self.Single and self.type != lev_ques:
			Button(parent_obj=self.bottom_left,action=self.close_yes,hint='Accept and close',text=YesName,TakeFocus=1,side='right') # todo: mes
		else:
			Button(parent_obj=self.bottom_left,action=self.close_no,hint='Reject and close',text=NoName,side='left') # todo: mes
			Button(parent_obj=self.bottom_right,action=self.close_yes,hint='Accept and close',text=YesName,TakeFocus=1,side='right') # todo: mes
		
	def title(self,text=None):
		if text:
			text += ':'
		else:
			text = 'Title:' # todo: mes
		self.obj.title(text=text)
		
	def update(self,text='Message'):
		# Otherwise, updating text will not work
		self.txt.read_only(ReadOnly=False)
		self.txt.clear_text()
		self.txt.insert(text=text)
		self.txt.read_only(ReadOnly=True)
	
	def reset(self,text='Message',title='Title:'):
		self.update(text=text)
		self.title(text=title)
		return self
	
	def show(self,Lock=False,*args):
		self.obj.show()
	
	def close(self,*args):
		self.obj.close()
		# todo: fix tkinter's wait_variable problem; this partly helps
		#self.obj.widget.destroy()
		
	def close_yes(self,*args):
		self.Yes = True
		self.close()
		
	def close_no(self,*args):
		self.Yes = False
		self.close()
		
	def picture(self,*args):
		if os.path.exists(self.path):
			# We need to assign self.variable to Label, otherwise, it gets destroyed
			# Without explicitly indicating 'master', we get "image pyimage1 doesn't exist"
			self.label = Label(parent_obj=self.top_left,image=tk.PhotoImage(master=self.top_left.widget,file=self.path))
		else:
			log.append('MessageBuilder.picture',lev_warn,'Picture "%s" was not found!' % self.path) # todo: mes



class Clipboard: # Requires 'widgets'
	
	# We need to explicitly set the root object, otherwise, Tk hangs when launched from another module
	def __init__(self,root_obj,Silent=False,trigger_obj=None):
		self.Silent = Silent
		self.root_obj = root_obj
		self.trigger_obj = trigger_obj
	
	def copy(self,text,CopyEmpty=True):
		if text or CopyEmpty:
			text = str(text)
			self.root_obj.widget.clipboard_clear()
			self.root_obj.widget.clipboard_append(text)
			try:
				self.root_obj.widget.clipboard_clear()
				self.root_obj.widget.clipboard_append(text)
			except tk.TclError:
				# todo: Show a window to manually copy from
				Message(func='Clipboard.copy',type=lev_err,message=globs['mes'].clipboard_failure,Silent=self.Silent)
			except tk._tkinter.TclError:
				# Do not use GUI
				log.append('Clipboard.copy',lev_warn,'The parent has already been destroyed.') # todo: mes
			except:
				log.append('Clipboard.copy',lev_err,'An unknown error has occurred.') # todo: mes
			log.append('Clipoard.copy',lev_debug,text)
		else:
			log.append('Clipboard.copy',lev_warn,globs['mes'].empty_input)
				
	def paste(self):
		text = ''
		try:
			text = str(self.root_obj.widget.clipboard_get())
		except tk.TclError:
			Message(func='Clipboard.paste',type=lev_err,message=globs['mes'].clipboard_paste_failure,Silent=self.Silent)
		except tk._tkinter.TclError:
			# Do not use GUI
			log.append('Clipboard.paste',lev_warn,'The parent has already been destroyed.') # todo: mes
		except:
			log.append('Clipboard.paste',lev_err,'An unknown error has occurred.') # todo: mes
		# Further actions: strip, delete double line breaks
		log.append('Clipoard.paste',lev_debug,text)
		return text



class Widgets:
	
	def __init__(self):
		self._root = self._warning = self._error = self._question = self._info = self._edit_clip = self._waitbox = self._txt = self._entry = self._clipboard = None
		self._lst = []
		
	def root(self,Close=True):
		if not self._root:
			self._root = Root()
			if Close:
				self._root.close()
		return self._root
	
	def start(self):
		self.root()
		self._root.close()
		
	def end(self):
		self.close_all()
		self.root().kill()
		self._root.run()
		
	def add(self,obj):
		log.append('Widgets.add',lev_info,'Add %s' % type(obj)) # todo: mes
		self._lst.append(obj)
	
	def warning(self):
		if not self._warning:
			self._warning = MessageBuilder(parent_obj=self.root(),type=lev_warn)
			self._lst.append(self._warning)
		return self._warning
		
	def error(self):
		if not self._error:
			self._error = MessageBuilder(parent_obj=self.root(),type=lev_err)
			self._lst.append(self._error)
		return self._error
		
	def question(self):
		if not self._question:
			self._question = MessageBuilder(parent_obj=self.root(),type=lev_ques)
			self._lst.append(self._question)
		return self._question
	
	def info(self):
		if not self._info:
			self._info = MessageBuilder(parent_obj=self.root(),type=lev_info)
			self._lst.append(self._info)
		return self._info
		
	def close_all(self):
		log.append('Widgets.close_all',lev_info,'Close %d widgets' % len(self._lst)) # todo: mes
		for i in range(len(self._lst)):
			if hasattr(self._lst[i],'close'):
				self._lst[i].close()
			else:
				log.append('Widgets.close_all',lev_err,'Widget "%s" does not have a "close" action!' % type(self._lst[i]))
				
	def clipboard(self):
		if not self._clipboard:
			self._clipboard = Clipboard(root_obj=self.root())
		return self._clipboard
				
	def edit_clip(self):
		if not self._edit_clip:
			h_top = Top(parent_obj=self.root(),Maximize=False)
			self._edit_clip = TextBox(parent_obj=h_top)
			self._edit_clip.title(text=globs['mes'].correct_clipboard)
			self._edit_clip.focus()
			self._lst.append(self._edit_clip)
			Geometry(parent_obj=h_top).set('400x300')
		return self._edit_clip
		
	def txt(self,words=None,Spelling=False):
		if not self._txt:
			h_top = Top(parent_obj=self.root(),Maximize=True)
			self._txt = TextBox(parent_obj=h_top,words=words,Spelling=Spelling)
			self._txt.focus()
			self._lst.append(self._txt)
		return self._txt
		
	def entry(self):
		if not self._entry:
			h_top = Top(parent_obj=self.root())
			self._entry = Entry(parent_obj=h_top)
			self._entry.focus()
			self._lst.append(self._entry)
		return self._entry
	
	def waitbox(self):
		if not self._waitbox:
			self._waitbox = WaitBox(parent_obj=self.root())
			self._lst.append(self._waitbox)
		return self._waitbox



widgets = Widgets()

if __name__ == '__main__':
	widgets.start()
	text = '''Something funny with this guy
	I am glad he is not my test
	Glad is so angry'''
	words = Words(text)
	h_top = Top(parent_obj=widgets.root())
	h_txt = TextBox(parent_obj=h_top,words=words)
	h_txt.title(text='My text is:')
	h_txt.insert(text)
	h_txt.widget.focus_set()
	Geometry(parent_obj=h_top).set('500x350')
	h_txt.show()
	widgets.end()
