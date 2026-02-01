from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
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

# Main Menu
class SoloMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Adding background
        self.add_widget(Background())

        # Buttons
        def create_button(name, x, y, screen):
            self.button = Button(text=name, 
                            size_hint=(.3,.15),
                            pos_hint={'center_x':x,'center_y':y},
                            font_size=40,
                            font_name='./fonts/BebasNeue-Regular.ttf',
                            color=(0.2, 0.8, 1, 1),
                            background_color=[0.05,0.05,0.05,1])
            self.button.bind(on_release=lambda instance: self.press(instance,screen))     
            self.add_widget(self.button)
    
        create_button('Day 1', .5, .7, 'day_one')
        create_button('Day 2', .5, .5, 'day_two')
        create_button('Day 3', .5, .3, 'day_three')

    def press(self, instance, screen):
        self.manager.transition.direction ='left'
        self.manager.current=screen

# Screen Day 1
class SoloDayOne(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Background())

        self.button = Button(text="Go Back", 
                            size_hint=(.3,.15),
                            pos_hint={'center_x':.5,'center_y':.7},
                            font_size=40,
                            font_name='./fonts/BebasNeue-Regular.ttf',
                            color=(0.2, 0.8, 1, 1),
                            background_color=[0.05,0.05,0.05,1])
        self.button.bind(on_release=self.press)     
        self.add_widget(self.button)
        
    def press(self, instance):
        self.manager.transition.direction ='right'
        self.manager.current='menu'

# Screen Day 2
class SoloDayTwo(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Background())

        self.button = Button(text="Go Back", 
                            size_hint=(.3,.15),
                            pos_hint={'center_x':.5,'center_y':.7},
                            font_size=40,
                            font_name='./fonts/BebasNeue-Regular.ttf',
                            color=(0.2, 0.8, 1, 1),
                            background_color=[0.05,0.05,0.05,1])
        self.button.bind(on_release=self.press)     
        self.add_widget(self.button)

    def press(self, instance):
        self.manager.transition.direction ='right'
        self.manager.current='menu'
# Screen Day 3
class SoloDayThree(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Background())
        self.button = Button(text="Go Back", 
                            size_hint=(.3,.15),
                            pos_hint={'center_x':.5,'center_y':.7},
                            font_size=40,
                            font_name='./fonts/BebasNeue-Regular.ttf',
                            color=(0.2, 0.8, 1, 1),
                            background_color=[0.05,0.05,0.05,1])
        self.button.bind(on_release=self.press)     
        self.add_widget(self.button)

    def press(self, instance):
        self.manager.transition.direction ='right'
        self.manager.current='menu'

class SoloApp(App):
    def build(self):
        sm = ScreenManager()

        menu = SoloMenu(name='menu')
        day_one = SoloDayOne(name='day_one')
        day_two = SoloDayTwo(name='day_two')
        day_three = SoloDayThree(name='day_three')

        sm.add_widget(menu)
        sm.add_widget(day_one)
        sm.add_widget(day_two)
        sm.add_widget(day_three)

        return sm

if __name__ == "__main__":
    SoloApp().run()