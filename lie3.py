from __future__ import division

import pygame
from pygame.locals import *

import THREE
from THREE.utils import Expando

from OpenGL.GL import *

import numpy as np

width = 800
height = 600
renderer = THREE.OpenGLRenderer

pygame.init()
pygame.display.set_mode( (width, height), DOUBLEBUF|OPENGL )
renderer.init()
renderer.setSize( width, height )

texture = THREE.TextureLoader().load("crate.gif")

scene = THREE.Scene()
camera = THREE.PerspectiveCamera( 75, width / height, 0.1, 1000 )

geometry = THREE.BoxGeometry( 1, 1, 1 )
material = THREE.MeshBasicMaterial( Expando( map = texture ) )
cube = THREE.Mesh( geometry, material )
scene.add( cube )

camera.position.z = 5

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            quit()

    cube.rotation.x += 0.05
    cube.rotation.y += 0.05
    renderer.render( scene, camera )

    pygame.display.flip()
    pygame.time.wait( 10 )