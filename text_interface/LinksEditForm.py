import npyscreen
import curses
import os
from text_interface.TitleTools import title_tools


class LinksEditButton(npyscreen.Button):
    def __init__(self, parent, data=None, source=None, out=None, *args, ** keywords):
        super(LinksEditButton, self).__init__(parent, *args, ** keywords)
        self.data = data
        self.source = source
        self.out = out

    def whenToggled(self):
        if self.source:
            if self.value:
                if self.source.name == "Add one":
                    with open("program_files/links.txt", "r+") as f:
                        file_data = f.readlines()
                        file_data.append(self.source.value + '\n')
                        f.seek(0)
                        f.truncate(0)
                        for elem in file_data:
                            f.write(elem)
                        self.data = [str(i) + '. ' + x for i, x in enumerate(file_data)]
                else:
                    with open("program_files/links.txt", "r+") as f:
                        file_data = f.readlines()
                        try:
                            file_data.pop(int(self.source.value))
                        except (ValueError, IndexError):
                            pass
                        f.seek(0)
                        f.truncate(0)
                        for elem in file_data:
                            f.write(elem)
                        self.data = [str(i) + '. ' + x for i, x in enumerate(file_data)]
            self.out.update_value(self.data)
            self.value = False
            self.source.value = ""
            self.source.hidden = True
            self.source.set_editable(False)
            self.hidden = True
            self.set_editable(False)
            self.parent.display()


class InputBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.Textfield


class OutputBox(npyscreen.BoxTitle):
    def update_value(self, data):
        self.values = data
        self.display()


class LinksEditForm(npyscreen.FormBaseNew):
    def create(self):
        y, x = self.useable_space()
        try:
            with open("program_files/links.txt", "r") as f:
                file_data = f.readlines()
                self.link_list = [str(i)+'. ' + x for i, x in enumerate(file_data)]
        except FileNotFoundError:
            with open("program_files/links.txt", 'w'):
                self.link_list = []
        self.add(npyscreen.MultiLineEdit, value=title_tools, max_height=7, rely=2, editable=False)
        self.add(npyscreen.TitleText, name="Choose option:", value="", editable=False)
        self.add(npyscreen.TitleText, name="1. List", value="", editable=False)
        self.add(npyscreen.TitleText, name="2. Add one", value="", editable=False)
        self.add(npyscreen.TitleText, name="3. Clear one", value="", editable=False)
        self.add(npyscreen.TitleText, name="4. Clear all", value="", editable=False)
        self.add(npyscreen.TitleText, name="0. Return", value="", editable=False)
        self.inputbox_obj = self.add(InputBox, name="", rely=17, max_height=3)
        self.outputbox_obj = self.add(OutputBox, name="List", rely=24,)
        self.button_obj = self.add(LinksEditButton, name="Accept", rely=20, data=self.link_list,
                                   source=self.inputbox_obj, out=self.outputbox_obj)
        self.add(npyscreen.Button, name="", rely=y-3, relx=x-6, cursor_color=curses.COLOR_GREEN)

        self.inputbox_obj.hidden = True
        self.inputbox_obj.set_editable(False)
        self.button_obj.hidden = True
        self.button_obj.set_editable(False)
        self.outputbox_obj.hidden = True
        self.outputbox_obj.set_editable(False)

        self.add_handlers({"1": self.show_list,
                           "2": self.add_one,
                           "3": self.clear_one,
                           "4": self.clear_all,
                           "0": self.switch_screen_MAIN})

    def show_list(self, *args, **kwargs):
        if self.outputbox_obj.hidden:
            with open("program_files/links.txt", "r") as f:
                file_data = f.readlines()
                self.link_list = [str(i)+'. ' + x for i, x in enumerate(file_data)]
            self.outputbox_obj.hidden = False
            self.outputbox_obj.update_value(self.link_list)
        else:
            self.outputbox_obj.hidden = True
            self.outputbox_obj.update_value(self.link_list)

    def add_one(self, *args, **kwargs):
        self.inputbox_obj.name = "Add one"
        self.inputbox_obj.hidden = False
        self.inputbox_obj.set_editable(True)
        self.button_obj.hidden = False
        self.button_obj.set_editable(True)
        self.display()

    def clear_one(self, *args, **kwargs):
        self.inputbox_obj.name = "Clear one"
        self.inputbox_obj.hidden = False
        self.inputbox_obj.max_width = 10
        self.inputbox_obj.set_editable(True)
        self.button_obj.hidden = False
        self.button_obj.set_editable(True)
        self.display()

    def clear_all(self, *args, **kwargs):
        with open("program_files/links.txt", "r") as f:
            f.seek(0)
            f.truncate(0)
            self.link_list.clear()
        self.outputbox_obj.display()

    def switch_screen_MAIN(self, *args, **kwargs):
        self.parentApp.change_form("LINKS")
