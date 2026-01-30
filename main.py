from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.lang import Builder

class Background(Label):
    # Creating background image
    def __init__(self,*args, **kwargs):
        super().__init__(**kwargs)
        # Rectangle with image from folder 'images'
        with self.canvas.before:
            self.bg_rect = Rectangle(source='./images/background.png',
                                     pos=self.pos,
                                     size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class SoloFloatLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Adding background to layout
        self.add_widget(Background())

        # Buttons   
        def create_button(text, pos_x, pos_y):
            self.button = Button(text=text, 
                             size_hint=(.3,.15),
                             pos_hint={'center_x':pos_x,'center_y':pos_y},
                             font_size=40,
                             font_name='./fonts/BebasNeue-Regular.ttf',
                             color=(0.2, 0.8, 1, 1),
                             background_color=[0.1,0.1,0.1,1])         
            self.add_widget(self.button)


        create_button("Day 1", .5, .7)

        create_button("Day 2", .5, .5)

        create_button("Day 3", .5, .3)

class SoloApp(App):
    def build(self):
        return SoloFloatLayout()

if __name__ == "__main__":
    SoloApp().run()