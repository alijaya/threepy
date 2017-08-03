from ctypes import c_void_p

from OpenGL.GL import *

mode = None
type = None
bytesPerElement = None

def setMode( value ):

    global mode
    mode = value

def setIndex( value ):

    global type, bytesPerElement

    type = value.type
    bytesPerElement = value.bytesPerElement

def render( start, count ):

    glDrawElements( mode, count, type, c_void_p( start * bytesPerElement ) )

    # TODO infoRender

# TODO def renderInstances( geometry, start, count ):