# Launchpad

Launchpad is a Python module that lets developers communicate with different types of Novation Launchpads without needing to know the specifics of each type. The currently supported Launchpads are:

- Launchpad Mini
- Launchpad MK2
- Launchpad Mini MK3

## Setup

- `pip install python-rtmidi`
- `pip install "kivy[base]"` - to run sample_app

## Coordinate system

The code uses the following coordinate system:

- `main_grid` (boolean): True when referring to the 8\*8 grid on the Launchpad, and False when referring to the top or side auxiliary buttons
- `x`: If `main_grid` is True, this is the x-index (0 to 7) of the button. If False, this is 0 for the top buttons and 1 for the side buttons.
- `y`: If `main_grid` is True, this is the y-index (0 to 7) of the button. If False, this is the index (0-7) of the auxiliary top or side button.

Note that (x=0, y=0) is the button on the top left.

## Usage

There are two main files here:

- `launchpad.py` defines the `Launchpad` object, with the two main methods `register_callback` and `set_color`
- `sample_app.py` is a sample app showing basic usage, made with [Kivy](https://kivy.org/).

First, create the launchpad object, and register a callback to receive button actions:

```
self.launchpad = Launchpad()
self.launchpad.register_callback( CALLBACK_FUNC )
```

Where `CALLBACK_FUNC` takes 4 arguments: `main_grid`, `x`, `y`, `down_up`.

- `main_grid`, `x`, `y` define the button coordinate, as described above.
- `down_up` is a boolean with either `True` for button down or `False` for button up.

To set colors on a Launchpad:

```
 self.launchpad.set_color(main_grid, x, y, color)
```

- `main_grid`, `x`, `y` define the button coordinate, as described above.
- `color` is the tuple `(R,G,B)` for the desired color. Each value should be an integer between 0 and 127. (0,0,0) represents turning the button off. The colors that will actually appear are the best approximation of the desired color for the particular version of the hardware.
