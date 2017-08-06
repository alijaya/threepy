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
materials = None
parameters = None
clock = pygame.time.Clock()

width, height = 800, 600

windowHalfX = width / 2
windowHalfY = height / 2

def toAbs( rel ):

    return os.path.join( os.path.dirname( __file__ ), rel )

def init():

    global renderer, camera, scene, materials, parameters

    pygame.init()
    pygame.display.set_mode( (width, height), DOUBLEBUF|OPENGL )
    renderer = THREE.OpenGLRenderer
    renderer.init()
    renderer.setSize( width, height )

    camera = THREE.PerspectiveCamera( 75, width / height, 1, 3000 )
    camera.position.z = 1000

    scene = THREE.Scene()
    scene.fog = THREE.FogExp2( 0x000000, 0.0008 )

    geometry = THREE.Geometry()

    textureLoader = THREE.TextureLoader()
    sprite1 = textureLoader.load( toAbs( "textures/sprites/snowflake1.png" ) )
    sprite2 = textureLoader.load( toAbs( "textures/sprites/snowflake2.png" ) )
    sprite3 = textureLoader.load( toAbs( "textures/sprites/snowflake3.png" ) )
    sprite4 = textureLoader.load( toAbs( "textures/sprites/snowflake4.png" ) )
    sprite5 = textureLoader.load( toAbs( "textures/sprites/snowflake5.png" ) )

    for i in xrange( 10000 ):

        vertex = THREE.Vector3()
        vertex.x = random.uniform( -1000, 1000 )
        vertex.y = random.uniform( -1000, 1000 )
        vertex.z = random.uniform( -1000, 1000 )

        geometry.vertices.append( vertex )

    parameters = [
        [ [1.0, 0.2, 0.5], sprite2, 20 ],
        [ [0.95, 0.1, 0.5], sprite3, 15 ],
        [ [0.90, 0.05, 0.5], sprite1, 10 ],
        [ [0.85, 0, 0.5], sprite5, 8 ],
        [ [0.80, 0, 0.5], sprite4, 5 ]
    ]

    materials = []

    for param in parameters:

        color = param[0]
        sprite = param[1]
        size = param[2]

        mat = THREE.PointsMaterial( size = size, map = sprite, blending = THREE.AdditiveBlending, depthTest = False, transparent = True )
        mat.color.setHSL( color[0], color[1], color[2] )
        materials.append( mat )

        particles = THREE.Points( geometry, mat )

        particles.rotation.x = random.uniform( 0, 2 * math.pi )
        particles.rotation.y = random.uniform( 0, 2 * math.pi )
        particles.rotation.z = random.uniform( 0, 2 * math.pi )

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

        for i in xrange( len( scene.children ) ):

            object = scene.children[ i ]

            if isinstance( object, THREE.Points ):

                object.rotation.y = time * ( i + 1 if i < 4 else - ( i + 1 ) )

        for i in xrange( len( parameters ) ):

            color = parameters[i][0]

            h = ( 360 * ( color[0] + time ) % 360 ) / 360
            materials[i].color.setHSL( h, color[1], color[2] )

        renderer.render( scene, camera )

        pygame.display.flip()
        pygame.time.wait( 10 )

if __name__ == "__main__":

    init()
    animate()