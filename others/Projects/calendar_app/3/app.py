from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from screens.mainscreen import MainScreen
from screens.monthview import MonthView
from screens.yearview import YearView
from screens.editscreen import EditScreen
from screens.statscreen import StatScreen
from screens.searchscreen import SearchScreen
from screens.dayview import DayView

# 导入 .kv 文件
from kivy.lang import Builder
Builder.load_file('kv/main.kv')

class MyApp(App):
    def build(self):
        self.sm = ScreenManager()

        # 主屏幕
        main_screen = MainScreen(name='main')
        self.sm.add_widget(main_screen)

        # 月视图
        month_screen = MonthView(name='month')
        self.sm.add_widget(month_screen)

        # 年视图
        year_screen = YearView(name='year')
        self.sm.add_widget(year_screen)

        # 编辑屏幕
        edit_screen = EditScreen(name='edit')
        self.sm.add_widget(edit_screen)

        # 统计屏幕
        stat_screen = StatScreen(name='stat')
        self.sm.add_widget(stat_screen)

        # 搜索屏幕
        search_screen = SearchScreen(name='search')
        self.sm.add_widget(search_screen)

        # 日视图
        day_screen = DayView(name='day')
        self.sm.add_widget(day_screen)

        return self.sm

if __name__ == '__main__':
    MyApp().run()
