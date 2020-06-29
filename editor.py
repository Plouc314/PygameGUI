from interface import Interface, TextBox, Cadre, Font, C, Button, InputText, Form
from settings import Settings
import pygame

DIM_TOOLS = (400, 80)
DIM_DRAG = (200,60)
DIM_BDONE = (120, 60)
DIM_CORNER = (15,15)
POS_TY = 200
POS_WIN = (600, 200)

SEPARATOR = '/'

class DragSurf(Form):
    def __init__(self, pos, color, objtype):
        super().__init__(DIM_DRAG, pos, color)
        self.objtype = objtype
    
    def run(self):
        pos = pygame.mouse.get_pos()
        self.display(pos=pos)

POS_X = Interface.dim.x - 600

class GuiObj(Button):
    changing_dim = False
    chan_dim_corner = None
    name = ''
    color = 'WHITE'
    is_draging = False
    drag_delay = 3
    delay = 0
    delta_pos = None # dif between mouse pos and topleft when draging

    def __init__(self, pos, color, objtype):
        # don't scale pos as it is the mouse pos
        super().__init__(DIM_DRAG, pos,color, scale_pos=False)
        self.input_text = InputText(DIM_DRAG, pos, C.WHITE, font=Font.f(25), centered=True, scale_pos=False)
        self.objtype = objtype
        self.selected = True
        self.SELECT_COLOR = C.BLUE
        self.set_corners_points()
        self.color_choice = 'default' # store color choice way: default, text or range

        # color range
        self.ptr_pos = None
        self.bptr_y = None

        if self.objtype == 'TextBox' or self.objtype == 'Button':
            self.can_input = True
        else:
            self.can_input = False
    
    def get_real_pos(self):
        return (self.pos[0]-POS_WIN[0], self.pos[1]-POS_WIN[1])

    def set_corners_points(self):
        corner = Button(DIM_CORNER, (0,0), C.BLUE)
        corner.MARGE_WIDTH = 3
        self.CTOPLEFT = corner
        self.CTOPLEFT.set_pos(self.TOPLEFT, center=True)

        corner = Button(DIM_CORNER, (0,0), C.BLUE)
        corner.MARGE_WIDTH = 3
        self.CTOPRIGHT = corner
        self.CTOPRIGHT.set_pos(self.TOPRIGHT, center=True)
        
        corner = Button(DIM_CORNER, (0,0), C.BLUE)
        corner.MARGE_WIDTH = 3
        self.CBOTTOMRIGHT = corner
        self.CBOTTOMRIGHT.set_pos(self.BOTTOMRIGHT, center=True)

        corner = Button(DIM_CORNER, (0,0), C.BLUE)
        corner.MARGE_WIDTH = 3
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
        
        self.set_new_dim(dim, pos)

    def set_new_dim(self, dim, pos):
        self.set_dim_pos(dim, pos)
        self.input_text.set_dim_pos(dim, pos)
        self.set_corners_points()
        # change text in setting
        Settings.set_pos(pos)
        Settings.set_dim(dim)

    def set_select_color(self, color):
        self.SELECT_COLOR = color
        for cp in self.corners_points:
            cp.set_color(color, marge=True)

    def display(self):
        super().display()
        self.input_text.display()

        if self.selected:
            pygame.draw.line(Interface.screen, self.SELECT_COLOR, self.BOTTOMLEFT, self.BOTTOMRIGHT, 3)
            pygame.draw.line(Interface.screen, self.SELECT_COLOR, self.TOPLEFT, self.TOPRIGHT, 3)
            pygame.draw.line(Interface.screen, self.SELECT_COLOR, self.TOPLEFT, self.BOTTOMLEFT, 3)
            pygame.draw.line(Interface.screen, self.SELECT_COLOR, self.TOPRIGHT, self.BOTTOMRIGHT, 3)
            for cp in self.corners_points:
                cp.display()

    def react_events(self, events, pressed):
        
        self.as_change_dim = False
        mouse_pos = pygame.mouse.get_pos()

        if self.selected:
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    self.is_draging = False
                    self.delay = 0 # reset delay
                    if self.changing_dim:
                        try:
                            self.set_new_dim_mouse()
                        except:
                            print('Error in setting new dim')
                        
                        self.changing_dim = False
                        self.set_select_color(C.BLUE)
                        self.as_change_dim = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if Editor.TOP_RIGHT[0] > mouse_pos[0]:
                        self.is_draging = True
                        dx = mouse_pos[0] - self.TOPLEFT[0]
                        dy = mouse_pos[1] - self.TOPLEFT[1]
                        self.delta_pos = [dx, dy]

        # when draging: update pos
        if self.is_draging:
            self.delay += 1
            if self.delay >= self.drag_delay:
                new_x = mouse_pos[0] - self.delta_pos[0]
                new_y = mouse_pos[1] - self.delta_pos[1]
                self.set_new_dim(self.dim, (new_x, new_y))

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
    button_text_box = Button(DIM_TOOLS, (0, POS_TY), C.XLIGHT_GREY,'TextBox')
    button_button = Button(DIM_TOOLS, (0, POS_TY+80), C.XLIGHT_GREY,'Button')
    button_input_text = Button(DIM_TOOLS, (0, POS_TY+160), C.XLIGHT_GREY,'InputText')
    button_cadre = Button(DIM_TOOLS, (0, POS_TY+240), C.XLIGHT_GREY,'Cadre')
    button_done = Button(DIM_BDONE, (2800, 1400), C.LIGHT_BLUE,'Done',font=Font.f(30))
    drag_surf = None
    objs = []
    state = 'running'

    # set attr here for on_resize method
    window = None
    TOP_LEFT     = [0,0]
    TOP_RIGHT    = [0,0]
    BOTTOM_LEFT  = [0,0]
    BOTTOM_RIGHT = [0,0]

    current_selected = None

    @classmethod
    def set_window(cls, window):
        cls.window = window
        # don't rescale window.dim to have the original dimension stored (for on_resize)
        dim = window.dim
        cls.cadre = Cadre(dim, POS_WIN, C.WHITE)
        cls.TOP_LEFT     = Interface.dim.scale([POS_WIN[0], POS_WIN[1]])
        cls.TOP_RIGHT    = Interface.dim.scale([POS_WIN[0] + dim[0], POS_WIN[1]])
        cls.BOTTOM_LEFT  = Interface.dim.scale([POS_WIN[0], POS_WIN[1] + dim[1]])
        cls.BOTTOM_RIGHT = Interface.dim.scale([POS_WIN[0] + dim[0], POS_WIN[1] + dim[1]] )

    @staticmethod
    def on_resize(factor):
        if Editor.window:
            dim = Editor.window.dim
            Editor.TOP_LEFT     = Interface.dim.scale([POS_WIN[0], POS_WIN[1]])
            Editor.TOP_RIGHT    = Interface.dim.scale([POS_WIN[0] + dim[0], POS_WIN[1]])
            Editor.BOTTOM_LEFT  = Interface.dim.scale([POS_WIN[0], POS_WIN[1] + dim[1]])
            Editor.BOTTOM_RIGHT = Interface.dim.scale([POS_WIN[0] + dim[0], POS_WIN[1] + dim[1]] )

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
        string += str(gobj.color) + '\n' # can be either str or list
        string += str(gobj.input_text.font['size'])
        return string

    @classmethod
    def create_savefile(cls):
        # create file
        with open(cls.window.name+'.pygui','w') as file:
            sep = '\n'+SEPARATOR+'\n'
            # first write name, dim of window
            global_info = f'{cls.window.name} {cls.window.dim[0]} {cls.window.dim[1]}'
            file.write(global_info)
            file.write(sep)
            for gobj in cls.objs:
                file.write(cls.str_gobj(gobj))
                file.write(sep)

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
        
        
                    
        
        
        


