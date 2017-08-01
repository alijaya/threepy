from __future__ import division

from OpenGL.GL import *

import numpy as np

from ..objects.mesh import Mesh
from ..math.frustum import Frustum
from ..math.vector3 import Vector3
from ..math.vector4 import Vector4

from opengl import OpenGLObjects as objects
from opengl import OpenGLState as state
from opengl import OpenGLProperties as properties
from opengl import OpenGLRenderLists as renderLists
from opengl import OpenGLBackground as background
from opengl import OpenGLPrograms as programCache
from shaders.shaderLib import ShaderLib
from shaders import UniformsUtils

# internal cache

_currentMaterialId = -1
_currentCamera = None
_currentRenderTarget = None
_currentGeometryProgram = None
_currentViewport = Vector4()
_currentScissor = Vector4()
_currentScissorTest = None
_pixelRatio = 1

_width = 800
_height = 600
_viewport = Vector4( 0, 0, _width, _height )
_scissor = Vector4( 0, 0, _width, _height )
_scissorTest = False

def getRenderTarget():

    return _currentRenderTarget

def setRenderTarget( renderTarget ):

    _currentRenderTarget = renderTarget

    # TODO textures setupRenderTarget

    framebuffer = None
    isCube = False

    # TODO if renderTarget exists

    _currentViewport.copy( _viewport ).multiplyScalar( _pixelRatio )
    _currentScissor.copy( _scissor ).multiplyScalar( _pixelRatio )
    _currentScissorTest = _scissorTest

    # bind framebuffer

    state.viewport( _currentViewport )
    state.scissor( _currentScissor )
    state.setScissorTest( _currentScissorTest )

    # TODO isCube

def projectObject( object, camera, projScreenMatrix, frustum, currentRenderList, sortObjects ):

    # if not visible, nothing to render
    if not object.visible: return

    # test if the object is in the same layer with camera
    visible = object.layers.test( camera.layers )

    if visible:

        # if object is Mesh type
        if hasattr( object, "isMesh" ):

            # whether it in Frustum
            if not object.frustumCulled or frustum.intersectsObject( object ):

                if sortObjects:

                    # get z position in screen space

                    z = Vector3().setFromMatrixPosition( object.matrixWorld ).applyMatrix4( projScreenMatrix ).z

                geometry = objects.update( object )
                material = object.material

                if isinstance( material, list ): # if more than one material

                    for group in geometry.groups: # loop all vertex group

                        groupMaterial = material.get( group.materialIndex )

                        if groupMaterial and groupMaterial.visible: # if the material is valid and visible

                            currentRenderList.push( object, geometry, groupMaterial, z, group )

                else: # if only one material

                    if material.visible:

                        currentRenderList.push( object, geometry, material, z, None )
        
    # traverse children

    for child in object.children:

        projectObject( child, camera, projScreenMatrix, frustum, currentRenderList, sortObjects )

def releaseMaterialProgramReference( material ):

    programInfo = properties.get( material )[ "program" ]

    del material.program

    if programInfo:

        programCache.releaseProgram( programInfo )

def initMaterial( material, fog, object ):

    materialProperties = properties.get( material )

    # parameters = programCache.getParameters( material, lights.state, shadowsArray, fog, _clipping.numPlanes, _clipping.numIntersection, object )
    parameters = programCache.getParameters( material, None, None, fog, None, None, object )

    code = programCache.getProgramCode( material, parameters )

    program = materialProperties.get( "program" )
    programChange = True

    if not program:

        # new material
        # material.addEventListener( "dispose", onMaterialDispose )
        pass

    elif program.code != code:

        # changed glsl or parameters
        releaseMaterialProgramReference( material )

    elif not parameters.get( "ShaderID" ):

        # same glsl and uniform list
        return

    else:

        # only rebuild uniform list
        programChange = False

    if programChange:

        if parameters.get( "shaderID" ):

            shader = ShaderLib[ parameters.get( "shaderID" ) ]

            materialProperties[ "shader" ] = {
                "name": material.type,
                "uniforms": UniformsUtils.clone( shader["uniforms"] ),
                "vertexShader": shader["vertexShader"],
                "fragmentShader": shader["fragmentShader"]
            }
        
        else:

            materialProperties[ "shader" ] = {
                "name": material.type,
                "uniforms": material.uniforms,
                "vertexShader": material.vertexShader,
                "fragmentShader": material.fragmentShader
            }
        
        # material.onBeforeCompile( materialProperties[ "shader" ] )

        program = programCache.acquireProgram( material, materialProperties[ "shader" ], parameters, code )

        materialProperties[ "program" ] = program
        material.program = program

    programAttributes = program.getAttributes()

    # TODO morphTargets

    uniforms = materialProperties[ "shader" ][ "uniforms" ]

    # TODO clipping

    materialProperties[ "fog" ] = fog

    # store the light setup it was created for

    # TODO lights

    progUniforms = materialProperties[ "program" ].getUniforms()
    uniformsList = OpenGLUniforms.seqWithValue( progUniforms.seq, uniforms )

    materialProperties[ "uniformsList" ] = uniformsList

