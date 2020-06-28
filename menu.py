from interface import TextBox, Cadre, Font, C, Button, InputText
from window import create_py_file
from editor import Editor

DIM_INPDIM = (150, 60)
DIM_INPNAME = (300, 60)
DIM_BDONE = (120, 60)
DIM_CREATE = (600, 400)

class Window:
    def __init__(self, name, dim):
        self.name = name
        self.dim = list(dim)

class NewWindow:
    def __init__(self, pos):
        self.dim = (800, 600)
        self.pos = list(pos)
        self.cadre = Cadre(self.dim, pos, C.WHITE,set_transparent=True)
        self.text_newwindow = TextBox((self.dim[0],80), pos, C.WHITE,'New Window')
        self.text_dim = TextBox((400,60), (pos[0]+200, pos[1] + 150), C.WHITE,
                     "Enter window dimension", font=Font.f(30))
        self.input_x = InputText(DIM_INPDIM, (pos[0]+210, pos[1]+250),C.WHITE, text='1000', limit=4)
        self.input_y = InputText(DIM_INPDIM, (pos[0]+410, pos[1]+250),C.WHITE, text='1000', limit=4)
        self.text_name = TextBox((150,60), (pos[0]+100, pos[1] + 350), C.WHITE,'File name:', font=Font.f(30))
        self.input_name = InputText(DIM_INPNAME, (pos[0]+300, pos[1]+350),C.WHITE)
        self.button_done = Button(DIM_BDONE, (pos[0]+650,pos[1]+500), C.LIGHT_BLUE,'Done',font=Font.f(30))

    def react_events(self, events, pressed):
        self.input_x.run(events, pressed)
        self.input_y.run(events, pressed)
        self.input_name.run(events, pressed)
            
    def create_windows(self):
        try:
            x = int(self.input_x.content)
            y = int(self.input_y.content)
            if x > 3000 or y > 1600:
                print('Wrong coord')
                return
            name = self.input_name.content
        except: 
            print('Wrong coord')
            return
        new_win = Window(name, (x,y))
        return new_win    

    def display(self):
        self.cadre.display()
        self.text_newwindow.display()
        self.text_dim.display()
        self.input_x.display()
        self.input_y.display()
        self.text_name.display()
        self.input_name.display()
        self.button_done.display()

class CreatePy:
    state = 'wait'
    def __init__(self, dim, pos):
        self.cadre = Cadre(dim, pos,C.WHITE)
        self.text_create = TextBox(DIM_INPNAME, (pos[0]+40, pos[1]+100), C.WHITE,'Create a python file?', font=Font.f(30))
        self.button_yes = Button(DIM_BDONE, (pos[0]+40, pos[1]+180), C.LIGHT_GREEN,'Yes', font=Font.f(30))
        self.button_no = Button(DIM_BDONE, (pos[0]+200, pos[1]+180), C.LIGHT_RED,'No', font=Font.f(30))
    
    def display(self):
        self.cadre.display()
        self.button_yes.display()
        self.button_no.display()
        self.text_create.display()
    
    def react_events(self, events, pressed):
        if self.button_yes.pushed(events):
            self.state = 'yes'
        elif self.button_no.pushed(events):
            self.state = 'no'

class Menu:
    state = 'start'
    new_window = NewWindow((1100, 500))
    create_window = CreatePy(DIM_CREATE, (1100, 500))
    def run(self, events, pressed):
        if self.state == 'start':
            self.run_start(events, pressed)
        elif self.state == 'main':
            Editor.display()
            Editor.react_events(events, pressed)
            if Editor.state == 'done':
                self.state = 'done'
        elif self.state == 'done':
            self.create_window.display()
            self.create_window.react_events(events, pressed)
            if self.create_window.state == 'yes':
                create_py_file(f'{Editor.window.name}.pygui')
                self.state = 'end'
            elif self.create_window.state == 'no':
                self.state = 'end'


    def run_start(self, events, pressed):
        self.new_window.display()
        self.new_window.react_events(events, pressed)
        if self.new_window.button_done.pushed(events):
            self.state = 'main'
            win = self.new_window.create_windows()
            Editor.set_window(win)
    
