from __future__ import division
import math

import os

import pygame
from pygame.locals import *

import THREE
from THREE.utils import Expando

renderer = None
camera = None
scene = None
clock = pygame.time.Clock()

width, height = 800, 600

def toAbs( rel ):

    return os.path.join( os.path.dirname( __file__ ), rel )

def init():

    global renderer, camera, scene, mesh

    pygame.init()
    pygame.display.set_mode( (width, height), DOUBLEBUF|OPENGL )
    renderer = THREE.OpenGLRenderer
    renderer.init()
    renderer.setSize( width, height )

    camera = THREE.PerspectiveCamera( 45, width / height, 10, 2000 ) # change near from 1 to 10, to avoid z fighting :(
    camera.position.z = 400

    scene = THREE.Scene()

    # scene.add( THREE.AmbientLight( 0x404040 ) )

    # light = THREE.DirectionLight( 0xffffff )
    # light.position.set( 0, 1, 0 )
    # scene.add( light )

    map = THREE.TextureLoader().load( toAbs( "textures/UV_Grid_Sm.jpg" ) )
    map.wrapS = map.wrapT = THREE.RepeatWrapping
    map.anisotropy = 16

    material = THREE.MeshLambertMaterial( map = map, side = THREE.DoubleSide )
    # material = THREE.MeshBasicMaterial( map = map, side = THREE.DoubleSide )

    object = THREE.Mesh( THREE.SphereGeometry( 75, 20, 10 ), material )
    object.position.set( -400, 0, 200 )
    scene.add( object )

    object = THREE.Mesh( THREE.IcosahedronGeometry( 75, 1 ), material )
    object.position.set( -200, 0, 200 )
    scene.add( object )

    object = THREE.Mesh( THREE.OctahedronGeometry( 75, 2 ), material )
    object.position.set( 0, 0, 200 )
    scene.add( object )

    object = THREE.Mesh( THREE.TetrahedronGeometry( 75, 0 ), material )
    object.position.set( 200, 0, 200 )
    scene.add( object )

    #

    object = THREE.Mesh( THREE.PlaneGeometry( 100, 100, 4, 4 ), material )
    object.position.set( -400, 0, 0 )
    scene.add( object )

    object = THREE.Mesh( THREE.BoxGeometry( 100, 100, 100, 4, 4, 4 ), material )
    object.position.set( -200, 0, 0 )
    scene.add( object )

    object = THREE.Mesh( THREE.CircleGeometry( 50, 20, 0, math.pi * 2 ), material )
    object.position.set( 0, 0, 0 )
    scene.add( object )

    object = THREE.Mesh( THREE.RingGeometry( 10, 40, 20, 5, 0, math.pi * 2 ), material )
    object.position.set( 200, 0, 0 )
    scene.add( object )

    object = THREE.Mesh( THREE.CylinderGeometry( 25, 75, 100, 40, 5 ), material )
    object.position.set( 400, 0, 0 )
    scene.add( object )

    #

    points = []

    for i in xrange( 50 ):

        points.append( THREE.Vector2( math.sin( i * 0.2 ) * math.sin( i * 0.1 ) * 15 + 50, ( i - 5 ) * 2 ) )
    
    object = THREE.Mesh( THREE.LatheGeometry( points, 20 ), material )
    object.position.set( -400, 0, -200 )
    scene.add( object )

    object = THREE.Mesh( THREE.TorusGeometry( 50, 20, 20, 20 ), material )
    object.position.set( -200, 0, -200 )
    scene.add( object )

    object = THREE.Mesh( THREE.TorusKnotGeometry( 50, 10, 50, 20 ), material )
    object.position.set( 0, 0, -200 )
    scene.add( object )

    # object = THREE.AxisHelper( 50 )
    # object.position.set( 200, 0, -200 )
    # scene.add( object )

    # object = THREE.ArrowHelper( THREE.Vector3( 0, 1, 0 ), THREE.Vector3( 0, 0, 0 ), 50 )
    # object.position.set( 400, 0, -200 )
    # scene.add( object )

def animate():

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                quit()

        clock.tick()
        # print( clock.get_fps() )

        timer = pygame.time.get_ticks() * 0.0001

        camera.position.x = math.cos( timer ) * 800
        camera.position.y = math.sin( timer ) * 800

        camera.lookAt( scene.position )

        for object in scene.children:

            object.rotation.x = timer * 5
            object.rotation.y = timer * 2.5

        renderer.render( scene, camera )

        pygame.display.flip()
        pygame.time.wait( 10 )

if __name__ == "__main__":

    init()
    animate()