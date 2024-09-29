from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.markup import MarkdownLabel
from kivy.uix.richtext import RichTextWidget

class MarkdownRichTextApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Markdown输入框
        self.markdown_input = TextInput(hint_text='输入Markdown文本', size_hint=(1, 0.5))
        layout.add_widget(self.markdown_input)

        # Markdown预览标签
        self.markdown_preview = MarkdownLabel(size_hint=(1, 0.5))
        layout.add_widget(self.markdown_preview)

        # 富文本输入框
        self.rich_text_input = RichTextWidget(size_hint=(1, 0.5))
        layout.add_widget(self.rich_text_input)

        # 绑定事件，当Markdown输入框内容改变时，更新预览
        self.markdown_input.bind(text=self.on_markdown_change)

        return layout

    def on_markdown_change(self, instance, value):
        # 更新Markdown预览标签的内容
        self.markdown_preview.text = value

if __name__ == '__main__':
    MarkdownRichTextApp().run()
