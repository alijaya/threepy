from __future__ import division

from OpenGL.GL import *

import pygame
from pygame.locals import *

from ctypes import *

width = 800
height = 600

pygame.init()
pygame.display.set_mode( (width, height), DOUBLEBUF|OPENGL )

diffuse = ( 1.0, 1.0, 1.0 )

image = pygame.transform.flip( pygame.image.load( "crate.gif" ), False, True ).convert( (0xff, 0xff00, 0xff0000, 0xff000000) )

vertices = [
    -0.5, -0.5,
    -0.5, 0.5,
    0.5, 0.5,
    0.5, -0.5
]
vertices = ( c_float * len( vertices ) )( *vertices )

vbo = glGenBuffers( 1 )
glBindBuffer( GL_ARRAY_BUFFER, vbo )
glBufferData( GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW )

tex = glGenTextures( 1 )
glActiveTexture( GL_TEXTURE0 )
glBindTexture( GL_TEXTURE_2D, tex )
glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE )
glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE )
glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, c_void_p( image._pixels_address ) )

vertexSource = """
#version 120
attribute vec2 position;
void main() {
    gl_Position = vec4( position, 0.0, 1.0 );
    gl_PointSize = 100;
}
"""

fragmentSource = """
#version 120
uniform sampler2D map;
void main() {
    gl_FragColor = texture2D( map, gl_PointCoord );
}
"""

glEnable( GL_POINT_SMOOTH )
glEnable( GL_POINT_SPRITE )
glEnable( GL_VERTEX_PROGRAM_POINT_SIZE )

glEnable( GL_BLEND )
glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )

vertexShader = glCreateShader( GL_VERTEX_SHADER )
glShaderSource( vertexShader, vertexSource )
glCompileShader( vertexShader )

print( "VertexShader", glGetShaderInfoLog( vertexShader ) )

fragmentShader = glCreateShader( GL_FRAGMENT_SHADER )
glShaderSource( fragmentShader, fragmentSource )
glCompileShader( fragmentShader )

print( "FragmentShader", glGetShaderInfoLog( fragmentShader ) )

shaderProgram = glCreateProgram()
glAttachShader( shaderProgram, vertexShader )
glAttachShader( shaderProgram, fragmentShader )

glLinkProgram( shaderProgram )

print( glGetProgramInfoLog( shaderProgram ) )

glUseProgram( shaderProgram )

glActiveTexture( GL_TEXTURE0 )
glBindTexture( GL_TEXTURE_2D, tex )
mapAttrib = glGetUniformLocation( shaderProgram, "map" )
glUniform1i( mapAttrib, 0 )

posAttrib = glGetAttribLocation( shaderProgram, "position" )
glBindBuffer( GL_ARRAY_BUFFER, vbo )
glVertexAttribPointer( posAttrib, 2, GL_FLOAT, GL_FALSE, 0, None )
glEnableVertexAttribArray( posAttrib )

glClearColor( 0.0, 0.0, 0.0, 1.0 )
glClear( GL_COLOR_BUFFER_BIT )

glDrawArrays( GL_POINTS, 0, len( vertices ) // 2 )

pygame.display.flip()

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            quit()
    
    pygame.time.wait( 10 )