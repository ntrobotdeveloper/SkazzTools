import npyscreen
import curses
from text_interface.TitleTools import title_tools


class LinksForm(npyscreen.FormBaseNew):
    def create(self):
        y, x = self.useable_space()
        self.control_external = self.parentApp.control_external
        self.add(npyscreen.MultiLineEdit, value=title_tools, max_height=7, rely=2, editable=False)
        self.add(npyscreen.TitleText, name="Choose option:", value="", editable=False)
        self.status = self.add(npyscreen.TitleText, name="1. Status:", value="OFF", editable=False)
        self.add(npyscreen.TitleText, name="2. Edit channels", value="", editable=False)
        self.add(npyscreen.TitleText, name="0. Return", value="", editable=False)
        self.add(npyscreen.Button, name="", rely=y-3, relx=x-6, cursor_color=curses.COLOR_GREEN)

        self.add_handlers({"1": self.toggle,
                           "2": self.switch_screen_EDIT_LINKS,
                           "0": self.switch_screen_MAIN})

    def toggle(self, *args, **kwargs):
        if self.status.value == "ON":
            self.status.value = "OFF"
            self.parentApp.main_form.links_title.value = "OFF"
            self.control_external.links_status = "OFF"
        elif self.status.value == "OFF":
            self.status.value = "ON"
            self.parentApp.main_form.links_title.value = "ON"
            self.control_external.links_status = "ON"
        self.status.display()

    def switch_screen_EDIT_LINKS(self, *args, **kwargs):
        self.parentApp.change_form("EDIT_LINKS")

    def switch_screen_MAIN(self, *args, **kwargs):
        self.parentApp.change_form("MAIN")
