from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.logger import Logger
import time
from launchpad import lp

class Design2App(App):
    name = ""
    def build(self):
        from functools import partial
        layout = GridLayout(cols=8)

        self.mybuttons = list() # access buttons by [row][col] in this list of lists

        for row in range(8):
            buttonrow = list()
            for col in range(8):
                button = Button()
                layout.add_widget(button)
                button.bind(on_press=partial(self.button_callback, row=row, col=col))
                buttonrow.append(button)
            self.mybuttons.append(buttonrow)

        self.midi_io = lp()

        self.midi_io.register_callback(self.input_message)

        return layout
    
    def input_message(self, midi):
        # (on/off, bool, x, y)
        print(midi) # include for printing
        if midi[1]:
            if midi[0]:
                self.mybuttons[midi[3]][midi[2]].state = "normal"
            else:
                self.mybuttons[midi[3]][midi[2]].state = "down"
        return

    def button_callback(self, instance, row, col):
        # send some midi to the launchpad! code is currently written to demonstrate the RGB range (and off)
        Logger.info(f'Button: {row}, {col}') # include for printing
        self.midi_io.set_color(True, row, col, (row*32, col*32, (row+col)*16))


if __name__ == '__main__':
    thing = Design2App()
    thing.run()
