class Window:
    def __init__(self, name, dim):
        self.name = name
        self.dim = list(dim)

SEPARATOR = '/'

def create_py_file(path):
    with open(path, 'r') as file:
        content = file.read()
    # first split by separator
    content = content.split(SEPARATOR)
    # get global infos
    global_infos = content[0].strip().replace('\n','').split(' ')
    win_name = global_infos[0]
    dim_win = (int(global_infos[1]), int(global_infos[2]))

    gobjs = []

    print(win_name, dim_win)

    for part in content[1:]:
        gobj = create_gobj(part)
        if gobj:
            gobjs.append(gobj)
    
    print(gobjs)
    write_py_file(win_name, dim_win, gobjs)

def create_gobj(string):
    string = string.split('\n')[1:-1]
    if string:
        dim = string[2].split(' ')
        dim = (int(dim[0]), int(dim[1]))
        pos = string[3].split(' ')
        pos = (int(pos[0]), int(pos[1]))
        gobj = {'name':string[0], 'objtype':string[1], 'dim':dim, 'pos':pos,
                'text':string[4], 'color':string[5], 'font':string[6]}
        return gobj

def write_py_file(win_name, dim, gobjs):
    obj_name = win_name[0].upper() + win_name[1:]
    content = f'''
from base import TextBox, Cadre, Font, C, Button, dim, InputText, E, scale, Form, screen
import pygame

class {obj_name}:
    def __init__(self, pos):
        self.cadre = Cadre((E({dim[0]}), E({dim[1]})), C.WHITE, pos)
'''
    py_names = []
    for gobj in gobjs:
        name = gobj['name']
        dim = gobj['dim']
        color = gobj['color']
        pos = gobj['pos']
        text = gobj['text']
        font = gobj['font']

        if gobj['objtype'] == 'TextBox':
            string = f'        self.text_{name} = TextBox((E({dim[0]}), E({dim[1]})), C.{color}, (pos[0]+E({pos[0]}),pos[1]+E({pos[1]})),"{text}",font=Font.{font})'
            py_names.append(f'text_{name}')

        elif gobj['objtype'] == 'Button':
            string = f'        self.button_{name} = Button((E({dim[0]}), E({dim[1]})), C.{color}, (pos[0]+E({pos[0]}),pos[1]+E({pos[1]})),"{text}",font=Font.{font})'
            py_names.append(f'button_{name}')
        
        elif gobj['objtype'] == 'InputText':
            string = f'        self.input_{name} = InputText((E({dim[0]}), E({dim[1]})), (pos[0]+E({pos[0]}),pos[1]+E({pos[1]})), C.{color},text="{text}",font=Font.{font})'
            py_names.append(f'input_{name}')
        
        elif gobj['objtype'] == 'Cadre':
            string = f'        self.cadre_{name} = Cadre((E({dim[0]}), E({dim[1]})), C.{color}, (pos[0]+E({pos[0]}),pos[1]+E({pos[1]})))'
            py_names.append(f'cadre_{name}')
        
        content += string + '\n'

    # create display func
    content += '\n    def display(self):\n        self.cadre.display()\n'

    for pyname in py_names:
        content += f'        self.{pyname}.display()\n'

    #create react func
    content += '\n    def react_events(self, events, pressed):\n'

    for gobj in gobjs:
        if gobj['objtype'] == 'Button':
            name = gobj['name']
            content += f'        if self.button_{name}.pushed(events):\n            pass\n'
        elif gobj['objtype'] == 'InputText':
            name = gobj['name']
            content += f'        self.input_{name}.run(events, pressed)\n'


    with open(win_name+'.py', 'w') as file:
        file.write(content)