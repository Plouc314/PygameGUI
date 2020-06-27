import pygame
from pygame.locals import *

pygame.init()

def mean(array):
    total = 0
    for v in array:
        total += v
    return total/len(array)

def center_text(dim_box, font, text):
    width, height = font.size(text)
    if width > dim_box[0] or height > dim_box[1]:
        print('interface.py - WARNING: Dimension too small for text')
    
    x_marge = int((dim_box[0] - width)/2)
    y_marge = int((dim_box[1] - height)/2)
    return x_marge, y_marge

class Delayer:
    '''
    Creates decorators,

    The decorated function should return True/False depending on whether or not it has been activated,
    if true, creates a delay in order to be spammed.
    '''
    wait = 0
    delayed = False
    def __init__(self, delay):
        self.delay = delay
        
    def __call__(self, func):
        def inner(*args, **kwargs):
            if self.delayed:
                self.wait += 1
                if self.wait == self.delay:
                    self.delayed = False
                    self.wait = 0
            else:
                # first argument if a boolean value of if the tested key was pressed
                executed = func(*args, **kwargs)
                if executed:
                    self.delayed = True
                return executed
        return inner

class Dimension:
    f = 1
    def __init__(self, dim, f):
        self.f = f
        self.WINDOW = dim # original dim: CONST!
        
        # unscaled
        self.center_x = int(dim[0]/2)
        self.center_y = int(dim[1]/2)
        self.center = (self.center_x, self.center_y)
        self.x = dim[0]
        self.y = dim[1]
    
    @property
    def rx(self):
        '''Scaled x dimension'''
        return self.E(self.WINDOW[0])
    
    @property
    def ry(self):
        '''Scaled y dimension'''
        return self.E(self.WINDOW[1])

    @property
    def size(self):
        '''Scaled dimension of the window'''
        return self.scale(self.WINDOW)

    def scale(self, x, factor = None):
        
        if factor:
            f = factor
        else:
            f = self.f

        if type(x) == list or type(x) == tuple:
            x = list(x)
            for i in range(len(x)):
                x[i] = int(x[i]*f)
        else:
            x = int(x*f)
        return x

    def inv_scale(self, x):
        return self.scale(x, factor=1/self.f)

    def E(self, x):
        return round(x*self.f)

fontname = 'Arial'
font_factor = 1

class C:
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    LIGHT_BLUE = (135,206,250)
    BLUE = (65,105,225)
    DARK_BLUE = (7, 19, 134)
    LIGHT_GREY = (200,200,200)
    XLIGHT_GREY = (230,230,230)
    LIGHT_RED = (255, 80, 80)
    RED = (225, 50, 50)
    LIGHT_GREEN = (124,252,100)
    GREEN = (94,222,70)
    DARK_GREEN = (17, 159, 26)
    LIGHT_BROWN = (225, 167, 69)
    DARK_PURPLE = (140, 17, 159)
    PURPLE = (180, 57, 199)
    LIGHT_PURPLE = (210, 87, 229)
    YELLOW = (253, 240, 49)

class Font:
    f25 =  {'size':25 , 'font':pygame.font.SysFont( fontname, 25)}
    f30 =  {'size':30 , 'font':pygame.font.SysFont( fontname, 30)}
    f50 =  {'size':50 , 'font':pygame.font.SysFont( fontname, 50)}
    f70 =  {'size':70 , 'font':pygame.font.SysFont( fontname, 70)}
    f100 = {'size':100, 'font':pygame.font.SysFont(fontname, 100)}
    @classmethod
    def set_dimfactor(cls, factor):
        cls.f25 =  {'size':25 , 'font':pygame.font.SysFont(fontname, round(factor*25 ))}
        cls.f30 =  {'size':30 , 'font':pygame.font.SysFont(fontname, round(factor*30 ))}
        cls.f50 =  {'size':50 , 'font':pygame.font.SysFont(fontname, round(factor*50 ))}
        cls.f70 =  {'size':70 , 'font':pygame.font.SysFont(fontname, round(factor*70 ))}
        cls.f100 = {'size':100, 'font':pygame.font.SysFont(fontname, round(factor*100))}

