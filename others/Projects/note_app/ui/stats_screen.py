from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform

import sqlite3
from kivy.core.window import Window

class StatsScreen(Screen):
    def __init__(self, **kwargs):
        super(StatsScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Statistics View
        self.stats_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height - 50))
        self.stats_grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.stats_grid.bind(minimum_height=self.stats_grid.setter('height'))
        self.stats_view.add_widget(self.stats_grid)
        self.layout.add_widget(self.stats_view)

        # Back Button
        self.back_button = Button(text="Back to Calendar", on_press=self.switch_to_calendar)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

        self.load_stats()

    def load_stats(self):
        conn = sqlite3.connect('notes.db')
        c = conn.cursor()
        c.execute("SELECT * FROM notes ORDER BY date DESC")
        notes = c.fetchall()
        conn.close()

        for note in notes:
            note_id, title, content, date, reminder_time, repeat, tags = note
            note_label = Label(text=f"{date}\n{title}\n{tags}", size_hint_y=None, height=100)
            self.stats_grid.add_widget(note_label)

    def switch_to_calendar(self, instance):
        self.manager.current = 'calendar'