from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.webview import WebView  # 确保这个模块能正常导入
import markdown

class MarkdownApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Markdown文本输入框
        self.markdown_input = TextInput(hint_text='输入Markdown文本', size_hint=(1, 0.5))
        layout.add_widget(self.markdown_input)

        # WebView用于显示Markdown渲染后的HTML
        self.webview = WebView(size_hint=(1, 0.5))
        layout.add_widget(self.webview)

        # 绑定事件，当Markdown文本输入框内容改变时，更新WebView显示
        self.markdown_input.bind(text=self.on_markdown_change)

        return layout

    def on_markdown_change(self, instance, value):
        # 将Markdown文本转换为HTML
        html = markdown.markdown(value)
        # 加载HTML到WebView
        self.webview.load_html(html)

if __name__ == '__main__':
    MarkdownApp().run()
