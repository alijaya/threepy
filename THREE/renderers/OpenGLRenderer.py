from __future__ import division

from OpenGL.GL import *

import numpy as np

from ctypes import c_void_p

import logging

from ..constants import REVISION, RGBAFormat, HalfFloatType, FloatType, ByteType, UnsignedByteType, FrontFaceDirectionCW, TriangleFanDrawMode, TriangleStripDrawMode, TrianglesDrawMode, NoColors, NoToneMapping, LinearToneMapping
from ..objects.mesh import Mesh
from ..math.frustum import Frustum
from ..math.vector3 import Vector3
from ..math.vector4 import Vector4
from ..math.matrix4 import Matrix4
from ..utils import Expando

from opengl import OpenGLObjects as objects
from opengl import OpenGLState as state
from opengl import OpenGLProperties as properties
from opengl import OpenGLCapabilities as capabilities
from opengl import OpenGLRenderLists as renderLists
from opengl import OpenGLBackground as background
from opengl import OpenGLPrograms as programCache
from opengl import OpenGLIndexedBufferRenderer as indexedBufferRenderer
from opengl import OpenGLBufferRenderer as bufferRenderer
from opengl import OpenGLAttributes as attributes
from opengl import OpenGLTextures as textures

from opengl.openGLUniforms import OpenGLUniforms

from shaders.shaderLib import ShaderLib
from shaders import UniformsUtils

# internal cache

_currentRenderTarget = None
_currentFramebuffer = None
_currentMaterialId = -1
_currentGeometryProgram = ""

_currentCamera = None

_currentViewport = Vector4()
_currentScissor = Vector4()
_currentScissorTest = None

#

_usedTextureUnits = 0

#

_width = 0
_height = 0

_pixelRatio = 1

_viewport = Vector4( 0, 0, _width, _height )
_scissor = Vector4( 0, 0, _width, _height )
_scissorTest = False

# frustum

_frustum = Frustum()

# clipping

# camera matrices cache

_projScreenMatrix = Matrix4()

# info

_infoMemory = Expando(
    geometries = 0,
    textures = 0
)

_infoRender = Expando(
    frame = 0,
    calls = 0,
    vertices = 0,
    faces = 0,
    points = 0
)

info = Expando(
    render = _infoRender,
    memory = _infoMemory,
    programs = None
)

#

currentRenderList = None

# clearing

autoClear = True
autoClearColor = True
autoClearDepth = True
autoClearStencil = True

# scene graph

sortObjects = True

# TODO clipping

# physically based shading

gammaFactor = 2.0
gammaInput = False
gammaOutput = False

# tone mapping

toneMapping = LinearToneMapping
toneMappingExposure = 1.0
toneMappingWhitePoint = 1.0

# init, need to be called after OpenGL Context created

inited = False

def init():

    global inited

    if inited: return

    inited = True

    capabilities.init()
    state.init()

# API

def getPixelRatio():

    return _pixelRatio

def setPixelRatio( value ):

    global _pixelRatio

    if not value: return

    _pixelRatio = value

    setSize( _width, _height, False )

def getSize():

    return Expando(
        width = _width,
        height = _height
    )

def setSize( width, height ):

    global _width
    global _height

    # TODO vr

    _width = width
    _height = height

    setViewport( 0, 0, width, height )

def getDrawingBufferSize():

    return Expando(
        width = _width * _pixelRatio,
        height = _height * _pixelRatio
    )

def setDrawingBufferSize( width, height, pixelRatio ):

    global _width
    global _height
    global _pixelRatio

    _width = width
    _height = height

    self.setViewport( 0, 0, width, height )

def setViewport( x, y, width, height ):

    _viewport.set( x, _height - y - height, width, height )
    state.viewport( _currentViewport.copy( _viewport ).multiplyScalar( _pixelRatio ) )

def setScissor( x, y, width, height ):

    _scissor.set( x, _height - y - height, width, height )
    state.scissor( _currentScissor.copy( _scissor ).multiplyScalar( _pixelRatio ) ) 

def setScissorTest( boolean ):

    global _scissorTest
    _scissorTest = boolean
    state.setScissorTest( _scissorTest )

# Clearing

getClearColor = background.getClearColor
setClearColor = background.setClearColor
getClearAlpha = background.getClearAlpha
setClearAlpha = background.setClearAlpha

def clear( color = True, depth = True, stencil = True ):

    bits = 0

    if color: bits |= GL_COLOR_BUFFER_BIT
    if depth: bits |= GL_DEPTH_BUFFER_BIT
    if stencil: bits |= GL_STENCIL_BUFFER_BIT

    glClear( bits )

def clearColor():

    clear( True, False, False )

def clearDepth():

    clear( False, True, False )

