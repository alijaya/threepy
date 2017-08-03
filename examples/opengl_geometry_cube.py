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

width, height = 1920, 1080

def toAbs( rel ):

    return os.path.join( os.path.dirname( __file__ ), rel )

def init():

    global renderer, camera, scene, mesh

    camera = THREE.PerspectiveCamera( 70, width / height, 1, 1000 )
    camera.position.z = 400

    scene = THREE.Scene()

    texture = THREE.TextureLoader().load( toAbs( "textures/crate.gif" ) )

    geometry = THREE.BoxBufferGeometry( 200, 200, 200 )
    material = THREE.MeshBasicMaterial( Expando( map = texture ) )

    mesh = THREE.Mesh( geometry, material )
    scene.add( mesh )

    renderer = THREE.OpenGLRenderer
    pygame.init()
    pygame.display.set_mode( (width, height), DOUBLEBUF|OPENGL )
    renderer.setSize( width, height )

def animate():

    while True:

        mesh.rotation.x += 0.005
        mesh.rotation.y += 0.01

        renderer.render( scene, camera )

if __name__ == "__main__":

    init()
    animate()