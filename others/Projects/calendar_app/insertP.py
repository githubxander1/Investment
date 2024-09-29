from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.video import Video


class TextBoxWithMedia(BoxLayout):
    def __init__(self, **kwargs):
        super(TextBoxWithMedia, self).__init__(**kwargs)
        # 图片
        self.img = Image(source='path_to_your_image.png', allow_stretch=True)
        self.add_widget(self.img)

        # 视频
        self.video = Video(source='path_to_your_video.mp4', state='play')
        self.add_widget(self.video)


class TextBoxWithMediaApp(App):
    def build(self):
        return TextBoxWithMedia()


if __name__ == '__main__':
    TextBoxWithMediaApp().run()