#!/usr/bin/env python

import time
import wx

TIMER_ID1 = 2000
TIMER_ID2 = 2001


class MyForm(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, wx.ID_ANY, "Timer Tutorial 1", size = (500,500))
		
		panel = wx.Panel(self, wx.ID_ANY)
		
		self.timer1 = wx.Timer(self, id = TIMER_ID1)
		self.timer2 = wx.Timer(self, id = TIMER_ID2)
		self.Bind(wx.EVT_TIMER, self.update, self.timer1)
		self.Bind(wx.EVT_TIMER, self.update, self.timer2)

		self.toggleBtn1 = wx.Button(panel, wx.ID_ANY, "Start Timer 1")
		self.toggleBtn2 = wx.Button(panel, wx.ID_ANY, "Start Timer 2")

		self.toggleBtn1.Bind(wx.EVT_BUTTON, self.onStartTimer)
		self.toggleBtn2.Bind(wx.EVT_BUTTON, self.onStartTimer)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.toggleBtn1, 0, wx.ALL|wx.CENTER, 5)
		sizer.Add(self.toggleBtn2, 0, wx.ALL|wx.CENTER, 5)
		
		panel.SetSizer(sizer)
		
		self.objDict = {self.toggleBtn1: (1, self.timer1, 1000),
						self.toggleBtn2: (2, self.timer2, 3000)}


	def onStartTimer(self, event):
		btn = event.GetEventObject()
		timerNum, timer, secs = self.objDict[btn]
		if timer.IsRunning():
			timer.Stop()
			btn.SetLabel("Start Timer %s" % timerNum)
			print "timer %s stopped!" % timerNum
	
		else:
			print "starting timer %s..." % timerNum
			timer.Start(secs)
			btn.SetLabel("Stop Timer %s" % timerNum)

	def update(self, event):
		timerID = event.GetId()
		if timerID == self.timer1.GetId():
			print "\ntimer 1 updated: ",
		else:
			print "\ntimer 2 updated: ",
		print time.ctime()

if __name__ == '__main__':
	app = wx.App()

	frame = MyForm().Show()
	
	app.MainLoop()
		
