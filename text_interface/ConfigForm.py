import npyscreen
import curses
from text_interface.TitleTools import title_tools


class InputBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.Textfield


class ConfigButton(npyscreen.Button):
    def __init__(self, parent, target=None, source=None, *args, ** keywords):
        super(ConfigButton, self).__init__(parent, *args, ** keywords)
        self.target = target
        self.source = source

    def whenToggled(self):
        if self.target and self.source:
            if self.value:
                self.target.value = self.source.value
                with open("program_files/token.txt", "w") as f:
                    f.write(self.source.value)
                self.value = False
            self.source.value = ""
            self.source.hidden = True
            self.source.set_editable(False)
            self.hidden = True
            self.set_editable(False)
            self.source.display()
            self.display()


class ConfigForm(npyscreen.FormBaseNew):
    def create(self):
        y, x = self.useable_space()
        try:
            with open("program_files/token.txt", "r") as f:
                data = f.read().split()[0]
        except FileNotFoundError:
            with open("program_files/token.txt", 'w'):
                data = ""
        self.add(npyscreen.MultiLineEdit, value=title_tools, max_height=7, rely=2, editable=False)
        self.add(npyscreen.TitleText, name="Choose option:", value="", editable=False)
        self.token = self.add(npyscreen.TitleText, name="1. Token: ", value=data, editable=False)
        self.add(npyscreen.TitleText, name="0. Return", value="", editable=False, rely=17)
        self.inputbox_obj = self.add(InputBox, name='Input token', max_height=3, rely=12)
        self.button_obj = self.add(ConfigButton, name='Accept', target=self.token, source=self.inputbox_obj, rely=15)
        self.add(npyscreen.Button, name="", rely=y-3, relx=x-6, cursor_color=curses.COLOR_GREEN)

        self.inputbox_obj.hidden = True
        self.inputbox_obj.set_editable(False)
        self.button_obj.hidden = True
        self.button_obj.set_editable(False)

        self.add_handlers({"1": self.set_token,
                           "0": self.switch_screen_MAIN,})

    def set_token(self, *args, **kwargs):
        if self.inputbox_obj.hidden:
            self.inputbox_obj.hidden = False
            self.inputbox_obj.set_editable(True)
            self.button_obj.hidden = False
            self.button_obj.set_editable(True)
        else:
            self.inputbox_obj.hidden = True
            self.inputbox_obj.set_editable(False)
            self.button_obj.hidden = True
            self.button_obj.set_editable(False)
        self.display()

    def switch_screen_MAIN(self, *args, **kwargs):
        self.parentApp.change_form("MAIN")
