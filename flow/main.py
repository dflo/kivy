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
from kivy.clock import Clock
from kivy.properties import ListProperty

Config.set('graphics', 'width', '400') # change to 1200 for Nexus 7
Config.set('graphics', 'height', '640') # change to 1920 for Nexus 7

# root of the app
root = None
# color values in stupid decimal
clear = (0,0,0,0)
red = (1,0,0,1)
orange = (1,0.5,0,1)
yellow = (1,1,0,1)
green = (0,0.4,0,1)
blue = (0,0,1,1)
purple = ()
cyan = ()
pink = ()
colors = [clear, red, orange, yellow, green, blue, purple, cyan, pink]
# board file names
board0 = 'testboard0.txt'
board1 = 'testboard1.txt'
board2 = 'testboard2.txt'
board3 = 'testboard3.txt'
board4 = 'testboard4.txt'
board5 = 'testboard5.txt'
board6 = 'testboard6.txt'
boards = [board0, board1, board2, board3, board4, board5, board6]
place = 0
# Other vars
num_of_pipes = 0
score = 'Score: 0'
attempts = 0
saved_board = None
saved_children = []
pipes_visted = 0

def change_board():
    global place 
    place = (place + 1) % len(boards)
    root.flowgame.open_board(boards[place])


def save_game():
    global saved_board
    saved_board = (place - 1) % len(boards)
    for child in root.flowgame.children:
        saved_children.append(child)



def load_game():
    global place
    if saved_board != None:
        place = saved_board
        change_board()
        root.flowgame.clear_widgets()
        for i in range(len(saved_children) - 1, -1, -1):
            child = saved_children[i]
            root.flowgame.add_widget(child)
            


def update_prev_shape(touch):
    if touch.prev.shape[0] == None or touch.prev.shape[1] == None:
        pass
    elif touch.prev.shape[0] == touch.prev.shape[1]:
        if touch.prev.shape[0] % 2 == 0:
            touch.prev.color_tb = touch.prev.leader.color
        else:
            touch.prev.color_lr = touch.prev.leader.color
    elif touch.prev.shape[0] + touch.prev.shape[1] == 3:
        if touch.prev.shape[0] < touch.prev.shape[1]:
            touch.prev.color_tr = touch.prev.leader.color
        else:
            touch.prev.color_bl = touch.prev.leader.color
    else:
        if touch.prev.shape[0] == 2 or touch.prev.shape[0] == 1:
            touch.prev.color_br = touch.prev.leader.color
        else:
            touch.prev.color_tl = touch.prev.leader.color


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
        self.shape = [None,None]

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # if this tile has pipe group and has been
            # click on reset their colors
            if len(self.group) != 0:
                self.clear_group(0)
            # create touch.prev to be ourself
            # and a list of our group we paint
            touch.prev = self
            touch.origin = self
 
    def on_touch_up(self, touch):
        global score
        global attempts
        if self.collide_point(*touch.pos) and self.parent.collide_point(*touch.opos):
            if (touch.origin.color == self.color) and (touch.origin != self):
                # add the move made to shape list of previous node
                touch.prev.shape[1] = touch.prev.cardinal.index(self)
                print 'previous shape', touch.prev.shape
                # complete a pipe
                print('congrats on connecting one pipe')
                update_prev_shape(touch)
                attempts += 1
                self.parent.completion.append(self.color)
                score = 'Score: %.2f' %(100 * (len(self.parent.completion) / float(num_of_pipes)) * (num_of_pipes - abs(num_of_pipes - attempts)))
                print score
                root.menubar.label_score.text = score
                print 'target', len(self.parent.array) - 2 * num_of_pipes
                print 'current', pipes_visted
                if len(self.parent.completion) == num_of_pipes and (len(self.parent.array) - 2 * num_of_pipes == pipes_visted):
                    print('Game complete!')
                    self.parent.msg.open()
                self.group = touch.origin.group
                self.sibling = touch.origin

    def clear_group(self, index):
        global pipes_visted
        for i in range(index, len(self.group)):
            item = self.group[i]
            if (item.leader == self) or (item.leader == self.sibling):
                item.color_bc = clear
                item.color_lc = clear
                item.color_tc = clear
                item.color_rc = clear
                item.color_tb = clear
                item.color_lr = clear
                item.color_tl = clear
                item.color_tr = clear
                item.color_bl = clear
                item.color_br = clear
                item.visited = 0
                item.leader = None
                pipes_visted -= 1
        if self.color in self.parent.completion:
            self.parent.completion.remove(self.color)
        self.group = self.group[:index]
        if self.sibling:
            self.sibling.group = []


