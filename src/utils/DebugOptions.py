'''
Created on 2013-07-16

@author: Neil
'''

import math

debug_opts = {"No debug settings"  : None,
              "View only stars"    : "STARS ONLY",
              "Stars, Const, Mess" : "FIRST 3",
              "View only points"   : "POINTS ONLY",
              "Draw all regions"   : "YES",
              "View white objects" : "WHITE ONLY",
              "Capture screen"     : "YES",
              "Rotate screen"      : "YES"}

class Debug(object):
    LAYER = debug_opts["No debug settings"]
    DRAWING = debug_opts["No debug settings"]
    ALLREGIONS = debug_opts["No debug settings"]
    COLOR = debug_opts["No debug settings"]
    PHOTO = debug_opts["Capture screen"]
    ROTATE = debug_opts["No debug settings"]
    
def rotateUpRight():
    return [math.pi/2, 0]

# def print_screen(context):
#     '''
#     '''
#     import Image
#     import OpenGL.GL as GL
#     save_count = 0
#     
#     vp = GL.glGetIntegerv(GL.GL_VIEWPORT)
#     print vp
#     pixel_array = GL.glReadPixels(0,0,vp[2],vp[3],GL.GL_RGB,GL.GL_UNSIGNED_BYTE)
#     
#     pilImage = Image.fromstring(mode="RGBA",size=(vp[3],vp[2]),data=pixel_array)
#     pilImage = pilImage.transpose(Image.FLIP_TOP_BOTTOM)
#     pilImage.save(str(save_count) + '.png')
    
    