import npyscreen
import curses
from text_interface.TitleTools import title_tools

class NitroForm(npyscreen.FormBaseNew):
    def create(self):
        self.control_external = self.parentApp.control_external
        y, x = self.useable_space()
        self.add(npyscreen.MultiLineEdit, value=title_tools, max_height=7, rely=2, editable=False)
        self.add(npyscreen.TitleText, name="Choose option:", value="", editable=False)
        self.status = self.add(npyscreen.TitleText, name="1. Status:", value="OFF", editable=False)
        self.add(npyscreen.TitleText, name="0. Return", value="", editable=False)
        self.add(npyscreen.Button, name="", rely=y-3, relx=x-6, cursor_color=curses.COLOR_GREEN)

        self.add_handlers({"1": self.toggle,
                           "0": self.switch_screen_MAIN})

    def toggle(self, *args, **kwargs):
        if self.status.value == "ON":
            self.status.value = "OFF"
            self.parentApp.main_form.nitro_title.value = "OFF"
            self.control_external.nitro_status = "OFF"
        elif self.status.value == "OFF":
            self.status.value = "ON"
            self.parentApp.main_form.nitro_title.value = "ON"
            self.control_external.nitro_status = "ON"
        self.status.display()

    def switch_screen_MAIN(self, *args, **kwargs):
        self.parentApp.change_form("MAIN")
