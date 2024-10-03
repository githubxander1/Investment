from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from datetime import datetime
import sqlite3
from kivy.resources import resource_find
from kivy.graphics import Color, Rectangle  # 导入 Color 和 Rectangle
# 从 kv 文件中导入自定义控件
from kivy.lang import Builder
# Builder.load_file('../style.kv')  # 确保路径正确

class AddNoteScreen(Screen):
    def __init__(self, name, app, **kwargs):
        super(AddNoteScreen, self).__init__(name=name, **kwargs)
        self.app = app

        # with self.canvas.before:
        #     # 设置背景颜色
        #     Color(0.95, 0.95, 0.95, 1)  # 浅灰色背景
        #     self.rect = Rectangle(size=self.size, pos=self.pos)
        #     self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.selected_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.note_id = None  # 用来存储当前笔记的ID，如果是新笔记则为None
        self.previous_screen = 'calendar'  # 默认从日历页面进入

        # 标题
        self.title_input = TextInput(hint_text="请输入标题", multiline=False, font_name=resource_find('simhei.ttf'))
        self.layout.add_widget(self.title_input)

        # 内容
        self.content_input = TextInput(hint_text="请输入内容", multiline=True, size_hint_y=None, height=200, font_name=resource_find('simhei.ttf'))
        self.layout.add_widget(self.content_input)

        # 日期和提醒时间布局
        left_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_x=0.5)

        self.date_label = Label(text="日期:")
        self.date_input = TextInput(text=self.selected_date, hint_text="请选择日期", font_name=resource_find('simhei.ttf'))
        left_layout.add_widget(self.date_label)
        left_layout.add_widget(self.date_input)

        self.reminder_label = Label(text="提醒时间:")
        self.reminder_time_input = TextInput(hint_text="请输入提醒时间", font_name=resource_find('simhei.ttf'))
        left_layout.add_widget(self.reminder_label)
        left_layout.add_widget(self.reminder_time_input)

        # 重复和标签布局
        right_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_x=0.5)

        self.repeat_label = Label(text="重复:")
        self.repeat_input = Spinner(
            text='无',
            values=('无', '每天', '每周', '每月'),
            size_hint=(1, None),
            height=50
        )
        right_layout.add_widget(self.repeat_label)
        right_layout.add_widget(self.repeat_input)

        self.tags_label = Label(text="标签:")
        self.tags_input = TextInput(hint_text="点击选择标签", readonly=True, on_focus=self.show_tag_popup, font_name=resource_find('simhei.ttf'))
        right_layout.add_widget(self.tags_label)
        right_layout.add_widget(self.tags_input)

        # 将左右布局放入主布局
        main_layout = BoxLayout(orientation='horizontal', spacing=10)
        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)
        self.layout.add_widget(main_layout)

        # 按钮布局
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        self.back_button = Button(text="返回", on_press=self.switch_back, size_hint=(1, None), height=40)
        self.save_button = Button(text="保存", on_press=self.save_note, size_hint=(1, None), height=40)
        self.delete_button = Button(text="删除", on_press=self.delete_note, size_hint=(1, None), height=40)
        button_layout.add_widget(self.back_button)
        button_layout.add_widget(self.save_button)
        button_layout.add_widget(self.delete_button)
        self.layout.add_widget(button_layout)

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
            if self.note_id is None:  # 如果note_id为None，表示这是新笔记
                self.insert_into_db(title, content, date, reminder_time, repeat, tags)
            else:  # 否则是更新现有笔记
                self.update_db(self.note_id, title, content, date, reminder_time, repeat, tags)
            self.clear_inputs()
            self.show_popup("笔记保存成功！")
            self.refresh_calendar()  # 保存后刷新日历页
        else:
            self.show_popup("请填写所有字段。")

    def delete_note(self, instance):
        if self.note_id is not None:
            self.delete_from_db(self.note_id)
            self.clear_inputs()
            self.show_popup("笔记删除成功！")
            self.refresh_calendar()  # 删除后刷新日历页
            self.refresh_stats()
        else:
            self.show_popup("没有可删除的笔记。")

    def refresh_stats(self):
        # 通知 StatsScreen 刷新数据
        stats_screen = self.app.sm.get_screen('statistics')
        stats_screen.load_all_notes()  # 刷新统计页面

    def insert_into_db(self, title, content, date, reminder_time, repeat, tags):
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

    def update_db(self, note_id, title, content, date, reminder_time, repeat, tags):
        # 更新数据库中的笔记
        conn = sqlite3.connect('notes.db')
        c = conn.cursor()

        # 更新笔记
        c.execute('''
            UPDATE notes
            SET title=?, content=?, date=?, reminder_time=?, repeat=?, tags=?
            WHERE id=?
        ''', (title, content, date, reminder_time, repeat, tags, note_id))

        # 提交事务并关闭连接
        conn.commit()
        conn.close()

        print("笔记更新成功")

    def delete_from_db(self, note_id):
        # 从数据库中删除笔记
        conn = sqlite3.connect('notes.db')
        c = conn.cursor()

        # 删除笔记
        c.execute('''
            DELETE FROM notes
            WHERE id=?
        ''', (note_id,))

        # 提交事务并关闭连接
        conn.commit()
        conn.close()

        print("笔记删除成功")

    def clear_inputs(self):
        self.title_input.text = ""
        self.content_input.text = ""
        self.date_input.text = self.selected_date  # 使用选定的日期
        self.reminder_time_input.text = ""
        self.repeat_input.text = "无"  # 重置下拉框
        self.tags_input.text = ""

    def show_popup(self, message):
        popup = Popup(title="通知", content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def switch_to_calendar(self, instance):
        self.manager.current = 'calendar'

    def switch_back(self, instance):
        # 返回到上一个屏幕
        self.app.sm.current = self.previous_screen

    def load_note(self, note):
        # 加载笔记内容
        self.note_id = note[0]  # 存储笔记ID
        self.title_input.text = note[1]
        self.content_input.text = note[2]
        self.date_input.text = note[3]
        self.reminder_time_input.text = note[4]
        self.repeat_input.text = note[5]  # 设置下拉框值
        self.tags_input.text = note[6]

    def reset_screen(self):
        # 重置屏幕状态，清除输入框和笔记ID
        self.clear_inputs()
        self.note_id = None

    def refresh_calendar(self):
        # 刷新日历页
        self.app.calendar_screen.refresh_notes()

    def show_tag_popup(self, instance):
        # 创建一个标签选择弹窗
        tag_popup = Popup(title="选择标签", size_hint=(0.8, 0.8))

        # 获取已保存的标签
        saved_tags = self.get_saved_tags()

        # 创建一个滚动视图来容纳标签选择项
        scroll_view = ScrollView(do_scroll_x=False)
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # 添加已保存的标签到布局
        for tag in saved_tags:
            checkbox = CheckBox(group='tags', active=False)
            checkbox.tag = tag
            checkbox.bind(active=self.on_checkbox_active)
            layout.add_widget(checkbox)
            layout.add_widget(Label(text=tag))

        # 添加一个自定义标签输入框
        custom_tag_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        self.custom_tag_input = TextInput(hint_text="自定义标签", font_name=resource_find('simhei.ttf'))
        add_custom_tag_button = Button(text="添加", on_press=self.add_custom_tag)
        custom_tag_layout.add_widget(self.custom_tag_input)
        custom_tag_layout.add_widget(add_custom_tag_button)
        layout.add_widget(custom_tag_layout)

        # 添加完成按钮
        done_button = Button(text="完成", on_press=tag_popup.dismiss, size_hint_y=None, height=40)
        layout.add_widget(done_button)

        # 将布局添加到滚动视图
        scroll_view.add_widget(layout)
        tag_popup.content = scroll_view
        tag_popup.open()

    def get_saved_tags(self):
        # 从数据库中获取已保存的标签
        conn = sqlite3.connect('notes.db')
        c = conn.cursor()
        c.execute('SELECT DISTINCT tags FROM notes WHERE tags IS NOT NULL AND tags != ""')
        tags = [tag[0].strip() for tag in c.fetchall()]
        conn.close()
        return list(set(tags))  # 去重

    def on_checkbox_active(self, checkbox, value):
        if value:
            self.add_tag(checkbox.tag)
        else:
            self.remove_tag(checkbox.tag)

    def add_tag(self, tag):
        current_tags = self.tags_input.text.split(',')
        if tag not in current_tags:
            if self.tags_input.text:
                self.tags_input.text += f", {tag}"
            else:
                self.tags_input.text = tag

    def remove_tag(self, tag):
        current_tags = self.tags_input.text.split(',')
        self.tags_input.text = ', '.join([t.strip() for t in current_tags if t.strip() != tag])

    def add_custom_tag(self, instance):
        custom_tag = self.custom_tag_input.text.strip()
        if custom_tag:
            self.add_tag(custom_tag)
            self.custom_tag_input.text = ''