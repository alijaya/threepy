import OpenGLState as state

from OpenGL.GL import *

from ...math import color

clearColor = color.Color( 0x000000 )
clearAlpha = 0

def setClear( color, alpha ):

    premultipliedAlpha = True # TODO
    state.colorBuffer.setClear( color.r, color.g, color.b, alpha, premultipliedAlpha )

def render( renderList, scene, camera, forceClear ):

    background = scene.background

    if not background:

        setClear( clearColor, clearAlpha )
    
    elif background and hasattr( background, "isColor" ):

        setClear( background, 1 )
        forceClear = True

    # TODO another type of background