class Form(pygame.sprite.Sprite):
    screen = None
    MARGE_WIDTH = 4
    rs_marge_width = 4
    MARGE_TEXT = 5
    rs_marge_text = 5
    dim_object = None
    def __init__(self, dim, pos, color=C.WHITE, rescale=True, scale_pos=True, scale_dim=True, surface=None):
        super().__init__()
        
        self.set_dim_attr(dim, scale=scale_dim, update_surf=False)
        
        self.set_pos_attr(pos, scale=scale_pos)
        
        self.COLOR = color
    
        self.set_surf(surface)
        
        if rescale:
            # add every gui obj to interface to be able to rezise gui objs auto
            Interface.gui_objects.append(self)

    def set_surf(self, surface=None):
        '''
        Set the surface attribute
        
        Arguments:
            surface : can be either a pygame.Surface or numpy.ndarray object, by default: uni-color surf
        '''
        try:
            if not surface:
                # by default: create a uni-colored surface
                self.surf_type = 'default'
                self.surf = pygame.Surface(self.dim)
                self.surf.fill(self.COLOR)
            else:
                # if custom surface: keep a original surf to rescale properly
                self.surf_type = 'custom'
                self.ori_surf = surface
                self.surf = pygame.transform.scale(surface, self.dim)
        except ValueError:
            # numpy array
            self.surf_type = 'custom'
            self.ori_surf = pygame.surfarray.make_surface(surface)
            self.surf = pygame.transform.scale(self.ori_surf, self.dim)

    def set_dim_attr(self, dim, scale=False, update_original=True, update_surf=True):
        if scale:
            self.dim = self.dim_object.scale(dim)
            if update_original:
                self.ORI_DIM = list(dim)
        else:
            self.dim = list(dim)
            if update_original:
                self.ORI_DIM = self.dim_object.scale(dim, factor=1/self.dim_object.f)
        
        if update_surf:
            self.rescale_surf()
    
    def set_pos_attr(self, pos, scale=False, update_original=True):
        if scale:
            self.pos = self.dim_object.scale(pos)
            if update_original:
                self.ORI_POS = list(pos)
        else:
            self.pos = list(pos)
            if update_original:
                self.ORI_POS = self.dim_object.scale(pos, factor=1/self.dim_object.f)

    def set_color(self, color, marge=False):
        self.surf.fill(color)
        self.COLOR = color
        if marge:
            self.set_highlight_color()
            self.MARGE_COLOR = self.high_color

    def set_highlight_color(self):
        light_color = []
        for i in range(3):
            if self.COLOR[i] <= 235:
                light_color.append(self.COLOR[i] + 20)
            else:
                light_color.append(255)
        dark_color = []
        for i in range(3):
            if self.COLOR[i] >= 20:
                dark_color.append(self.COLOR[i] - 20)
            else:
                dark_color.append(0)
        if mean(self.COLOR) < 130:
            self.high_color = light_color
        else:
            self.high_color = dark_color

    def display_margin(self):
        pygame.draw.line(self.screen, self.MARGE_COLOR, self.TOPLEFT, self.TOPRIGHT, self.rs_marge_width)
        pygame.draw.line(self.screen, self.MARGE_COLOR, self.TOPLEFT, self.BOTTOMLEFT, self.rs_marge_width)
        pygame.draw.line(self.screen, self.MARGE_COLOR, self.TOPRIGHT, self.BOTTOMRIGHT, self.rs_marge_width)
        pygame.draw.line(self.screen, self.MARGE_COLOR, self.BOTTOMLEFT, self.BOTTOMRIGHT, self.rs_marge_width)

    def display(self, pos=None, marge=False):
        '''Display form
        
        Arguments:
            pos : can specify position where the form is displayed
            marge : if the marges are also displayed
        '''
        if pos:
            self.screen.blit(self.surf, pos)
        else:
            self.screen.blit(self.surf, self.pos)
        if marge:
            self.display_margin()
    
    def on_it(self):    
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] > self.TOPLEFT[0] and mouse_pos[0] < self.TOPRIGHT[0]:
            if mouse_pos[1] > self.TOPLEFT[1] and mouse_pos[1] < self.BOTTOMLEFT[1]:
                return True
        return False

    def set_corners(self):
        self.TOPLEFT = self.pos.copy()
        self.TOPRIGHT = (self.pos[0]+self.dim[0],self.pos[1])
        self.BOTTOMLEFT = (self.pos[0], self.pos[1]+self.dim[1])
        self.BOTTOMRIGHT = (self.pos[0]+self.dim[0],self.pos[1]+self.dim[1])

    def rescale_surf(self):
        '''Rescale the surf attribute to the current dimension'''
        if self.surf_type == 'default':
            self.surf = pygame.Surface(self.dim)
            self.surf.fill(self.COLOR)
        elif self.surf_type:
            self.surf = pygame.transform.scale(self.ori_surf, self.dim)

    def set_pos(self, pos, center=False, scale=False):
        '''Set a new position
        
        Arguments:
            - pos : the new position
            - center : if true, the form will be centered on the new pos, else the new pos is the top left of the obj
            - scale : if the position needs to be rescaled to the current window's dimension
        '''
        if not center:
            self.set_pos_attr(pos, scale=scale)
            self.set_corners()
        else:
            if scale:
                pos = self.dim_object.scale(pos)
            else:
                pos = list(pos)
            top_left = [int(pos[0]-self.dim[0]/2), int(pos[1]-self.dim[1]/2)]
            self.set_pos_attr(top_left)
            self.set_corners()

    def set_dim_pos(self, dim, pos, scale_dim=False, scale_pos=False, update_original=True):
        '''
        Reset dimension & position of form
        
        Arguments:
            - dim, pos : new dimension, position
            - scale_dim/pos : if new dim/pos need to be scaled to current window's dimension
            - update_original : if new dim/pos are kept when window is resized
        '''
        self.set_dim_attr(dim, scale=scale_dim, update_original=update_original)
        self.set_pos_attr(pos, scale=scale_pos, update_original=update_original)
        self.set_corners()

