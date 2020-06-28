

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


    for part in content[1:]:
        gobj = create_gobj(part)
        if gobj:
            gobjs.append(gobj)
    
    write_py_file(win_name, dim_win, gobjs)

def create_gobj(string):
    string = string.split('\n')[1:-1]
    if string:
        dim = string[2].split(' ')
        dim = (int(dim[0]), int(dim[1]))
        pos = string[3].split(' ')
        pos = (int(pos[0]), int(pos[1]))

        # check if color is str or tuple
        if string[5].find('[') == -1:
            color = 'C.' + string[5]
        else:
            color = string[5]

        gobj = {'name':string[0], 'objtype':string[1], 'dim':dim, 'pos':pos,
                'text':string[4], 'color':color, 'font':string[6]}
        return gobj

def write_py_file(win_name, dim, gobjs):
    obj_name = win_name[0].upper() + win_name[1:]
    content = f'''
from interface import Interface, TextBox, Cadre, Font, C, Button, InputText, Form
import pygame

class {obj_name}:
    def __init__(self, pos):
        self.cadre = Cadre(({dim[0]}, {dim[1]}), pos, C.WHITE)
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
            string = f'        self.text_{name} = TextBox(({dim[0]}, {dim[1]}), (pos[0]+{pos[0]},pos[1]+{pos[1]}), {color},"{text}",font=Font.f({font}))'
            py_names.append(f'text_{name}')

        elif gobj['objtype'] == 'Button':
            string = f'        self.button_{name} = Button(({dim[0]}, {dim[1]}), (pos[0]+{pos[0]},pos[1]+{pos[1]}), {color}, "{text}",font=Font.f({font}))'
            py_names.append(f'button_{name}')
        
        elif gobj['objtype'] == 'InputText':
            string = f'        self.input_{name} = InputText(({dim[0]}, {dim[1]}), (pos[0]+{pos[0]},pos[1]+{pos[1]}), {color},text="{text}",font=Font.f({font}))'
            py_names.append(f'input_{name}')
        
        elif gobj['objtype'] == 'Cadre':
            string = f'        self.cadre_{name} = Cadre(({dim[0]}, {dim[1]}), (pos[0]+{pos[0]},pos[1]+{pos[1]}), {color})'
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