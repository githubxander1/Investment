from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, DictProperty, ListProperty
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from data_manager import DataManager

class DayView(Screen):
    selected_date = StringProperty('')
    events = ListProperty([])
    data_manager = DataManager()

    def on_pre_enter(self):
        self.update_day_view(self.selected_date)

    def update_day_view(self, selected_date):
        self.selected_date = selected_date
        self.events = self.data_manager.get_events_for_date(selected_date)

        self.ids.events.clear_widgets()

        for event in self.events:
            label = Label(text=f"Title: {event['title']}, Content: {event['content']}, Tags: {event['tags']}")
            self.ids.events.add_widget(label)
