#!/usr/bin/env python

import wx
class A(wx.Frame):
	def __init__(self, parent, title):
		super(A, self).__init__(parent, title=title, size=(200,200))
	
		self.SetPosition((29,30))
		self.InitUI()
#		self.Centre()
		self.Show()
	def InitUI(self):
		self.x = 0
		self.y = 0
		panel = wx.Panel(self, -1)
		self.button = wx.Button(panel)
		self.button.Bind(wx.EVT_BUTTON, self.onclick)
		
		self.Bind(wx.EVT_MOVE, self.move)

	def move(self, e):
		self.x,self.y = e.GetPosition()
	def onclick(self,e):
		b = B(None, title="Exercise")
		b.SetPosition((self.x, self.y))
		b.Show(True)


class B(A):
	def __init__(self, parent,  title):
		super(B, self).__init__(parent, title=title )

	print A.x, A.y
if __name__ == '__main__':
	app = wx.App(False)
	main_frame = A(None, title = "ABC")
	app.MainLoop()
