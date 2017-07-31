from __future__ import division

import pygame
from pygame.locals import *

import THREE
from THREE.renderers import webGLRenderer

width = 800
height = 600

pygame.init()
pygame.display.set_mode( (width, height), DOUBLEBUF|OPENGL )

scene = THREE.Scene()
camera = THREE.PerspectiveCamera( 75, width / height, 0.1, 1000 )

renderer = THREE.WebGLRenderer()

geometry = THREE.BoxGeometry( 1, 1, 1 )
material = THREE.MeshBasicMaterial( { "color": 0x00ff00 } )
cube = THREE.Mesh( geometry, material )
scene.add( cube )

camera.position.z = 5