#!/usr/bin/env python


import wx

class MyFrame(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title,size=(250, 250))

		topPanel = wx.Panel(self)

		panel1 = wx.Panel(topPanel, -1,pos=(0,100),size=(100,100))
		panel1.SetBackgroundColour('#6f8089')
		button1 = wx.Button(panel1, -1, label="click me")

		panel2 = wx.Panel(topPanel, -1,pos=(0,200))
		panel2.SetBackgroundColour('#9f8089')
		button2 = wx.Button(panel2, -1, label="click me")
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(panel1,0,wx.EXPAND|wx.ALL,border=10)
		sizer.Add(panel2,0,wx.EXPAND|wx.ALL,border=10)

		topPanel.SetSizer(sizer)



class MyApp(wx.App):
	def OnInit(self):
		frame = MyFrame(None, -1, 'frame')
		frame.Show(True)
		return True

app = MyApp(0)
app.MainLoop()

