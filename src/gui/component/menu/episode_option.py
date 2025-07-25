import wx

from utils.config import Config

from utils.common.enums import EpisodeDisplayType

from gui.id import ID

class EpisodeOptionMenu(wx.Menu):
    def __init__(self):
        wx.Menu.__init__(self)

        single_menuitem = wx.MenuItem(self, ID.EPISODE_SINGLE_MENU, "显示单个视频", kind = wx.ITEM_RADIO)
        in_section_menuitem = wx.MenuItem(self, ID.EPISODE_IN_SECTION_MENU, "显示视频所在的列表", kind = wx.ITEM_RADIO)
        all_section_menuitem = wx.MenuItem(self, ID.EPISODE_ALL_SECTIONS_MENU, "显示全部相关视频", kind = wx.ITEM_RADIO)
        show_episode_full_name = wx.MenuItem(self, ID.EPISODE_FULL_NAME_MENU, "显示完整剧集名称", kind = wx.ITEM_CHECK)

        self.Append(wx.NewIdRef(), "剧集列表显示设置")
        self.AppendSeparator()
        self.Append(single_menuitem)
        self.Append(in_section_menuitem)
        self.Append(all_section_menuitem)
        self.AppendSeparator()
        self.Append(show_episode_full_name)

        match EpisodeDisplayType(Config.Misc.episode_display_mode):
            case EpisodeDisplayType.Single:
                single_menuitem.Check(True)

            case EpisodeDisplayType.In_Section:
                in_section_menuitem.Check(True)

            case EpisodeDisplayType.All:
                all_section_menuitem.Check(True)

        show_episode_full_name.Check(Config.Misc.show_episode_full_name)