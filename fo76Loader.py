from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from webbrowser import open as webopen
from shutil import copyfile
from time import sleep
import os, sys, json
from manageMods import *
from time import ctime

# Configure window
Config.set('graphics', 'width', '880')
Config.set('graphics', 'height', '846')
Config.set('graphics', 'resizable', False)

# Build app from .kv
Builder.load_file('loader.kv')

class Loader(TabbedPanel, FloatLayout):
    def __init__(self, **kwargs):
        super(Loader, self).__init__(**kwargs)

        # App variables
        self.setting_inputs = {}
        self.settings = self.loadSettings()
        self.game_mode = 0 if os.path.exists(self.settings['home_dir'] + r'\Fallout76Custom.ini') else 1

        # App directories
        self.loader_dir = os.path.dirname(os.path.abspath(__file__))
        self.img_dir = self.loader_dir + r'\Images\\'
        self.mods_dir = self.settings['game_dir'] + r'\Data'

        # Window
        self.ids.ADV.source = self.img_dir + r'adv_{}selected.png'.format('un' if self.game_mode == 1 else '')
        self.ids.NW.source = self.img_dir + r'nw_{}selected.png'.format('un' if self.game_mode == 0 else '')

        # Settings
        for key,value in self.settings.items():
            if type(value)==str:
                inp = TextInput(height=50, multiline=False, size_hint=(0.7, None), text=value)
                self.ids.settings.add_widget(Label(height=50, size_hint=(0.3, None), text=key))
                self.ids.settings.add_widget(inp)
                self.setting_inputs[key] = inp

        self.ids.settings.add_widget(Button(height=50, size_hint=(1, None), text='Save settings',on_press=self.updateSettings))

        # Mods
        self.mod_inputs = {}
        for mod in findModFiles(self.mods_dir):
            mod_checkbox = CheckBox(active=os.path.exists('Fallout76Custom.ini') and mod in open('Fallout76Custom.ini').read(),height=50, size_hint=(0.1,None))
            self.ids.modList.add_widget(mod_checkbox)
            self.ids.modList.add_widget(Label(size_hint=(0.9,None), height=50, text=mod))
            self.mod_inputs[mod] = mod_checkbox

        self.customIniButton = Button(id='createCustomIni', height=50, size_hint=(1, None), text='Create custom ini', on_press=self.createCustomIni)
        self.ids.modList.add_widget(self.customIniButton)

    def updateSettings(self,instance):
        for key,value in self.settings.items():
            if type(value)==str:
                self.settings[key] = self.setting_inputs[key].text
        self.saveSettings()
        
    def loadSettings(self):
        try:
            settings = json.loads(open('settings.json').read())
        except:
            settings = {
                'game_dir':'',
                'home_dir':''
            }
            self.saveSettings(settings)

        return settings

    def saveSettings(self, settings=None):
        with open('settings.json', 'w') as file:
            file.write(json.dumps(settings if settings else self.settings))

    def adventure(self):
        self.ids.ADV.source = self.img_dir + 'adv_selected.png'
        self.ids.NW.source = self.img_dir + 'nw_unselected.png'
        self.game_mode = 0

    def nw(self):
        self.ids.ADV.source = self.img_dir + 'adv_unselected.png'
        self.ids.NW.source = self.img_dir + 'nw_selected.png'
        self.game_mode = 1

    def updateFiles(self):
        if self.game_mode == 0:
            copyfile(self.loader_dir + r'\Fallout76Custom.ini', self.settings['home_dir'] + r'\Fallout76Custom.ini')
        else:
            os.remove(self.settings['home_dir'] + r'\Fallout76Custom.ini')

    def loadGame(self):
        self.updateFiles()
        webopen('bethesdanet://run/20')
        quit()

    def createCustomIni(self, instance):
        ignore_mods = []
        for name,obj in self.mod_inputs.items():
            if obj.active == False:
                ignore_mods.append(name)
            
            createIni(self.mods_dir, self.settings['home_dir'], ignore_mods)
            self.customIniButton.text = 'Create custom ini (last updated: {})'.format(ctime(os.path.getmtime(self.loader_dir + r'\Fallout76Custom.ini')))

class Setup(StackLayout):
    def __init__(self, **kwargs):
        super(Setup, self).__init__(**kwargs)

    def completeSetup(self):
        settings = {'game_dir':self.ids.game_dir.text, 'home_dir':self.ids.home_dir.text}
        with open('settings.json', 'w') as file:
            file.write(json.dumps(settings))
        App.get_running_app().stop()
        App().run()

class App(App):
    def build(self):
        self.icon = r'Images\icon.png'
        if os.path.exists('settings.json'):
            self.title = "Fallout 76 Loader"
            return Loader()
        else:
            self.title = "Setup"
            return Setup()

if __name__ == '__main__':
    App().run()
