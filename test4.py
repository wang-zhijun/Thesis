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

		self.toggleBtn1.Bind(wx.EVT_BUTTON, self.onStartTimerOne)
		self.toggleBtn2.Bind(wx.EVT_BUTTON, self.onStartTimerOne)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.toggleBtn1, 0, wx.ALL|wx.CENTER, 5)
		sizer.Add(self.toggleBtn2, 0, wx.ALL|wx.CENTER, 5)
		
		panel.SetSizer(sizer)

	def onStartTimerOne(self, event):
		buttonObj = event.GetEventObject()
		btnLabel = buttonObj.GetLabel()
		timerNum = int(btnLabel[-1:])
		print timerNum
		
		if btnLabel == 'Start Timer %s' % timerNum:
			if timerNum == 1:
				print "starting timer 1..."
				self.timer1.Start(1000)
			else:
				print "starting timer 2..."
				self.timer2.Start(3000)
			buttonObj.SetLabel("Stop Timer %s" % timerNum)
		else:
			if timerNum == 1:
				self.timer1.Stop()
				print "timer 1 stopped!"
			else:
				self.timer2.Stop()
				print "timer 2 stopped!"
			buttonObj.SetLabel("Start Timer %s" % timerNum)

	def update(self, event):
		timerID = event.GetId()
		if timerID == TIMER_ID1:
			print "\ntimer 1 updated: ",
		if timerID == TIMER_ID2:
			print "\ntimer 2 updated: ",
		print time.ctime()

if __name__ == '__main__':
	app = wx.App()

	frame = MyForm().Show()
	
	app.MainLoop()
		
