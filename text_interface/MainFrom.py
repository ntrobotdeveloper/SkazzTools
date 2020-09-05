import npyscreen
import curses
from text_interface.TitleTools import title_tools


class MainForm(npyscreen.FormBaseNew):
    def create(self):
        y, x = self.useable_space()
        self.add(npyscreen.MultiLineEdit, value=title_tools, max_height=7, rely=2, editable=False)
        self.add(npyscreen.TitleText, name="Choose option:", editable=False)
        self.nitro_title = self.add(npyscreen.TitleText, name="1. Nitro", value="OFF", editable=False)
        self.links_title = self.add(npyscreen.TitleText, name="2. Links", value="OFF", editable=False)
        self.invites_title = self.add(npyscreen.TitleText, name="3. Invites", value="OFF", editable=False)
        self.add(npyscreen.TitleText, name="4. Config", editable=False)
        self.add(npyscreen.TitleText, name="0. Exit", editable=False)
        self.add(npyscreen.Button, name="", rely=y-3, relx=x-6, cursor_color=curses.COLOR_GREEN)

        self.add_handlers({"1": self.switch_screen_NITRO,
                           "2": self.switch_screen_LINKS,
                           "3": self.switch_screen_INVITES,
                           "4": self.switch_screen_CONFIG,
                           "0": self.close_app})

    def switch_screen_NITRO(self, *args, **kwargs):
        self.parentApp.change_form("NITRO")

    def switch_screen_LINKS(self, *args, **kwargs):
        self.parentApp.change_form("LINKS")

    def switch_screen_INVITES(self, *args, **kwargs):
        self.parentApp.change_form("INVITES")

    def switch_screen_CONFIG(self, *args, **kwargs):
        self.parentApp.change_form("CONFIG")

    def close_app(self, *args, **kwargs):
        self.parentApp.switchForm(None)

    def on_ok(self):
        self.parentApp.switchForm(None)