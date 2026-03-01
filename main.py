from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Rectangle
from kivy.properties import NumericProperty
from kivy.storage.jsonstore import JsonStore
from kivy.metrics import sp
import os
from save_load import save_exercise, load_exercise, save_level, load_level

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
    # Updating the exp label and increasing max_exp and level
    def refresh_exp_text(self, instance, value):
        app = App.get_running_app()
        self.exp_label.text = f"EXP: {value}/{app.max_exp}"
        if value >= app.max_exp:
            app.max_exp += 60
            app.exp = 0
            app.level += 1

    # Updating max_exp
    def refresh_max_exp_text(self,instance, value):
        app = App.get_running_app()
        self.exp_label.text = f"EXP: {app.exp}/{value}"

    # Updating level label
    def refresh_level_text(self, instance, value):
        self.level_label.text = f"LEVEL: {value}"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Adding background
        self.add_widget(Background())

        app = App.get_running_app()
            
        # Label indicating level and experience
        self.exp_label = Label(
            text=f"EXP: {app.exp}/{app.max_exp}",
            pos_hint={'center_x': .5, 'center_y': .85},
            font_size=sp(25)
        )
        self.add_widget(self.exp_label)

        app.bind(exp=self.refresh_exp_text)
        app.bind(max_exp=self.refresh_max_exp_text)

        self.level_label = Label(
            text=f"LEVEL: {app.level}",
            pos_hint={'center_x': .5, 'center_y': .9},
            font_size=sp(30)
        )
        self.add_widget(self.level_label)

        app.bind(level=self.refresh_level_text)

        # Buttons
        def create_button(name, x, y, screen):
            self.button = Button(text=name, 
                            size_hint=(.3,.10),
                            pos_hint={'center_x':x,'center_y':y},
                            font_size=sp(40),
                            font_name='./fonts/BebasNeue-Regular.ttf',
                            color=(0.2, 0.8, 1, 1),
                            background_color=[0.05,0.05,0.05,1])
            self.button.bind(on_release=lambda instance: self.press(instance,screen))     
            self.add_widget(self.button)
    
        create_button('Day 1', .5, .45, 'day_one')
        create_button('Day 2', .5, .3, 'day_two')
        create_button('Day 3', .5, .15, 'day_three')

    # After pressing the "Day number" button, we move to another screen
    def press(self, instance, screen):
        self.manager.transition.direction ='left'
        self.manager.current=screen

# Base screen class
class DaysScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Background())
        app=App.get_running_app()
                # Button "Go Back"
        self.buttonGoBack = Button(text="Go Back", 
                            size_hint=(.3,.10),
                            pos_hint={'center_x':.7,'center_y':.1},
                            font_size=sp(40),
                            font_name='./fonts/BebasNeue-Regular.ttf',
                            color=(0.2, 0.8, 1, 1),
                            background_color=[0.05,0.05,0.05,1])
        self.buttonGoBack.bind(on_release=self.press_back)     
        self.add_widget(self.buttonGoBack)

        # Button "Delete"
        self.buttonDel = Button(text="DELETE", 
                            size_hint=(.3,.10),
                            pos_hint={'center_x':.3,'center_y':.1},
                            font_size=sp(40),
                            font_name='./fonts/BebasNeue-Regular.ttf',
                            color=(0.2, 0.8, 1, 1),
                            background_color=[0.05,0.05,0.05,1])
        self.buttonDel.bind(on_release=self.press_delete)     
        self.add_widget(self.buttonDel)

        # Button "+"
        self.buttonPlus = Button(text="+",
                             size_hint=(.8,.06),
                             pos_hint={'center_x':.5,'center_y':app.centerY},
                             font_size=sp(40),
                             font_name="./fonts/BebasNeue-Regular.ttf",
                             color=(0.2, 0.8, 1, 1),
                             background_color=[0.05,0.05,0.05,1])
        self.buttonPlus.bind(on_release=self.create_exercise)
        self.buttonPlus.bind(on_release=self.spaceForButton)
        self.add_widget(self.buttonPlus)
    
    # Function for removing button "+" when it cover other buttons
    def spaceForButton(self, instance):
        if abs(self.buttonPlus.pos_hint.get('center_y')-self.buttonGoBack.pos_hint.get('center_y'))<0.2:  
            self.buttonPlus.pos_hint={'center_x':10}
            self.do_layout()

    # When we press the button "+", we creating text input and button "Done"
    def create_exercise(self, instance):

        app=App.get_running_app()

        self.text_input = TextInput(size_hint=(.7,.06),
                                    pos_hint={'center_x':.45,'center_y':app.centerY},
                                    font_size=sp(20),
                                    foreground_color=(0.2, 0.8, 1, 1),
                                    background_color=[0,0,0,1],
                                    multiline=False)
        self.text_input.exercise = True
        self.add_widget(self.text_input)
        
        self.buttonDone = Button(text="DONE", 
                            size_hint=(.1,.06),
                            pos_hint={'center_x':.85,'center_y':app.centerY},
                            font_size=sp(25),
                            font_name='./fonts/BebasNeue-Regular.ttf',
                            color=(0.2, 0.8, 1, 1),
                            background_color=[0.05,0.05,0.05,1])
        self.buttonDone.exercise = True
        self.buttonDone.bind(on_release=self.press_exp)    
        self.add_widget(self.buttonDone)

        app.centerY -= 0.07

        self.buttonPlus.pos_hint={'center_y':app.centerY}
    
    # We can get experience for level when we press the button "Done"
    def press_exp(self, instance):
        app = App.get_running_app()
        app.exp += 20

        save_level(app)

    # Clearing all buttons and text inputs when we press the button "Delete"
    def press_delete(self, instance):
        app = App.get_running_app()

        for widget in list(self.children):
                if hasattr(widget, 'exercise'):
                    self.remove_widget(widget)
                    
        app.centerY = 0.9
        self.buttonPlus.pos_hint={'center_x':.5,'center_y':app.centerY}

    # Returning to the menu screen after pressing the "Go Back" button
    def press_back(self, instance):
        self.manager.transition.direction ='right'
        self.manager.current='menu'

    key = ""

    ctg_workout = ""

    ctg_plus = ""

    # This function for saving exercises when we leave screen
    def on_leave(self):
        save_exercise(self, self.ctg_workout, self.ctg_plus)

    # Loading saved exercises from file 'data.json'
    def on_pre_enter(self, *args):
        load_exercise(self, self.ctg_workout, self.ctg_plus)

# Screen Day 1
class SoloDayOne(DaysScreen):
    key = "day_1"
    ctg_plus = "plus_dayOne"
    ctg_workout = "workout_dayOne"
    
# Screen Day 2
class SoloDayTwo(DaysScreen):
    key = "day_2"
    ctg_plus = "plus_dayTwo"
    ctg_workout = "workout_dayTwo"

# Screen Day 3
class SoloDayThree(DaysScreen):
    key = "day_3"
    ctg_plus = "plus_dayThree"
    ctg_workout = "workout_dayThree"

# Main App    
class SoloApp(App):

    exp = NumericProperty(0)
    max_exp = NumericProperty (200)
    level = NumericProperty(1)

    centerY = NumericProperty(0.9)

    # Loading level and experience when we start the app
    def on_start(self):
        data_path = os.path.join(self.user_data_dir, 'data.json')
        self.store = JsonStore(data_path)
        load_level(self)

    # Saving our progress (level, experience) in file 'data.json'
    def on_stop(self):
        save_level(self)

    # Screens    
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