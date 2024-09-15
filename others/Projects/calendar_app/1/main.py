# app.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.lang import Builder

from screens.mainscreen import MainScreen
from screens.editscreen import EditScreen
from screens.statscreen import StatScreen

Builder.load_file('kv/mainscreen.kv')

class MyApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='main'))
        self.sm.add_widget(EditScreen(name='edit'))
        self.sm.add_widget(StatScreen(name='stat'))
        return self.sm

if __name__ == '__main__':
    MyApp().run()
