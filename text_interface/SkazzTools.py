import npyscreen
import random
import os

from text_interface.ValidationForm import ValidationForm
from text_interface.MainFrom import MainForm
from text_interface.NitroForm import NitroForm
from text_interface.LinksForm import LinksForm
from text_interface.LinksEditForm import LinksEditForm
from text_interface.InvitesForm import InvitesForm
from text_interface.InvitesEditForm import InvitesEditForm
from text_interface.ConfigForm import ConfigForm


class TuiApp(npyscreen.NPSAppManaged):
    STARTING_FORM = "VALIDATION"

    def __init__(self):
        super().__init__()
        self.control_external = None

    def onStart(self):
        os.system("mode con cols=170 lines=45")
        self.addForm("VALIDATION", ValidationForm, name="Validation", color="IMPORTANT")
        self.main_form = self.addForm("MAIN", MainForm, name="Main", color="IMPORTANT", )
        self.nitro_form = self.addForm("NITRO", NitroForm, name="Nitro", color="IMPORTANT", )
        self.links_form = self.addForm("LINKS", LinksForm, name="Links", color="IMPORTANT", )
        self.addForm("EDIT_LINKS", LinksEditForm, name="Edit Links", color="IMPORTANT", )
        self.invites_form = self.addForm("INVITES", InvitesForm, name="Invites", color="IMPORTANT", )
        self.addForm("EDIT_INVITES", InvitesEditForm, name="Edit Invites", color="IMPORTANT", )
        self.addForm("CONFIG", ConfigForm, name="Config", color="IMPORTANT", )

    def onCleanExit(self):
        phrases = ["Не уходи, прошу тебя!", "Надеюсь ты найдешь свою любовь!", "Всегда помни, что я твоя Тулза, а ты мой Сказз",
                   "Девочка сосочка почему одна, щас будет 2"]
        #npyscreen.notify_wait(random.choice(phrases))
        npyscreen.notify_wait("До свидания! Буду ждать!")

    def change_form(self, name):
        self.switchForm(name)
        self.resetHistory()


def main():
    TA = TuiApp()
    TA.run()


if __name__ == '__main__':
    main()