class Cadre(Form):
    def __init__(self, dim, pos, color=C.WHITE, set_transparent=False, scale_dim=True, scale_pos=True):
        
        super().__init__(dim, pos, color, scale_dim=scale_dim, scale_pos=scale_pos)
        
        self.set_corners()
        self.set_highlight_color()
        self.MARGE_COLOR = self.high_color
        if set_transparent:
            self.surf.set_colorkey(color)

    def display(self):
        super().display(self.pos)
        self.display_margin()

class Button(Form):
    def __init__(self, dim, pos, color=C.WHITE, text='', text_color=(0,0,0), 
                    centered=True, font=Font.f50, surface=None, scale_dim=True, scale_pos=True, highlight=True):
        
        super().__init__(dim, pos, color, scale_dim=scale_dim, scale_pos=scale_pos, surface=surface)

        self.text = text
        
        self.text_color = text_color
        self.set_corners()
        self.highlighted = highlight
        self.centered = centered
        self.font = font
        self.set_highlight_color()
        self.MARGE_COLOR = self.high_color

    def pushed(self, events):
        if self.on_it():
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    return True

    def highlight(self):        
        if self.on_it():
            self.surf.fill(self.high_color)
        else:
            self.surf.fill(self.COLOR)
        
    def display(self):
        
        if self.highlighted:
            self.highlight()
        
        super().display()
        
        self.display_margin()
        
        if self.text: # check that there is text
            x_marge, y_marge = center_text(self.dim, self.font['font'], self.text)
            if not self.centered:
                x_marge = self.rs_marge_text
            font_text = self.font['font'].render(self.text,True,self.text_color)
            self.screen.blit(font_text,(self.pos[0]+x_marge,self.pos[1]+y_marge))

class TextBox(Form):
    
    def __init__(self, dim, pos, color=C.WHITE, text='', 
                    text_color=(0,0,0), centered=True, font=Font.f50, marge=False, scale_dim=True, scale_pos=True):
        
        super().__init__(dim, pos, color, scale_dim=scale_dim, scale_pos=scale_pos)
        
        self.text = text
        self.centered = centered
        self.font = font
        self.lines = text.split('\n')
        self.text_color = text_color
        self.set_corners()
        self.as_marge = marge
        if marge:
            self.set_highlight_color()
            self.MARGE_COLOR = self.high_color

    def set_text(self, text):
        self.text = text
        self.lines = text.split('\n')

    def display(self):
        super().display()
        if self.as_marge:
            self.display_margin()

        # split the box in n part for n lines
        y_line = round(self.dim[1]/len(self.lines))
        for i, line in enumerate(self.lines):
            x_marge, y_marge = center_text((self.dim[0],y_line), self.font['font'], line)
            if not self.centered:
                x_marge = self.rs_marge_text
            font_text = self.font['font'].render(line,True,self.text_color)
            self.screen.blit(font_text,(self.pos[0]+x_marge,self.pos[1]+i*y_line+y_marge))

