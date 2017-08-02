from __future__ import division

import numpy as np

from OpenGL.GL import *

import pygame
from pygame.locals import *

from ctypes import c_void_p

width = 800
height = 600

pygame.init()
pygame.display.set_mode( (width, height), DOUBLEBUF|OPENGL )

vertices = np.array( [
    0,0,
    -0.5, -0.5,
    -0.5, 0.5,
    0.5, 0.5,
    0.5, -0.5
], np.float32 )

indices = np.array( [
    0, 1, 2,
    0, 2, 3,
    0, 3, 4,
    0, 4, 1
], np.uint32 )

vbo = glGenBuffers( 1 )
glBindBuffer( GL_ARRAY_BUFFER, vbo )
glBufferData( GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW )

vbi = glGenBuffers( 1 )
glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, vbi )
glBufferData( GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW )

vertexSource = """
attribute vec2 position;
void main() {
    gl_Position = vec4( position, 0.0, 1.0 );
}
"""

fragmentSource = """
uniform vec3 diffuse;
void main() {
    gl_FragColor = vec4( diffuse, 1.0 );
}
"""

vertexShader = glCreateShader( GL_VERTEX_SHADER )
glShaderSource( vertexShader, vertexSource )
glCompileShader( vertexShader )

print( glGetShaderInfoLog( vertexShader ) )

fragmentShader = glCreateShader( GL_FRAGMENT_SHADER )
glShaderSource( fragmentShader, fragmentSource )
glCompileShader( fragmentShader )

print( glGetShaderInfoLog( fragmentShader ) )

shaderProgram = glCreateProgram()
glAttachShader( shaderProgram, vertexShader )
glAttachShader( shaderProgram, fragmentShader )

glLinkProgram( shaderProgram )

print( glGetProgramInfoLog( shaderProgram ) )

glUseProgram( shaderProgram )

difAttrib = glGetUniformLocation( shaderProgram, "diffuse" )
glUniform3fv( difAttrib, 1, np.array([1.0, 0.0, 0.0], np.float32) )

posAttrib = glGetAttribLocation( shaderProgram, "position" )
glVertexAttribPointer( posAttrib, 2, GL_FLOAT, GL_FALSE, 0, None )
glEnableVertexAttribArray( posAttrib )

glClearColor( 0.0, 0.0, 0.0, 0.0 )
glClear( GL_COLOR_BUFFER_BIT )

# glDrawArrays( GL_TRIANGLES, 0, 3 )
startIndex = 1
itemPerData = 3
dataSize = 4
count = 3
glDrawElements( GL_TRIANGLES, itemPerData * count, GL_UNSIGNED_INT, c_void_p( startIndex * itemPerData * dataSize ) )


pygame.display.flip()

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            quit()
    
    pygame.time.wait( 10 )