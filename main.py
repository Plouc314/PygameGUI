from base import Interface
from menu import Menu
from testfile import Testfile

inter = Interface()

menu = Menu()

tf = Testfile((100,100))

while inter.running:
    pressed, events = inter.run()
    #
    #tf.display()
    #
    menu.run(events, pressed)
    if menu.state == 'end':
        inter.running = False