def clearStencil():

    clear( False, False, True )

def clearTarget( renderTarget, color, depth, stencil ):

    self.setRenderTarget( renderTarget )
    self.clear( color, depth, stencil )

#

def dispose():

    renderLists.dispose()

    # TODO vr

#

def getRenderTarget():

    return _currentRenderTarget

def setRenderTarget( renderTarget ):

    global _currentRenderTarget
    global _currentScissorTest

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

# Textures

def allocTextureUnit():

    global _usedTextureUnits

    textureUnit = _usedTextureUnits

    if textureUnit >= capabilities.maxTextures:

        logging.warning( "THREE.OpenGLRenderer: Trying to use %s texture units while this GPU supports only %s" % ( textureUnit, capabilities.maxTextures ) )

    _usedTextureUnits += 1

    return textureUnit

def setTexture2D( texture, slot ):

    if texture and hasattr( texture, "isOpenGLRenderTarget" ):

        logging.warning( "THREE.WebGLRenderer.setTexture2D: don't use render targets as textures. Use their .texture property instead." )
        
        texture = texture.texture
    
    textures.setTexture2D( texture, slot )

def projectObject( object, camera, sortObjects ):

    # if not visible, nothing to render
    if not object.visible: return

    # test if the object is in the same layer with camera
    visible = object.layers.test( camera.layers )

    if visible:

        # if object is Mesh type
        if hasattr( object, "isMesh" ):

            # whether it in Frustum
            if not object.frustumCulled or _frustum.intersectsObject( object ):

                if sortObjects:

                    # get z position in screen space

                    z = Vector3().setFromMatrixPosition( object.matrixWorld ).applyMatrix4( _projScreenMatrix ).z

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

        projectObject( child, camera, sortObjects )

def releaseMaterialProgramReference( material ):

    programInfo = properties.get( material ).program

    del material.program

    if programInfo:

        programCache.releaseProgram( programInfo )

def initMaterial( material, fog, object ):

    materialProperties = properties.get( material )

    # parameters = programCache.getParameters( material, lights.state, shadowsArray, fog, _clipping.numPlanes, _clipping.numIntersection, object )
    parameters = programCache.getParameters( material, None, None, fog, 0, None, object ) # TODO

    code = programCache.getProgramCode( material, parameters )

    program = materialProperties.program
    programChange = True

    if not program:

        # new material
        # material.addEventListener( "dispose", onMaterialDispose )
        pass

    elif program.code != code:

        # changed glsl or parameters
        releaseMaterialProgramReference( material )

    elif "shaderID" not in parameters:

        # same glsl and uniform list
        return

    else:

        # only rebuild uniform list
        programChange = False

    if programChange:

        if "shaderID" in parameters:

            shader = ShaderLib[ parameters.shaderID ]

            materialProperties.shader = Expando(
                name = material.type,
                uniforms = UniformsUtils.clone( shader.uniforms ),
                vertexShader = shader.vertexShader,
                fragmentShader = shader.fragmentShader
            )
        
        else:

            materialProperties.shader = Expando(
                name = material.type,
                uniforms = material.uniforms,
                vertexShader = material.vertexShader,
                fragmentShader = material.fragmentShader
            )
        
        # material.onBeforeCompile( materialProperties.shader )

        program = programCache.acquireProgram( material, materialProperties.shader, parameters, code )

        materialProperties.program = program
        material.program = program

    programAttributes = program.getAttributes()

    # TODO morphTargets

    uniforms = materialProperties.shader.uniforms

    # TODO clipping

    materialProperties.fog = fog

    # store the light setup it was created for

    # TODO lights

    progUniforms = materialProperties.program.getUniforms()
    uniformsList = OpenGLUniforms.seqWithValue( progUniforms.seq, uniforms )

    materialProperties.uniformsList = uniformsList

# Uniforms (refresh uniforms objects)

