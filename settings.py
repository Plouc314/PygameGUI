from interface import Interface, TextBox, Cadre, Font, C, Button, InputText, Form, center_text
from colorrange import ColorRange
import pygame

DIM_X = 400
DIM_Y = 60
POS_X = Interface.dim.x - 600
POS_WIN = (600, 200)

class Settings:
    activate = False
    text_name = TextBox((150, DIM_Y), (POS_X, 200), C.LIGHT_BLUE,
                        'Name:',font=Font.f(25))
    input_name = InputText((250, DIM_Y), (POS_X+150,200), C.WHITE,font=Font.f(25), limit=20)
    text_coord = TextBox((100, DIM_Y), (POS_X, 260), C.LIGHT_BLUE,'pos',font=Font.f(25))
    input_coordx = InputText((150, DIM_Y), (POS_X+100, 260), C.WHITE,font=Font.f(25))
    input_coordy = InputText((150, DIM_Y), (POS_X+250, 260), C.WHITE,font=Font.f(25))
    text_dim = TextBox((100, DIM_Y), (POS_X, 320), C.LIGHT_BLUE, 'dim',font=Font.f(25))
    input_dimx = InputText((150, DIM_Y), (POS_X+100, 320), C.WHITE,font=Font.f(25))
    input_dimy = InputText((150, DIM_Y), (POS_X+250, 320), C.WHITE,font=Font.f(25))
    text_font = TextBox((200, DIM_Y), (POS_X, 380), C.LIGHT_BLUE, 'Fontsize:',font=Font.f(25))
    input_font = InputText((200, DIM_Y), (POS_X+200,380), C.WHITE, text='25', font=Font.f(25), limit=4)
    text_color = TextBox((200, DIM_Y), (POS_X, 440), C.LIGHT_BLUE,'Color:',font=Font.f(25))
    input_color = InputText((200, DIM_Y), (POS_X+200, 440), C.WHITE, text='',font=Font.f(25), pretext='default...') 
    color_range = ColorRange((600, 330), (POS_X-100, 520))

    @classmethod
    def set_pos(cls, pos):
        '''Update the position to have a unscaled relative position'''
        pos = Interface.dim.inv_scale(pos) # keep precision
        pos[0] -= POS_WIN[0]
        pos[1] -= POS_WIN[1]
        cls.input_coordx.set_text(f'{pos[0]:.1f}') # don't display all decimals
        cls.input_coordy.set_text(f'{pos[1]:.1f}')

    @classmethod
    def set_dim(cls, dim):
        '''Update the dimension to have unscaled dimension'''
        dim = Interface.dim.inv_scale(dim)
        cls.input_dimx.set_text(f'{dim[0]:.1f}') # don't display all decimals
        cls.input_dimy.set_text(f'{dim[1]:.1f}')

    @classmethod
    def set_obj(cls, obj):
        cls.objtype = obj.objtype
        cls.obj = obj
        cls.activate = True
        # set attr to input
        cls.input_name.set_text(cls.obj.name)
        cls.input_font.set_text(cls.obj.input_text.font['size'])

        # set inp color text: if with pretext or not
        if cls.obj.color_choice == 'text':
            cls.input_color.set_text(cls.obj.color)
        elif cls.obj.color_choice == 'range':
            # set custom as pretext
            cls.input_color.pretext = 'custom...'
            cls.input_color.set_text('', with_pretext=True)
        else:
            cls.input_color.pretext = 'default...'
            cls.input_color.set_text('', with_pretext=True)
        
        # pos
        cls.set_pos(cls.obj.pos)
        
        # dim
        cls.set_dim(cls.obj.dim)

        # color range
        if cls.obj.ptr_pos and cls.obj.bptr_pos:
            cls.color_range.pointer.set_pos(cls.obj.ptr_pos, scale=True)
            cls.color_range.bar_pointer.set_pos(cls.obj.bptr_pos, scale=True)
        else:
            # default pos
            cls.color_range.pointer.set_pos((POS_X, 620), scale=True)
            cls.color_range.bar_pointer.set_pos((POS_X+269, 520), scale=True)
        cls.color_range.set_color_range()

    @classmethod
    def run(cls, events, pressed):
        if cls.activate:
            cls.react_events(events, pressed)
            cls.display()

    @classmethod
    def save(cls):
        # name
        cls.obj.name = cls.input_name.content
        
        try:
            # scale dim
            dim = (float(cls.input_dimx.content), float(cls.input_dimy.content))
            dim = Interface.dim.scale(dim)
        except:
            print('Incorrect dim')
            dim = cls.obj.dim
        
        try:
            # scale pos
            pos = [float(cls.input_coordx.content), float(cls.input_coordy.content)]
            pos[0] += POS_WIN[0]
            pos[1] += POS_WIN[1]
            pos = Interface.dim.scale(pos)
        except:
            print('Incorrect pos')
            pos = cls.obj.pos

        cls.obj.set_new_dim(dim, pos)
        
        # fontsize
        try:
            font_size = int(cls.input_font.content)
            font = Font.f(font_size)
            cls.obj.input_text.font = font
        except AttributeError:
            print('Incorrect font')
        
        # color
        try:
            # get text and not content !!! -> see if pretext or not
            str_color = cls.input_color.text
            # check if still default
            if str_color == 'default...':
                color = C.WHITE
                cls.obj.color = 'WHITE'
            else:
                # try to set a predefined color
                try:
                    color = getattr(C, str_color)
                    cls.obj.color = str_color
                    # store that color is chosen by text
                    cls.obj.color_choice = 'text'
                except AttributeError:
                    # get the color range color
                    color = cls.color_range.chosen_color
                    cls.obj.color = color # in this case a tuple (and not str)
                    cls.obj.color_choice = 'range'
            
            cls.obj.input_text.set_color(color)
        except:
            print('Incorrect color')
        
        # color range
        # store in "original" size to be able to rescale in between
        cls.obj.ptr_pos = Interface.dim.inv_scale(cls.color_range.pointer.pos)
        cls.obj.bptr_pos = Interface.dim.inv_scale(cls.color_range.bar_pointer.pos)
 
    @classmethod
    def deselect(cls):
        cls.activate = False
        cls.save()

    @classmethod
    def display(cls):
        cls.text_name.display()
        cls.input_name.display()
        cls.text_coord.display()
        cls.input_coordx.display()
        cls.input_coordy.display()
        cls.text_dim.display()
        cls.input_dimx.display()
        cls.input_dimy.display()
        cls.text_font.display()
        cls.input_font.display()
        cls.text_color.display()
        cls.input_color.display()
        cls.color_range.display()
    
    @classmethod
    def react_events(cls, events, pressed):
        cls.color_range.react_events(events, pressed)
        cls.input_font.run(events, pressed)
        cls.input_name.run(events, pressed)
        cls.input_color.run(events, pressed)
        cls.input_coordx.run(events, pressed)
        cls.input_coordy.run(events, pressed)
        cls.input_dimx.run(events, pressed)
        cls.input_dimy.run(events, pressed)