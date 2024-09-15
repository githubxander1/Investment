from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, DictProperty, ListProperty
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from data_manager import DataManager

class StatScreen(Screen):
    events_by_date = ListProperty([])
    events_by_tag = ListProperty([])
    data_manager = DataManager()

    def on_pre_enter(self):
        self.update_statistics()

    def update_statistics(self):
        self.events_by_date = self.data_manager.get_events_by_date()
        self.events_by_tag = self.data_manager.get_events_by_tag()

        self.ids.events_by_date.clear_widgets()
        self.ids.events_by_tag.clear_widgets()

        for date, count in self.events_by_date.items():
            label = Label(text=f"{date}: {count}")
            self.ids.events_by_date.add_widget(label)

        for tag, count in self.events_by_tag.items():
            label = Label(text=f"{tag}: {count}")
            self.ids.events_by_tag.add_widget(label)
