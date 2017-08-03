from __future__ import division
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

    from ..OpenGLRenderer import _infoRender as infoRender

    glDrawElements( mode, count, type, c_void_p( start * bytesPerElement ) )

    infoRender.calls += 1
    infoRender.vertices += count

    if mode == GL_TRIANGLES: infoRender.faces += count // 3
    elif mode == GL_POINTS: infoRender.points += count

# TODO def renderInstances( geometry, start, count ):