def setProgram( camera, fog, material, object ):

    materialProperties = properties.get( material )

    # TODO clipping

    # TODO if material.needsUpdate

    # for now, force update
    initMaterial( material, fog, object )
    material.needsUpdate = False

    refreshProgram = False
    refreshMaterial = False
    refreshLights = False

    program = materialProperties[ "program" ]
    p_uniforms = program.getUniforms()
    m_uniforms = materialProperties[ "shader" ].uniforms

    if state.useProgram( program.program ):

        refreshProgram = True
        refreshMaterial = True
        refreshLights = True

    if material.id != _currentMaterialId:

        _currentMaterialId = material.id
        
        refreshMaterial = True

    if refreshProgram or camera != _currentCamera:

        p_uniforms.setValue( "projectionMatrix", camera.projectionMatrix )

        # TODO capabilities.logarithmicDepthBuffer

        # TODO array camera

        _currentCamera = camera

        refreshMaterial = True
        refreshLights = True

        if  hasattr( material, "isHaderMaterial" ) or \
            hasattr( material, "isMeshPongMaterial" ) or \
            hasattr( material, "isMeshStandardMaterial" ) or \
            material.envMap:

            uCamPos = p_uniforms.map.get( "cameraPosition" )

            if uCamPos:

                uCamPos.setValue( vector3.Vector3().setFromMatrixPosition( camera.matrixWorld ) )
        
        if  hasattr( material, "isMeshPhongMaterial" ) or \
            hasattr( material, "isMeshLambertMaterial" ) or \
            hasattr( material, "isMeshBasicMaterial" ) or \
            hasattr( material, "isMeshStandardMaterial" ) or \
            hasattr( material, "isShaderMaterial" ) or \
            material.skinning:

            p_uniforms.setValue( "viewMatrix", camera.matrixWorldInverse )
    
    # skinning uniforms must be set even if material didn't change
    # auto-setting of texture unit for bone textur must go before other textures
    # not sure why, but otherwise weird things happen

    # TODO material.skinning

    if refreshMaterial:

        # p_uniforms.setValue( "toneMappingExposure", toneMappingExposure )
        # p_uniforms.setValue( "toneMappingWhitePoint", toneMappingWhitePoint )

        # TODO light

        if fog and material.fog:

            refreshUniformsFog( m_uniforms, fog )

        if hasattr( material, "isMeshBasicMaterial" ):

            refreshUniformsCommon( m_uniforms, material )

        # elif hasattr( material, "isMeshLambertMaterial" ):

        #     refreshUniformsCommon( m_uniforms, material )
        #     refreshUniformsLamber( m_uniforms, material )
        
        # elif hasattr( material, "isMeshPhongMaterial" ):

        #     refreshUniformsCommon( m_uniforms, material )

        #     if hasattr( material, "isMeshToonMaterial" ):

        #         refreshUniformsToon( m_uniforms, material )
            
        #     else:

        #         refreshUniformsPhong( m_uniforms, material )

        # TODO RectAreaLight Texture

        WebGLUniforms.upload( materialProperties[ "uniformsList" ], m_uniforms, self )

    # common matrices

    p_uniforms.setValue( "modelViewMatrix", object.modelViewMatrix )
    p_uniforms.setValue( "normalMatrix",  object.normalMatrix )
    p_uniforms.setValue( "modelMatrix", object.matrixWorld )

    return program

