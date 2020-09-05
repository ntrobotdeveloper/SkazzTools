from threading import Thread
import time
from auto_modules.DiscordModule import DiscordModule
from text_interface.SkazzTools import TuiApp


class Control:
    def __init__(self):
        self.links_status = "OFF"
        self.nitro_status = "OFF"
        self.invites_status = "OFF"


class MAIN:
    def __init__(self):
        self.ctrl_obj = Control()

        self.invites_channels = self._get_channels("invites")
        self.links_channels = self._get_channels("links")
        self.token = self._get_token()

        self.tui = TuiApp()
        self.tui.control_external = self.ctrl_obj

        self.dm = DiscordModule(token=self.token)
        self.dm.ctrl_external = self.ctrl_obj
        self.dm.links_channels = self.links_channels
        self.dm.invites_channels = self.invites_channels

    @staticmethod
    def _get_channels(module):
        file_name = "program_files/" + module + ".txt"
        with open(file_name, "r") as f:
            file_data = f.readlines()
            channels = [int(x[:-1:]) for x in file_data]
        return channels

    @staticmethod
    def _get_token():
        file_name = "program_files/token.txt"
        with open(file_name, "r") as f:
            token = f.read()
        return token

    def info(self):
        while True:
            with open("program_files/info.txt", "r+", encoding="utf-8") as f:
                file_data = f.read()
                file_data += "               NITRO  LINKS  INVITES\n"
                file_data += "MAIN:          " + self.ctrl_obj.nitro_status + "    " + self.ctrl_obj.links_status + "    " + \
                             self.ctrl_obj.invites_status + "\n"
                file_data += "DiscordModule: " + self.dm.ctrl_external.nitro_status + "    " + self.dm.ctrl_external.links_status + "    " + \
                             self.dm.ctrl_external.invites_status + "\n"
                file_data += "SkazzTools:    " + self.tui.control_external.nitro_status + "    " + self.tui.control_external.links_status + "    " + \
                             self.tui.control_external.invites_status + "\n"
                file_data += "=" * 50 + "\n"
                f.seek(0)
                f.truncate(0)
                f.write(file_data)
            time.sleep(2)

    def RUN(self):
        thread_tui = Thread(target=self.tui.run)
        thread_discord = Thread(target=self.dm.run, daemon=True)
        thread_info = Thread(target=self.info, daemon=True)

        thread_tui.start()
        thread_discord.start()
        thread_info.start()

        thread_tui.join()


def main():
    loop = MAIN()
    loop.RUN()


if __name__ == "__main__":
    main()
