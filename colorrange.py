from interface import Interface, Form, Button, C, Delayer, Cadre
import numpy as np
import pygame

def get_color_range(base_color):

    base_color = np.array(base_color, dtype='float32')

    arr_color = np.zeros((256,256,3), dtype='int32')

    y_deltas = base_color/256

    for y in range(256):
        max_v = 255-y
        cp = np.full((3),max_v, dtype='float32')
        y_dest_values = base_color - y_deltas*y
        deltas = -(y_dest_values-max_v)/256

        for x in range(256):
            cp = cp - deltas
            arr_color[x,y,:] = cp

    return arr_color

def create_color_bar(width):
    arr_color = np.zeros((6*256,width,3),dtype='int32')
    cp = np.array([0,0,0], dtype='int32')
    dy = 0
    cp[0] = 255
    
    for y in range(256):
        cp[2] = y
        for x in range(width):
            arr_color[y+dy,x,:] = cp
    dy += 256
    
    for y in range(256):
        cp[0] = 255-y
        for x in range(width):
            arr_color[y+dy,x,:] = cp
    dy += 256
    
    for y in range(256):
        cp[1] = y
        for x in range(width):
            arr_color[y+dy,x,:] = cp
    dy += 256
    
    for y in range(256):
        cp[2] = 255-y
        for x in range(width):
            arr_color[y+dy,x,:] = cp
    dy += 256
    
    for y in range(256):
        cp[0] = y
        for x in range(width):
            arr_color[y+dy,x,:] = cp
    dy += 256
    
    for y in range(256):
        cp[1] = 255-y
        for x in range(width):
            arr_color[y+dy,x,:] = cp
    
    return np.rot90(arr_color, axes=(0,1)) # rotate the array of 90° as it was in the wrong direction

set_color_range_deco = Delayer(10)

class ColorRange:
    '''
    Graphical interface to choose colors

    Advise: choose a dimension with a 9/5 ration

    Selected color stored in: chosen_color

    '''
    def __init__(self, dim, pos):
        
        dim_cr = (round(dim[0]*5/9), dim[1])
        dim_bar = (round(dim[0]*1/18), dim[1])
        dim_ptr = (round(dim[0]/90), round(dim[0]/90))
        dim_view = (round(dim[0]*5/18), dim[1])

        pos_ptr = (round(pos[0]+dim_cr[0]/2), round(pos[1]+dim_cr[1]/2))
        pos_bar = (pos[0]+dim_cr[0]+dim_bar[0], pos[1])
        pos_view = (pos[0]+dim_cr[0]+3*dim_bar[0], pos[1])

        self.cadre = Cadre(dim, pos, set_transparent=True)
        # create color range img
        self.arr_color = get_color_range([255,0,0])
        self.color_range = Button(dim_cr,pos, surface=self.arr_color, highlight=False)

        self.pointer = Form(dim_ptr, pos_ptr, C.LIGHT_GREY)
        self.bar_pointer = Form((dim_bar[0], dim_ptr[0]), pos_bar, C.LIGHT_GREY)
        
        self.arr_bar = create_color_bar(150)
        self.color_bar = Button(dim_bar, pos_bar, surface=self.arr_bar, highlight=False)

        self.color_view = Form(dim_view, pos_view)

        self.range_active = False
        self.bar_active = False
        self.chosen_color = None

    def react_events(self, events, pressed):
        if self.color_range.pushed(events):
            self.range_active = not self.range_active # activate/deactivate color selection
        
        if self.color_bar.pushed(events):
            self.bar_active = not self.bar_active
        
        # update pointer position
        if self.range_active:
            mouse_pos = Interface.mouse_pos
            # check that pointer is still on surf
            if self.color_range.on_it():
                self.pointer.set_pos(mouse_pos, center=True)
            else:
                self.range_active = False
        
        # update bar pointer position
        if self.bar_active:
            mouse_pos = Interface.mouse_pos
            # check that pointer is still on surf
            if self.color_bar.on_it():
                self.bar_pointer.set_pos((self.bar_pointer.pos[0], mouse_pos[1]))
            else:
                self.bar_active = False
                # set last color range
                self.set_color_range()

    def set_color_range(self):
        '''Create a new color range based on the current bar color'''
        # first get base_color
        y = self.bar_pointer.pos[1] - self.cadre.pos[1]
        y = int(y*6*256/self.cadre.dim[1])

        base_color = self.arr_bar[0,y,:]

        # create a new color range
        self.arr_color = get_color_range(base_color)
        self.color_range.set_surf(surface=self.arr_color)

    @set_color_range_deco
    def check_set_color_range(self):
        '''Use a delayer to avoid freaking out the cpu for no reason (creating the color range is quite heavy)'''
        if self.bar_active:
            self.set_color_range()
            return True

    def set_view_color(self):
        '''
        Get the selected color in color range, get the correct pixel of arr_color and set color_view's color
        '''
        # get color
        x = self.pointer.pos[0] - self.cadre.pos[0]
        x = int(x*256/self.color_range.dim[0])
        y = self.pointer.pos[1] - self.cadre.pos[1]
        y = int(y*256/self.color_range.dim[1])
        
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        
        color = self.arr_color[x,y,:]
        # set new color
        self.color_view.set_color(color)
        # store color
        self.chosen_color = color

    def display(self):
        # update colors
        self.set_view_color()
        self.check_set_color_range()
        # display everything
        self.color_range.display()
        self.color_bar.display()
        self.pointer.display()
        self.bar_pointer.display()
        self.color_view.display()
        self.cadre.display()
