'''
Created on 2013-07-16

@author: Neil
'''

debug_opts = {"No debug settings"  : None,
              "View only stars"    : "STARS ONLY",
              "View only points"   : "POINTS ONLY",
              "View white objects" : "WHITE ONLY",
              "Capture screen"     : "YES"}

class Debug(object):
    LAYER = debug_opts["View only stars"]
    DRAWING = debug_opts["View only points"]
    COLOR = debug_opts["View white objects"]
    PHOTO = debug_opts["Capture screen"]
    
def print_screen(context):
    '''
    '''
    import Image
    import OpenGL.GL as GL
    save_count = 0
    
    vp = GL.glGetIntegerv(GL.GL_VIEWPORT)
    print vp
    pixel_array = GL.glReadPixels(0,0,vp[2],vp[3],GL.GL_RGB,GL.GL_UNSIGNED_BYTE)
    
    pilImage = Image.fromstring(mode="RGBA",size=(vp[3],vp[2]),data=pixel_array)
    pilImage = pilImage.transpose(Image.FLIP_TOP_BOTTOM)
    pilImage.save(str(save_count) + '.png')
    
    