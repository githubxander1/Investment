from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, DictProperty, ListProperty
from kivy.metrics import dp
from datetime import datetime, timedelta
# from data_manager import DataManager
from kivy.uix.button import Button
from kivy.metrics import dp
# 导入 .kv 文件
from kivy.lang import Builder
Builder.load_file('kv/main.kv')

class MainScreen(Screen):
    current_date = StringProperty('')
    events_dict = DictProperty({})
    current_events = ListProperty([])
    view_mode = StringProperty('month')  # 默认为月视图
    # data_manager = DataManager()

    def on_pre_enter(self):
        self.update_current_date()
        self.update_view()

    def update_current_date(self):
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        self.generate_calendar(datetime.now().month, datetime.now().year)

    def generate_calendar(self, month, year):
        # 确保 calendar_grid 已经存在
        if 'calendar_grid' in self.ids:
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
                        btn.bind(on_press=self.on_day_button_press)
                        self.ids.calendar_grid.add_widget(btn)
                        day += 1
                    else:
                        break
        else:
            print("Error: calendar_grid not found in MainScreen")

    def update_view(self):
        if self.view_mode == 'month':
            self.generate_calendar(datetime.now().month, datetime.now().year)
        elif self.view_mode == 'year':
            self.generate_year_view()

    def generate_year_view(self):
        # 确保 calendar_grid 已经存在
        if 'calendar_grid' in self.ids:
            # 清空现有日历
            self.ids.calendar_grid.clear_widgets()

            # 当前年份
            current_year = datetime.now().year

            # 创建年视图
            for month in range(1, 13):
                btn = Button(text=f"{current_year}-{month:02d}", background_normal='', background_down='', size_hint=(None, None), size=(dp(50), dp(50)), color=(1, 1, 1, 1))
                btn.bind(on_press=self.on_year_button_press)
                self.ids.calendar_grid.add_widget(btn)
        else:
            print("Error: calendar_grid not found in MainScreen")

    def on_year_button_press(self, instance):
        year, month = map(int, instance.text.split('-'))
        self.manager.current = 'month'
        self.manager.get_screen('month').update_month_view(year, month)

    def on_day_button_press(self, instance):
        day = int(instance.text)
        selected_date = datetime.now().replace(day=day).strftime('%Y-%m-%d')
        self.manager.current = 'day'
        self.manager.get_screen('day').update_day_view(selected_date)

    def add_event(self):
        # 添加新事件并跳转到编辑页面
        self.manager.current = 'edit'
        self.manager.get_screen('edit').set_date(self.current_date, '', '', '')

    def show_statistics(self):
        self.manager.current = 'stat'
