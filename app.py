import urllib
import urllib2
import wx
import json


class MainWindow(wx.Frame):

    API_HOST = 'http://localhost:8888'
    USER_NAME = 'someuser'

    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, title=title)
        self.CreateStatusBar()

        # Setting up the menu.
        menu = wx.Menu()
        menu_reload = menu.Append(wx.ID_ANY, "Reload notes", " Reload notes")
        menu_add = menu.Append(wx.ID_ANY, "Add note", " Add note")
        menu_exit = menu.Append(wx.ID_ANY, "Exit", " Exit the program")

        # Creating the menu bar.
        menu_bar = wx.MenuBar()
        menu_bar.Append(menu, "Menu")
        self.SetMenuBar(menu_bar)

        # Events.
        self.Bind(wx.EVT_MENU, self.on_exit, menu_exit)
        self.Bind(wx.EVT_MENU, self.on_add, menu_add)
        self.Bind(wx.EVT_MENU, self.on_reload, menu_reload)

        self.notes = self.load_notes()

        self.panels = []
        self.sizer = wx.GridSizer(2)
        for note in self.notes:
            panel = self.create_note_panel(note)
            self.panels.append(panel)
            self.sizer.Add(panel, 0, wx.EXPAND)

        #Layout sizer
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.Show()

    def on_exit(self, e):
        self.Close(True)

    def create_note_panel(self, note):
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        title_input = wx.TextCtrl(panel, style=wx.TE_LINEWRAP, value=note.get('title'))
        text_input = wx.TextCtrl(panel, style=wx.TE_MULTILINE, size=wx.Size(200, 50), value=note.get('text'))
        update_button = wx.Button(panel, label='Update', name=note.get('note_id'))
        self.Bind(wx.EVT_BUTTON, self.on_update, update_button)

        sizer.Add(title_input, 0, wx.EXPAND)
        sizer.Add(text_input, 0, wx.EXPAND)
        sizer.Add(update_button, 1, wx.EXPAND)
        panel.SetSizer(sizer)
        return panel

    def on_update(self, e):
        title = e.EventObject.Parent.Children[0].GetValue()
        text = e.EventObject.Parent.Children[1].GetValue()
        note_id = e.EventObject.Parent.Children[2].GetName()
        note = self.post_note({'text': text, 'title': title, 'note_id': note_id})
        print(note)

    def on_add(self, e):
        note = self.post_note({'text': '', 'title': ''})
        print(note)

    def on_reload(self, e):
        self.Update()

    def do_post_request(self, uri, params):
        url = self.API_HOST + '/' + uri + '/' + self.USER_NAME + '/'
        data = urllib.urlencode(params)
        resp = urllib2.urlopen(urllib2.Request(url, data))
        return json.load(resp)

    def do_get_request(self, uri, params):
        url = self.API_HOST + '/' + uri + '/' + self.USER_NAME + '/' + urllib.urlencode(params)
        resp = urllib2.urlopen(url)
        return json.load(resp)

    def load_notes(self):
        data = self.do_get_request('notes', {})
        return data.get('notes')

    def post_note(self, note):
        data = self.do_post_request('note', note)
        return data.get('note')

app = wx.App(False)
frame = MainWindow(None, "Nevernote")
app.MainLoop()