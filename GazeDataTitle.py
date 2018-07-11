#!/usr/bin/env python
# -*- coding: utf-8 -*-

# gaze_dataをウィンドウタイトルに表示するプログラム
 
import wx
import tobii_research as tr

gaze_data_string = 'gaze_data_string'

found_eyetrackers = tr.find_all_eyetrackers()
eyetracker = found_eyetrackers[0]

def gaze_data_callback(gaze_data):
    global gaze_data_string
    print(str(gaze_data['left_gaze_point_on_display_area']))
    gaze_data_string = str(gaze_data['left_gaze_point_on_display_area'])
 
eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

class MyWindow(wx.Frame):
    def __init__(self, parent=None, id=-1, title=None):
        wx.Frame.__init__(self, parent, id, title)
        self.panel = wx.Panel(self, size=(1000, 200))
        self.panel.SetBackgroundColour('WHITE')
        self.Fit()
 
        self.Bind(wx.EVT_CLOSE, self.CloseWindow)
 
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer.Start(100)
 
    def CloseWindow(self, event):
        global eyetracker, tr
        eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
        self.timer.Stop()
        wx.Exit()
 
    def OnTimer(self, event):
        global gaze_data_string
        print('OnTimer')
        self.SetTitle(gaze_data_string)
 
if __name__ == '__main__':
    app = wx.PySimpleApp()
    w = MyWindow(title='wxgr-ball')
    w.Center()
    w.Show()
    app.MainLoop()