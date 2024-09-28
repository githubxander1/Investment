from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from ui.main_screen import MainScreen
from ui.calendar_screen import CalendarScreen
from ui.add_note_screen import AddNoteScreen
from ui.stats_screen import StatsScreen
from ui.search_screen import SearchScreen
import sqlite3,os

from kivy.resources import resource_add_path, resource_find
from kivy.uix.image import Image

# 添加字体路径
resource_add_path(os.path.join(os.path.dirname(__file__), 'fonts'))
print(os.path.join(os.path.dirname(__file__), 'fonts'))
print(resource_find('simhei.ttf'))
def init_database(db_path):
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 创建 notes 表（如果尚不存在）
    c.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT,
                date TEXT,
                reminder_time TEXT,  -- 添加这一列
                repeat TEXT,
                tags TEXT
            )
    ''')

    # 提交事务并关闭连接
    conn.commit()
    conn.close()

class NoteApp(App):
    def build(self):
        # 初始化数据库
        db_path = r'D:\1document\1test\PycharmProject_gitee\others\Projects\note_app\notes.db'  # 替换为实际的数据库文件路径
        init_database(db_path)

        # 创建 ScreenManager 并添加屏幕
        self.sm = ScreenManager()
        self.main_screen = MainScreen(name='main')
        self.calendar_screen = CalendarScreen(name='calendar',app=self)
        self.add_note_screen = AddNoteScreen(name='add_note',app=self)
        self.stats_screen = StatsScreen(name='stats')
        self.search_screen = SearchScreen(name='search')

        # 将屏幕添加到 ScreenManager
        self.sm.add_widget(self.main_screen)
        self.sm.add_widget(self.calendar_screen)
        self.sm.add_widget(self.add_note_screen)
        self.sm.add_widget(self.stats_screen)
        self.sm.add_widget(self.search_screen)

        # 设置初始屏幕为 CalendarScreen
        self.sm.current = 'calendar'

        return self.sm

if __name__ == '__main__':
    NoteApp().run()