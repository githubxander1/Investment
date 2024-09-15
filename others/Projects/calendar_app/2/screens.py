from tkinter import Button

from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, DictProperty, ListProperty, ObjectProperty
from datetime import datetime

class MainScreen(Screen):
    current_date = StringProperty('')
    events_dict = DictProperty({})
    current_events = ListProperty([])

    def on_pre_enter(self):
        self.update_current_date()

    def update_current_date(self):
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        self.update_events(datetime.now())

    def update_events(self, date):
        # 获取当前日期的日程列表
        self.current_events = self.events_dict.get(date.strftime('%Y-%m-%d'), [])
        self.ids.date_label.text = 'Events for ' + date.strftime('%Y-%m-%d')
        self.ids.events_grid.clear_widgets()
        for event in self.current_events:
            btn = Button(
                text=event['title'],
                on_release=lambda x, e=event: self.on_event_button_click(x, e),
                size_hint_y=None,
                height=dp(40)
            )
            self.ids.events_grid.add_widget(btn)

    def on_event_button_click(self, instance, event):
        # 切换到编辑页面并填充现有的日程信息
        self.manager.current = 'edit'
        self.manager.get_screen('edit').set_date(self.current_date, event['title'], event['description'], event['tag'])

    def add_event(self):
        # 添加新事件并跳转到编辑页面
        self.manager.current = 'edit'
        self.manager.get_screen('edit').set_date(self.current_date, '', '', '')


class EditScreen(Screen):
    current_date = StringProperty('')
    current_title = StringProperty('')
    current_description = StringProperty('')
    current_tag = StringProperty('')
    current_events = ListProperty([])

    def set_date(self, date, title='', description='', tag=''):
        self.current_date = date
        self.current_title = title
        self.current_description = description
        self.current_tag = tag
        self.ids.event_title.text = title
        self.ids.event_description.text = description
        self.ids.event_tag.text = tag

        # 如果是按日期统计，则获取该日期的所有事件
        if date:
            main_screen = self.manager.get_screen('main')
            self.current_events = main_screen.events_dict.get(date, [])
            self.update_events()

    def update_events(self):
        self.ids.events_layout.clear_widgets()
        for event in self.current_events:
            btn = Button(
                text=f'{event["title"]}: {event["description"]}',
                on_release=lambda x, e=event: self.on_event_button_click(x, e),
                size_hint_y=None,
                height=dp(40)
            )
            self.ids.events_layout.add_widget(btn)

    def on_event_button_click(self, instance, event):
        # 切换到编辑页面并填充现有的日程信息
        self.set_date(self.current_date, event['title'], event['description'], event['tag'])

    def save_event(self):
        title = self.ids.event_title.text
        description = self.ids.event_description.text
        tag = self.ids.event_tag.text
        if title or description:
            main_screen = self.manager.get_screen('main')
            events_list = main_screen.events_dict.setdefault(main_screen.current_date, [])
            event_updated = False
            for i, event in enumerate(events_list):
                if event['title'] == self.current_title:
                    events_list[i] = {'title': title, 'description': description, 'tag': tag, 'date': self.current_date}
                    event_updated = True
                    break
            if not event_updated:
                events_list.append({'title': title, 'description': description, 'tag': tag, 'date': self.current_date})
            self.manager.current = 'main'
            main_screen.update_events(datetime.strptime(main_screen.current_date, '%Y-%m-%d'))

    def delete_event(self):
        # 删除事件
        main_screen = self.manager.get_screen('main')
        events_list = main_screen.events_dict.setdefault(main_screen.current_date, [])
        new_events_list = [event for event in events_list if event['title'] != self.current_title]
        main_screen.events_dict[main_screen.current_date] = new_events_list
        self.manager.current = 'main'
        main_screen.update_events(datetime.strptime(main_screen.current_date, '%Y-%m-%d'))


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