get_input_deco = Delayer(3)
cursor_deco = Delayer(15)

class InputText(Button):
    CURSOR_WIDTH = 2
    bool_cursor = True
    def __init__(self, dim, pos, color=C.WHITE, text_color=(0,0,0), centered=False, font=Font.f30,
                    limit=None, cache=False, text='', scale_dim=True, scale_pos=True):
        super().__init__(dim, pos, color, text_color=text_color, centered=centered, font=font, scale_dim=scale_dim, scale_pos=scale_pos)
        self.active = False
        self.cursor_place = len(text)
        self.limit = limit # max char
        self.cache = cache # if true text -> ***
        # text: text that is display
        # content: text that is input
        self.set_text(text)
    
    def set_text(self, text):
        self.content = text
        self.cursor_place = len(text)
        if self.cache:
            self.text = '$' * len(self.content)
        else:
            self.text = self.content

    @get_input_deco
    def is_moving_left(self, pressed):
        if pressed[pygame.K_LEFT]:
            return True

    @get_input_deco
    def is_moving_right(self, pressed):
        if pressed[pygame.K_RIGHT]:
            return True

    @get_input_deco
    def get_input(self, events, pressed):
        self.active = True
        
        # check for end active
        if pressed[pygame.K_RETURN]:
            self.active = False
            self.highlighted = False
            return False
        elif not self.on_it():
            pushed = False
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    pushed =  True 
            if pushed:
                self.active = False
                self.highlighted = False
                return False

        key = get_pressed_key(pressed)
        if key:
            self.content = self.content[:self.cursor_place] + key + self.content[self.cursor_place:]
            self.cursor_place += 1
            if self.limit:
                if len(self.content) > self.limit:
                    self.content = self.content[:-1]
                    self.cursor_place -= 1
                
            try:
                center_text(self.dim, self.font['font'], self.content)
            except ValueError:
                self.content = self.content[:-1]
                self.cursor_place -= 1
            return True
        
        if pressed[pygame.K_BACKSPACE]:
            self.content = self.content[:self.cursor_place-1] + self.content[self.cursor_place:]
            self.cursor_place -= 1
            return True
    
        # check for cursor change
        if self.is_moving_left(pressed):
            if self.cursor_place > 0:
                self.cursor_place -= 1
        
        if self.is_moving_right(pressed):
            if self.cursor_place < len(self.content):
                self.cursor_place += 1

        if self.cache:
            self.text = '$' * len(self.content)
        else:
            self.text = self.content

        return False
    
    def display_text_cursor(self):
        width, height = self.font['font'].size(self.text[:self.cursor_place])
        x_marge, y_marge = center_text(self.dim, self.font['font'], self.text[:self.cursor_place])
        if not self.centered:
            x_marge = self.rs_marge_text

        bottom_pos = (self.TOPLEFT[0] + x_marge + width, self.BOTTOMLEFT[1]-y_marge)
        top_pos = (self.TOPLEFT[0] + x_marge + width, self.TOPLEFT[1]+y_marge)
        
        if self.bool_cursor:
            pygame.draw.line(self.screen, C.BLACK, top_pos, bottom_pos, self.CURSOR_WIDTH)
        self.change_cursor_state()

    @cursor_deco
    def change_cursor_state(self):
        self.bool_cursor = not self.bool_cursor
        return True

    def run(self, events, pressed):
        if self.pushed(events):
            self.active = True
        
        if self.active:
            self.highlighted = True
            self.display_text_cursor()
            self.get_input(events, pressed)


