'''
Created on 2013-05-14

@author: Neil
'''

import sys
from PySide.QtGui import QApplication

from skypython.SkyPython import SkyPython
from layers.LayerManager import instantiate_layer_manager
from control.AstronomerModel import AstronomerModel
from renderer.SkyRenderer import SkyRenderer
from control.ZeroMagneticDeclinationCalculator import ZeroMagneticDeclinationCalculator as ZMDC

def start_application():
    layer_manager = instantiate_layer_manager()
    sky_renderer = SkyRenderer()
    model = AstronomerModel(ZMDC())
    
    app = QApplication(sys.argv)
    w = SkyPython(sky_renderer, layer_manager, model)
    w.show()
    app.exec_()

if __name__ == '__main__':
    start_application()
    
    