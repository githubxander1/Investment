from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.utils import platform
from datetime import datetime, timedelta
import sqlite3,os
import calendar
from kivy.resources import resource_add_path, resource_find
from kivy.uix.image import Image
# 添加字体路径
resource_add_path(os.path.join(os.path.dirname(__file__), 'fonts'))
# print(os.path.join(os.path.dirname(__file__), 'fonts'))
print(resource_find('simhei.ttf'))

class CalendarScreen(Screen):
    def __init__(self, name, app, **kwargs):

        super(CalendarScreen, self).__init__(name=name, **kwargs)
        self.app = app
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=(0, 0, 0, 0))  # 去掉所有留白
        self.year = datetime.now().year
        self.month = datetime.now().month
        self.day = datetime.now().day
        self.view_mode = 'month'  # 默认为月视图

        # 添加图标路径
        resource_add_path(r'D:\1document\1test\PycharmProject_gitee\others\Projects\note_app\resources\icons')  # 假设图标文件在 icons/ 目录下

        # # 创建布局
        # self.layout = BoxLayout(orientation='vertical', spacing=10, padding=(10, 0, 10, 10))

        # 使用内置图标
        calendar_icon = resource_find('calendar.png')
        if calendar_icon:
            image = Image(source=calendar_icon, size_hint=(None, None), size=(50, 50))
        else:
            image = Image(source='', size_hint=(None, None), size=(50, 50))


        # 顶部布局用于按钮
        top_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50, padding=(10, 0, 10, 10))

        # 日历按钮
        self.calendar_button = Button(text="📅", size_hint_x=None, width=50, on_press=self.toggle_view)
        self.calendar_button.add_widget(image)  # 将图标添加到按钮中
        top_layout.add_widget(self.calendar_button)

        # 年份和月份显示
        self.date_label = Label(text=f"{self.year} - {calendar.month_name[self.month]}")
        top_layout.add_widget(self.date_label)

        # 导航按钮
        self.prev_button = Button(text="<", size_hint_x=None, width=50, on_press=self.prev_month)
        self.next_button = Button(text=">", size_hint_x=None, width=50, on_press=self.next_month)
        top_layout.add_widget(self.prev_button)
        top_layout.add_widget(self.next_button)

        # 新建和搜索按钮
        self.add_button = Button(text="+", size_hint_x=None, width=50, on_press=self.add_note)
        self.search_button = Button(text="🔍", size_hint_x=None, width=50, on_press=self.search_notes)
        top_layout.add_widget(self.add_button)
        top_layout.add_widget(self.search_button)

        self.layout.add_widget(top_layout)

        # 日历网格
        self.calendar_grid = GridLayout(cols=7, rows=7, size_hint_y=None, height=400, padding=(10, 0, 10, 10))
        self.layout.add_widget(self.calendar_grid)

        # 日程区域
        self.schedule_area = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=200, padding=(10, 0, 10, 10))
        self.layout.add_widget(self.schedule_area)

        self.add_widget(self.layout)
        self.update_calendar()

    def update_calendar(self):
        self.calendar_grid.clear_widgets()
        cal = calendar.TextCalendar(calendar.SUNDAY)
        weeks = cal.monthdayscalendar(self.year, self.month)

        for week in weeks:
            for day in week:
                if day == 0:
                    continue
                day_button = Button(text=str(day), on_press=self.on_day_select)
                if day == self.day:
                    day_button.background_color = (0.8, 0.8, 0.8, 1)  # 高亮今天
                if self.has_event(day):
                    day_button.color = (0.9, 0, 0, 1)  # 标记有事件的日期
                self.calendar_grid.add_widget(day_button)

    def has_event(self, day):
        # 检查给定日期是否有事件
        conn = sqlite3.connect('notes.db')
        c = conn.cursor()
        c.execute('SELECT * FROM notes WHERE date LIKE ?', (f"{self.year}-{self.month:02d}-{day:02d}%",))
        result = c.fetchone()
        conn.close()
        return result is not None

    def on_day_select(self, instance):
        self.day = int(instance.text)
        self.update_schedule()

    def update_schedule(self):
        self.schedule_area.clear_widgets()
        conn = sqlite3.connect('notes.db')
        c = conn.cursor()
        c.execute('SELECT * FROM notes WHERE date LIKE ?', (f"{self.year}-{self.month:02d}-{self.day:02d}%",))
        notes = c.fetchall()
        conn.close()

        if notes:
            for note in notes:
                note_label = Label(text=f"{note[4]} - {note[1]}", size_hint_y=None, height=50)
                self.schedule_area.add_widget(note_label)
        else:
            no_notes_label = Label(text="该日期没有笔记。")
            self.schedule_area.add_widget(no_notes_label)

    def prev_month(self, instance):
        if self.view_mode == 'month':
            if self.month == 1:
                self.month = 12
                self.year -= 1
            else:
                self.month -= 1
            self.date_label.text = f"{self.year} - {calendar.month_name[self.month]}"
            self.update_calendar()
        elif self.view_mode == 'year':
            self.year -= 1
            self.date_label.text = f"{self.year}"
            self.update_year_view()

    def next_month(self, instance):
        if self.view_mode == 'month':
            if self.month == 12:
                self.month = 1
                self.year += 1
            else:
                self.month += 1
            self.date_label.text = f"{self.year} - {calendar.month_name[self.month]}"
            self.update_calendar()
        elif self.view_mode == 'year':
            self.year += 1
            self.date_label.text = f"{self.year}"
            self.update_year_view()

    def toggle_view(self, instance):
        if self.view_mode == 'month':
            self.view_mode = 'year'
            self.update_year_view()
        else:
            self.view_mode = 'month'
            self.update_calendar()

    def update_year_view(self):
        self.calendar_grid.clear_widgets()
        for month in range(1, 13):
            month_button = Button(text=calendar.month_abbr[month], on_press=self.select_month)
            if month == self.month:
                month_button.background_color = (0.8, 0.8, 0.8, 1)  # 高亮当前月份
            self.calendar_grid.add_widget(month_button)

    def select_month(self, instance):
        self.month = list(calendar.month_abbr).index(instance.text)
        self.view_mode = 'month'
        self.date_label.text = f"{self.year} - {calendar.month_name[self.month]}"
        self.update_calendar()

    def add_note(self, instance):
        # 传递选定的日期到 AddNoteScreen
        selected_date = f"{self.year}-{self.month:02d}-{self.day:02d} {datetime.now().strftime('%H:%M:%S')}"
        add_note_screen = self.app.sm.get_screen('add_note')
        add_note_screen.set_selected_date(selected_date)
        self.app.sm.current = 'add_note'

    def search_notes(self, instance):
        self.app.sm.current = 'search'