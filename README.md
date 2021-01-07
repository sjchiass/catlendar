# Requirements

`Pillow` and `numpy` are required

Most likely this only runs on Linux since `Pillow` uses DejaVu fonts for the calendar. On Windows, you can either get these fonts or modify the code to use Windows font files (TODO: clean up code to make this a lot easier).

# Actions

This is my first time using GitHub actions.

  * I have one action running `make.py` on different python versions. This is sort of like a coverage test.
  * Another action releases a self-contained html file with the calendar.
