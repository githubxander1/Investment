# statscreen.py
from tkinter import Button

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.metrics import dp

class StatScreen(Screen):
    stats_layout = ObjectProperty(None)

    def show_by_date(self):
        main_screen = self.manager.get_screen('main')
        stats_by_date = {}
        for date, events in main_screen.events_dict.items():
            stats_by_date[date] = len(events)

        self.ids.stats_layout.clear_widgets()
        for date, count in stats_by_date.items():
            btn = Button(
                text=f'Date: {date}, Events: {count}',
                on_release=lambda x, d=date: self.show_events_by_date(d),
                size_hint_y=None,
                height=dp(50)
            )
            self.ids.stats_layout.add_widget(btn)

    def show_events_by_date(self, date):
        main_screen = self.manager.get_screen('main')
        events = main_screen.events_dict.get(date, [])
        self.ids.stats_layout.clear_widgets()
        for event in events:
            btn = Button(
                text=f'Event: {event["title"]}, Tag: {event["tag"]}',
                on_release=lambda x, e=event: self.show_event_details(e),
                size_hint_y=None,
                height=dp(40)
            )
            self.ids.stats_layout.add_widget(btn)

    def show_by_tag(self):
        main_screen = self.manager.get_screen('main')
        stats_by_tag = {}
        for events in main_screen.events_dict.values():
            for event in events:
                tag = event.get('tag', '')
                if tag in stats_by_tag:
                    stats_by_tag[tag] += 1
                else:
                    stats_by_tag[tag] = 1

        self.ids.stats_layout.clear_widgets()
        for tag, count in stats_by_tag.items():
            btn = Button(
                text=f'Tag: {tag}, Count: {count}',
                on_release=lambda x, t=tag: self.show_events_by_tag(t),
                size_hint_y=None,
                height=dp(50)
            )
            self.ids.stats_layout.add_widget(btn)

    def show_events_by_tag(self, tag):
        main_screen = self.manager.get_screen('main')
        events_with_tag = []
        for events in main_screen.events_dict.values():
            for event in events:
                if event.get('tag') == tag:
                    events_with_tag.append(event)

        self.ids.stats_layout.clear_widgets()
        for event in events_with_tag:
            btn = Button(
                text=f'Event: {event["title"]}, Date: {event["date"]}',
                on_release=lambda x, e=event: self.show_event_details(e),
                size_hint_y=None,
                height=dp(40)
            )
            self.ids.stats_layout.add_widget(btn)

    def show_event_details(self, event):
        self.manager.current = 'edit'
        edit_screen = self.manager.get_screen('edit')
        edit_screen.set_date(event['date'], event['title'], event['description'], event['tag'])
