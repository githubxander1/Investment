from datetime import datetime, timedelta
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.properties import StringProperty, DictProperty, BooleanProperty, ListProperty

# 加载KV文件中的定义
Builder.load_file('calendar.kv')


class CalendarApp(App):
    def build(self):
        self.title = 'Calendar App'
        self.sm = ScreenManager()

        # 初始化屏幕
        self.main_screen = MainScreen(name='main')
        self.edit_screen = EditScreen(name='edit')
        self.stat_screen = StatScreen(name='stat')

        # 将屏幕添加到屏幕管理器中
        self.sm.add_widget(self.main_screen)
        self.sm.add_widget(self.edit_screen)
        self.sm.add_widget(self.stat_screen)

        # 生成当前月份的日历并默认选中今天
        self.generate_calendar(datetime.now().month, datetime.now().year)

        return self.sm

    def generate_calendar(self, month, year):
        # 清空现有日历
        self.main_screen.ids.calendar_grid.clear_widgets()

        # 获取该月的第一天和最后一天
        first_day_of_month = datetime(year, month, 1)
        last_day_of_month = (first_day_of_month + timedelta(days=34)).replace(day=1) - timedelta(days=1)

        # 添加星期标题
        for day in "Mon Tue Wed Thu Fri Sat Sun".split():
            self.main_screen.ids.calendar_grid.add_widget(Button(
                text=day,
                background_color=(0.8, 0.8, 0.8, 1),
                disabled=True,
                size_hint_y=None,
                height=dp(30)
            ))

        # 计算第一个显示的星期一
        days_offset = (first_day_of_month.weekday() + 1) % 7
        if days_offset == 0:
            days_offset = 7

        # 添加空白格子直到第一个星期一
        for _ in range(days_offset):
            self.main_screen.ids.calendar_grid.add_widget(Button(
                text='',
                background_color=(0.8, 0.8, 0.8, 1),
                disabled=True,
                size_hint_y=None,
                height=dp(30)
            ))

        # 添加本月的所有日期
        current_date = first_day_of_month
        while current_date <= last_day_of_month:
            btn = Button(
                text=str(current_date.day),
                on_release=lambda x, d=current_date: self.on_date_button_click(x, d),
                size_hint_y=None,
                height=dp(30)
            )
            if current_date == datetime.now().date():
                btn.background_color = (0.5, 0.5, 1, 1)
            self.main_screen.ids.calendar_grid.add_widget(btn)
            current_date += timedelta(days=1)

    def on_date_button_click(self, instance, date):
        # 获取点击的日期
        self.main_screen.current_date = date.strftime('%Y-%m-%d')
        self.main_screen.update_events(date)
        # 高亮显示点击的日期
        for child in self.main_screen.ids.calendar_grid.children:
            if isinstance(child, Button) and child.text.isdigit():
                if int(child.text) == date.day:
                    child.background_color = (0.5, 0.5, 1, 1)
                else:
                    child.background_color = (1, 1, 1, 1)


class MainScreen(Screen):
    current_date = StringProperty('')
    events_dict = DictProperty({})
    current_events = ListProperty([])

    def update_events(self, date):
        # 获取当前日期的日程列表
        self.current_events = self.events_dict.get(date.strftime('%Y-%m-%d'), [])
        self.ids.date_label.text = 'Events for ' + date.strftime('%Y-%m-%d')
        self.ids.events_grid.clear_widgets()
        for event in self.current_events:
            self.ids.events_grid.add_widget(Button(
                text=event['title'],
                on_release=lambda x, e=event: self.on_event_button_click(x, e),
                size_hint_y=None,
                height=dp(40)
            ))

    def on_event_button_click(self, instance, event):
        # 切换到编辑页面并填充现有的日程信息
        self.manager.current = 'edit'
        self.manager.get_screen('edit').set_date(self.current_date, event['title'], event['description'])

    def add_event(self):
        # 切换到编辑页面
        self.manager.current = 'edit'
        self.manager.get_screen('edit').set_date(self.current_date, '', '')


class EditScreen(Screen):
    current_date = StringProperty('')
    current_title = StringProperty('')
    current_description = StringProperty('')

    def set_date(self, date, title='', description=''):
        self.current_date = date
        self.current_title = title
        self.current_description = description
        self.ids.event_title.text = title
        self.ids.event_description.text = description

    def save_event(self):
        # 假设这里有一个函数将事件保存到数据库或其他地方
        # 这里只是一个简单的例子
        title = self.ids.event_title.text
        description = self.ids.event_description.text
        if title and description:
            # 更新主界面显示的新事件
            main_screen = self.manager.get_screen('main')
            events_list = main_screen.events_dict.setdefault(main_screen.current_date, [])
            if self.current_title:
                # 查找并更新现有的事件
                for i, event in enumerate(events_list):
                    if event['title'] == self.current_title:
                        events_list[i] = {'title': title, 'description': description}
                        break
            else:
                # 添加新的事件
                events_list.append({'title': title, 'description': description})
            main_screen.update_events(datetime.strptime(main_screen.current_date, '%Y-%m-%d'))
            self.manager.current = 'main'

    def delete_event(self):
        # 删除当前日程
        main_screen = self.manager.get_screen('main')
        events_list = main_screen.events_dict.get(main_screen.current_date, [])
        if self.current_title:
            events_list[:] = [event for event in events_list if event['title'] != self.current_title]
            main_screen.update_events(datetime.strptime(main_screen.current_date, '%Y-%m-%d'))
            self.manager.current = 'main'


class StatScreen(Screen):
    pass


if __name__ == '__main__':
    CalendarApp().run()