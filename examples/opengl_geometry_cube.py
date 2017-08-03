from __future__ import division

import os

import pygame
from pygame.locals import *

import THREE
from THREE.utils import Expando

renderer = None
camera = None
scene = None

mesh = None

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

    camera = THREE.PerspectiveCamera( 70, width / height, 1, 1000 )
    camera.position.z = 400

    scene = THREE.Scene()

    texture = THREE.TextureLoader().load( toAbs( "textures/crate.gif" ) )
    # print(texture.image)

    geometry = THREE.BoxBufferGeometry( 200, 200, 200 )
    material = THREE.MeshBasicMaterial( map = texture )

    mesh = THREE.Mesh( geometry, material )
    scene.add( mesh )

def animate():

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                quit()

        mesh.rotation.x += 0.005
        mesh.rotation.y += 0.01

        renderer.render( scene, camera )

        pygame.display.flip()
        pygame.time.wait( 10 )

if __name__ == "__main__":

    init()
    animate()