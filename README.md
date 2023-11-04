# Launchpad
Launchpad is a Python module that lets developers communicate with different types of Novation Launchpads without knowing the specifics of each type. The currently supported Launchpads are the Launchpad Mini, Launchpad MK2, and Launchpad Mini MK3.

## Coordinate system
The code uses the following coordinate system.
1. A boolean that is TRUE if you are referring to the 8*8 grid on the Launchpad, and FALSE if you are referring to the top or side buttons
2. If part (2) is TRUE, then this is the x-index (0 to 7) of the button you're referring to. If part (2) is FALSE, then this is 0 for the top buttons and 1 for the side buttons.
3. If part(2) is TRUE, then this is the y-index (0 to 7) of the button you're referring to. If part (2) is FALSE, then this is an integer from 0-7 referring to the index of the button.
Note that (x=0, y=0) is the button on the top left.

## Structure
There are two main files here:
- launchpad.py contains the relevant code for the module. The two functions users will use are register_callback and set_function
- sample_app.py is a basic app made with Kivy that is an example of how to use launchpad.py

To read in input from a connected launchpad, you will need to use the following lines:
```
self.midi_io = lp()
self.midi_io.register_callback( #CALLBACK_FUNC )
```
where you should replace #CALLBACK_FUNC with your callback function (function called when a button on the connected launchpad is pressed). Your callback function should take in a message that is a tuple of four things: a boolean describing if the button has turned on or off, and three things -- a boolean, an integer index, and an integer index -- that represent the coordinate system above.

To set colors on a connected launchpad, you will need the following line:
```
 self.midi_io.set_color(#BOOL, #x, #y, #(R,G,B))
```
where #BOOL, #x, and #y should be replaced with your desired buttons as described in the coordinate system. #(R,G,B) should be replaced with the RGB of your desired color. Each value should be an integer between 0 and 255 (inclusive), where (0,0,0) represents turning the button off. Note that the colors that will actually appear are the best estimates of your desired color given the hardware restrictions.