class Interface:
    clock = pygame.time.Clock()
    running = True
    gui_objects = [] # all gui objects, ex: button, form...
    resize_objects = [] # must have a on_resize(self, factor) method

    @classmethod
    def setup(cls, dim, win_title, FPS=30):
        '''
        Arguments:
            dim: default window dimension, used to set other object's dimension
        '''
        
        # create dimension
        cls.dim = Dimension(dim, 1)
        
        # create screen in full screen dimension: resize to specified dim

        infoObject = pygame.display.Info()
        fullscreen_dim = cls.dim.scale((infoObject.current_w, infoObject.current_h), factor=.95)

        cls.screen = pygame.display.set_mode(fullscreen_dim, HWSURFACE|DOUBLEBUF|RESIZABLE)
        cls.screen.fill(C.WHITE)
        pygame.display.set_caption(win_title)

        cls.FPS = FPS

        cls.set_screen(cls.screen)
        Form.dim_object = cls.dim # set dimension to rescale pos, dim in Font.__init__
        Form.rs_marge_width = cls.dim.E(Form.MARGE_WIDTH)
        Form.rs_marge_text = cls.dim.E(Form.MARGE_TEXT)

        cls.x_padding = Form((0,0),(0,0),C.WHITE, rescale=False)
        cls.y_padding = Form((0,0),(0,0),C.WHITE, rescale=False)

        # rescale window to correct dim
        cls.rescale(fullscreen_dim)
        
    @classmethod
    def set_screen(cls, screen):
        Form.screen = cls.screen
        TextBox.screen = cls.screen
        Button.screen = cls.screen
        InputText.screen = cls.screen
        Cadre.screen = cls.screen

        for gui_obj in cls.gui_objects:
            gui_obj.screen = screen

    @classmethod
    def add_resizable_objs(cls, objects):
        '''Object's method on_rezise(self, scale_factor) will be called when window is rezised
        
        scale_factor: factor of dimension compared to initial dimension
        '''
        cls.resize_objects.extend(objects)
        # resize a first time
        for obj in objects:
            obj.on_resize(cls.dim.f)

    @classmethod
    def rescale(cls, new_dim):

        # set new scale factor
        scale_factor = min(new_dim[0]/cls.dim.x, new_dim[1]/cls.dim.y)

        cls.dim.f = scale_factor

        # create padding to fill blank space
        dim_px = [new_dim[0] - cls.dim.size[0], cls.dim.size[1]]
        if dim_px[0] > 0:
            pos = [cls.dim.size[0], 0]
            cls.x_padding.set_dim_pos(dim_px, pos, update_original=False)
        
        dim_py = [cls.dim.size[0], new_dim[1] - cls.dim.size[1]]
        if dim_px[1] > 0:
            pos = [0, cls.dim.size[1]]
            cls.y_padding.set_dim_pos(dim_py, pos, update_original=False)

        # resize font
        Font.set_dimfactor(scale_factor)
        
        # resize marges
        Form.rs_marge_width = cls.dim.E(Form.MARGE_WIDTH)
        Form.rs_marge_text = cls.dim.E(Form.MARGE_TEXT)

        # resize every objects
        for gui_obj in cls.gui_objects:
            gui_obj.set_dim_pos(gui_obj.ORI_DIM, gui_obj.ORI_POS, scale_pos=True, scale_dim=True, update_original=False)
            
            # rezise existing fonts
            if hasattr(gui_obj, 'font'):
                fontsize = gui_obj.font['size']
                gui_obj.font = getattr(Font,f'f{fontsize}')

        for rz_obj in cls.resize_objects:
            rz_obj.on_resize(scale_factor)

    @classmethod
    def run(cls, fill=True):
        cls.x_padding.display()
        cls.y_padding.display()
        cls.clock.tick(cls.FPS)
        
        pygame.display.update()

        if fill:
            cls.screen.fill(C.WHITE)

        pressed = pygame.key.get_pressed()
        events = pygame.event.get()

        cls.mouse_pos = pygame.mouse.get_pos()

        for event in events:
            # check quit
            if event.type == pygame.QUIT:
                cls.running = False
            # check window resize
            if event.type == VIDEORESIZE:
                cls.rescale(event.dict['size'])
                
        if pressed[pygame.K_ESCAPE]:
            cls.running = False

        return pressed, events