def renderBufferDirect( camera, fog, geometry, material, object, group ):

    state.setMaterial( material )

    program = setProgram( camera, fog, material, object )
    geometryProgram = "%s_%s_%s" % ( geometry.id, program.id, bool( material.wireframe ) )
    
    updateBuffers = False

    if geometryProgram != _currentGeometryProgram:

        _currentGeometryProgram = geometryProgram
        updateBuffers = True

    # TODO morphTarget

    index = geometry.index
    position = geometry.attributes[ "position" ]
    rangeFactor = 1

    # TODO wireframe

    attribute = None
    renderer = bufferRenderer

    if index:

        attribute = attributes.get( index )

        renderer = indexedBufferRenderer
        renderer.setIndex( attribute )
    
    if updateBuffers:

        setupVertexAttributes( material, program, geometry )

        if index:

            glBindBuffer( GL_ELEMENT_ARRAY_BUFFER, attribute.buffer )
    
    dataCount = 0

    if index:

        dataCount = index.count

    elif position:

        dataCount = position.count

    rangeStart = geometry.drawRange.start * rangeFactor
    rangeCount = geometry.drawRange.count * rangeFactor

    groupStart = group.start * rangeFactor if group else 0
    groupCount = group.cound * rangeFactor if group else float("inf")

    drawStart = max( rangeStart, groupStart )
    drawEnd = min( dataCount, rangeStart + rangeCound, groupStart + groupCount ) - 1

    drawCount = max( 0, drawEnd - drawStart + 1 )

    if drawCount == 0: return

    if hasattr( object, "isMesh" ):

        # TODO wireframe

        # not wireframe
        dm = object.drawMode

        if dm == TrianglesDrawmode: renderer.setMode( GL_TRIANGLES )
        elif dm == TriangleStripDrawMode: renderer.setMode( GL_TRIANGLE_STRIP )
        elif dm == TriangleFanDrawMode: renderer.setMode( GL_TRIANGLE_FAN )

    # TODO isLine

    # TODO instance

    renderer.render( drawStart, drawCount )


def renderObject( object, scene, camera, geometry, material, group ):

    # TODO object.onBeforeRender

    # transform from world space to camera space
    object.modelViewMatrix.multiplyMatrices( camera.matrixWorldInverse, object.matrixWorld )
    object.normalMatrix.getNormalMatrix( object.modelViewMatrix )

    # TODO check if object.isImmediateRenderObject

    renderBufferDirect( camera, scene.fog, geometry, material, object, group )

    # TODO object.onAfterRender

def renderObjects( renderList, scene, camera, overrideMaterial = None ):

    for renderItem in renderList:

        object = renderItem[ "object" ]
        geometry = renderItem[ "geometry" ]
        material = overrideMaterial or renderItem[ "material" ]
        group = renderItem[ "group" ]

        # TODO array camera

        renderObject( object, scene, camera, geometry, material, group )

def render( scene, camera ):

    # update matrix world of all objects

    scene.updateMatrixWorld()

    # update matrix world of camera

    camera.updateMatrixWorld()

    # project to screen

    projScreenMatrix = camera.projectionMatrix.multiply( camera.matrixWorldInverse )
    frustum = Frustum().setFromMatrix( projScreenMatrix )
    
    currentRenderList = renderLists.get( scene, camera )
    currentRenderList.init()

    sortObjects = True

    # traverse scene, update opengl buffer, add to render list
    projectObject( scene, camera, projScreenMatrix, frustum, currentRenderList, sortObjects )

    if sortObjects: currentRenderList.sort()

    # TODO clipping

    # TODO lights

    # TODO custom renderTarget

    # TODO
    setRenderTarget( None )

    # render background

    forceClear = True # temp
    background.render( currentRenderList, scene, camera, forceClear )

    # render scene

    opaqueObjects = currentRenderList.opaque
    transparentObjects = currentRenderList.transparent

    if scene.overrideMaterial:

        overrideMaterial = scene.overrideMaterial

        if len( opaqueObjects ) > 0: renderObjects( opaqueObjects, scene, camera, overrideMaterial )
        if len( transparentObjects ) > 0: renderObjects( transparentObjects, scene, camera, overrideMaterial )

    else:

        if len( opaqueObjects ) > 0: renderObjects( opaqueObjects, scene, camera )
        if len( transparentObjects ) > 0: renderObjects( transparentObjects, scene, camera )