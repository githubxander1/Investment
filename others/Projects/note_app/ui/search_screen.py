from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform
import sqlite3
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.resources import resource_add_path, resource_find
from kivy.uix.image import Image

class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        with self.canvas.before:
            # 设置背景颜色
            Color(0.95, 0.95, 0.95, 1)  # 浅灰色背景
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))

        # 搜索输入框和按钮
        search_layout = BoxLayout(spacing=dp(5))
        self.search_label = Label(text="搜索:", size_hint_x=None, width=dp(80), font_size=dp(16), color=(0, 0, 0, 1))
        self.search_input = TextInput(multiline=False, font_size=dp(16), hint_text="请输入关键字", size_hint_x=None, height=dp(30), font_name=resource_find('simhei.ttf'), width=Window.width - dp(200))  # 调整宽度
        self.search_button = Button(text="搜索", on_press=self.perform_search, font_size=dp(16), size_hint=(None, None), size=(dp(100), dp(40)), background_color=(0.2, 0.6, 0.9, 1))

        search_layout.add_widget(self.search_label)
        search_layout.add_widget(self.search_input)
        search_layout.add_widget(self.search_button)
        self.layout.add_widget(search_layout)

        # 结果区域
        self.result_scrollview = ScrollView(do_scroll_x=False, bar_width=dp(10))
        self.result_area = GridLayout(cols=2, spacing=dp(10), size_hint_y=None)
        self.result_area.bind(minimum_height=self.result_area.setter('height'))
        self.result_scrollview.add_widget(self.result_area)
        self.layout.add_widget(self.result_scrollview)

        # 返回主屏幕按钮
        self.back_button = Button(text="返回", on_press=self.switch_to_calendar, font_size=dp(16), size_hint=(None, None), size=(dp(100), dp(40)), background_color=(0.7, 0.7, 0.7, 1))
        back_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
        back_layout.add_widget(self.back_button)
        self.layout.add_widget(back_layout)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def perform_search(self, instance):
        search_query = self.search_input.text.strip()
        if search_query:
            results = self.search_notes(search_query)
            self.display_results(results)
        else:
            self.show_popup("请输入搜索关键字。")

    def search_notes(self, query):
        # 连接到 SQLite 数据库
        conn = sqlite3.connect('notes.db')
        c = conn.cursor()

        # 执行模糊匹配查询
        c.execute('SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?',
                  (f"%{query}%", f"%{query}%", f"%{query}%"))

        results = c.fetchall()
        conn.close()
        return results

    def display_results(self, results):
        self.result_area.clear_widgets()
        if results:
            # 按日期分类显示结果
            date_dict = {}
            for note in results:
                note_id, title, content, date, reminder_time, repeat, tags = note
                date_str = date.split()[0]  # 取日期部分
                # date_str = note[2].split()[0]  # 假设日期格式为 "YYYY-MM-DD HH:MM:SS"
                if date_str not in date_dict:
                    date_dict[date_str] = []
                date_dict[date_str].append(note)

            last_date = None
            for date, notes in sorted(date_dict.items(), reverse=True):  # 按日期降序排列
                for i, note in enumerate(notes):
                    if date != last_date:
                        # 显示日期标签
                        date_label = Label(text=f"{date}", font_size=dp(16), color=(0, 0, 0, 1), size_hint_y=None, height=dp(50))
                        self.result_area.add_widget(date_label)
                        last_date = date
                    else:
                        # 如果日期已经显示过，则添加空白占位符
                        self.result_area.add_widget(Label(size_hint_y=None, height=dp(50)))

                    result_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))
                    # date_label = Label(text=f"{date}", font_size=dp(16), color=(0, 0, 0, 1), size_hint_x=None, width=dp(150))
                    note_button = Button(
                        text=f"{note[1]} - {note[6]}",  # 显示标题和标签
                        size_hint_x=None,
                        width=Window.width - dp(150) - dp(20),  # 减去日期栏宽度和间距
                        height=dp(50),
                        on_press=lambda x, n=note: self.open_note(n),
                        font_size=dp(16),
                        background_normal='',
                        background_color=(0.9, 0.9, 0.9, 1),
                        color=(0, 0, 0, 1)
                    )
                    self.result_area.add_widget(note_button)
        else:
            no_results_label = Label(text="没有找到相关笔记。", font_size=dp(16), color=(0.5, 0.5, 0.5, 1))
            self.result_area.add_widget(no_results_label)

    def show_popup(self, message):
        popup = Popup(title="通知", content=Label(text=message, font_size=dp(16), color=(0, 0, 0, 1)), size_hint=(None, None), size=(dp(400), dp(200)))
        popup.open()

    def switch_to_calendar(self, instance):
        self.manager.current = 'calendar'

    def open_note(self, note):
        # 跳转到 AddNoteScreen 并加载笔记内容
        add_note_screen = self.manager.get_screen('add_note')
        add_note_screen.load_note(note)
        add_note_screen.previous_screen = 'search'  # 记录上一个屏幕
        self.manager.current = 'add_note'