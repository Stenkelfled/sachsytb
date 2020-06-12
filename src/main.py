
import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.popup import Popup

import os

if 'android' in kivy.utils.platform:
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path
elif 'linux' in kivy.utils.platform:
    from pathlib import Path

kivy.require('1.10.1')


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    start_path = StringProperty('')


class FileWin(FloatLayout):
    text_input = ObjectProperty(None)
    os_name = StringProperty(kivy.utils.platform)
    f_name = StringProperty("<no file opened>")

    def dismiss_popup(self):
        self._popup.dismiss()

    def load_file(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.text_input.text = stream.read()
        self.f_name = filename[0]

        self.dismiss_popup()

    def load_dialog(self):
        start_path = os.path.dirname(os.path.abspath(__file__))
        if 'android' in kivy.utils.platform:
            start_path = primary_external_storage_path()
        elif 'linux' in kivy.utils.platform:
            start_path = str(Path.home())
        content = LoadDialog(load=self.load_file, cancel=self.dismiss_popup, start_path=start_path)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()


class SachsytbApp(App):

    def build(self):
        if 'android' in kivy.utils.platform:
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
        return FileWin()


if __name__ == "__main__":
    SachsytbApp().run()
