import time
import rtmidi


class lp:

    def __init__(self):
        self.midiin = rtmidi.MidiIn()

        self.midiout = rtmidi.MidiOut()
        self.midiout.open_port(0)
        self.name = self.midiin.get_port_name(0)
        
        if self.name == "Launchpad MK2" or self.name == "Launchpad Mini":
            self.midiin.open_port(0)
        elif "Launchpad Mini MK3" in self.name:
            self.midiin.open_port(1)


    def register_callback(self, func):
        self.midiin.set_callback(lambda m, dt : func(self.get_midi(m, dt)))


    def set_color(self, bool, x, y, led):
        """
        input: msg is a tuple (bool, x, y, led)
            - if bool is true, then working with the grid. x and y range from 0 to 7
            - if bool is false, then working with side buttons. x is 0 or 1 for top or side, respectively, and y is 0 through 7 for which button
            - led is tuple RGB. 0 for off, max 127 for each.
        input: name is identifier for launchpad
        """
        name = self.name

        if max(led)>255:
            raise ValueError("Sorry, your RGB is out of bounds. Please restrict values to 0 to 255.")
        if name == "Launchpad MK2":
            num = -1
            if bool: # working with grid
                num = 10 * (8-x) + y+1
            else:
                if x: # working with side bar
                    num = (8-y)*10 + 9
                else: # working with top bar
                    num = 104 + y 
            self.midiout.send_message( [0xf0] + [ 0, 32, 41, 2, 24, 11, num] + [led[i]//4 for i in range(0, 3)] + [0xf7] )
        elif name == "Launchpad Mini":
            num = -1
            if bool: # working with grid
                num = (16 * x)+y
                num1 = 144
            else:
                if x: # working with side bar
                    num = y*16+8
                    num1 = 144
                else: # working with top bar
                    num = 104+y
                    num1 = 176
            r,g = led[0], led[1]
            r = r//64 # scale from 0 to 3 of how much red
            g = g//32 + 1  # scale from 1 to 7 of how much green
            self.midiout.send_message([num1, num, 8*g+r])
        elif "Launchpad Mini MK3" in name:
            # set to programmer mode
            self.midiout.send_message( [0xf0] + [ 0, 32, 41, 2, 13, 14, 1] + [0xf7] )
            # normal code:
            num = -1
            if bool: # working with grid
                num = 10 * (8-x) + y+1
            else:
                if x: # working with side bar
                    num = (8-y)*10 + 9
                else: # working with top bar
                    num = 91 + y
            self.midiout.send_message( [0xf0] + [ 0, 32, 41, 2, 13, 3, 3, num] + [led[i]//2 for i in range(0, 3)] + [0xf7] )


    def get_midi(self, m, dt = 0.01):
        """
        - internal function for register_callback
        """
        if m:
            message = self.process_midi(m)
            if message:
                return message
        raise NotImplementedError("Sorry, we can't process this device.")


    def process_midi(self, midi):
        """
        process_midi:
        - internal function for get_midi
        - (input) midi is the midi input from that launchpad
        - (output) output tuple (on/off, bool, x, y) where bool represents the grid or the buttons
            - on/off is whether button is showing on or off
            - if bool is true, then working with the grid. x and y range from 0 to 7
            - if bool is false, then working with side buttons. x is 0 or 1 for top or side, respectively, and y is 0 through 7 for which button
        - process_midi takes in input from the launchpads and translates it to a format that we feed into kivy
        - no velocity for now, no output for now
        """
        name = self.name

        if name == "Launchpad MK2":
            # midi in format ([144/176, button num, velocity], deltatime)
            # grid is 81... 88; 71... 78; first number is 144
            # top buttons are 104, 105, ... 111. first number is 176
            # side buttons are 89, 79... 19, first number is 144
            onoff = False
            if (midi[0][2] == 0):
                onoff = True

            if midi[0][0] == 176:
                # top row
                return (onoff, False, 0, midi[0][1]-104)
            elif midi[0][1] % 10 == 9:
                # side row
                return (onoff, False, 1, 8- int(midi[0][1] // 10))
            else:
                # grid
                x = int(midi[0][1] % 10 - 1)
                y = 8- int(midi[0][1] // 10)
                return (onoff, True, x, y)

        if name == "Launchpad Mini":
            # midi in format ([144/176, button num, velocity], deltatime)
            # grid is 0 1 2 3 4 5 6 7 ; 16, 17, 18, 19, 20, 21, 22, 23; first number is 144
            # top buttons are 104, 105, ... 111. first number is 176
            # side buttons are 8, 24, 40... 120, first numbe is 144
            onoff = False
            if (midi[0][2] == 0):
                onoff = True

            if midi[0][0] == 176:
                # top row
                return (onoff, False, 0, midi[0][1]-104)
            elif midi[0][1] % 16 == 8:
                # side row
                return (onoff, False, 1, int((midi[0][1] / 8 - 1) / 2))
            else:
                # grid
                x = int(midi[0][1] % 8)
                y = int((midi[0][1] / 8) / 2)
                return (onoff, True, x, y)
        
        if "Launchpad Mini MK3" in name:
            # midi in format ([144/176, button num, velocity], deltatime)
            # MAKE SURE YOU'RE IN PROGRAMMER MODE: PRESS SESSION THEN PRESS THE ORANGE BUTTON ON THE BOTTOM RIGHT
            # grid is 81... 88; 71... 78; first number is 144
            # top buttons are 91, 92, ... 99. first number is 176
            # side buttons are 89, 79... 19, first number is 144
            onoff = False
            if (midi[0][2] == 0):
                onoff = True

            if midi[0][0] == 176:
                # top row
                return (onoff, False, 0, midi[0][1]-91)
            elif midi[0][1] % 10 == 9:
                # side row
                return (onoff, False, 1, 8- int(midi[0][1] // 10))
            else:
                # grid
                x = int(midi[0][1] % 10 - 1)
                y = 8- int(midi[0][1] // 10)
                return (onoff, True, x, y)
