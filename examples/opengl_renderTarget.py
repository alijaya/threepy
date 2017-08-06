from __future__ import division

import os

import pygame
from pygame.locals import *

import THREE
from THREE.utils import Expando

renderer = None
camera = None
scene = None
bufferScene = None
bufferCamera = None
bufferTexture = None
boxObject = None
mainBoxObject = None

width, height = 800, 600

def toAbs( rel ):

    return os.path.join( os.path.dirname( __file__ ), rel )

def init():

    global renderer, camera, scene, boxObject, bufferScene, bufferTexture, bufferCamera, mainBoxObject

    pygame.init()
    pygame.display.set_mode( (width, height), DOUBLEBUF|OPENGL )
    renderer = THREE.OpenGLRenderer
    renderer.init()
    renderer.setSize( width, height )

    camera = THREE.PerspectiveCamera( 70, width / height, 1, 1000 )

    bufferCamera = THREE.PerspectiveCamera( 70, 1, 1, 1000 )

    scene = THREE.Scene()

    bufferScene = THREE.Scene()

    bufferTexture = THREE.OpenGLRenderTarget( 256, 256, minFilter = THREE.LinearFilter, magFilter = THREE.NearestFilter )
    
    redMaterial = THREE.MeshBasicMaterial( color = 0xF06565 )
    boxGeometry = THREE.BoxGeometry( 5, 5, 5 )
    boxObject = THREE.Mesh( boxGeometry, redMaterial )
    boxObject.position.z = -10
    bufferScene.add( boxObject )

    blueMaterial = THREE.MeshBasicMaterial( color = 0x7074FF )
    plane = THREE.PlaneBufferGeometry( width, height )
    planeObject = THREE.Mesh( plane, blueMaterial )
    planeObject.position.z = -15
    bufferScene.add( planeObject )

    boxMaterial = THREE.MeshBasicMaterial( map = bufferTexture.texture )
    boxGeometry2 = THREE.BoxGeometry( 5, 5, 5 )
    mainBoxObject = THREE.Mesh( boxGeometry2, boxMaterial )
    mainBoxObject.position.z = -10
    scene.add( mainBoxObject )

def animate():

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                quit()

        boxObject.rotation.y += 0.01
        boxObject.rotation.x += 0.01

        mainBoxObject.rotation.y += 0.01
        mainBoxObject.rotation.x += 0.01

        renderer.render( bufferScene, bufferCamera, bufferTexture )
        renderer.render( scene, camera )

        pygame.display.flip()
        pygame.time.wait( 10 )

if __name__ == "__main__":

    init()
    animate()