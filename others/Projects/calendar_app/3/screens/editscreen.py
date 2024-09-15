# screens/editscreen.py

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.metrics import dp
from data_manager import DataManager

class EditScreen(Screen):
    def __init__(self, **kwargs):
        super(EditScreen, self).__init__(**kwargs)
        self.data_manager = DataManager()

    def save_event(self, date, title, description, tags):
        self.data_manager.save_event(date, title, description, tags)
        print("Event saved successfully")
        # self.manager.current = 'main'

    def set_date(self, date, title, description, tags):
        self.ids.date_input.text = date
        self.ids.title_input.text = title
        self.ids.content_input.text = description
        self.ids.tags_input.text = tags
