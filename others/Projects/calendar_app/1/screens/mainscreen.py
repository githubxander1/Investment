# mainscreen.py
from tkinter import Button

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, DictProperty, ListProperty
from kivy.metrics import dp
from datetime import datetime, timedelta

class MainScreen(Screen):
    current_date = StringProperty('')
    events_dict = DictProperty({})
    current_events = ListProperty([])

    def on_pre_enter(self):
        self.update_current_date()

    def update_current_date(self):
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        self.generate_calendar(datetime.now().month, datetime.now().year)

    def generate_calendar(self, month, year):
        # 清空现有日历
        self.ids.calendar_grid.clear_widgets()

        # 获取该月的第一天和最后一天
        first_day_of_month = datetime(year, month, 1)
        last_day_of_month = (datetime(year, month, 1) + timedelta(days=35)).replace(day=1) - timedelta(days=1)

        # 计算当前月份的日历起始星期
        start_weekday = first_day_of_month.weekday()

        # 创建日历格子
        day = 1
        for week in range(6):
            for day_of_week in range(7):
                if week == 0 and day_of_week < start_weekday:
                    # 填充空白格子
                    btn = Button(text='', background_normal='', background_down='', size_hint=(None, None), size=(dp(50), dp(50)), color=(1, 1, 1, 1))
                    self.ids.calendar_grid.add_widget(btn)
                elif day <= last_day_of_month.day:
                    btn = Button(text=str(day), background_normal='', background_down='', size_hint=(None, None), size=(dp(50), dp(50)), color=(1, 1, 1, 1))
                    self.ids.calendar_grid.add_widget(btn)
                    day += 1
                else:
                    break

    def add_event(self):
        # 添加新事件并跳转到编辑页面
        self.manager.current = 'edit'
        self.manager.get_screen('edit').set_date(self.current_date, '', '', '')

    def show_statistics(self):
        self.manager.current = 'stat'
