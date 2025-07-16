import wx

from utils.parse.interact_video import InteractVideoInfo

from gui.component.webview import Webview
from gui.component.window.frame import Frame

class GraphWindow(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, f"Graph Viewer")

        self.init_UI()

        self.SetSize(self.FromDIP((960, 540)))

        self.Bind_EVT()

        self.init_utils()

        self.CenterOnParent()

    def init_UI(self):
        self.webview = Webview(self)

        self.webview.browser.SetPage(self.webview.get_page("graph.html"), "")
        self.webview.browser.EnableAccessToDevTools(True)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.webview.browser, 1, wx.ALL | wx.EXPAND)

        self.SetSizerAndFit(vbox)

    def Bind_EVT(self):
        self.webview.browser.Bind(wx.html2.EVT_WEBVIEW_SCRIPT_MESSAGE_RECEIVED, self.onMessageEVT)

        self.webview.browser.Bind(wx.html2.EVT_WEBVIEW_LOADED, self.onLoadedEVT)

    def init_utils(self):
        self.webview.browser.AddScriptMessageHandler("MainApplication")

    def onLoadedEVT(self, event):
        self.webview.browser.RunScriptAsync(f"initGraph('{self.get_graphviz_dot()}'); setTitle('{InteractVideoInfo.title}');")

    def onMessageEVT(self, event):
        msg = event.GetString()

        if msg == "fullscreen":
            self.Maximize(not self.IsMaximized())

    def get_graphviz_dot(self):
        fontname = self.GetFont().GetFaceName()

        dot = [
            "rankdir=LR;",
            f'node [shape = box, fontname = "{fontname}", width=1.5, height = 0.5];',
            f'edge [fontname="{fontname}"];'
        ]

        node_name = {}

        for node in InteractVideoInfo.node_list:
            node_name[node.cid] = node.title

            for option in node.options:
                if option.show:
                    label = f' [label = "{option.name}"];'
                else:
                    label = ''

                dot.append(f'"{node.cid}" -> "{option.target_node_cid}"{label}')

        result = "".join(dot)

        for key, value in node_name.items():
            result = result.replace(str(key), value)

        return "digraph {" + result + "}"