from OpenGL.GL import *

mode = None

def setMode( value ):

    global mode
    mode = value

def render( start, count ):

    glDrawArrays( mode, start, count )

    # TODO infoRender

# TODO def renderInstances( geometry, start, count ):