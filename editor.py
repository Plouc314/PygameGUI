from base import TextBox, Cadre, Font, C, Button, dim, InputText, E, windows, scale, Form, screen
from settings import Settings
import pygame

DIM_TOOLS = scale((400, 80))
DIM_DRAG = scale((200,60))
DIM_BDONE = scale((120, 60))
DIM_CORNER = scale((15,15))
POS_TY = E(200)
POS_WIN = scale((600, 200))

SEPARATOR = '/'

class DragSurf(Form):
    def __init__(self, pos, color, objtype):
        super().__init__(DIM_DRAG, color)
        self.pos = list(pos)
        self.objtype = objtype
    
    def run(self):
        pos = pygame.mouse.get_pos()
        self.display(pos)

class GuiObj(Button):
    changing_dim = False
    chan_dim_corner = None
    name = ''
    fontname = 'f25'
    color = 'WHITE'

    def __init__(self, pos, color, objtype):
        super().__init__(DIM_DRAG, color, pos)
        self.set_corners(pos, DIM_DRAG)
        self.pos = list(pos)
        self.objtype = objtype
        self.input_text = InputText(DIM_DRAG, pos, C.WHITE, font=Font.f25, centered=True)
        self.selected = True
        self.SELECT_COLOR = C.BLUE
        self.set_corners_points()

        if self.objtype == 'TextBox' or self.objtype == 'Button':
            self.can_input = True
        else:
            self.can_input = False
    
    def get_real_pos(self):
        return (self.pos[0]-POS_WIN[0], self.pos[1]-POS_WIN[1])

    def set_corners_points(self):
        corner = Button(DIM_CORNER, C.BLUE, (0,0))
        corner.MARGE_WIDTH = E(3)
        self.CTOPLEFT = corner
        self.CTOPLEFT.set_pos(self.TOPLEFT, center=True)

        corner = Button(DIM_CORNER, C.BLUE, (0,0))
        corner.MARGE_WIDTH = E(3)
        self.CTOPRIGHT = corner
        self.CTOPRIGHT.set_pos(self.TOPRIGHT, center=True)
        
        corner = Button(DIM_CORNER, C.BLUE, (0,0))
        corner.MARGE_WIDTH = E(3)
        self.CBOTTOMRIGHT = corner
        self.CBOTTOMRIGHT.set_pos(self.BOTTOMRIGHT, center=True)

        corner = Button(DIM_CORNER, C.BLUE, (0,0))
        corner.MARGE_WIDTH = E(3)
        self.CBOTTOMLEFT = corner
        self.CBOTTOMLEFT.set_pos(self.BOTTOMLEFT, center=True)

        self.corners_points = [self.CTOPLEFT, self.CTOPRIGHT, self.CBOTTOMLEFT, self.CBOTTOMRIGHT]

    def set_new_dim_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.chan_dim_corner == 0:
            pos = mouse_pos
            dim = [self.TOPRIGHT[0] -mouse_pos[0], self.BOTTOMLEFT[1] - mouse_pos[1]]
        elif self.chan_dim_corner == 1:
            pos = [self.pos[0], mouse_pos[1]]
            dim = [mouse_pos[0] - self.TOPLEFT[0], self.BOTTOMLEFT[1] - mouse_pos[1]]
        elif self.chan_dim_corner == 2:
            pos = [mouse_pos[0], self.pos[1]]
            dim = [self.BOTTOMRIGHT[0] - mouse_pos[0], mouse_pos[1] - self.TOPLEFT[1]]
        elif self.chan_dim_corner == 3:
            pos = self.pos
            dim = [mouse_pos[0] - self.TOPLEFT[0], mouse_pos[1] - self.TOPLEFT[1]]
        
        # change text in setting
        Settings.input_coordx.set_text(str(pos[0]))
        Settings.input_coordy.set_text(str(pos[1]))
        Settings.input_dimx.set_text(str(dim[0]))
        Settings.input_dimy.set_text(str(dim[1]))

        self.set_new_dim(dim, pos)

    def set_new_dim(self, dim, pos):
        self.set_dim_pos(dim, pos)
        self.input_text.set_dim_pos(dim, pos)
        self.set_corners_points()

    def set_select_color(self, color):
        self.SELECT_COLOR = color
        for cp in self.corners_points:
            cp.set_color(color, marge=True)

    def display(self):
        super().display()
        self.input_text.display()

        if self.selected:
            pygame.draw.line(screen, self.SELECT_COLOR, self.BOTTOMLEFT, self.BOTTOMRIGHT, E(3))
            pygame.draw.line(screen, self.SELECT_COLOR, self.TOPLEFT, self.TOPRIGHT, E(3))
            pygame.draw.line(screen, self.SELECT_COLOR, self.TOPLEFT, self.BOTTOMLEFT, E(3))
            pygame.draw.line(screen, self.SELECT_COLOR, self.TOPRIGHT, self.BOTTOMRIGHT, E(3))
            for cp in self.corners_points:
                cp.display()

    def react_events(self, events, pressed):
        
        self.as_change_dim = False

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.changing_dim:
                    try:
                        self.set_new_dim_mouse()
                    except:
                        print('Error in setting new dim')
                    
                    self.changing_dim = False
                    self.set_select_color(C.BLUE)
                    self.as_change_dim = True
        
        if not self.as_change_dim: # bool value to avoid reselect instantly
            for i, cp in enumerate(self.corners_points):
                if cp.pushed(events):
                    self.chan_dim_corner = i
                    self.changing_dim = True
                    self.set_select_color(C.GREEN)
        
        if self.selected and self.can_input:
            self.input_text.run(events, pressed)
    
        
