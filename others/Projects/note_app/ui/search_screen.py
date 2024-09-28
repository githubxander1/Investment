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

class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super(SearchScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # 搜索输入框
        self.search_label = Label(text="搜索:")
        self.search_input = TextInput(multiline=False)
        self.layout.add_widget(self.search_label)
        self.layout.add_widget(self.search_input)

        # 搜索按钮
        self.search_button = Button(text="搜索", on_press=self.perform_search)
        self.layout.add_widget(self.search_button)

        # 结果区域
        self.result_area = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=300)
        self.layout.add_widget(self.result_area)

        # 返回主屏幕按钮
        self.back_button = Button(text="返回主屏幕", on_press=self.switch_to_main)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def perform_search(self, instance):
        search_query = self.search_input.text
        if search_query:
            results = self.search_notes(search_query)
            self.display_results(results)
        else:
            self.show_popup("请输入搜索关键字。")

    def search_notes(self, query):
        # 连接到 SQLite 数据库
        conn = sqlite3.connect('notes.db')
        c = conn.cursor()

        # 执行搜索查询
        c.execute('SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?',
                  (f"%{query}%", f"%{query}%", f"%{query}%"))

        results = c.fetchall()
        conn.close()
        return results

    def display_results(self, results):
        self.result_area.clear_widgets()
        if results:
            for note in results:
                note_label = Label(text=f"{note[4]} - {note[1]}", size_hint_y=None, height=50)
                self.result_area.add_widget(note_label)
        else:
            no_results_label = Label(text="没有找到相关笔记。")
            self.result_area.add_widget(no_results_label)

    def show_popup(self, message):
        popup = Popup(title="通知", content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def switch_to_main(self, instance):
        self.manager.current = 'main'