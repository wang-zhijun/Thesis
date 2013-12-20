#!/usr/bin/python
# -*- coding: utf-8 -*-


import wx

import sys, os, re, errno, time
import urllib2
# invoke 'play'(linux) or 'afplay'(Mac OS X) command
import subprocess
# generate random number in exercise mode
from random import randint
from bs4 import BeautifulSoup
from colorama import Fore

import dbm
# for exercise mode, shuffle the words list
from random import shuffle

class Example(wx.Frame):
	def __init__(self, parent, title):
		super(Example, self).__init__(parent, title=title, size=(560, 400))
            
		self.InitUI()
		self.Centre()
		self.Show()     
	def InitUI(self):
		self.word=""
		self.audio_url = ""
		self.audio_name = ""
		
		# store frame position
		self.x = 0
		self.y = 0

		panel = wx.Panel(self, -1)
		panel.SetBackgroundColour('#726E6D')

		vbox = wx.BoxSizer(wx.VERTICAL)

		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)	
		hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		hbox4 = wx.BoxSizer(wx.HORIZONTAL)

		# create,add word area and search button
		self.word_search = wx.TextCtrl(panel, id = 10, style = wx.PROCESS_ENTER)
		self.icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('resize_voice.png'))
		self.zh_check = wx.CheckBox(panel, label='中文', size=(30,30))
		self.zh_check.SetValue(True)
		
  
		# create chinese meaning text area
		self.zh_meaning = wx.TextCtrl(panel, id = 22, size=(350,170),style = wx.TE_MULTILINE)

		self.memo = wx.TextCtrl(panel, id = 30, style = wx.TE_MULTILINE)

		# Add save memo button
		save_btn = wx.Button(panel, label='Save')
		self.exercise_btn = wx.Button(panel, label='Exercise')
			
		hbox1.Add(self.word_search, proportion=4, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		hbox1.Add(self.icon, flag=wx.EXPAND|wx.TOP, border=10)
		hbox1.Add(self.zh_check, proportion=1, flag=wx.LEFT|wx.TOP, border=10)
		hbox2.Add(self.zh_meaning, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
		hbox3.Add(self.memo, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		hbox4.Add(save_btn, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		hbox4.Add(self.exercise_btn, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
        
		vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		vbox.Add(hbox3, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		vbox.Add(hbox4, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

		# Set focus on the word_search area
		self.word_search.SetFocus()

		# Bind  methods to word_search and check boxes
		self.word_search.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)
		save_btn.Bind(wx.EVT_BUTTON, self.OnSaveMemo)
		self.exercise_btn.Bind(wx.EVT_BUTTON, self.InitSUBUI) 
		self.icon.Bind(wx.EVT_LEFT_DOWN, self.OnSound)
		self.Bind(wx.EVT_MOVE, self.OnMove)
		panel.SetSizer(vbox)

		mkdir_p('mp3_dir')

		font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
		self.word_search.SetFont(font)
		self.zh_meaning.SetFont(font)
		self.memo.SetFont(font)

	def OnMove(self, e):
		self.x, self.y = e.GetPosition()

	def OnSearch(self, event):
		# Get input word to search
		#http://stackoverflow.com/questions/17887503/how-can-i-improve-this-code-for-checking-if-text-fields-are-empty-in-wxpython
		self.word = self.word_search.GetValue().strip() or None
		if self.word is None:
			self.zh_meaning.Clear()
			return 
		# create word url
		zh_word_url = 'http://dict.cn/'+self.word

		zh_word_content = ""

		self.audio_url = "http://translate.google.com/translate_tts?tl=en&q="+self.word
		self.audio_dir = os.getcwd()+"/mp3_dir"
		self.audio_name = self.audio_dir+'/'+self.word+'.mp3'


		if self.zh_check.IsChecked():
			
			zh_file = urllib2.urlopen(zh_word_url)
			zh_html = zh_file.read()
			soup = BeautifulSoup(zh_html)

			phonetic = soup.find('div', class_ = 'phonetic')
			# if can not find the word
			try:
				pronunciations = phonetic.find_all('bdo')
				pronun = pronunciations[0].find(text=True)
				zh_word_content = pronun + '\n\n'
			except AttributeError:
				pass
			except IndexError:
				pass
			# basic meanings of the word
			layout_dual = soup.find('div', class_ = 'layout dual')
			if layout_dual is None:
				basic = soup.find('div', class_ = 'layout basic clearfix')
				try:
					word_meanings = basic.find_all('strong')
				except AttributeError:
					self.zh_meaning.Clear()
					self.memo.Clear()
					self.word_search.SelectAll()
					return 

				for meaning in word_meanings:
					text = meaning.find(text=True)
					zh_word_content = zh_word_content + text + '\n\n'
				self.zh_meaning.SetValue(zh_word_content.encode('utf-8'))
			else:
				# word meanings in detail
				li_tags = layout_dual.find_all('li')
				for li in li_tags:
					zh_word_content = zh_word_content + li.get_text() + '\n\n'
				self.zh_meaning.SetValue(zh_word_content.encode('utf-8'))

		process_audio(self.audio_url, self.audio_name)	
		
		self.word_search.SelectAll()
		
		##############################################
		#try to find the memo about the word from file
		##############################################
		f = dbm.open('memo_words', 'c')
		try:
			self.memo.SetValue(f[self.word].decode('utf-8'))
		except KeyError, e:
			self.memo.Clear()
		finally:
			f.close()	

	def	OnSaveMemo(self,e):
		zh_file = dbm.open('zh_words','c')  
		memo_file = dbm.open('memo_words','c')  
		if self.word is '':
			return 
		try:
			zh_file[self.word] = self.zh_meaning.GetValue().strip().encode('utf-8')		
		except AttributeError: 
			return 
		memo_file[self.word] = self.memo.GetValue().strip().encode('utf-8')		
		zh_file.close()
		memo_file.close()
		self.word_search.SetFocus()

	def InitSUBUI(self, e):
		exercise_ui = SUBUI(None,title = 'Exercise')	
		exercise_ui.SetPosition((self.x, self.y)) 
		exercise_ui.Show(True)	
		# MakeModal(modal):Disables all other windows in the application so that the user can only interact with this window.
		exercise_ui.MakeModal(True)


	def OnSound(self, event):
		if self.word is "":
			return
		else:
			process_audio(self.audio_url, self.audio_name)

class SUBUI(wx.Frame):
	def __init__(self, parent, title):
		super(SUBUI, self).__init__(parent, title=title, size=(560, 400))
		
		self.InitUI()

	def InitUI(self):
		self.last_word = ""
		self.audio_url = ""
		self.audio_name = ""
	
		self.audio_url = ""
		self.audio_dir = os.getcwd()+"/mp3_dir"
		self.audio_name = "" 

		self.db_memo = dbm.open('memo_words', 'c')
		self.db_words = dbm.open('zh_words', 'c')

		panel = wx.Panel(self, -1)
		panel.SetBackgroundColour('#726E6D')


		vbox = wx.BoxSizer(wx.VERTICAL)
		
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)	
		hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		hbox4 = wx.BoxSizer(wx.HORIZONTAL)

		self.zh_meaning = wx.TextCtrl(panel, id = 50, size=(350,170),style = wx.TE_MULTILINE)
		self.memo = wx.TextCtrl(panel, id = 60, style = wx.TE_MULTILINE)
		self.word_search = wx.TextCtrl(panel, id = 70, style = wx.PROCESS_ENTER)
		self.start_btn = wx.Button(panel, id = 72,label='Start')
		self.icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('resize_voice.png'))
		self.gauge = wx.Gauge(panel)
		self.del_btn = wx.Button(panel, id = 80, label = 'Delete word')


		hbox1.Add(self.zh_meaning, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
		hbox2.Add(self.memo, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
		hbox3.Add(self.word_search, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
		hbox3.Add(self.start_btn, flag=wx.EXPAND| wx.LEFT|wx.RIGHT, border=10)
		hbox3.Add(self.icon, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
		hbox3.Add(self.gauge, proportion=2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
		hbox4.Add(self.del_btn, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)

		vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		vbox.Add(hbox3, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		vbox.Add(hbox4, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)


		panel.SetSizer(vbox)

		self.start_btn.SetFocus()
		# Start timer
		self.timer1 = wx.Timer(self, id = 100)
		self.Bind(wx.EVT_TIMER, self.update, self.timer1)
		self.Bind(wx.EVT_BUTTON, self.OnStartTimer, self.start_btn)
		self.icon.Bind(wx.EVT_LEFT_DOWN, self.OnSound)
		self.Bind(wx.EVT_CLOSE, self.on_close)
		self.Bind(wx.EVT_TEXT_ENTER, self.OnCheck, self.word_search)
		self.Bind(wx.EVT_BUTTON, self.OnDeleteWord, self.del_btn)

		font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
		self.zh_meaning.SetFont(font)
		self.memo.SetFont(font)

	def OnStartTimer(self, event):
		if self.timer1.IsRunning():
			self.timer1.Stop()
			self.start_btn.SetLabel("Start")
		else:
			self.start_btn.SetLabel("Typing...")
			self.word_search.SetFocus() 
			self.timer1.Start(1000)
			self.start = time.time()	
			self.exercise_mode()
	
	def update(self, event):
			end = time.time() - self.start
	
	def on_close(self, evt):
		self.MakeModal(False)
		evt.Skip()	

	# Get the value from word_search area
	def OnCheck(self, event):

		#http://effbot.org/librarybook/dbm.htm
		input_str = self.word_search.GetValue() or None
		if self.last_word == None:
			self.word_search.Clear()
			return
		if input_str == self.last_word:
			self.count = self.count + 1
			self.gauge.SetValue(self.count)
			if self.count == self.task_range:
				self.word_search.Clear()
				self.zh_meaning.Clear()
				self.memo.Clear()
				self.timer1.Stop()
				self.start_btn.SetLabel("Start")
				self.start_btn.SetFocus()
				self.gauge.SetLabel("Task Completed")
				return
			try:
				self.last_word = self.zh_li.pop() 
			except IndexError:
				self.word_search.Clear()
				self.zh_meaning.Clear()
				self.memo.Clear()
				self.timer1.Stop()
				self.start_btn.SetLabel("Start")
				self.start_btn.SetFocus()
				return 	

			self.zh_meaning.SetValue(self.db_words[self.last_word].decode('utf-8'))
			try:
				self.memo.SetValue(self.db_memo[self.last_word].decode('utf-8'))
			except KeyError:
				pass
			
			
			self.audio_url = "http://translate.google.com/translate_tts?tl=en&q="+self.last_word
			self.audio_name = self.audio_dir+'/'+self.last_word+'.mp3'
			process_audio(self.audio_url, self.audio_name)
			self.word_search.Clear()

		else:
			self.word_search.SetValue(self.last_word)
			self.word_search.SelectAll()

	def exercise_mode(self):
		self.zh_li = []
		for key in self.db_words.keys():
			self.zh_li.append(key)
		if len(self.zh_li)== 0:
			self.timer1.Stop()
			self.start_btn.SetLabel("Start")
			return 
		shuffle(self.zh_li)
		# gauge count
		self.count = 0
		self.task_range = len(self.zh_li)

		self.gauge.SetRange(self.task_range)
		try:
			self.last_word = self.zh_li.pop() 
		except IndexError:
			self.word_search.Clear()
			self.zh_meaning.Clear()
			self.memo.Clear()
			return 

		self.zh_meaning.SetValue(self.db_words[self.last_word].decode('utf-8'))
		try:
			self.memo.SetValue(self.db_memo[self.last_word].decode('utf-8'))
		except KeyError:
			pass
		# play sound after press Start button
		self.audio_url = "http://translate.google.com/translate_tts?tl=en&q="+self.last_word
		self.audio_name = self.audio_dir+'/'+self.last_word+'.mp3'
		process_audio(self.audio_url, self.audio_name)
	def OnDeleteWord(self,event):
		if self.last_word == "":
			return 
		try:
			del self.db_words[self.last_word]
			del self.db_memo[self.last_word]
			self.count = self.count + 1
			self.gauge.SetValue(self.count)
			self.word_search.SetFocus()
		except KeyError:
			pass
		try:
			self.last_word = self.zh_li.pop()
		except IndexError:
			self.timer1.Stop()
			self.start_btn.SetLabel("Start")
			self.word_search.Clear()
			self.zh_meaning.Clear()
			self.memo.Clear()
			return 

		self.zh_meaning.SetValue(self.db_words[self.last_word].decode('utf-8'))
		try:
			self.memo.SetValue(self.db_memo[self.last_word].decode('utf-8'))
		except KeyError:
			pass


	def OnSound(self, event):
		if self.last_word is "":
			return
		else:
			process_audio(self.audio_url, self.audio_name)

def process_audio(audio_url, mp3_name):
	if os.path.exists(mp3_name):
		if sys.platform == 'darwin':
			process = subprocess.Popen(['afplay', mp3_name], stdout=dev_null, stderr=dev_null)
		else:
			process = subprocess.Popen(['play', mp3_name], stdout=open("/dev/null","w"), stderr=subprocess.STDOUT)
#		retcode = process.wait()
	else:
		# download mp3 file to $HOME/mp3.dir
		download_mp3(audio_url, mp3_name)
		# find wait function on the last line
		if sys.platform == 'darwin':
			process = subprocess.Popen(['afplay', mp3_name], stdout=dev_null, stderr=dev_null)
		else:
			process = subprocess.Popen(['play', mp3_name], stdout=open("/dev/null","w"), stderr=subprocess.STDOUT)
#		retcode = process.wait()


def download_mp3(audio_url, mp3_name):
	headers = {'User-Agent':'Mozilla/5.0'}
	request = urllib2.Request(audio_url, None, headers)
	mp3file = urllib2.urlopen(request)
	with open(mp3_name, 'wb') as output_mp3:
		output_mp3.write(mp3file.read())
			

def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc:
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else:
			raise

if __name__ == '__main__':

    app = wx.App(False)
    main_frame = Example(None, title='Dictionary')
    app.MainLoop()
