from __future__ import division

import logging

from OpenGL import GL

from ...constants import BackSide
from ...cameras import orthographicCamera
from ...cameras import perspectiveCamera
from ...geometries.BoxGeometry import boxBufferGeometry
from ...geometries.PlaneGeometry import planeBufferGeometry
from ...materials import meshBasicMaterial
from ...materials import shaderMaterial
from ...math import color
from ...objects import mesh
from ..shaders import shaderLib
"""
 * @author mrdoob / "http":#mrdoob.com/
 """

class WebGLBackground( object ):

    def __init__( self, renderer, state, geometries, premultipliedAlpha ):

        self.clearColor = color.Color( 0x000000 )
        self.clearAlpha = 0

        self.planeCamera = None
        self.planeMesh = None
        self.boxMesh = None

    def render( self, renderList, scene, camera, forceClear ):

        background = scene.background

        if background is None :

            setClear( self.clearColor, self.clearAlpha )

        elif background and hasattr( background, "isColor" ) :

            setClear( background, 1 )
            forceClear = True

        if renderer.autoClear or forceClear :

            renderer.clear( renderer.autoClearColor, renderer.autoClearDepth, renderer.autoClearStencil )

        if background and hasattr( background, "isCubeTexture" ) :

            if self.boxMesh is None :

                self.boxMesh = mesh.Mesh(
                    boxBufferGeometry.BoxBufferGeometry( 1, 1, 1 ),
                    shaderMaterial.ShaderMaterial( {
                        "uniforms": shaderLib.ShaderLib.cube.uniforms,
                        "vertexShader": shaderLib.ShaderLib.cube.vertexShader,
                        "fragmentShader": shaderLib.ShaderLib.cube.fragmentShader,
                        "side": backSide.BackSide,
                        "depthTest": True,
                        "depthWrite": False,
                        "polygonOffset": True,
                        "fog": False
                    } )
                )

                self.boxMesh.geometry.removeAttribute( "normal" )
                self.boxMesh.geometry.removeAttribute( "uv" )

                def onBeforeRender( self, renderer, scene, camera ):

                    scale = camera.far

                    self.matrixWorld.makeScale( scale, scale, scale )
                    self.matrixWorld.copyPosition( camera.matrixWorld )

                    self.material.polygonOffsetUnits = scale * 10

                self.boxMesh.onBeforeRender = onBeforeRender

                geometries.update( self.boxMesh.geometry )

            self.boxMesh.material.uniforms.tCube.value = background

            renderList.append( self.boxMesh, self.boxMesh.geometry, self.boxMesh.material, 0, None )

        elif background and hasattr( background, "isTexture" ) :

            if self.planeCamera is None :

                self.planeCamera = orthographicCamera.OrthographicCamera( - 1, 1, 1, - 1, 0, 1 )

                self.planeMesh = mesh.Mesh(
                    planeBufferGeometry.PlaneBufferGeometry( 2, 2 ),
                    meshBasicMaterial.MeshBasicMaterial( { "depthTest": False, "depthWrite": False, "fog": False } ) )

                geometries.update( self.planeMesh.geometry )

            self.planeMesh.material.map = background

            # TODO Push self to renderList

            renderer.renderBufferDirect( self.planeCamera, None, self.planeMesh.geometry, self.planeMesh.material, self.planeMesh, None )

    def setClear( self, color, alpha ):

        state.buffers.color.setClear( color.r, color.g, color.b, alpha, premultipliedAlpha )

    def getClearColor( self ):

        return self.clearColor

    def setClearColor( self, color, alpha ):

        self.clearColor.set( color )
        self.clearAlpha = alpha if alpha is not None else 1
        setClear( self.clearColor, self.clearAlpha )

    def getClearAlpha( self ):

        return self.clearAlpha

    def setClearAlpha( self, alpha ):

        self.clearAlpha = alpha
        setClear( self.clearColor, self.clearAlpha )
