from OpenGL.GL import *

mode = None

def setMode( value ):

    mode = value

def render( start, count ):

    glDrawArrays( mode, start, count )

    # TODO infoRender

# TODO def renderInstances( geometry, start, count ):