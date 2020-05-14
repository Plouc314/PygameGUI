from base import TextBox, Cadre, Font, C, Button, dim, InputText, E, windows, scale, Form, screen
import pygame

DIM_X = E(400)
DIM_Y = E(60)
POS_X = dim.x - E(600)


class Settings:
    activate = False
    text_name = TextBox((E(150), DIM_Y), C.LIGHT_BLUE, (POS_X, E(200)),
                        'Name:',font=Font.f25)
    input_name = InputText((E(250), DIM_Y), (POS_X+E(150), E(200)), C.WHITE,font=Font.f25, limit=10)
    text_coord = TextBox((E(100), DIM_Y), C.LIGHT_BLUE, (POS_X, E(260)),'pos',font=Font.f25)
    input_coordx = InputText((E(150), DIM_Y), (POS_X+E(100), E(260)), C.WHITE,font=Font.f25)
    input_coordy = InputText((E(150), DIM_Y), (POS_X+E(250), E(260)), C.WHITE,font=Font.f25)
    text_dim = TextBox((E(100), DIM_Y), C.LIGHT_BLUE, (POS_X, E(320)),'dim',font=Font.f25)
    input_dimx = InputText((E(150), DIM_Y), (POS_X+E(100), E(320)), C.WHITE,font=Font.f25)
    input_dimy = InputText((E(150), DIM_Y), (POS_X+E(250), E(320)), C.WHITE,font=Font.f25)
    text_font = TextBox((E(200), DIM_Y), C.LIGHT_BLUE, (POS_X, E(380)), 'Fontsize:',font=Font.f25)
    input_font = InputText((E(200), DIM_Y), (POS_X+E(200), E(380)), C.WHITE, text='f25', font=Font.f25, limit=4)
    text_color = TextBox((E(200), DIM_Y), C.LIGHT_BLUE, (POS_X, E(440)), 'Color:',font=Font.f25)
    input_color = InputText((E(200), DIM_Y), (POS_X+E(200), E(440)), C.WHITE, text='WHITE',font=Font.f25) 

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

    @classmethod
    def run(cls, events, pressed):
        if cls.activate:
            cls.react_events(events, pressed)
            cls.display()

    @classmethod
    def save(cls):
        # name
        cls.obj.name = cls.input_name.content
        # dim
        try:
            dim = (int(cls.input_dimx.content), int(cls.input_dimy.content))
            cls.obj.set_new_dim(dim, cls.obj.pos)
        except:
            print('Incorrect dim')
        # pos
        try:
            pos = (int(cls.input_coordx.content), int(cls.input_coordy.content))
            cls.obj.set_new_dim(cls.obj.dim, pos)
        except:
            print('Incorrect pos')
        # fontsize
        try:
            font_str = cls.input_font.content
            font = getattr(Font, font_str)
            cls.obj.input_text.font = font
            cls.obj.fontname = font_str
        except:
            print('Incorrect font')
        # color
        try:
            str_color = cls.input_color.content
            color = getattr(C, str_color)
            cls.obj.input_text.set_color(color)
            cls.obj.color = str_color
        except:
            print('Incorrect color')
        
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
    
    @classmethod
    def react_events(cls, events, pressed):
        cls.input_font.run(events, pressed)
        cls.input_name.run(events, pressed)
        cls.input_color.run(events, pressed)
        cls.input_coordx.run(events, pressed)
        cls.input_coordy.run(events, pressed)
        cls.input_dimx.run(events, pressed)
        cls.input_dimy.run(events, pressed)