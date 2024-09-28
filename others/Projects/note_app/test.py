from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRectangleFlatButton, MDFillRoundFlatIconButton

class TestApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # 添加 MDRectangleFlatButton
        button1 = MDRectangleFlatButton(text="Rectangle Flat Button", on_press=self.on_press)
        layout.add_widget(button1)

        # 添加 MDFillRoundFlatIconButton
        button2 = MDFillRoundFlatIconButton(text="Fill Round Flat Icon Button", icon="android")
        layout.add_widget(button2)

        return layout

    def on_press(self, instance):
        print(f"Button {instance.text} pressed")

if __name__ == '__main__':
    TestApp().run()