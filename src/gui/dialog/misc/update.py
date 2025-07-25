import wx

from utils.config import Config

from gui.component.text_ctrl.text_ctrl import TextCtrl
from gui.component.window.dialog import Dialog

class UpdateDialog(Dialog):
    def __init__(self, parent, info: dict):
        self.info = info

        Dialog.__init__(self, parent, "检查更新")

        self.init_UI()

        self.CenterOnParent()

        self.showUpdateInfo()

        wx.Bell()

    def init_UI(self):
        font: wx.Font = self.GetFont()
        font.SetFractionalPointSize(int(font.GetFractionalPointSize() + 5))

        title_lab = wx.StaticText(self, -1, "有新的更新可用")
        title_lab.SetFont(font)

        self.detail_lab = wx.StaticText(self, -1, "Version 1.00，发布于 1970/1/1，大小 0MB")

        top_border = wx.StaticLine(self, -1, style = wx.HORIZONTAL)

        font: wx.Font = self.GetFont()
        font.SetFractionalPointSize(int(font.GetFractionalPointSize() + 1))

        self.changelog = TextCtrl(self, -1, size = self.FromDIP((600, 320)), style = wx.TE_MULTILINE | wx.TE_READONLY)
        self.changelog.SetFont(font)

        bottom_border = wx.StaticLine(self, -1, style = wx.HORIZONTAL)

        self.update_btn = wx.Button(self, wx.ID_OK, "更新", size = self.FromDIP((90, 28)))
        self.ignore_btn = wx.Button(self, wx.ID_CANCEL, "忽略", size = self.FromDIP((90, 28)))

        bottom_hbox = wx.BoxSizer(wx.HORIZONTAL)
        bottom_hbox.AddStretchSpacer()
        bottom_hbox.Add(self.update_btn, 0, wx.ALL, self.FromDIP(6))
        bottom_hbox.Add(self.ignore_btn, 0, wx.ALL & (~wx.LEFT), self.FromDIP(6))

        update_vbox = wx.BoxSizer(wx.VERTICAL)
        update_vbox.Add(title_lab, 0, wx.ALL, self.FromDIP(6))
        update_vbox.Add(self.detail_lab, 0, wx.ALL & (~wx.TOP), self.FromDIP(6))
        update_vbox.Add(top_border, 0, wx.EXPAND)
        update_vbox.Add(self.changelog, 1, wx.ALL | wx.EXPAND, self.FromDIP(6))
        update_vbox.Add(bottom_border, 0, wx.EXPAND)
        update_vbox.Add(bottom_hbox, 0, wx.EXPAND, 0)

        self.SetSizerAndFit(update_vbox)

        self.set_dark_mode()
    
    def onOKEVT(self):
        import webbrowser

        webbrowser.open(self.info["url"])

        self.Hide()

    def showUpdateInfo(self):
        self.SetTitle("检查更新")

        self.changelog.SetValue(self.info["changelog"])

        self.detail_lab.SetLabel(f"Version {self.info['version']}，发布于 {self.info['date']}，大小 {self.info['size']}")

        self.update_btn.Show(True)

        self.Layout()

    def set_dark_mode(self):
        if not Config.Sys.dark_mode:
            self.SetBackgroundColour("white")
            self.changelog.SetBackgroundColour("white")