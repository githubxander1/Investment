# editscreen.py
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ListProperty
from kivy.metrics import dp
from kivy.uix.button import Button

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
