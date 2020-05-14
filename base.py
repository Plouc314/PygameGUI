from interface import Interface, TextBox, InputText, Button, Font, C, E, Cadre, Dimension, set_screen, Form
import pygame

windows = []

def scale(x):
    if type(x) == list or type(x) == tuple:
        x = list(x)
        for i in range(len(x)):
            x[i] = int(x[i]*Dimension.f)
    else:
        x = int(x*Dimension.f)
    return x

dim = Dimension(scale((3000,1600)))

screen = pygame.display.set_mode(dim.window)
screen.fill(C.WHITE)
pygame.display.set_caption('GUI creator')

set_screen(screen)