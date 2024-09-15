from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, DictProperty, ListProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from data_manager import DataManager

class SearchScreen(Screen):
    search_input = ObjectProperty(None)
    search_results = ListProperty([])
    data_manager = DataManager()

    def search_events(self):
        keyword = self.search_input.text
        self.search_results = self.data_manager.search_events(keyword)

        self.ids.search_results.clear_widgets()

        for event in self.search_results:
            label = Label(text=f"Date: {event['date']}, Title: {event['title']}, Content: {event['content']}, Tags: {event['tags']}")
            self.ids.search_results.add_widget(label)