class Pipe(Button):
    color_bc = ListProperty([0,0,0,0])
    color_lc = ListProperty([0,0,0,0])
    color_tc = ListProperty([0,0,0,0])
    color_rc = ListProperty([0,0,0,0])
    color_tb = ListProperty([0,0,0,0])
    color_lr = ListProperty([0,0,0,0])
    color_tl = ListProperty([0,0,0,0])
    color_tr = ListProperty([0,0,0,0])
    color_bl = ListProperty([0,0,0,0])
    color_br = ListProperty([0,0,0,0])

    def __init__(self, **kwargs):
        super(Pipe, self).__init__(**kwargs)
        self.leader = None
        self.east = None
        self.west = None
        self.north = None
        self.south = None
        self.cardinal = []
        self.visited = 0
        self.shape = [None,None]

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.leader: 
                self.leader.clear_group(self.leader.group.index(self) + 1)
                # clear coloring
                self.color_bc = clear
                self.color_lc = clear
                self.color_tc = clear
                self.color_rc = clear
                self.color_tb = clear
                self.color_lr = clear
                self.color_tl = clear
                self.color_tr = clear
                self.color_bl = clear
                self.color_br = clear
                # update coloring 
                self.update_curr_shape
                touch.origin = self.leader
                touch.prev = self
            else:
                touch.origin = None
                touch.prev = None

    def on_touch_move(self, touch):
        global pipes_visted
        if self.collide_point(*touch.pos) and self.parent.collide_point(*touch.opos):
            # check if we're a cardinal position from the touch
            # AND check if we haven't been colored already to avoid backtracking
            if touch.prev and (self in touch.prev.cardinal) and (self.visited == 0):
                # we're in the cardinal position of a prev touch
                # if there is a prev and it's not our current leader
                # assign our leader to it and append ourselves to its
                # list of group. Change our color to match the prev
                if touch.prev != self.leader:
                    self.leader = touch.origin
                    self.leader.group.append(self)
                    self.color_ce = self.leader.color
                    self.visited = 1
                    pipes_visted += 1
                    # add the move made to shape list of previous node
                    touch.prev.shape[1] = touch.prev.cardinal.index(self)
                    update_prev_shape(touch)
                    # add the move made to shape list of current node
                    self.shape[0] = touch.prev.cardinal.index(self)
                    self.update_curr_shape()
                    # print 'current shape', self.shape
                    # update previous node of touch
                    touch.prev = self

    def update_curr_shape(self):
        if self.shape[0] == 3:
            self.color_rc = self.leader.color
        elif self.shape[0] == 2:
            self.color_tc = self.leader.color
        elif self.shape[0] == 1:
            self.color_lc = self.leader.color
        elif self.shape[0] == 0:
            self.color_bc = self.leader.color


