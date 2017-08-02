from __future__ import division

import pygame
from pygame.locals import *

import THREE
from THREE.utils import Expando

from OpenGL.GL import *

import numpy as np

width = 800
height = 600

pygame.init()
pygame.display.set_mode( (width, height), DOUBLEBUF|OPENGL )

scene = THREE.Scene()
camera = THREE.PerspectiveCamera( 75, width / height, 0.1, 1000 )

renderer = THREE.OpenGLRenderer

geometry = THREE.BoxGeometry( 1, 1, 1 )
material = THREE.MeshBasicMaterial( Expando( color = 0x00ff00 ) )
cube = THREE.Mesh( geometry, material )
scene.add( cube )

camera.position.z = 5

scene.updateMatrixWorld()
camera.updateMatrixWorld()

projectionMatrix = camera.projectionMatrix.clone().multiply( camera.matrixWorldInverse ).elements
cube.modelViewMatrix.multiplyMatrices( camera.matrixWorldInverse, cube.matrixWorld )
modelViewMatrix = cube.modelViewMatrix.elements

diffuse = ( 0.0, 1.0, 0.0 )
opacity = 1.0

def flatten( vs ):
    ret = []
    for v in vs: ret.extend( [ v.x, v.y, v.z ] )
    return ret

positions = np.array( flatten( cube.geometry.vertices ), np.float32 )

def flatten2( idxs ):
    ret = []
    for idx in idxs: ret.extend( [ idx.a, idx.b, idx.c ] )
    return ret

indices = np.array( flatten2( cube.geometry.faces ), np.uint32 )


glPositionBuffer = glGenBuffers( 1 )
glBindBuffer( GL_ARRAY_BUFFER, glPositionBuffer )
glBufferData( GL_ARRAY_BUFFER, positions, GL_STATIC_DRAW )

glIndicesBuffer = glGenBuffers( 1 )
glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, glIndicesBuffer )
glBufferData( GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW )


vertexGlsl = """
uniform mat4 modelViewMatrix;
uniform mat4 projectionMatrix;
attribute vec3 position;
void main() {
    gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
}"""    
fragmentGlsl = """
uniform vec3 diffuse;
uniform float opacity;
void main() {
    gl_FragColor = vec4( 1., 1., 1., 1. );
}"""

glVertex = glCreateShader( GL_VERTEX_SHADER )
glShaderSource( glVertex, vertexGlsl )
glCompileShader( glVertex )

glFragment = glCreateShader( GL_FRAGMENT_SHADER )
glShaderSource( glFragment, fragmentGlsl )
glCompileShader( glFragment )

glProgram = glCreateProgram()
glAttachShader( glProgram, glVertex )
glAttachShader( glProgram, glFragment )
glLinkProgram( glProgram )
glUseProgram( glProgram )


glProjectionMatrixUniform = glGetUniformLocation( glProgram, "projectionMatrix" )
glModelViewMatrixUniform = glGetUniformLocation( glProgram, "modelViewMatrix" )
glDiffuseUniform = glGetUniformLocation( glProgram, "diffuse" )
glOpacityUniform = glGetUniformLocation( glProgram, "opacity" )

glUniformMatrix4fv( glProjectionMatrixUniform, 1, False, projectionMatrix )
glUniformMatrix4fv( glModelViewMatrixUniform, 1, False, modelViewMatrix )
glUniform3f( glDiffuseUniform, diffuse[ 0 ], diffuse[ 1 ], diffuse[ 2 ] )
glUniform1f( glOpacityUniform, opacity )


glPositionAttrib = glGetAttribLocation( glProgram, "position" )
glEnableVertexAttribArray( glPositionAttrib )
glVertexAttribPointer( glPositionAttrib, 3, GL_FLOAT, False, 0, None )


glClearColor( 0.0, 0.0, 0.0, 1.0 )
glClear( GL_COLOR_BUFFER_BIT )

# glDrawArrays( GL_TRIANGLES, 0, positions.size )
glDrawElements( GL_TRIANGLES, indices.size, GL_UNSIGNED_INT, None )

pygame.display.flip()

# renderer.render( scene, camera )

while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            quit()
    
    pygame.time.wait( 10 )