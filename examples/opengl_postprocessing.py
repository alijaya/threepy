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
scene = None

object = None

width, height = 800, 600

def toAbs( rel ):

    return os.path.join( os.path.dirname( __file__ ), rel )

def init():

    global renderer, camera, scene, object

    pygame.init()
    pygame.display.set_mode( (width, height), DOUBLEBUF|OPENGL )
    renderer = THREE.OpenGLRenderer
    renderer.init()
    renderer.setSize( width, height )

    camera = THREE.PerspectiveCamera( 70, width / height, 10, 1000 )
    camera.position.z = 400

    scene = THREE.Scene()
    scene.fog = THREE.Fog( 0x000000, 1, 1000 )

    object = THREE.Object3D()
    scene.add( object )

    geometry = THREE.SphereGeometry( 1, 4, 4 )
    material = THREE.MeshLambertMaterial( color = 0xffffff, flatShading = True )

    for i in xrange( 100 ):

        mesh = THREE.Mesh( geometry, material )
        mesh.position.set( random.uniform( -0.5, 0.5 ), random.uniform( -0.5, 0.5 ), random.uniform( -0.5, 0.5 ) ).normalize()
        mesh.position.multiplyScalar( random.uniform( 0, 400 ) )
        mesh.rotation.set( random.uniform( 0, 2 ), random.uniform( 0, 2 ), random.uniform( 0, 2 ) )
        mesh.scale.x = mesh.scale.y = mesh.scale.z = random.uniform( 0, 50 )
        object.add( mesh )

    scene.add( THREE.AmbientLight( 0x222222 ) )

    light = THREE.DirectionalLight( 0xffffff )
    light.position.set( 1, 1, 1 )
    scene.add( light )

    # composer = THREE.EffectComposer()
    # composer.addPass( THREE.RenderPass( scene, camera ) )

    # effect = THREE.ShaderPass( THREE.DotScreenShader )
    # effect.uniforms[ "scale" ].value = 4
    # composer.addPass( effect )

    # effect = THREE.ShaderPass( THREE.RGBShiftShader )
    # effect.uniforms[ "amount" ].value = 0.0015
    # composer.addPass( effect )

def animate():

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                quit()

        object.rotation.x += 0.005
        object.rotation.y += 0.01

        renderer.render( scene, camera )
        # composer.render()

        pygame.display.flip()
        pygame.time.wait( 10 )

if __name__ == "__main__":

    init()
    animate()