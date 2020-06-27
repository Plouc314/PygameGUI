from interface import Interface, TextBox, Cadre, Font, C, Button, InputText, Form, center_text
from colorrange import ColorRange
import pygame

DIM_X = 400
DIM_Y = 60
POS_X = Interface.dim.x - 600


class Settings:
    activate = False
    text_name = TextBox((150, DIM_Y), (POS_X, 200), C.LIGHT_BLUE,
                        'Name:',font=Font.f25)
    input_name = InputText((250, DIM_Y), (POS_X+150,200), C.WHITE,font=Font.f25, limit=20)
    text_coord = TextBox((100, DIM_Y), (POS_X, 260), C.LIGHT_BLUE,'pos',font=Font.f25)
    input_coordx = InputText((150, DIM_Y), (POS_X+100, 260), C.WHITE,font=Font.f25)
    input_coordy = InputText((150, DIM_Y), (POS_X+250, 260), C.WHITE,font=Font.f25)
    text_dim = TextBox((100, DIM_Y), (POS_X, 320), C.LIGHT_BLUE, 'dim',font=Font.f25)
    input_dimx = InputText((150, DIM_Y), (POS_X+100, 320), C.WHITE,font=Font.f25)
    input_dimy = InputText((150, DIM_Y), (POS_X+250, 320), C.WHITE,font=Font.f25)
    text_font = TextBox((200, DIM_Y), (POS_X, 380), C.LIGHT_BLUE, 'Fontsize:',font=Font.f25)
    input_font = InputText((200, DIM_Y), (POS_X+200,380), C.WHITE, text='f25', font=Font.f25, limit=4)
    text_color = TextBox((200, DIM_Y), (POS_X, 440), C.LIGHT_BLUE,'Color:',font=Font.f25)
    input_color = InputText((200, DIM_Y), (POS_X+200, 440), C.WHITE, text='default',font=Font.f25) 
    color_range = ColorRange((600, 330), (POS_X-100, 520))

    @classmethod
    def set_obj(cls, obj):
        cls.objtype = obj.objtype
        cls.obj = obj
        cls.activate = True
        # set attr to input
        cls.input_name.set_text(cls.obj.name)
        cls.input_font.set_text(cls.obj.fontname)
        cls.input_color.set_text(cls.obj.color)
        # pos
        cls.input_coordx.set_text(str(cls.obj.pos[0]))
        cls.input_coordy.set_text(str(cls.obj.pos[1]))
        # dim
        cls.input_dimx.set_text(str(cls.obj.dim[0]))
        cls.input_dimy.set_text(str(cls.obj.dim[1]))
        # color range
        if cls.obj.ptr_pos and cls.obj.bptr_pos:
            cls.color_range.pointer.set_pos(cls.obj.ptr_pos, scale=True)
            cls.color_range.bar_pointer.set_pos(cls.obj.bptr_pos, scale=True)
        else:
            # default pos
            cls.color_range.pointer.set_pos((POS_X, 620), scale=True)
            cls.color_range.bar_pointer.set_pos((POS_X+268, 520), scale=True)
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
            dim = (int(cls.input_dimx.content), int(cls.input_dimy.content))
        except:
            print('Incorrect dim')
            dim = cls.obj.dim
        
        try:
            pos = (int(cls.input_coordx.content), int(cls.input_coordy.content))
        except:
            print('Incorrect pos')
            pos = cls.obj.pos

        cls.obj.set_new_dim(dim, pos)
        
        # fontsize
        try:
            font_str = cls.input_font.content
            font = getattr(Font, font_str)
            # try to center text -> avoid exception: Dimension too small for text
            center_text(cls.obj.dim, font['font'], cls.obj.input_text.content)
            cls.obj.input_text.font = font
            cls.obj.fontname = font_str
        except AttributeError:
            print('Incorrect font')
        
        # color
        try:
            str_color = cls.input_color.content
            # check if still default
            if 'default' in str_color.lower():
                color = C.WHITE
            else:
                # try to set a predefined color
                try:
                    color = getattr(C, str_color)
                except AttributeError:
                    # get the color range color
                    color = cls.color_range.chosen_color
            cls.obj.input_text.set_color(color)
            cls.obj.color = str_color
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