def refreshUniformsCommon( uniforms, material ):

    uniforms.opacity.value = material.opacity

    if material.color: uniforms.diffuse.value = material.color

    if material.emissive: uniforms.emissive.value.copy( material.emissive ).multiplyScalar( material.emissiveIntensity )

    if material.map: uniforms.map.value = material.map

    if material.alphaMap: uniforms.alphaMap.value = material.alphaMap

    if material.specularMap: uniforms.specularMap.value = material.specularMap

    if material.envMap:
        
        uniforms.envMap.value = material.envMap

        # don't flip CubeTexture envMaps, flip everything else:
        # OpenGLRenderTargetCube will be flipped for backwards compatibility
        # OpenGLRenderTargetCube.texture will be flipped because it's a Texture and NOT a CubeTexture
        # this check must be handled differently, or removed entirely, if OpenGLRenderTargetCube uses a CubeTexture in the future
        uniforms.flipEnvMap.value = 1 if not ( material.envMap and hasattr( material.envMap, "isCubeTexture" ) ) else - 1

        uniforms.reflectivity.value = material.reflectivity
        uniforms.refractionRatio.value = material.refractionRatio
    
    if material.lightMap:

        uniforms.lightMap.value = material.lightMap
        uniforms.lightMapIntensity.value = material.lightMapIntensity
    
    if material.aoMap:

        uniforms.aoMap.value = material.aoMap
        uniforms.aoMapIntensity.value = material.aoMapIntensity

    # uv repeat and offset setting priorities
    # 1. color map
    # 2. specular map
    # 3. normal map
    # 4. bump map
    # 5. alpha map
    # 6. emissive map

    uvScaleMap = None

    if   material.map: uvScaleMap = material.map
    elif material.specularMap: uvScaleMap = material.specularMap
    elif material.displacementMap: uvScaleMap = material.displacementMap
    elif material.normalMap: uvScaleMap = material.normalMap
    elif material.bumpMap: uvScaleMap = material.bumpMap
    elif material.roughnessMap: uvScaleMap = material.roughnessMap
    elif material.metalnessMap: uvScaleMap = material.metalnessMap
    elif material.alphaMap: uvScaleMap = material.alphaMap
    elif material.emissiveMap: uvScaleMap = material.emissiveMap

    if uvScaleMap:

        # backwards compatibility
        if hasattr( uvScaleMap, "isOpenGLRenderTarget" ): uvScaleMap = uvScaleMap.texture

        offset = uvScaleMap.offset
        repeat = uvScaleMap.repeat

        uniforms.offsetRepeat.value.set( offset.x, offset.y, repeat.x, repeat.y )

def setProgram( camera, fog, material, object ):

    global _usedTextureUnits

    _usedTextureUnits = 0

    materialProperties = properties.get( material )

    # TODO clipping

    # TODO if material.needsUpdate

    # for now, force update
    initMaterial( material, fog, object )
    material.needsUpdate = False

    refreshProgram = False
    refreshMaterial = False
    refreshLights = False

    program = materialProperties.program
    p_uniforms = program.getUniforms()
    m_uniforms = materialProperties.shader.uniforms

    global _currentMaterialId
    global _currentCamera

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

        if  material.isShaderMaterial or \
            material.isMeshPongMaterial or \
            material.isMeshStandardMaterial or \
            material.envMap:

            uCamPos = p_uniforms.map.get( "cameraPosition" )

            if uCamPos:

                uCamPos.setValue( vector3.Vector3().setFromMatrixPosition( camera.matrixWorld ) )
        
        if  material.isMeshPhongMaterial or \
            material.isMeshLambertMaterial or \
            material.isMeshBasicMaterial or \
            material.isMeshStandardMaterial or \
            material.isShaderMaterial or \
            material.skinning:

            p_uniforms.setValue( "viewMatrix", camera.matrixWorldInverse )
    
    # skinning uniforms must be set even if material didn't change
    # auto-setting of texture unit for bone textur must go before other textures
    # not sure why, but otherwise weird things happen

    # TODO material.skinning

    if refreshMaterial:

        p_uniforms.setValue( "toneMappingExposure", toneMappingExposure )
        p_uniforms.setValue( "toneMappingWhitePoint", toneMappingWhitePoint )

        # TODO light

        # if fog and material.fog:

        #     refreshUniformsFog( m_uniforms, fog )

        if material.isMeshBasicMaterial:

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

        OpenGLUniforms.upload( materialProperties.uniformsList, m_uniforms )

    # common matrices

    p_uniforms.setValue( "modelViewMatrix", object.modelViewMatrix )
    p_uniforms.setValue( "normalMatrix",  object.normalMatrix )
    p_uniforms.setValue( "modelMatrix", object.matrixWorld )

    return program

