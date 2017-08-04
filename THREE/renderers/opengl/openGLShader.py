
from OpenGL.GL import *

import logging

def addLineNumbers( string ):

    lines = string.split( "\n" )

    for i in xrange( len( lines ) ):

        lines[ i ] = "%4s| %s" % ( ( i + 1 ), lines[ i ] )

    return "\n".join( lines )

def OpenGLShader( type, string ):

    shader = glCreateShader( type )

    glShaderSource( shader, string )
    glCompileShader( shader )

    # debug

    if glGetShaderiv( shader, GL_COMPILE_STATUS ) == False:

        logging.error( "THREE.WebGLShader: Shader couldn't compile.")

    infoLog = glGetShaderInfoLog( shader )
    if infoLog != "":

        logging.warning( "THREE.WebGLShader: gl.getShaderInfoLog() %s \n%s \n%s", 
            "vertex" if type == GL_VERTEX_SHADER else "fragment", 
            infoLog,
            addLineNumbers( string ) )

    return shader