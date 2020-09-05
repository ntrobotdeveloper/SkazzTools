import npyscreen
import json
import requests
import hashlib
import datetime


class ValidationButton(npyscreen.Button):
    def __init__(self, parent, source=None, dest=None, *args, **keywords):
        super(ValidationButton, self).__init__(parent, *args, **keywords)
        self.source = source
        self.dest = dest

    @staticmethod
    def converter(code):
        offset = datetime.timezone(datetime.timedelta(hours=3))
        result = hashlib.sha3_256(bytes(code + str(datetime.datetime.now(offset).hour), "utf-8"))
        return result.hexdigest()

    def whenToggled(self):
        if self.value:
            code = self.source.value
            url = 'https://skazztools-auth.herokuapp.com/auth?key=' + code
            try:
                r = requests.get(url)
                if r.status_code == 200:
                    hexhash = self.converter(code)
                    if hexhash != r.json()["hash"]:
                        response = "Error: incorrect code"
                    elif r.json()["active"]:
                        response = "Error: this code is on usage"
                    else:
                        response = "Success"
                        self.parent.parentApp.change_form("MAIN")
                else:
                    response = "Error: response code = " + str(r.status_code)
            except json.decoder.JSONDecodeError:
                response = "Error: incorrect response format"
            self.dest.value = response
        self.dest.display()
        self.value = False
        self.display()


class ValidationForm(npyscreen.ActionForm):
    def create(self):
        self.input_obj = self.add(npyscreen.TitleText, name="Input code:", value="")
        self.output_obj = self.add(npyscreen.TitleText, name="Log:", value="", rely=10, editable=False)
        self.button_obj = self.add(ValidationButton, name="Validate", source=self.input_obj, dest=self.output_obj,
                                   rely=4)

    def on_ok(self):
        self.parentApp.switchForm(None)
