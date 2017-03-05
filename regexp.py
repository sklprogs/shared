#!/usr/bin/python3

import re
import sre_constants
import shared as sh
import sharedGUI as sg



# This class is for both checking a regular expression and replacing matches through text (these actions require different arguments and are not necessarily interconnected)
class Record:
	
	''' Example:
			# Expressions must be raw strings, otherwise, there will be no match
			orig:		r'(\d+)[\s]{0,1}[–-][\s]{0,1}(\d+)'
			final:		r'\1-\2'
			what1:		'Figures 1 - 2 show that...'
			with1:		'Figures 1-2 show that...'
		'''
	
	def __init__(self,orig,final,what1=None,with1=None,what2=None,with2=None,what3=None,with3=None,_id='Unknown id',Silent=False):
		self.Success = True
		self._orig = orig
		self._final = final
		self._what1 = what1
		self._with1 = with1
		self._what2 = what2
		self._with2 = with2
		self._what3 = what3
		self._with3 = with3
		self._id = _id
		self._what = self._with = ''
		self.Silent = Silent
		if not self._orig or not self._final:
			self.Success = False
			sg.Message('Record.__init__',sh.lev_warn,sh.globs['mes'].not_enough_input_data,Silent=self.Silent)
	
	def apply(self,text):
		if self.Success:
			try:
				result = re.sub(self._orig,self._final,text)
			except sre_constants.error:
				result = ''
				self.Success = False
				sg.Message('Record.apply',sh.lev_warn,'A syntax error in the regular expression (id: %s)!' % str(self._id)) # todo: mes
			return result
		else:
			sh.log.append('Record.apply',sh.lev_warn,sh.globs['mes'].canceled)
	
	def _check(self):
		if self.Success:
			result = self.apply(text=self._what)
			if self.Success and result != self._with:
				self.Success = False
				sg.Message('Record._check',sh.lev_warn,sh.globs['mes'].reg_ex_failure % (str(self._id),str(self._with),str(result)))
		else:
			sh.log.append('Record.check',sh.lev_warn,sh.globs['mes'].canceled)
		return self.Success
	
	def check(self):
		if self.Success:
			cond1 = self._what1 and self._with1
			cond2 = self._what2 and self._with2
			cond3 = self._what3 and self._with3
			if cond1 or cond2 or cond3:
				if cond1:
					self._what = self._what1
					self._with = self._with1
					self._check()
				if self.Success and cond2:
					self._what = self._what2
					self._with = self._with2
					self._check()
				if self.Success and cond3:
					self._what = self._what3
					self._with = self._with3
					self._check()
			else:
				self.Success = False
				sg.Message('Record.check',sh.lev_warn,sh.globs['mes'].not_enough_input_data)
		else:
			sh.log.append('Record.check',sh.lev_warn,sh.globs['mes'].canceled)
		return self.Success



if __name__ == '__main__':
	orig = r'([Cc]laim|[Cc]olumn|[Pp]age|[Ss]heet|[Pp]aragraph|[Ll]ine)[s]{0,1}[\s]{0,1}(\d+[,-][\s]{0,1}\d+)'
	final = r'\1s \2'
	#text = 'Records 200 - 300 have undergone a regular procedure...'
	what1 = 'pages 1-2'
	with1 = 'pages 1-2'
	rec = Record(orig=orig,final=final,what1=what1,with1=with1)
	print(rec.check())
	#print(rec.apply(text=what1))
