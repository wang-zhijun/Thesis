#!/usr/bin/env python

import time
import wx

class MyForm(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, wx.ID_ANY, "Timer Tutorial 1", size = (500,500))
		
		panel = wx.Panel(self, wx.ID_ANY)
		
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.update, self.timer)

		self.toggleBtn = wx.Button(panel, wx.ID_ANY, "Start")
		self.toggleBtn.Bind(wx.EVT_BUTTON, self.onToggle)

	def onToggle(self, event):
		'''
		btnLabel = self.toggleBtn.GetLabel()
		if btnLabel == "Start":
			print "starting timer..."
			self.timer.Start(1000)
			self.toggleBtn.SetLabel("Stop")
		else:
			print "timer stopped!"
			self.timer.Stop()
			self.toggleBtn.SetLabel("Start")
		'''
		
		# Check weather the timer is running
		if self.timer.IsRunning():
			self.timer.Stop()
			self.toggleBtn.SetLabel("Start")
			print "timer stopped!"
		else:
			print "starting timer..."
			self.timer.Start(1000)
			self.toggleBtn.SetLabel("Stop")



	def update(self, event):
		print "\nupdated: ",
		print time.ctime()

if __name__ == '__main__':
	app = wx.App()

	frame = MyForm().Show()
	
	app.MainLoop()
		
