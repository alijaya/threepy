import OpenGLState as state

from OpenGL.GL import *

from ...math import color

clearColor = color.Color( 0x000000 )
clearAlpha = 0

def getClearColor():

    return clearColor

def setClearColor( color, alpha = 1 ):

    global clearAlpha

    clearColor.set( color )
    clearAlpha = alpha
    setClear( clearColor, clearAlpha )

def getClearAlpha():

    return clearAlpha

def setClearAlpha( alpha ):

    global clearAlpha
    clearAlpha = alpha

def setClear( color, alpha ):

    premultipliedAlpha = True # TODO
    state.colorBuffer.setClear( color.r, color.g, color.b, alpha, premultipliedAlpha )

def render( renderList, scene, camera, forceClear ):

    from .. import OpenGLRenderer as renderer

    background = scene.background

    if not background:

        setClear( clearColor, clearAlpha )
    
    elif background and hasattr( background, "isColor" ):

        setClear( background, 1 )
        forceClear = True

    if renderer.autoClear or forceClear:

        renderer.clear( renderer.autoClearColor, renderer.autoClearDepth, renderer.autoClearStencil )

    # TODO another type of background