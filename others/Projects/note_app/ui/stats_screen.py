from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform
import sqlite3
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.metrics import dp  # 导入 dp 函数
from datetime import datetime
from kivy.graphics import Color, Rectangle  # 导入 Color 和 Rectangle

class StatsScreen(Screen):
    def __init__(self, app, **kwargs):
        super(StatsScreen, self).__init__(**kwargs)
        self.app = app  # 保存 app 实例以便后续使用

        with self.canvas.before:
            # 设置背景颜色
            Color(0.95, 0.95, 0.95, 1)  # 浅灰色背景
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # self.layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(20))
        # 主布局
        self.layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))

        # 视图选择按钮
        self.view_buttons = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(40))
        self.all_notes_button = Button(text="全部", on_press=self.load_all_notes, size_hint_x=None, width=dp(150))
        self.tag_notes_button = Button(text="标签", on_press=self.show_tag_input_popup, size_hint_x=None, width=dp(150))
        self.view_buttons.add_widget(self.all_notes_button)
        self.view_buttons.add_widget(self.tag_notes_button)
        self.layout.add_widget(self.view_buttons)

        # 统计视图
        self.stats_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height - dp(100)))  # 调整高度以留出空间给返回按钮
        self.stats_grid = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.stats_grid.bind(minimum_height=self.stats_grid.setter('height'))
        self.stats_view.add_widget(self.stats_grid)
        self.layout.add_widget(self.stats_view)

        # 视图选择按钮
        self.view_buttons = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        self.all_notes_button = Button(text="全部", on_press=self.load_all_notes)
        self.tag_notes_button = Button(text="标签", on_press=self.show_tag_input_popup)
        self.view_buttons.add_widget(self.all_notes_button)
        self.view_buttons.add_widget(self.tag_notes_button)
        self.layout.add_widget(self.view_buttons)

        # 返回按钮
        self.back_button = Button(text="返回", on_press=self.switch_to_calendar, size_hint_y=None, height=dp(50))
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

        # 默认加载全部笔记
        self.load_all_notes()

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def load_stats(self, tag=None):
        conn = sqlite3.connect('notes.db')
        c = conn.cursor()
        if tag:
            c.execute("SELECT * FROM notes WHERE tags LIKE ? ORDER BY date DESC", (f"%{tag}%",))
        else:
            c.execute("SELECT * FROM notes ORDER BY date DESC")
        notes = c.fetchall()
        conn.close()

        # 清除现有的笔记
        self.stats_grid.clear_widgets()

        # 按日期分组
        notes_by_date = {}
        for note in notes:
            note_id, title, content, date, reminder_time, repeat, tags = note
            note_date = date.split()[0]  # 取日期部分
            if note_date not in notes_by_date:
                notes_by_date[note_date] = []
            notes_by_date[note_date].append(note)

        last_date = None
        for date, date_notes in sorted(notes_by_date.items(), reverse=True):
            for i, note in enumerate(date_notes):
                if date != last_date:
                    # 显示日期标签
                    date_label = Label(text=date, font_size=dp(16), color=(0, 0, 0, 1), size_hint_y=None, height=dp(50))
                    self.stats_grid.add_widget(date_label)
                    last_date = date

                # 创建一个包含日期和笔记的水平布局
                note_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(50))

                if i == 0:
                    # 第一个笔记时添加日期标签
                    date_label = Label(text=date, font_size=dp(16), color=(0, 0, 0, 1), size_hint_x=None, width=dp(150))
                    note_layout.add_widget(date_label)
                else:
                    # 其他笔记时添加空白占位符
                    note_layout.add_widget(Label(size_hint_x=None, width=dp(150)))

                # 添加笔记按钮
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
                note_layout.add_widget(note_button)

                self.stats_grid.add_widget(note_layout)

    def load_all_notes(self, instance=None):
        """加载所有笔记"""
        self.load_stats()

    def show_tag_input_popup(self, instance):
        """显示输入标签的弹出窗口"""
        box = BoxLayout(orientation='vertical', spacing=dp(10))
        self.tag_input = TextInput(hint_text="输入标签", multiline=False, font_size=dp(20))
        box.add_widget(self.tag_input)

        # 添加确认按钮
        confirm_button = Button(text="确认", on_press=self.load_notes_by_tag, size_hint_y=None, height=dp(40))
        box.add_widget(confirm_button)

        popup = Popup(title="按标签筛选", content=box, size_hint=(None, None), size=(dp(400), dp(200)))
        popup.open()

    def load_notes_by_tag(self, instance):
        """根据标签加载笔记"""
        tag = self.tag_input.text.strip()
        if tag:
            self.load_stats(tag)
        self.tag_input.text = ""  # 清空输入框

    def switch_to_calendar(self, instance):
        """切换到日历屏幕"""
        self.manager.current = 'calendar'  # 返回到日历屏幕

    def open_note(self, note):
        """打开笔记详情"""
        # 跳转到 AddNoteScreen 并加载笔记内容
        add_note_screen = self.app.sm.get_screen('add_note')
        add_note_screen.load_note(note)
        add_note_screen.previous_screen = 'statistics'  # 记录上一个屏幕
        self.app.sm.current = 'add_note'