import wx
import service
import urllib2
import os

from gui.preferenceView import PreferenceView
from gui import bitmapLoader

import gui.mainFrame
import service
import gui.globalEvents as GE


class PFHTMLExportPref ( PreferenceView):
    title = "Pyfa HTML Export Options"

    def populatePanel( self, panel ):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.HTMLExportSettings = service.settings.HTMLExportSettings.getInstance()

        self.dirtySettings = False

        mainSizer = wx.BoxSizer( wx.VERTICAL )

        self.stTitle = wx.StaticText( panel, wx.ID_ANY, self.title, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stTitle.Wrap( -1 )
        self.stTitle.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )

        mainSizer.Add( self.stTitle, 0, wx.ALL, 5 )

        
        self.exportEnabled = wx.CheckBox( panel, wx.ID_ANY, u"Enable HTML export", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.exportEnabled.SetValue(self.HTMLExportSettings.getEnabled())
        mainSizer.Add( self.exportEnabled, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticline2 = wx.StaticLine( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        mainSizer.Add( self.m_staticline2, 0, wx.EXPAND, 5 )

        self.stPTitle = wx.StaticText( panel, wx.ID_ANY, "HTML export path", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stPTitle.Wrap( -1 )
        self.stPTitle.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        mainSizer.Add( self.stPTitle, 0, wx.ALL, 5 )


        self.stPSetPath = wx.StaticText( panel, wx.ID_ANY, u"Path:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stPSetPath.Wrap( -1 )

        self.PathTextCtrl = wx.TextCtrl( panel, wx.ID_ANY, self.HTMLExportSettings.getPath(), wx.DefaultPosition, wx.DefaultSize, 0)
        self.PathTextCtrl.Disable()
        
        self.fileSelectDialog = wx.FileDialog(None, "Save Fitting As...", wildcard = "EvE IGB HTML fitting file (*.html)|*.html", style = wx.FD_SAVE)
        self.fileSelectDialog.SetPath(self.HTMLExportSettings.getPath())
        self.fileSelectDialog.SetFilename(os.path.basename(self.HTMLExportSettings.getPath()));
        self.fileSelectButton = wx.Button(panel, -1, "Set export destination", pos=(0,0)) 
        self.fileSelectButton.Bind(wx.EVT_BUTTON, self.selectHTMLExportFilePath)
        
        mainSizer.Add( self.stPSetPath, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        mainSizer.Add(self.PathTextCtrl, 0, wx.ALL|wx.EXPAND, 5)  
        mainSizer.Add( self.fileSelectButton, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        self.btnApply = wx.Button( panel, wx.ID_ANY, u"Apply", wx.DefaultPosition, wx.DefaultSize, 0 )
        btnSizer = wx.BoxSizer( wx.HORIZONTAL )
        btnSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        btnSizer.Add( self.btnApply, 0, wx.ALL, 5 )

        mainSizer.Add(btnSizer, 0, wx.EXPAND,5)
        self.exportEnabled.Bind(wx.EVT_CHECKBOX, self.OnExportEnabledChange)

        self.btnApply.Bind(wx.EVT_BUTTON, self.OnBtnApply)
        self.UpdateApplyButtonState()
        panel.SetSizer( mainSizer )
        panel.Layout()

    def selectHTMLExportFilePath(self, event):
        if self.fileSelectDialog.ShowModal() == wx.ID_OK:
            self.exportFilePath = self.fileSelectDialog.GetPath()
            self.dirtySettings = True
            self.PathTextCtrl.SetValue(self.exportFilePath)
            self.UpdateApplyButtonState()

    def OnExportEnabledChange(self, event):
        self.dirtySettings = True
        self.UpdateApplyButtonState()

    def OnBtnApply(self, event):
        self.dirtySettings = False
        self.UpdateApplyButtonState()
        self.SaveSettings()

    def SaveSettings(self):
        self.HTMLExportSettings.setPath(self.exportFilePath)
        self.HTMLExportSettings.setEnabled(self.exportEnabled.GetValue())

    def UpdateApplyButtonState(self):
        if self.dirtySettings:
            self.btnApply.Enable()
        else:
            self.btnApply.Disable()

    def getImage(self):
        return bitmapLoader.getBitmap("pyfa64", "icons")

PFHTMLExportPref.register()