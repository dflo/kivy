import kivy
kivy.require('1.7.2') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.config import Config
from kivy.graphics import Color, Ellipse
from kivy.properties import NumericProperty
from kivy.uix.popup import Popup

Config.set('graphics', 'width', '400') # change to 1200 for Nexus 7
Config.set('graphics', 'height', '640') # change to 1920 for Nexus 7

try:
    fin = open('board01', "r")
except IOError as e:
    print("Error! Could not open input file!", e)
    exit(1)


class Tile(Button):
    def __init__(self, **kwargs):
        super(Tile, self).__init__(**kwargs)
        self.group = []
        self.sibling = None
        self.east = None
        self.west = None
        self.north = None
        self.south = None
        self.cardinal = []

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # if this tile has pipe group and has been
            # click on reset their colors
            if len(self.group) != 0:
                for item in self.group:
                    if (item.leader == self) or (item.leader == self.sibling):
                        item.color = (0,0,0,0)
                        item.visited = 0
                        item.leader = None
                self.parent.completion -= 1
                self.group = []
                if self.sibling:
                    self.sibling.group = []
            # create touch.prev to be ourself
            # and a list of our group we paint
            touch.prev = self
            touch.origin = self
            # self.group = [] don't think I need this anymore 
    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if (touch.origin.color == self.color) and (touch.origin != self):
                # complete a pipe
                print('congrats on connecting one pipe')
                self.parent.completion += 1
                if self.parent.completion == 5:
                    print('Game complete!')
                    self.parent.msg.open()
                self.group = touch.origin.group
                self.sibling = touch.origin
                # touch.origin.sibling = self ???


class Pipe(Button):
    def __init__(self, **kwargs):
        super(Pipe, self).__init__(**kwargs)
        self.leader = None
        self.east = None
        self.west = None
        self.north = None
        self.south = None
        self.cardinal = []
        self.visited = 0

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.leader:
                touch.origin = self.leader
                touch.prev = self
            else:
                touch.origin = None
                touch.prev = None

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            # check if we're a cardinal position from the touch
            # AND check if we haven't been colored already to avoid backtracking
            if (self in touch.prev.cardinal) and (self.visited == 0):
                # we're in the cardinal position of prev touch
                # print 'In cardinal position'
                # if there is a prev and it's not our current leader
                # assign our leader to it and append ourselves to its
                # list of group. Change our color to match the prev
                if touch.prev and (touch.prev != self.leader):
                    # if self.parent and (touch.prev != self.parent):
                    #     print('remove this child from parent')
                    self.leader = touch.origin
                    self.leader.group.append(self)
                    self.color = self.leader.color
                    self.visited = 1
                    touch.prev = self
            else:
                pass
                # print 'NOT in cardinal position'
                # we're not


class FlowGame(GridLayout):
    def __init__(self, **kwargs):
        super(FlowGame, self).__init__(**kwargs)
        layout = GridLayout(cols=1)
        layout.add_widget(Label(text="[b]You've Completed the Game!!![/b]", markup=True, font_size=15, size_hint=(0.5,0.5)))
        btn = Button(text='Done', size_hint_y=0.15)
        btn.bind(on_release=exit)
        layout.add_widget(btn)
        self.msg = Popup(title='Congradulations!!!', markup=True, halign='center', content=layout, auto_dismiss=False, size_hint=(0.66,0.5))

        self.array = []
        self.completion = 0
        for line in fin:
            line = line.rstrip()
            line = line.split(',')
            for value in line:
                if value == '1':
                    btn = Tile(color=(1,0,0,1))
                elif value == '2':
                    btn = Tile(color=(1,0.5,0,1))
                elif value == '3':
                    btn = Tile(color=(1,1,0,1))
                elif value == '4':
                    btn = Tile(color=(0,0.4,0,1))
                elif value == '5':
                    btn = Tile(color=(0,0,1,1))
                else:
                    btn = Pipe(color=(0,0,0,0))
                self.add_widget(btn)
                self.array.append(btn)
        self.set_parameters()


    def set_parameters(self):
        # place all the widgets in an array and use
        # indexes to locate adjacent widgets
        for i in range(0, len(self.array)):
            if ((i + 1) % 5) != 0:
                self.array[i].east = self.array[i + 1]
            if (i + 5) <= 24:
                self.array[i].west = self.array[i + 5]
            if ((i - 1) % 5) != 4:
                self.array[i].north = self.array[i - 1]
            if (i - 5) >= 0:
                self.array[i].south = self.array[i - 5]
        for node in self.array:
            node.cardinal = [node.east, node.west, node.north, node.south]


class MenuBar(StackLayout):
    def __init__(self, **kwargs):
        super(MenuBar, self).__init__(**kwargs)
        btn = Button(text='Exit', size_hint_x=0.15)
        btn.bind(on_release=exit)
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
