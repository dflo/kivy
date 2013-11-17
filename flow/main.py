import kivy
kivy.require('1.7.2') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.config import Config
from kivy.graphics import Color, Ellipse
from kivy.properties import NumericProperty

Config.set('graphics', 'width', '400') # change to 1200 for Nexus 7
Config.set('graphics', 'height', '640') # change to 1920 for Nexus 7

try:
    fin = open('board01', "r")
except IOError as e:
    print "Error! Could not open input file!" + e

class Tile(Button):
    def __init__(self, **kwargs):
        super(Tile, self).__init__(**kwargs)
        self.d = self.width * .6
        self.type = self.font_size
        with self.canvas:
            if self.type == 1:
                Color(1,0,0,1,mode='rgba')
            elif self.type == 2:
                Color(1,0.50,0,1,mode='rgba')
            elif self.type == 3:
                Color(1,1,0,1,mode='rgba')
            elif self.type == 4:
                Color(0,0.4,0,1,mode='rgba')
            elif self.type == 5:
                Color(0,0,1,1,mode='rgba')
            else:
                Color(0,0,0,0,mode='rgba')
            self.ellipse = Ellipse(pos=self.pos, size=(self.d,self.d))

        self.bind(pos=self.redraw)
        self.bind(size=self.redraw)

    def redraw(self, *args):
        self.ellipse.pos = (self.center_x - self.d/2, self.center_y - self.d/2)

class FlowGame(GridLayout):
    def __init__(self, **kwargs):
        super(FlowGame, self).__init__(**kwargs)
        for line in fin:
            line = line.rstrip()
            line = line.split(',')
            for value in line:
                    btn = Tile(font_size=int(value), background_color=(0.3,0.3,0.3,0.3))
                    self.add_widget(btn)

class MenuBar(StackLayout):
    def __init__(self, **kwargs):
        super(MenuBar, self).__init__(**kwargs)
        btn = Button(text='Exit', size_hint_x=0.15)
        btn.bind(on_press=exit)
        self.add_widget(btn)

class AppBackground(StackLayout):
    pass

class FlowApp(App):
    def build(self):
        root = AppBackground()
        root.add_widget(Label(text='[b]Flow Game[/b]', markup=True, font_size=15, size_hint_y=0.1))
        root.add_widget(MenuBar(size_hint_y=0.1, padding=15, orientation='rl-tb'))
        root.add_widget(FlowGame(size_hint_y=0.625))
        root.add_widget(Label(text='[b]Created by DFLO[/b]', markup=True, font_size=20, size_hint_y=0.175))
        return root

if __name__ == '__main__':
    FlowApp().run()
