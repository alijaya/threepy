from __future__ import division
import math
import random

import os

import pygame
from pygame.locals import *

import THREE
from THREE.utils import Expando

renderer = None
camera = None
material = None
clock = pygame.time.Clock()

width, height = 800, 600

windowHalfX = width / 2
windowHalfY = height / 2

def toAbs( rel ):

    return os.path.join( os.path.dirname( __file__ ), rel )

def init():

    global renderer, camera, scene, material

    pygame.init()
    pygame.display.set_mode( (width, height), DOUBLEBUF|OPENGL )
    renderer = THREE.OpenGLRenderer
    renderer.init()
    renderer.setSize( width, height )

    camera = THREE.PerspectiveCamera( 50, width / height, 10, 3000 )
    camera.position.z = 1400

    scene = THREE.Scene()
    scene.fog = THREE.FogExp2( 0x000000, 0.0009 )

    geometry = THREE.Geometry()

    sprite = THREE.TextureLoader().load( toAbs( "textures/sprites/ball.png" ) )

    for i in xrange( 5000 ):

        vertex = THREE.Vector3()
        vertex.x = random.uniform( -1000, 1000 )
        vertex.y = random.uniform( -1000, 1000 )
        vertex.z = random.uniform( -1000, 1000 )

        geometry.vertices.append( vertex )

        color = THREE.Color()
        color.setHSL( ( vertex.x + 1000 ) / 2000, 1, 0.5 )
        geometry.colors.append( color )

    material = THREE.PointsMaterial( size = 85, map = sprite, vertexColors = THREE.VertexColors, alphaTest = 0.5, transparent = True )
    material.color.setHSL( 1.0, 0.2, 0.7 )

    particles = THREE.Points( geometry, material )
    scene.add( particles )

def animate():

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                quit()

        clock.tick()
        # print( clock.get_fps() )

        time = pygame.time.get_ticks() * 0.0001

        mouseX, mouseY = pygame.mouse.get_pos()

        mouseX -= windowHalfX
        mouseY -= windowHalfY

        camera.position.x += ( mouseX - camera.position.x ) * 0.05
        camera.position.y += ( - mouseY - camera.position.y ) * 0.05

        camera.lookAt( scene.position )

        h = ( 360 * ( 1.0 + time ) % 360 ) / 360
        material.color.setHSL( h, 1.0, 0.6 )

        renderer.render( scene, camera )

        pygame.display.flip()
        pygame.time.wait( 10 )

if __name__ == "__main__":

    init()
    animate()