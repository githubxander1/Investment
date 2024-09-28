# ui/add_note_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.utils import platform
from datetime import datetime
import sqlite3

class AddNoteScreen(Screen):
    def __init__(self, name, app, **kwargs):
        super(AddNoteScreen, self).__init__(name=name, **kwargs)
        self.app = app
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.selected_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 标题
        self.title_label = Label(text="标题:")
        self.title_input = TextInput(multiline=False)
        self.layout.add_widget(self.title_label)
        self.layout.add_widget(self.title_input)

        # 内容
        self.content_label = Label(text="内容:")
        self.content_input = TextInput(multiline=True)
        self.layout.add_widget(self.content_label)
        self.layout.add_widget(self.content_input)

        # 日期
        self.date_label = Label(text="日期:")
        self.date_input = TextInput(multiline=False, text=self.selected_date)
        self.layout.add_widget(self.date_label)
        self.layout.add_widget(self.date_input)

        # 提醒时间
        self.reminder_label = Label(text="提醒时间:")
        self.reminder_time_input = TextInput(multiline=False)
        self.layout.add_widget(self.reminder_label)
        self.layout.add_widget(self.reminder_time_input)

        # 重复
        self.repeat_label = Label(text="重复:")
        self.repeat_input = TextInput(multiline=False)
        self.layout.add_widget(self.repeat_label)
        self.layout.add_widget(self.repeat_input)

        # 标签
        self.tags_label = Label(text="标签:")
        self.tags_input = TextInput(multiline=False)
        self.layout.add_widget(self.tags_label)
        self.layout.add_widget(self.tags_input)

        # 保存按钮
        self.save_button = Button(text="保存", on_press=self.save_note)
        self.layout.add_widget(self.save_button)

        # 返回主屏幕按钮 -> 更改为返回日历屏幕按钮
        self.back_button = Button(text="返回日历", on_press=self.switch_to_calendar)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def set_selected_date(self, selected_date):
        # 设置从 CalendarScreen 传递过来的日期
        self.selected_date = selected_date
        self.date_input.text = selected_date

    def save_note(self, instance):
        title = self.title_input.text
        content = self.content_input.text
        date = self.date_input.text  # 使用选定的日期
        reminder_time = self.reminder_time_input.text
        repeat = self.repeat_input.text
        tags = self.tags_input.text

        if title and content:
            self.save_to_db(title, content, date, reminder_time, repeat, tags)
            self.clear_inputs()
            self.show_popup("笔记保存成功！")
        else:
            self.show_popup("请填写所有字段。")

    def save_to_db(self, title, content, date, reminder_time, repeat, tags):
        # 连接到 SQLite 数据库
        conn = sqlite3.connect('notes.db')  # 确保数据库文件路径正确
        c = conn.cursor()

        # 插入笔记到 notes 表
        c.execute('''
            INSERT INTO notes (title, content, date, reminder_time, repeat, tags)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (title, content, date, reminder_time, repeat, tags))

        # 提交事务并关闭连接
        conn.commit()
        conn.close()

        print("笔记保存成功")

    def clear_inputs(self):
        self.title_input.text = ""
        self.content_input.text = ""
        self.date_input.text = self.selected_date  # 使用选定的日期
        self.reminder_time_input.text = ""
        self.repeat_input.text = ""
        self.tags_input.text = ""

    def show_popup(self, message):
        popup = Popup(title="通知", content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def switch_to_calendar(self, instance):
        self.manager.current = 'calendar'