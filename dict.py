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

class Example(wx.Frame):
  
	def __init__(self, parent, title):
		super(Example, self).__init__(parent, title=title, size=(560, 400))
            
		self.InitUI()
		self.Centre()
		self.Show()     
        
	def InitUI(self):
    
		panel = wx.Panel(self, -1)
		panel.SetBackgroundColour('#6f8089')

		vbox = wx.BoxSizer(wx.VERTICAL)

		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)	
		hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		hbox4 = wx.BoxSizer(wx.HORIZONTAL)

		# create,add word area and search button
		self.word_search = wx.TextCtrl(panel, id = 10, style = wx.PROCESS_ENTER)
		self.zh_check = wx.CheckBox(panel, label='中文')
		self.zh_check.SetValue(True)
		
  
		# create chinese meaning text area
		self.zh_meaning = wx.TextCtrl(panel, id = 22, size=(350,170),style = wx.TE_MULTILINE)

		self.memo = wx.TextCtrl(panel, id = 30, style = wx.TE_MULTILINE)

		# Add save memo button
		save_btn = wx.Button(panel, label='Save')
		self.exercise_btn = wx.Button(panel, label='Exercise')
			
		hbox1.Add(self.word_search, proportion=5, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
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
		panel.SetSizer(vbox)
		
        
	def OnSearch(self, event):
		# Get input word to search
		self.word = self.word_search.GetValue()
		# create word url
		zh_word_url = 'http://dict.cn/'+self.word
		jp_word_url = 'http://kotobank.jp/ejword/'+self.word
		zh_word_content = ""
		jp_word_content = ""

		if self.zh_check.IsChecked():
			
			zh_file = urllib2.urlopen(zh_word_url)
			zh_html = zh_file.read()
			soup = BeautifulSoup(zh_html)

			phonetic = soup.find('div', class_ = 'phonetic')
			# if can not find the word
			if phonetic is None:
				self.zh_meaning.SetValue('Cannot find the word')
				return 
			else:
				pronunciations = phonetic.find_all('bdo')
				pronun = pronunciations[0].find(text=True)
				zh_word_content = pronun + '\n\n'

			# basic meanings of the word
			layout_dual = soup.find('div', class_ = 'layout dual')
			if layout_dual is None:
				basic = soup.find('div', class_ = 'layout basic clearfix')
				word_meanings = basic.find_all('strong')
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

		self.word_search.SelectAll()

	def	OnSaveMemo(self,e):
		zh_file = dbm.open('zh_words','c')  
		memo_file = dbm.open('memo_words','c')  
		zh_file[self.word] = self.zh_meaning.GetValue().encode('utf-8')		
		memo_file[self.word] = self.memo.GetValue().encode('utf-8')		
		zh_file.close()
		memo_file.close()

	def InitSUBUI(self, e):
		exercise_ui = SUBUI(None,title = 'Exercise')	
		exercise_ui.Show(True)	
		exercise_ui.Centre()	
		# MakeModal(modal):Disables all other windows in the application so that the user can only interact with this window.
		exercise_ui.MakeModal(True)

class SUBUI(wx.Frame):
	def __init__(self, parent, title):
		super(SUBUI, self).__init__(parent, title=title, size=(560, 400))
		
		self.InitUI()

	def InitUI(self):
		panel = wx.Panel(self, -1)
		panel.SetBackgroundColour('#6f8089')


		vbox = wx.BoxSizer(wx.VERTICAL)
		
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)	
		hbox3 = wx.BoxSizer(wx.HORIZONTAL)

		self.zh_meaning = wx.TextCtrl(panel, id = 50, size=(350,170),style = wx.TE_MULTILINE)
		self.memo = wx.TextCtrl(panel, id = 60, style = wx.TE_MULTILINE)
		self.word_search = wx.TextCtrl(panel, id = 70, style = wx.PROCESS_ENTER)
		self.start_btn = wx.Button(panel, id = 72,label='Start')
		self.elapsed_time = wx.StaticText(panel, id = 74 )

		hbox1.Add(self.zh_meaning, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
		hbox2.Add(self.memo, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
		hbox3.Add(self.word_search, proportion=2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
		hbox3.Add(self.start_btn, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)
		hbox3.Add(self.elapsed_time, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10)

		vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)
		vbox.Add(hbox3, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

		panel.SetSizer(vbox)

		self.start_btn.SetFocus()
		# Start timer
		self.timer1 = wx.Timer(self, id = 100)
		self.Bind(wx.EVT_TIMER, self.update, self.timer1)
		self.Bind(wx.EVT_BUTTON, self.OnStartTimer, self.start_btn)
		self.Bind(wx.EVT_CLOSE, self.on_close)

		font = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
		self.elapsed_time.SetFont(font)

	def OnStartTimer(self, event):
		if self.timer1.IsRunning():
			self.timer1.Stop()
			self.start_btn.SetLabel("Start")
		else:
			self.start_btn.SetLabel("Typing...")
			self.word_search.SetFocus() 
			self.timer1.Start(1000)
			self.start = time.time()	
	
	def update(self, event):
			end = time.time() - self.start
			elapsed_time = str(int(end)) + ' seconds'
			self.elapsed_time.SetLabel(elapsed_time)
	
	def on_close(self, evt):
		self.MakeModal(False)
		evt.Skip()	
		
			
	
if __name__ == '__main__':
    app = wx.App(False)
    main_frame = Example(None, title='Dictionary')
    app.MainLoop()