class FlowGame(GridLayout):
    def __init__(self, **kwargs):
        super(FlowGame, self).__init__(**kwargs)
        # initializations
        self.board_width = 0
        self.array = []
        self.completion = []
        self.open_board(boards[place])
        self.msg = self.pop_up()

    def open_board(self, board):
        global num_of_pipes
        global score
        global attempts
        global pipes_visted
        # try to open board file
        try:
            fin = open(board, "r")
        except IOError as e:
            print("Error! Could not open input file!", e)
            exit(1)
        # remove children
        self.clear_widgets()
        self.array = []
        self.completion = []
        num_of_pipes = 0
        pipes_visted = 0
        score = 'Score: 0'
        attempts = 0
        # create board
        for line in fin:
            line = line.strip()
            line = line.split(',')
            self.board_width = len(line)
            # reset # of columns
            self.cols = self.board_width
            for value in line:
                if value != '0':
                    btn = Tile(color=colors[int(value)])
                    if int(value) > num_of_pipes:
                        num_of_pipes = int(value)
                else:
                    btn = Pipe(color=colors[int(value)])
                self.add_widget(btn)
                self.array.append(btn)
        self.set_parameters()
        fin.close()
        
    def set_parameters(self):
        # place all the widgets in an array and use
        # indexes to locate adjacent widgets
        for i in range(0, len(self.array)):
            if (i - self.board_width) >= 0:
                self.array[i].north = self.array[i - self.board_width]
            if ((i + 1) % self.board_width) != 0:
                self.array[i].east = self.array[i + 1]
            if (i + self.board_width) <= len(self.array) - 1:
                self.array[i].south = self.array[i + self.board_width]
            if ((i - 1) % self.board_width) != self.board_width - 1:
                self.array[i].west = self.array[i - 1]
        for node in self.array:
            node.cardinal = [node.north, node.east, node.south, node.west]

    # Completion pop up msg
    def pop_up(self):
        layout = GridLayout(cols=1)
        layout.add_widget(Label(text="[b]You've Completed the Board!!![/b]", markup=True, font_size=15, size_hint=(0.5,0.5)))
        btn_done = Button(text='Exit', size_hint_y=0.15)
        btn_play = Button(text='Play Again', size_hint_y=0.15)
        btn_done.bind(on_release=exit)
        btn_play.bind(on_release=lambda widget: change_board())
        layout.add_widget(btn_done)
        layout.add_widget(btn_play)
        pop_up_msg = Popup(title='Congradulations!!!', markup=True, halign='center', content=layout, size_hint=(0.66,0.5))
        btn_play.bind(on_press=pop_up_msg.dismiss)
        return pop_up_msg

class MenuBar(StackLayout):
    def __init__(self, **kwargs):
        super(MenuBar, self).__init__(**kwargs)
        
    def buttons(self):
        global score
        # Label with Score
        self.label_score = Label(text=score, size_hint_x=0.25)
        self.add_widget(self.label_score)
        # Button to Change board
        btn_change = Button(text='New Game', size_hint_x=0.25)
        btn_change.bind(on_release=lambda widget: change_board())
        self.add_widget(btn_change)
        # Button to Save/Load a game
        btn_save_load = Button(text='Save/Load', size_hint_x=0.25)
        save_load_msg = self.pop_up()
        btn_save_load.bind(on_press=save_load_msg.open)
        self.add_widget(btn_save_load)
        # Button to exit the game
        btn_exit = Button(text='Exit', size_hint_x=0.15)
        btn_exit.bind(on_release=exit)
        self.add_widget(btn_exit)
    
    # Popup msg to Save/Load game
    def pop_up(self):
        layout = GridLayout(cols=1)
        layout.add_widget(Label(text="[b]What would you like to do?[/b]", markup=True, font_size=15, size_hint=(0.5,0.5)))
        btn_save = Button(text='Save Game', size_hint_y=0.15)
        btn_load = Button(text='Load Game', size_hint_y=0.15)
        btn_save.bind(on_press=lambda widget: save_game())
        btn_load.bind(on_press=lambda widget: load_game())
        layout.add_widget(btn_save)
        layout.add_widget(btn_load)
        save_load_msg = Popup(title='Save/Load Games', markup=True, content=layout, size_hint=(0.66,0.5))
        btn_save.bind(on_release=save_load_msg.dismiss)
        btn_load.bind(on_release=save_load_msg.dismiss)
        return save_load_msg
    

class AppBackground(StackLayout):
    pass


class FlowApp(App):
    def build(self):
        global root
        root = AppBackground()
        root.add_widget(Label(text='[b]Flow Game[/b]', markup=True, font_size=15, size_hint_y=0.1))
        root.menubar = MenuBar(size_hint_y=0.1, padding=15, orientation='lr-tb')
        root.add_widget(root.menubar)
        root.flowgame = FlowGame(size_hint_y=0.625)
        root.add_widget(root.flowgame)
        root.add_widget(Label(text='[b]Created by DFLO[/b]', markup=True, font_size=20, size_hint_y=0.175))
        root.menubar.buttons()
        return root

if __name__ == '__main__':
    FlowApp().run()
