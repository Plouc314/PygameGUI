from interface import Interface

Interface.setup((3000,1600),'GUI Editor')

from menu import Menu
#from testfile import Testfile

menu = Menu()

from editor import Editor

Interface.add_resizable_objs([Editor])

#tf = Testfile((100,100))

while Interface.running:
    pressed, events = Interface.run()
    #
    #tf.display()
    #
    menu.run(events, pressed)
    if menu.state == 'end':
        Interface.running = False