def setupVertexAttributes( material, program, geometry, startIndex = 0 ):

    # TODO check instancedBufferGeometry
    # if geometry and hasattr( geometry, "isInstancedBufferGeometry" ):

    state.initAttributes()

    geometryAttributes = geometry.attributes

    programAttributes = program.getAttributes()

    materialDefaultAttributeValues = material.defaultAttributeValues

    for name in programAttributes:

        programAttribute = programAttributes[ name ]

        if programAttribute >= 0:

            geometryAttribute = geometryAttributes[ name ]

            if geometryAttribute:

                normalized = geometryAttribute.normalized
                size = geometryAttribute.itemSize

                attribute = attributes.get( geometryAttribute )

                # TODO Attribute may not be available on context restore

                if not attribute: continue

                buffer = attribute.buffer
                type = attribute.type
                bytesPerElement = attribute.bytesPerElement

                # TODO
                if hasattr( geometryAttribute, "isInterleavedBufferAttribute" ):

                    # TODO
                    pass
                
                else:

                    if hasattr( geometryAttribute, "isInstancedBufferAttribute" ):

                        # TODO
                        pass

                    else:

                        state.enableAttribute( programAttribute )

                    glBindBuffer( GL_ARRAY_BUFFER, buffer )
                    glVertexAttribPointer( programAttribute, size, type, normalized, 0, c_void_p( startIndex * size * bytesPerElement ) )

            elif materialDefaultAttributeValues:

                value = materialDefaultAttributeValues[ name ]

                if value:

                    if   len( value ) == 2: glVertexAttrib2fv( programAttribute, value )
                    elif len( value ) == 3: glVertexAttrib3fv( programAttribute, value )
                    elif len( value ) == 4: glVertexAttrib4fv( programAttribute, value )
                    else: glVertexAttrib1fv( programAttribute, value )

    state.disableUnusedAttributes()


def renderBufferDirect( camera, fog, geometry, material, object, group ):

    global _currentGeometryProgram

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
    groupCount = group.count * rangeFactor if group else float("inf")

    drawStart = max( rangeStart, groupStart )
    drawEnd = min( dataCount, rangeStart + rangeCount, groupStart + groupCount ) - 1

    drawCount = max( 0, drawEnd - drawStart + 1 )

    # print( geometry.drawRange.start, geometry.drawRange.count )
    # print( rangeStart, rangeCount, groupStart, groupCount, drawStart, drawEnd, drawCount )

    if drawCount == 0: return

    if hasattr( object, "isMesh" ):

        # TODO wireframe

        # not wireframe
        dm = object.drawMode

        if dm == TrianglesDrawMode: renderer.setMode( GL_TRIANGLES )
        elif dm == TriangleStripDrawMode: renderer.setMode( GL_TRIANGLE_STRIP )
        elif dm == TriangleFanDrawMode: renderer.setMode( GL_TRIANGLE_FAN )

    # TODO isLine

    # TODO instance

    renderer.render( drawStart, drawCount )


def renderObject( object, scene, camera, geometry, material, group ):

    object.onBeforeRender( scene, camera, geometry, material, group )

    # transform from world space to camera space
    object.modelViewMatrix.multiplyMatrices( camera.matrixWorldInverse, object.matrixWorld )
    object.normalMatrix.getNormalMatrix( object.modelViewMatrix )

    # TODO check if object.isImmediateRenderObject

    renderBufferDirect( camera, scene.fog, geometry, material, object, group )

    object.onAfterRender( scene, camera, geometry, material, group )

def renderObjects( renderList, scene, camera, overrideMaterial = None ):

    for renderItem in renderList:

        object = renderItem.object
        geometry = renderItem.geometry
        material = overrideMaterial or renderItem.material
        group = renderItem.group

        # TODO array camera

        renderObject( object, scene, camera, geometry, material, group )

def render( scene, camera, renderTarget = None, forceClear = True ):

    if not inited:

        logging.warning( "THREE.OpenGLRenderer: Please call init() first." )
        quit()

    global _currentGeometryProgram, _currentMaterialId, _currentCamera
    global _projScreenMatrix, _frustum, currentRenderList

    _currentGeometryProgram = ""
    _currentMaterialId = - 1
    _currentCamera = None

    # update matrix world of all objects

    if scene.autoUpdate == True: scene.updateMatrixWorld()

    # update matrix world of camera

    if camera.parent is None: camera.updateMatrixWorld()

    # TODO vr

    # project to screen

    _projScreenMatrix.multiplyMatrices( camera.projectionMatrix, camera.matrixWorldInverse )
    _frustum.setFromMatrix( _projScreenMatrix )

    # TODO lightsArray, shadowsArray
    # TODO spritesArray, flaresArray
    # TODO clipping
    
    currentRenderList = renderLists.get( scene, camera )
    currentRenderList.init()

    # traverse scene, update opengl buffer, add to render list
    projectObject( scene, camera, sortObjects )

    if sortObjects: currentRenderList.sort()

    # TODO clipping

    # TODO lights

    _infoRender.frame += 1
    _infoRender.calls = 0
    _infoRender.vertices = 0
    _infoRender.faces = 0
    _infoRender.points = 0

    setRenderTarget( renderTarget )

    # render background

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

    # TODO custom renderers

    # TODO renderTarget

    # Ensure depth buffer writing is enabled so it can be cleared on next render

    state.buffers.depth.setTest( True )
    state.buffers.depth.setMask( True )
    state.buffers.color.setMask( True )

    # TODO state.setPolygonOffset( False )

    # TODO vr