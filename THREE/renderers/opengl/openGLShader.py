
from OpenGL.GL import *

def OpenGLShader( type, string ):

    shader = glCreateShader( type )

    glShaderSource( shader, string )
    glCompileShader( shader )

    # debug

    return shader