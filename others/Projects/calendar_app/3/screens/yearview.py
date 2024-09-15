from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, DictProperty, ListProperty
from kivy.metrics import dp
from datetime import datetime
from data_manager import DataManager

class YearView(Screen):
    current_date = StringProperty('')
    events_dict = DictProperty({})
    current_events = ListProperty([])
    view_mode = StringProperty('year')  # 默认为年视图
    data_manager = DataManager()

    def on_pre_enter(self):
        self.update_current_date()
        self.generate_year_view()

    def update_current_date(self):
        self.current_date = datetime.now().strftime('%Y-%m-%d')

    def generate_year_view(self):
        # 清空现有日历
        self.ids.calendar_grid.clear_widgets()

        # 当前年份
        current_year = datetime.now().year

        # 创建年视图
        for month in range(1, 13):
            btn = Button(text=f"{current_year}-{month}", background_normal='', background_down='', size_hint=(None, None), size=(dp(50), dp(50)), color=(1, 1, 1, 1))
            btn.bind(on_press=self.on_year_button_press)
            self.ids.calendar_grid.add_widget(btn)

    def on_year_button_press(self, instance):
        year, month = map(int, instance.text.split('-'))
        self.manager.current = 'month'
        self.manager.get_screen('month').update_month_view(year, month)
