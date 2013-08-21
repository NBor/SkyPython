This is SkyPython, a port of Google's Stardroid Android Java application.

The goal of this project is to recreate Stardroid in the Python programming 
language to so that it can be used for educational purposes as well as to use 
it on other platforms. 

This port is as close to the original Java source as possible and for ease, 
comments are often ported verbatim. In the absence of the Android framework,
PySide is used to complete SkyPython. The majority of the code that pertains
to PySide is encapsulated in the src/skypython/SkyPython.py file

FEATURES NOT IMPLEMENTED:
Searching, Night Vision Mode, Image Gallery and Time Travel.

KNOW ISSUSES:
1) Sky Gradient is not alligned with the sun
2) Text does not render exactly as in the original
3) Images for planets do not render

REQUIREMENTS:

1) Python 2.7 with standard library, Python 3 support is not available.

2) PySide 1.1.2, Python library with Qt bindings

3) PyOpenGL 3.0.2, OpenGL bindings for Python

4) NumPy, Python library for numerical and scientific computing

5) ProtoBuf, Google's data interchange format which is available for Python

USAGE ECLIPSE:

This project was developed in eclipse with the PyDev plugin and therfore
can be imported and run inside the eclipse IDE with this plugin.

USAGE COMMANDLINE:

This will start the program normally
:~>python main.py

This will run all available pydoc test found in src/testing. One failure is 
expected in UnitsTesting.py, line 99 (this failure is present in the original).
:~>python main.py -d

This will run the pydoc test as well as produce six images of the sky at
perpendicular angles specified in src/utils/DebugOptions.py.
:~>python main.py -d images

Note: "images" flag will break if 'DRAWING = debug_opts["No debug settings"]'
is set in src/utils/DebugOptions.py.