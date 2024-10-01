import os

from kivy.app import App
from kivy.resources import resource_add_path, resource_find
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from markdown import markdown
from kivy.core.text import LabelBase

# 加载字体资源
font_dir = os.path.join(os.path.dirname(__file__), 'resources', 'fonts')
resource_add_path(font_dir)
font_path = resource_find('simkai.ttf')
LabelBase.register(name='SimKai', fn_regular=font_path)

class MarkdownInputApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Markdown 输入框
        self.md_input = TextInput(text='', multiline=True, size_hint_y=None, height=200)
        self.md_input.bind(text=self.on_text_change)  # 绑定输入框内容变化事件
        layout.add_widget(self.md_input)

        return layout

    def on_text_change(self, instance, value):
        # 使用markdown库将输入的Markdown文本转换成HTML
        html_text = markdown(value)
        # 将转换后的HTML文本设置为输入框的内容
        self.md_input.text = self.convert_html_to_markup(html_text)

    def convert_html_to_markup(self, html_text):
        # 将HTML文本转换为Kivy的Markup格式
        markup_text = ''
        lines = html_text.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('<h1>') and line.endswith('</h1>'):
                markup_text += '[b]' + line[4:-5] + '[/b]\n'
            elif line.startswith('<h2>') and line.endswith('</h2>'):
                markup_text += '[b]' + line[4:-5] + '[/b]\n'
            elif line.startswith('<h3>') and line.endswith('</h3>'):
                markup_text += '[b]' + line[4:-5] + '[/b]\n'
            elif line.startswith('<h4>') and line.endswith('</h4>'):
                markup_text += '[b]' + line[4:-5] + '[/b]\n'
            elif line.startswith('<h5>') and line.endswith('</h5>'):
                markup_text += '[b]' + line[4:-5] + '[/b]\n'
            elif line.startswith('<h6>') and line.endswith('</h6>'):
                markup_text += '[b]' + line[4:-5] + '[/b]\n'
            elif line.startswith('<p>') and line.endswith('</p>'):
                markup_text += line[3:-4] + '\n'
            elif line.startswith('<ul>') or line.startswith('<ol>') or line.startswith('</ul>') or line.startswith('</ol>'):
                continue
            elif line.startswith('<li>') and line.endswith('</li>'):
                markup_text += '- ' + line[3:-4] + '\n'
            elif line.startswith('<pre><code>') or line.startswith('</code></pre>'):
                continue
            elif line.startswith('<code>') and line.endswith('</code>'):
                markup_text += '[color=0000ff]' + line[6:-7] + '[/color]\n'
            elif line.startswith('<del>') and line.endswith('</del>'):
                markup_text += '[s]' + line[5:-6] + '[/s]\n'
            elif line.startswith('<strong>') and line.endswith('</strong>'):
                markup_text += '[b]' + line[7:-8] + '[/b]\n'
            elif line.startswith('<em>') and line.endswith('</em>'):
                markup_text += '[i]' + line[4:-5] + '[/i]\n'
            else:
                markup_text += line + '\n'

        # 添加边界检查
        if len(markup_text) > 0:
            markup_text = markup_text.rstrip('\n') + '\n'

        return markup_text

if __name__ == '__main__':
    MarkdownInputApp().run()