def get_pressed_key(pressed):
    if pressed[pygame.K_a] and pressed[pygame.K_LSHIFT]:
        return 'A'
    elif pressed[pygame.K_b] and pressed[pygame.K_LSHIFT]:
        return 'B'
    elif pressed[pygame.K_c] and pressed[pygame.K_LSHIFT]:
        return 'C'
    elif pressed[pygame.K_d] and pressed[pygame.K_LSHIFT]:
        return 'D'
    elif pressed[pygame.K_e] and pressed[pygame.K_LSHIFT]:
        return 'E'
    elif pressed[pygame.K_f] and pressed[pygame.K_LSHIFT]:
        return 'F'
    elif pressed[pygame.K_g] and pressed[pygame.K_LSHIFT]:
        return 'G'
    elif pressed[pygame.K_h] and pressed[pygame.K_LSHIFT]:
        return 'H'
    elif pressed[pygame.K_i] and pressed[pygame.K_LSHIFT]:
        return 'I'
    elif pressed[pygame.K_j] and pressed[pygame.K_LSHIFT]:
        return 'J'
    elif pressed[pygame.K_k] and pressed[pygame.K_LSHIFT]:
        return 'K'
    elif pressed[pygame.K_l] and pressed[pygame.K_LSHIFT]:
        return 'L'
    elif pressed[pygame.K_m] and pressed[pygame.K_LSHIFT]:
        return 'M'
    elif pressed[pygame.K_n] and pressed[pygame.K_LSHIFT]:
        return 'N'
    elif pressed[pygame.K_o] and pressed[pygame.K_LSHIFT]:
        return 'O'
    elif pressed[pygame.K_p] and pressed[pygame.K_LSHIFT]:
        return 'P'
    elif pressed[pygame.K_q] and pressed[pygame.K_LSHIFT]:
        return 'Q'
    elif pressed[pygame.K_r] and pressed[pygame.K_LSHIFT]:
        return 'R'
    elif pressed[pygame.K_s] and pressed[pygame.K_LSHIFT]:
        return 'S'
    elif pressed[pygame.K_t] and pressed[pygame.K_LSHIFT]:
        return 'T'
    elif pressed[pygame.K_u] and pressed[pygame.K_LSHIFT]:
        return 'U'
    elif pressed[pygame.K_v] and pressed[pygame.K_LSHIFT]:
        return 'V'
    elif pressed[pygame.K_w] and pressed[pygame.K_LSHIFT]:
        return 'W'
    elif pressed[pygame.K_x] and pressed[pygame.K_LSHIFT]:
        return 'X'
    elif pressed[pygame.K_y] and pressed[pygame.K_LSHIFT]:
        return 'Y'
    elif pressed[pygame.K_z] and pressed[pygame.K_LSHIFT]:
        return 'Z'
    elif pressed[pygame.K_a]:
        return 'a'
    elif pressed[pygame.K_b]:
        return 'b'
    elif pressed[pygame.K_c]:
        return 'c'
    elif pressed[pygame.K_d]:
        return 'd'    
    elif pressed[pygame.K_e]:
        return 'e'
    elif pressed[pygame.K_f]:
        return 'f'
    elif pressed[pygame.K_g]:
        return 'g'
    elif pressed[pygame.K_h]:
        return 'h'
    elif pressed[pygame.K_i]:
        return 'i'
    elif pressed[pygame.K_j]:
        return 'j'
    elif pressed[pygame.K_k]:
        return 'k'
    elif pressed[pygame.K_l]:
        return 'l'
    elif pressed[pygame.K_m]:
        return 'm'
    elif pressed[pygame.K_n]:
        return 'n'
    elif pressed[pygame.K_o]:
        return 'o'
    elif pressed[pygame.K_p]:
        return 'p'
    elif pressed[pygame.K_q]:
        return 'q'
    elif pressed[pygame.K_r]:
        return 'r'
    elif pressed[pygame.K_s]:
        return 's'
    elif pressed[pygame.K_t]:
        return 't'
    elif pressed[pygame.K_u]:
        return 'u'
    elif pressed[pygame.K_v]:
        return 'v'
    elif pressed[pygame.K_w]:
        return 'w'
    elif pressed[pygame.K_x]:
        return 'x'
    elif pressed[pygame.K_y]:
        return 'y'
    elif pressed[pygame.K_z]:
        return 'z'
    elif pressed[pygame.K_1]:
        return '1'
    elif pressed[pygame.K_2]:
        return '2'
    elif pressed[pygame.K_3]:
        return '3'
    elif pressed[pygame.K_4]:
        return '4'
    elif pressed[pygame.K_5]:
        return '5'
    elif pressed[pygame.K_6]:
        return '6'
    elif pressed[pygame.K_7]:
        return '7'
    elif pressed[pygame.K_8]:
        return '8'
    elif pressed[pygame.K_9]:
        return '9'
    elif pressed[pygame.K_0]:
        return '0'
    elif pressed[pygame.K_SPACE]:
        return ' '
    elif pressed[pygame.K_MINUS] and pressed[pygame.K_LSHIFT]:
        return '_'
