#!/usr/bin/env python
import wx

class MainFrame(wx.Frame): 
    def __init__(self): 
        wx.Frame.__init__(self, None, wx.NewId(), "Main") 
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.button = wx.Button(self, wx.NewId(), "Open a child")
        self.sizer.Add(self.button, proportion=0, border=2, flag=wx.ALL)
        self.SetSizer(self.sizer)
        self.button.Bind(wx.EVT_BUTTON, self.on_button)

        self.Layout()

    def on_button(self, evt):
        frame = ChildFrame(self)
        frame.Show(True)
        frame.MakeModal(True)

class ChildFrame(wx.Frame): 
    def __init__(self, parent): 
        wx.Frame.__init__(self, parent, wx.NewId(), "Child")
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, evt):
        self.MakeModal(False)
        evt.Skip()

class MyApp(wx.App):
    def OnInit(self):
        frame = MainFrame()
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()    
