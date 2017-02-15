#!/usr/bin/python3
#coding=UTF-8

import os
import tkinter as tk # for PhotoImage
from constants import *
from sharedGUI import Root, Top, Button, TextBox, create_binding, Entry, Frame, Label, Geometry
from shared import h_os, log



# Not using tkinter.messagebox because it blocks main GUI (even if we specify a non-root parent)
class MessageBuilder: # Requires 'constants'
	
	def __init__(self,parent_obj,type,Single=True,YesNo=False): # Most often: 'root'
		self.Yes = False
		self.YesNo = YesNo
		self.Single = Single
		self.type = type
		self.paths()
		self.parent_obj = parent_obj
		self.obj = Top(parent_obj=self.parent_obj)
		self.widget = self.obj.widget
		self.frames()
		self.picture()
		self.txt = TextBox(parent_obj=self.top_right,Composite=True)
		self.buttons()
		Geometry(parent_obj=self.obj).set('400x300')
		self.close()
		
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
	
	def show(self,*args):
		self.obj.show()
	
	def close(self,*args):
		self.obj.close()
		
	def close_yes(self,*args):
		self.Yes = True
		self.close()
		
	def close_no(self,*args):
		self.Yes = False
		self.close()
		
	def picture(self,*args):
		if os.path.exists(self.path):
			# We need to assign self.variable to Label, otherwise, it gets destroyed
			self.label = Label(parent_obj=self.top_left,image=tk.PhotoImage(file=self.path))
		else:
			log.append('MessageBuilder.picture',lev_warn,'Picture "%s" was not found!' % self.path) # todo: mes



if __name__ == '__main__':
	h_root = Root()
	h_root.close()
	warn = MessageBuilder(parent_obj=h_root,type=lev_warn,Single=True,YesNo=False)
	warn_yesno = MessageBuilder(parent_obj=h_root,type=lev_warn,Single=True,YesNo=True)
	warn2 = MessageBuilder(parent_obj=h_root,type=lev_warn,Single=False,YesNo=False)
	warn2_yesno = MessageBuilder(parent_obj=h_root,type=lev_warn,Single=False,YesNo=True)

	err = MessageBuilder(parent_obj=h_root,type=lev_err,Single=True,YesNo=False)
	err_yesno = MessageBuilder(parent_obj=h_root,type=lev_err,Single=True,YesNo=True)
	err2 = MessageBuilder(parent_obj=h_root,type=lev_err,Single=False,YesNo=False)
	err2_yesno = MessageBuilder(parent_obj=h_root,type=lev_err,Single=False,YesNo=True)

	info = MessageBuilder(parent_obj=h_root,type=lev_info,Single=True,YesNo=False)
	info_yesno = MessageBuilder(parent_obj=h_root,type=lev_info,Single=True,YesNo=True)
	info2 = MessageBuilder(parent_obj=h_root,type=lev_info,Single=False,YesNo=False)
	info2_yesno = MessageBuilder(parent_obj=h_root,type=lev_info,Single=False,YesNo=True)

	ques = MessageBuilder(parent_obj=h_root,type=lev_ques,Single=True,YesNo=False)
	ques_yesno = MessageBuilder(parent_obj=h_root,type=lev_ques,Single=True,YesNo=True)
	ques2 = MessageBuilder(parent_obj=h_root,type=lev_ques,Single=False,YesNo=False)
	ques2_yesno = MessageBuilder(parent_obj=h_root,type=lev_ques,Single=False,YesNo=True)

	warn.reset(text='Предупреждение, 1 кнопка, OK/Cancel').show()
	warn_yesno.reset(text='Предупреждение, 1 кнопка, Yes/No').show()
	warn2.reset(text='Предупреждение, 2 кнопки, OK/Cancel').show()
	warn2_yesno.reset(text='Предупреждение, 2 кнопки, Yes/No').show()
	
	err.reset(text='Ошибка, 1 кнопка, OK/Cancel').show()
	err_yesno.reset(text='Ошибка, 1 кнопка, Yes/No').show()
	err2.reset(text='Ошибка, 2 кнопки, OK/Cancel').show()
	err2_yesno.reset(text='Ошибка, 2 кнопки, Yes/No').show()
	
	info.reset(text='Уведомление, 1 кнопка, OK/Cancel').show()
	info_yesno.reset(text='Уведомление, 1 кнопка, Yes/No').show()
	info2.reset(text='Уведомление, 2 кнопки, OK/Cancel').show()
	info2_yesno.reset(text='Уведомление, 2 кнопки, Yes/No').show()
	
	ques.reset(text='Вопрос, 1 кнопка (все равно 2 кнопки в итоге), OK/Cancel (Все равно Yes/No)').show()
	ques_yesno.reset(text='Вопрос, 1 кнопка (все равно 2 кнопки в итоге), Yes/No').show()
	ques2.reset(text='Вопрос, 2 кнопки, OK/Cancel (Все равно Yes/No)').show()
	ques2_yesno.reset(text='Вопрос, 2 кнопки, Yes/No').show()

	h_root.kill()
	h_root.run()
