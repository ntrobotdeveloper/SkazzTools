from discord.ext import commands
import webbrowser
import requests
import re


class Control:
    def __init__(self):
        self.links_status = "ON"
        self.nitro_status = "ON"
        self.invites_status = "ON"


class DiscordModule:
    def __init__(self, token=None):
        self.ctrl_external = None

        self.links_channels = None
        self.invites_channels = None

        self.token = token
        self.headers = {"authorization": self.token}

        self.invites_post_url = "https://discordapp.com/api/v6/invites/{}"
        self.nitro_post_url = "https://discordapp.com/api/v6/entitlements/gift-codes/{}/redeem"

        self.client = commands.Bot(command_prefix='*')
        @self.client.event
        async def on_message(ctx):
            invites = set()
            ninvites = set()
            if self.ctrl_external.invites_status == "ON":
                if ctx.channel.id in self.invites_channels:
                    reg_exp = re.compile('discord.gg\/(.{6})')
                    invites = set(re.findall(reg_exp, str(ctx.content)))
                    for embed in ctx.embeds:
                        invites.update(re.findall(reg_exp, str(embed.title)))
                        invites.update(re.findall(reg_exp, str(embed.description)))
                        invites.add((str(embed.url), ''))
                    for invite in invites:
                        requests.post(self.invites_post_url.format(invite), headers=self.headers)

            if self.ctrl_external.links_status == "ON":
                if ctx.channel.id in self.links_channels:
                    reg_exp = re.compile('(http.+?\/?)([) \n]|$)')
                    urls = set(re.findall(reg_exp, str(ctx.content)))
                    for embed in ctx.embeds:
                        urls.update(re.findall(reg_exp, str(embed.title)))
                        urls.update(re.findall(reg_exp, str(embed.description)))
                        urls.add((str(embed.url), ''))
                    for url in urls:
                        webbrowser.open_new_tab(url[0])

            if self.ctrl_external.nitro_status == "ON":
                reg_exp = re.compile('discord.gift\/(.+)')
                ninvites = set(re.findall(reg_exp, str(ctx.content)))
                for embed in ctx.embeds:
                    ninvites.update(re.findall(reg_exp, str(embed.title)))
                    ninvites.update(re.findall(reg_exp, str(embed.description)))
                    ninvites.add((str(embed.url), ''))
                for ninvite in ninvites:
                    requests.post(self.nitro_post_url.format(ninvite), headers=self.headers)

            if self.ctrl_external.nitro_status == "ON" or self.ctrl_external.links_status == "ON" or self.ctrl_external.invites_status == "ON" or True:
                with open("program_files/logs.txt", "r+", encoding="utf-8") as f:
                    file_data = f.read()
                    file_data += "links[" + self.ctrl_external.links_status + "] " + "invites[" + self.ctrl_external.invites_status + "] " + \
                                 "nitro[" + self.ctrl_external.nitro_status + "]" + "\n" + "content: " + ctx.content + "\n" + \
                                 "channel_id: " + str(ctx.channel.id) + "\n" + \
                                 "channels: " + str(self.links_channels) + "\n" + \
                                 "invites_code: " + str(invites) + "\n" + \
                                 "nitro_code: " + str(ninvites) + "\n"

                    file_data += "="*50 + "\n"
                    f.seek(0)
                    f.truncate(0)
                    f.write(file_data)

    def run(self):
        self.client.run(self.token, bot=False)


if __name__ == "__main__":
    dm = DiscordModule(token='mfa.IIH29n4Hw2K56scmF5mo_LEHrsVqJ2X5DhjntiyyvtpUIZt1y-XZ-_upMM59aFTxBYjeCyYuphvG7Owto5m4')
    dm.links_channels = [698173888928022551]
    dm.invites_channels = [698173888928022551]
    ctrl = Control()
    dm.ctrl_external = ctrl
    dm.run()


