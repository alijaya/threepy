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

image = pygame.image.load( "crate.gif" ).convert( (0xff, 0xff00, 0xff0000, 0xff000000) )
print(image.get_masks())

vertices = [
    -0.5, -0.5,
    -0.5, 0.5,
    0.5, 0.5,
    0.5, -0.5
]
vertices = ( c_float * len( vertices ) )( *vertices )

colors = [
    1.0, 1.0, 1.0,
    1.0, 1.0, 1.0,
    1.0, 1.0, 1.0,
    1.0, 1.0, 1.0
]
colors = ( c_float * len( colors ) )( *colors )

uvs = [
    0.0, 0.0,
    0.0, 1.0,
    1.0, 1.0,
    1.0, 0.0
]
uvs = ( c_float * len( uvs ) )( *uvs )

indices = [
    0, 1, 2,
    2, 3, 0
]
indices = ( c_uint * len( indices ) )( *indices )

vbo = glGenBuffers( 1 )
glBindBuffer( GL_ARRAY_BUFFER, vbo )
glBufferData( GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW )

vbc = glGenBuffers( 1 )
glBindBuffer( GL_ARRAY_BUFFER, vbc )
glBufferData( GL_ARRAY_BUFFER, colors, GL_STATIC_DRAW )

vbuv = glGenBuffers( 1 )
glBindBuffer( GL_ARRAY_BUFFER, vbuv )
glBufferData( GL_ARRAY_BUFFER, uvs, GL_STATIC_DRAW )

vbi = glGenBuffers( 1 )
glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, vbi )
glBufferData( GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW )

tex = glGenTextures( 1 )
glActiveTexture( GL_TEXTURE0 )
glBindTexture( GL_TEXTURE_2D, tex )
glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE )
glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE )
glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
glTexImage2D( GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, c_void_p( image._pixels_address ) )

vertexSource = """
attribute vec2 position;
attribute vec2 uv;
varying vec2 vUv;
void main() {
    gl_Position = vec4( position, 0.0, 1.0 );
    vUv = uv;
}
"""

fragmentSource = """
uniform vec3 diffuse;
uniform sampler2D map;
varying vec2 vUv;
void main() {
    gl_FragColor = texture2D( map, vUv );
}
"""

glEnable( GL_BLEND )
glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA )

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
glUniform3fv( difAttrib, 1, diffuse )

glActiveTexture( GL_TEXTURE0 )
glBindTexture( GL_TEXTURE_2D, tex )
mapAttrib = glGetUniformLocation( shaderProgram, "map" )
glUniform1i( mapAttrib, 0 )

posAttrib = glGetAttribLocation( shaderProgram, "position" )
glBindBuffer( GL_ARRAY_BUFFER, vbo )
glVertexAttribPointer( posAttrib, 2, GL_FLOAT, GL_FALSE, 0, None )
glEnableVertexAttribArray( posAttrib )

# colAttrib = glGetAttribLocation( shaderProgram, "color" )
# glBindBuffer( GL_ARRAY_BUFFER, vbc )
# glVertexAttribPointer( colAttrib, 3, GL_FLOAT, GL_FALSE, 0, None )
# glEnableVertexAttribArray( colAttrib )

uvAttrib = glGetAttribLocation( shaderProgram, "uv" )
glBindBuffer( GL_ARRAY_BUFFER, vbuv )
glVertexAttribPointer( uvAttrib, 2, GL_FLOAT, GL_FALSE, 0, None )
glEnableVertexAttribArray( uvAttrib )

glClearColor( 1.0, 1.0, 0.0, 1.0 )
glClear( GL_COLOR_BUFFER_BIT )

glDrawElements( GL_TRIANGLES, len( indices ), GL_UNSIGNED_INT, None )


pygame.display.flip()

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            quit()
    
    pygame.time.wait( 10 )