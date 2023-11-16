from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.logger import Logger
from launchpad import Launchpad
from functools import partial

class LaunchpadSampleApp(App):

    def build(self):
        layout = GridLayout(cols=8)

        self.my_buttons = list() # access buttons by [row][col] in this list of lists

        for row in range(8):
            button_row = list()
            for col in range(8):
                button = Button()
                layout.add_widget(button)
                button.bind(on_press = partial(self.button_callback, row=row, col=col, down=True))
                button.bind(on_release = partial(self.button_callback, row=row, col=col, down=False))
                button_row.append(button)
            self.my_buttons.append(button_row)

        self.launchpad = Launchpad()
        self.launchpad.register_callback(self.input_message)

        return layout
    
    def input_message(self, main_grid, x, y, down_up):
        print('input:', main_grid, x, y, down_up)

        if main_grid:
            if down_up:
                self.my_buttons[y][x].state = "down"
            else:
                self.my_buttons[y][x].state = "normal"

    def button_callback(self, _, row, col, down):
        # set colors on the launchpad buttons - demonstrating the RGB range (and off)
        Logger.info(f'Button: {row}, {col} => {down}') # include for printing
        if down:
            self.launchpad.set_color(True, row, col, (row*32, col*32, (row+col)*16))
        else:
            self.launchpad.set_color(True, row, col, (0,0,0))

if __name__ == '__main__':
    app = LaunchpadSampleApp()
    app.run()