class Editor:
    # tools
    button_text_box = Button(DIM_TOOLS, C.XLIGHT_GREY, (0, POS_TY), 'TextBox')
    button_button = Button(DIM_TOOLS, C.XLIGHT_GREY, (0, POS_TY+E(80)), 'Button')
    button_input_text = Button(DIM_TOOLS, C.XLIGHT_GREY, (0, POS_TY+E(160)), 'InputText')
    button_cadre = Button(DIM_TOOLS, C.XLIGHT_GREY, (0, POS_TY+E(240)), 'Cadre')
    button_done = Button(DIM_BDONE, C.LIGHT_BLUE, (E(2800), E(1400)), 'Done',font=Font.f30)
    drag_surf = None
    objs = []
    state = 'running'

    current_selected = None

    @classmethod
    def set_window(cls, window):
        cls.window = window
        dim = window.dim#(int(window.dim[0]*3/4), int(window.dim[1]*3/4))
        cls.cadre = Cadre(dim, C.WHITE, POS_WIN)
        cls.TOP_LEFT = [POS_WIN[0], POS_WIN[1]]
        cls.TOP_RIGHT = [POS_WIN[0] + dim[0], POS_WIN[1]]
        cls.BOTTOM_LEFT = [POS_WIN[0], POS_WIN[1] + dim[1]]
        cls.BOTTOM_RIGHT = [POS_WIN[0] + dim[0], POS_WIN[1] + dim[1]] 

    @classmethod
    def create_obj(cls, pos, objtype):
        gui_obj = GuiObj(pos, C.WHITE, objtype)
        cls.objs.append(gui_obj)
        cls.current_selected = gui_obj
        Settings.set_obj(gui_obj)

    @classmethod
    def check_deselect(cls):
        if cls.current_selected:
            if cls.cadre.on_it() and not cls.current_selected.as_change_dim:
                if not cls.current_selected.changing_dim and not cls.current_selected.on_it():
                    return True
        return False

    @classmethod
    def check_done(cls):
        for gobj in cls.objs:
            if not gobj.name:
                return
        return True

    @classmethod
    def str_gobj(cls, gobj):
        '''
        Name, objtype, dim, pos, text, color, font
        '''
        string = gobj.name + '\n'
        string += gobj.objtype + '\n'
        string += f'{gobj.dim[0]} {gobj.dim[1]}\n'
        pos = gobj.get_real_pos()
        string += f'{pos[0]} {pos[1]}\n'
        string += gobj.input_text.content + '\n'
        string += gobj.color + '\n'
        string += gobj.fontname
        return string

    @classmethod
    def create_savefile(cls):
        # create file
        with open(cls.window.name+'.txt','w') as file:
            # first write name, dim of window
            global_info = f'{cls.window.name} {cls.window.dim[0]} {cls.window.dim[1]}'
            file.write(global_info)
            file.write('\n'+SEPARATOR+'\n')
            for gobj in cls.objs:
                file.write(cls.str_gobj(gobj))
                file.write('\n'+SEPARATOR+'\n')

    @classmethod
    def display(cls):
        cls.cadre.display()
        cls.button_text_box.display()
        cls.button_button.display()
        cls.button_input_text.display()
        cls.button_cadre.display()
        cls.button_done.display()
        if cls.drag_surf:
            cls.drag_surf.run()
        
        for gui_obj in cls.objs:
            gui_obj.display()
    
    @classmethod
    def react_events(cls, events, pressed):
        pos = pygame.mouse.get_pos()
        
        Settings.run(events, pressed)

        # first check for changing dim
        for gobj in cls.objs:
            gobj.react_events(events, pressed)
        
        # check if click anywhere -> deselect gui obj
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if cls.check_deselect():
                    cls.current_selected.selected = False
                    cls.current_selected = None
                    Settings.deselect()

        # then check for new selected
        for gobj in cls.objs:
            if gobj.pushed(events):
                if not cls.current_selected:
                    cls.current_selected = gobj
                    gobj.selected = True  
                    Settings.set_obj(gobj)
        
        # check for gui obj to remove
        if pressed[pygame.K_DELETE]:
            if cls.current_selected:
                cls.objs.remove(cls.current_selected)
                cls.current_selected = None
                Settings.deselect()

        # check for deselect by enter
        if pressed[pygame.K_RETURN]:
            if cls.current_selected:
                cls.current_selected.selected = False
                cls.current_selected = None
                Settings.deselect()

        # last check for new gui obj
        if cls.drag_surf:
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    # set new obj on window
                    cls.create_obj(pos,cls.drag_surf.objtype)
                    # reset drag_surf
                    cls.drag_surf = None
        
        if cls.button_text_box.pushed(events):
            cls.drag_surf = DragSurf(pos, C.LIGHT_BLUE, 'TextBox')
        elif cls.button_button.pushed(events):
            cls.drag_surf = DragSurf(pos, C.LIGHT_BLUE, 'Button')
        elif cls.button_input_text.pushed(events):
            cls.drag_surf = DragSurf(pos, C.LIGHT_BLUE, 'InputText')
        elif cls.button_cadre.pushed(events):
            cls.drag_surf = DragSurf(pos, C.LIGHT_BLUE, 'Cadre')
        
        # end edition
        if cls.button_done.pushed(events):
            cls.create_savefile()
            cls.state = 'done'
        
        
                    
        
        
        


