from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.button import Button

def save_exercise(self, ctg_workout, ctg_plus):
    exercise_list = []
    for widget in list(self.children):
        if isinstance(widget, TextInput):
            exercise_list.append(widget.text)
    for widget in list(self.children):
            if hasattr(widget, 'exercise'):
                self.remove_widget(widget)
    app=App.get_running_app()
    y = self.buttonPlus.pos_hint.get('center_y')
    app.store.put(ctg_workout, exercises=exercise_list)
    app.store.put(ctg_plus, plus_x = 0.5, plus_y = y)

def load_exercise(self, ctg_workout, ctg_plus):
        app=App.get_running_app()
        app.centerY = 0.9
        if app.store.exists(ctg_workout):
            if app.store.exists(ctg_plus):
                x = app.store.get(ctg_plus)['plus_x']
                if app.store.get(ctg_plus)['plus_y'] is None:
                    y = 0.2
                    app.store.put(ctg_plus, plus_x = 0.5, plus_y = 0.2)
                else:
                    y = app.store.get(ctg_plus)['plus_y']
            exercise_list = app.store.get(ctg_workout)
            for exercise in reversed(exercise_list['exercises']):
                self.text_input = TextInput(text=exercise,
                                            size_hint=(.7,.06),
                                            pos_hint={'center_x':.45,'center_y':app.centerY},
                                            font_size=20,
                                            foreground_color=(0.2, 0.8, 1, 1),
                                            background_color=[0,0,0,1],
                                            multiline=False)
                self.text_input.exercise = True
                self.add_widget(self.text_input)
                
                self.buttonDone = Button(text="DONE", 
                                    size_hint=(.1,.06),
                                    pos_hint={'center_x':.85,'center_y':app.centerY},
                                    font_size=25,
                                    font_name='./fonts/BebasNeue-Regular.ttf',
                                    color=(0.2, 0.8, 1, 1),
                                    background_color=[0.05,0.05,0.05,1])
                self.buttonDone.exercise = True
                self.buttonDone.bind(on_release=self.press_exp)    
                self.add_widget(self.buttonDone)
                
                app.centerY -= 0.07

                self.buttonPlus.pos_hint={'center_x': x, 'center_y':y}

            if self.buttonPlus.pos_hint.get('center_y')<=0.2:  
                self.buttonPlus.pos_hint={'center_x':10}
            self.do_layout()

def save_level(self):
    self.store.put('user_stats', level=self.level, exp=self.exp, maxexp=self.max_exp)

def load_level(self):
    if self.store.exists('user_stats'):
        stats = self.store.get('user_stats')
        self.level = stats['level']
        self.exp = stats['exp']
        self.max_exp = stats['maxexp']