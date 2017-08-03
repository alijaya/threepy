from __future__ import division

from OpenGL.GL import *

mode = None

def setMode( value ):

    global mode
    mode = value

def render( start, count ):

    from ..OpenGLRenderer import _infoRender as infoRender

    glDrawArrays( mode, start, count )

    infoRender.calls += 1
    infoRender.vertices += count

    if mode == GL_TRIANGLES: infoRender.faces += count // 3
    elif mode == GL_POINTS: infoRender.points += count

# TODO def renderInstances( geometry, start, count ):