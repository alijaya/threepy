from __future__ import division

import logging

from OpenGL import GL

from ..constants import REVISION, RGBAFormat, HalfFloatType, FloatType, ByteType, UnsignedByteType, FrontFaceDirectionCW, TriangleFanDrawMode, TriangleStripDrawMode, TrianglesDrawMode, NoColors, LinearToneMapping
from ..math import _Math
from ..math import matrix4
# from ..textures import dataTexture
# from webgl import webGLUniforms
# from shaders import uniformsLib
# from shaders import uniformsUtils
# from shaders import shaderLib
from webgl import webGLFlareRenderer
# from webgl import webGLSpriteRenderer
# from webgl import webGLShadowMap
from webgl import webGLAttributes
from webgl import webGLBackground
# from webgl import webGLRenderLists
# from webgl import webGLMorphtargets
# from webgl import webGLIndexedBufferRenderer
# from webgl import webGLBufferRenderer
from webgl import webGLGeometries
# from webgl import webGLLights
# from webgl import webGLObjects
# from webgl import webGLPrograms
# from webgl import webGLTextures
# from webgl import webGLProperties
# from webgl import webGLState
from webgl import webGLCapabilities
# from webvr import webVRManager
from ..core import bufferGeometry
from webgl import webGLExtensions
from ..math import vector3
from ..math import sphere
from webgl import webGLClipping
from ..math import frustum
from ..math import vector4
from webgl import webGLUtils
#
"""
 * @author supereggbert / "http":#www.paulbrunt.co.uk/
 * @author mrdoob / "http":#mrdoob.com/
 * @author alteredq / "http":#alteredqualia.com/
 * @author szimek / "https":#github.com/szimek/
 * @author tschw
 """

class WebGLRenderer( object ):

    def __init__( self, parameters = None ):

        logging.info( "THREE.WebGLRenderer", REVISION )

        self.parameters = parameters or {}
        # _canvas = parameters.canvas if parameters.canvas is not None else document.createElementNS( "http://www.w3.org/1999/xhtml", "canvas" )
        # _context = parameters.context if parameters.context is not None else None

        # _alpha = parameters.alpha if parameters.alpha is not None else False
        # _depth = parameters.depth if parameters.depth is not None else True
        # _stencil = parameters.stencil if parameters.stencil is not None else True
        # _antialias = parameters.antialias if parameters.antialias is not None else False
        self._premultipliedAlpha = self.parameters.get( "premultipliedAlpha", True )
        # _preserveDrawingBuffer = parameters.preserveDrawingBuffer if parameters.preserveDrawingBuffer is not None else False

        self.lightsArray = []
        self.shadowsArray = []

        self.currentRenderList = None

        self.spritesArray = []
        self.flaresArray = []

        # public properties

        # self.domElement = _canvas
        self.context = None

        # clearing

        self.autoClear = True
        self.autoClearColor = True
        self.autoClearDepth = True
        self.autoClearStencil = True

        # scene graph

        self.sortObjects = True

        # user-defined clipping

        self.clippingPlanes = []
        self.localClippingEnabled = False

        # physically based shading

        self.gammaFactor = 2.0    # for backwards compatibility
        self.gammaInput = False
        self.gammaOutput = False

        # physical lights

        self.physicallyCorrectLights = False

        # tone mapping

        self.toneMapping = LinearToneMapping
        self.toneMappingExposure = 1.0
        self.toneMappingWhitePoint = 1.0

        # morphs

        self.maxMorphTargets = 8
        self.maxMorphNormals = 4

        # internal properties

        self._isContextLost = False

        # internal state cache

        self._currentRenderTarget = None
        self._currentFramebuffer = None
        self._currentMaterialId = - 1
        self._currentGeometryProgram = ""

        self._currentCamera = None
        self._currentArrayCamera = None

        self._currentViewport = vector4.Vector4()
        self._currentScissor = vector4.Vector4()
        self._currentScissorTest = None

        #

        self._usedTextureUnits = 0

        #

        self._width = 800 # TODO dummy value
        self._height = 600 # TODO dummy value

        self._pixelRatio = 1

        self._viewport = vector4.Vector4( 0, 0, self._width, self._height )
        self._scissor = vector4.Vector4( 0, 0, self._width, self._height )
        self._scissorTest = False

        # frustum

        self._frustum = frustum.Frustum()

        # clipping

        self._clipping = webGLClipping.WebGLClipping()
        self._clippingEnabled = False
        self._localClippingEnabled = False

        # camera matrices cache

        self._projScreenMatrix = matrix4.Matrix4()

        self._vector3 = vector3.Vector3()

        # info

        self._infoMemory = {
            "geometries": 0,
            "textures": 0
        }

        self._infoRender = {

            "frame": 0,
            "calls": 0,
            "vertices": 0,
            "faces": 0,
            "points": 0
            
        }

        self.info = {

            "render": self._infoRender,
            "memory": self._infoMemory,
            "programs": None

        }

        def getTargetPixelRatio():

            return self._pixelRatio if self._currentRenderTarget is None else 1

        # initialize

        self.extensions = None
        self.capabilities = None
        self.state = None

        self.properties = None
        self.textures = None
        self.attributes = None
        self.geometries = None
        self.objects = None
        self.lights = None

        self.programCache = None
        self.renderLists = None

        self.background = None
        self.morphtargets = None
        self.bufferRenderer = None
        self.indexedBufferRenderer = None

        self.flareRenderer = None
        self.spriteRenderer = None

        self.utils = None

        self.initGLContext()

        # vr

        vr = webVRManager.WebVRManager( self )

        self.vr = vr

        # shadow map

        shadowMap = webGLShadowMap.WebGLShadowMap( self, objects, capabilities.maxTextureSize )

        self.shadowMap = shadowMap

    def initGLContext( self ):

        self.extensions = webGLExtensions.WebGLExtensions()
        self.extensions.get( "WEBGL_depth_texture" )
        self.extensions.get( "OES_texture_float" )
        self.extensions.get( "OES_texture_float_linear" )
        self.extensions.get( "OES_texture_half_float" )
        self.extensions.get( "OES_texture_half_float_linear" )
        self.extensions.get( "OES_standard_derivatives" )
        self.extensions.get( "ANGLE_instanced_arrays" )

        if self.extensions.get( "OES_element_index_uint" ) :

            bufferGeometry.BufferGeometry.MaxIndex = 4294967296

        self.utils = webGLUtils.WebGLUtils( self.extensions )

        self.capabilities = webGLCapabilities.WebGLCapabilities( self.extensions, self.parameters )

        self.state = webGLState.WebGLState( extensions, utils )
        self.state.scissor( self._currentScissor.copy( self._scissor ).multiplyScalar( self._pixelRatio ) )
        self.state.viewport( self._currentViewport.copy( self._viewport ).multiplyScalar( self._pixelRatio ) )

        self.properties = webGLProperties.WebGLProperties()
        self.textures = webGLTextures.WebGLTextures( self.extensions, self.state, self.properties, self.capabilities, self.utils, self._infoMemory )
        self.attributes = webGLAttributes.WebGLAttributes()
        self.geometries = webGLGeometries.WebGLGeometries( self.attributes, self._infoMemory )
        self.objects = webGLObjects.WebGLObjects( self.geometries, self._infoRender )
        self.morphtargets = webGLMorphtargets.WebGLMorphtargets()
        self.programCache = webGLPrograms.WebGLPrograms( self, self.extensions, self.capabilities )
        self.lights = webGLLights.WebGLLights()
        self.renderLists = webGLRenderLists.WebGLRenderLists()

        self.background = webGLBackground.WebGLBackground( self, self.state, self.geometries, self._premultipliedAlpha )

        self.bufferRenderer = webGLBufferRenderer.WebGLBufferRenderer( self.extensions, self._infoRender )
        self.indexedBufferRenderer = webGLIndexedBufferRenderer.WebGLIndexedBufferRenderer( self.extensions, self._infoRender )

        self.flareRenderer = webGLFlareRenderer.WebGLFlareRenderer( self, self.state, self.extures, self.capabilities )
        self.spriteRenderer = webGLSpriteRenderer.WebGLSpriteRenderer( self, self.state, self.textures, self.capabilities )

        self.info.programs = self.programCache.programs

        self.context = GL

    # API

    # def getContext( self ):

    #     return GL

    # def getContextAttributes( self ):

    #     return GL.glGetContextAttributes()

    def forceContextLoss( self ):

        extension = self.extensions.get( "WEBGL_lose_context" )
        if extension : self.extension.loseContext()

    def forceContextRestore( self ):

        extension = self.extensions.get( "WEBGL_lose_context" )
        if extension : self.extension.restoreContext()

    def getPixelRatio( self ):

        return self._pixelRatio

    def setPixelRatio( self, value ):

        if value is None : return

        self._pixelRatio = value

        self.setSize( self._width, self._height, False )

    def getSize( self ):

        return {
            "width": self._width,
            "height": self._height
        }

    def setSize( self, width, height, updateStyle = True ):

        # device = vr.getDevice()

        # if device and hasattr( device, "isPresenting" ) :

        #     logging.warning( "THREE.WebGLRenderer: Can't change size while VR device is presenting." )
        #     return

        self._width = width
        self._height = height

        # _canvas.width = width * self._pixelRatio
        # _canvas.height = height * self._pixelRatio

        # if updateStyle != False :

        #     _canvas.style.width = width + "px"
        #     _canvas.style.height = height + "px"

        self.setViewport( 0, 0, width, height )

    def getDrawingBufferSize( self ):

        return {
            "width": self._width * self._pixelRatio,
            "height": self._height * self._pixelRatio
        }

    def setDrawingBufferSize( self, width, height, pixelRatio ):

        self._width = width
        self._height = height

        self._pixelRatio = pixelRatio

        # _canvas.width = width * pixelRatio
        # _canvas.height = height * pixelRatio

        self.setViewport( 0, 0, width, height )

    def setViewport( self, x, y, width, height ):

        self._viewport.set( x, self._height - y - height, width, height )
        self.state.viewport( self._currentViewport.copy( self._viewport ).multiplyScalar( self._pixelRatio ) )

    def setScissor( self, x, y, width, height ):

        self._scissor.set( x, self._height - y - height, width, height )
        self.state.scissor( self._currentScissor.copy( self._scissor ).multiplyScalar( self._pixelRatio ) )

    def setScissorTest( self, boolean ):

        self._scissorTest = boolean
        self.state.setScissorTest( self._scissorTest )

    # Clearing

    def getClearColor( self ):
        
        self.background.getClearColor()
    
    def setClearColor( self, color, alpha = 1 ):
        
        self.background.setClearColor( color, alpha )

    def getClearAlpha( self ):
    
        self.background.getClearAlpha()

    def setClearAlpha(self, alpha ):

        self.background.setClearAlpha( alpha )

    def clear( self, color = True, depth = True, stencil = True ):

        bits = 0

        if color : bits |= GL.GL_COLOR_BUFFER_BIT
        if depth : bits |= GL.GL_DEPTH_BUFFER_BIT
        if stencil : bits |= GL.GL_STENCIL_BUFFER_BIT

        GL.glClear( bits )

    def clearColor( self ):

        self.clear( True, False, False )

    def clearDepth( self ):

        self.clear( False, True, False )

    def clearStencil( self ):

        self.clear( False, False, True )

    def clearTarget( self, renderTarget, color, depth, stencil ):

        self.setRenderTarget( renderTarget )
        self.clear( color, depth, stencil )

    #

    def dispose( self ):

        # _canvas.removeEventListener( "webglcontextlost", onContextLost, False )
        # _canvas.removeEventListener( "webglcontextrestored", onContextRestore, False )

        self.renderLists.dispose()

        self.vr.dispose()

    # Events

    # def onContextLost( self, event ):

    #     # event.preventDefault()

    #     logging.log( "THREE.WebGLRenderer: Context Lost." )

    #     self._isContextLost = True

    # def onContextRestore( self, event ):

    #     logging.log( "THREE.WebGLRenderer: Context Restored." )

    #     self._isContextLost = False

    #     self.initGLContext()

    # def onMaterialDispose( self, event ):

    #     material = event.target

    #     material.removeEventListener( "dispose", onMaterialDispose )

    #     self.deallocateMaterial( material )

    # Buffer deallocation

    def deallocateMaterial( self, material ):

        self.releaseMaterialProgramReference( material )

        self.properties.remove( material )

    def releaseMaterialProgramReference( self, material ):

        programInfo = self.properties.get( material ).program

        material.program = None

        if programInfo is not None :

            self.programCache.releaseProgram( programInfo )

    # Buffer rendering

    def renderObjectImmediate( self, object, program, material ):

        def render( object ):

            self.renderBufferImmediate( object, program, material )

        object.render( render )

    def renderBufferImmediate( self, object, program, material ):

        self.state.initAttributes()

        buffers = self.properties.get( object )

        if object.hasPositions and not buffers.position : buffers.position = GL.glGenBuffers(1)
        if object.hasNormals and not buffers.normal : buffers.normal = GL.glGenBuffers(1)
        if object.hasUvs and not buffers.uv : buffers.uv = GL.glGenBuffers(1)
        if object.hasColors and not buffers.color : buffers.color = GL.glGenBuffers(1)

        programAttributes = program.getAttributes()

        if object.hasPositions :

            GL.glBindBuffer( GL.GL_ARRAY_BUFFER, buffers.position )
            GL.glBufferData( GL.GL_ARRAY_BUFFER, object.positionArray, GL.GL_DYNAMIC_DRAW )

            self.state.enableAttribute( programAttributes.position )
            GL.glVertexAttribPointer( programAttributes.position, 3, GL.GL_FLOAT, False, 0, 0 )

        if object.hasNormals :

            GL.glBindBuffer( GL.GL_ARRAY_BUFFER, buffers.normal )

            if  not hasattr( material, "isMeshPhongMaterial" ) and \
                not hasattr( material, "isMeshStandardMaterial" ) and \
                not hasattr( material, "isMeshNormalMaterial" ) and \
                material.flatShading == True :

                for i in range( 0, object.count * 3, 9 ) :

                    array = object.normalArray

                    nx = ( array[ i + 0 ] + array[ i + 3 ] + array[ i + 6 ] ) / 3
                    ny = ( array[ i + 1 ] + array[ i + 4 ] + array[ i + 7 ] ) / 3
                    nz = ( array[ i + 2 ] + array[ i + 5 ] + array[ i + 8 ] ) / 3

                    array[ i + 0 ] = nx
                    array[ i + 1 ] = ny
                    array[ i + 2 ] = nz

                    array[ i + 3 ] = nx
                    array[ i + 4 ] = ny
                    array[ i + 5 ] = nz

                    array[ i + 6 ] = nx
                    array[ i + 7 ] = ny
                    array[ i + 8 ] = nz

            GL.glBufferData( GL.GL_ARRAY_BUFFER, object.normalArray, GL.GL_DYNAMIC_DRAW )

            self.state.enableAttribute( programAttributes.normal )

            GL.glVertexAttribPointer( programAttributes.normal, 3, GL.GL_FLOAT, False, 0, 0 )

        if object.hasUvs and material.map :

            GL.glBindBuffer( GL.GL_ARRAY_BUFFER, buffers.uv )
            GL.glBufferData( GL.GL_ARRAY_BUFFER, object.uvArray, GL.GL_DYNAMIC_DRAW )

            self.state.enableAttribute( programAttributes.uv )

            GL.glVertexAttribPointer( programAttributes.uv, 2, GL.GL_FLOAT, False, 0, 0 )

        if object.hasColors and material.vertexColors != NoColors :

            GL.glBindBuffer( GL.GL_ARRAY_BUFFER, buffers.color )
            GL.glBufferData( GL.GL_ARRAY_BUFFER, object.colorArray, GL.GL_DYNAMIC_DRAW )

            self.state.enableAttribute( programAttributes.color )

            GL.glVertexAttribPointer( programAttributes.color, 3, GL.GL_FLOAT, False, 0, 0 )

        self.state.disableUnusedAttributes()

        GL.glDrawArrays( GL.GL_TRIANGLES, 0, object.count )

        object.count = 0

    def renderBufferDirect( self, camera, fog, geometry, material, object, group ):

        self.state.setMaterial( material )

        program = setProgram( camera, fog, material, object )
        geometryProgram = geometry.id + "_" + program.id + "_" + ( material.wireframe == True )

        updateBuffers = False

        if geometryProgram != self._currentGeometryProgram :

            self._currentGeometryProgram = geometryProgram
            updateBuffers = True

        if object.morphTargetInfluences :

            self.morphtargets.update( object, geometry, material, program )

            updateBuffers = True

        #

        index = geometry.index
        position = geometry.attributes.position
        rangeFactor = 1

        if material.wireframe == True :

            index = self.geometries.getWireframeAttribute( geometry )
            rangeFactor = 2

        attribute = None
        renderer = bufferRenderer

        if index is not None :

            attribute = attributes.get( index )

            renderer = indexedBufferRenderer
            renderer.setIndex( attribute )

        if updateBuffers :

            setupVertexAttributes( material, program, geometry )

            if index is not None :

                GL.glBindBuffer( GL.GL_ELEMENT_ARRAY_BUFFER, attribute.buffer )

        #

        dataCount = 0

        if index is not None :

            dataCount = index.count

        elif position is not None :

            dataCount = position.count

        rangeStart = geometry.drawRange.start * rangeFactor
        rangeCount = geometry.drawRange.count * rangeFactor

        groupStart = group.start * rangeFactor if group is not None else 0
        groupCount = group.count * rangeFactor if group is not None else float( "inf" )

        drawStart = max( rangeStart, groupStart )
        drawEnd = min( dataCount, rangeStart + rangeCount, groupStart + groupCount ) - 1

        drawCount = max( 0, drawEnd - drawStart + 1 )

        if drawCount == 0 : return

        #

        if hasattr( object, "isMesh" ) :

            if material.wireframe == True :

                self.state.setLineWidth( material.wireframeLinewidth * getTargetPixelRatio() )
                renderer.setMode( GL.GL_LINES )

            else:

                if object.drawMode == TrianglesDrawMode:
                    renderer.setMode( GL.GL_TRIANGLES )

                elif object.drawMode == TriangleStripDrawMode:
                    renderer.setMode( GL.GL_TRIANGLE_STRIP )

                elif object.drawMode == TriangleFanDrawMode:
                    renderer.setMode( GL.GL_TRIANGLE_FAN )

        elif hasattr( object, "isLine" ) :

            lineWidth = material.linewidth

            if lineWidth is None : lineWidth = 1 # Not using Line*Material

            state.setLineWidth( lineWidth * getTargetPixelRatio() )

            if hasattr( object, "isLineSegments" ) :

                renderer.setMode( GL.GL_LINES )

            elif hasattr( object, "isLineLoop" ) :

                renderer.setMode( GL.GL_LINE_LOOP )

            else:

                renderer.setMode( GL.GL_LINE_STRIP )

        elif hasattr( object, "isPoints" ) :

            renderer.setMode( GL.GL_POINTS )

        if geometry and hasattr( geometry, "isInstancedBufferGeometry" ) :

            if geometry.maxInstancedCount > 0 :

                renderer.renderInstances( geometry, drawStart, drawCount )

        else:

            renderer.render( drawStart, drawCount )

    def setupVertexAttributes( self, material, program, geometry, startIndex ):

        if geometry and hasattr( geometry, "isInstancedBufferGeometry" ) :

            if extensions.get( "ANGLE_instanced_arrays" ) is None :

                logging.error( "THREE.WebGLRenderer.setupVertexAttributes: using THREE.InstancedBufferGeometry but hardware does not support extension ANGLE_instanced_arrays." )
                return

        if startIndex is None : startIndex = 0

        self.state.initAttributes()

        geometryAttributes = geometry.attributes

        programAttributes = program.getAttributes()

        materialDefaultAttributeValues = material.defaultAttributeValues

        for name in programAttributes :

            programAttribute = programAttributes[ name ]

            if programAttribute >= 0 :

                geometryAttribute = geometryAttributes[ name ]

                if geometryAttribute is not None :

                    normalized = geometryAttribute.normalized
                    size = geometryAttribute.itemSize

                    attribute = attributes.get( geometryAttribute )

                    # TODO Attribute may not be available on context restore

                    if attribute is None : continue

                    buffer = attribute.buffer
                    type = attribute.type
                    bytesPerElement = attribute.bytesPerElement

                    if hasattr( geometryAttribute, "isInterleavedBufferAttribute" ) :

                        data = geometryAttribute.data
                        stride = data.stride
                        offset = geometryAttribute.offset

                        if data and hasattr( data, "isInstancedInterleavedBuffer" ) :

                            state.enableAttributeAndDivisor( programAttribute, data.meshPerAttribute )

                            if geometry.maxInstancedCount is None :

                                geometry.maxInstancedCount = data.meshPerAttribute * data.count

                        else:

                            state.enableAttribute( programAttribute )

                        GL.glBindBuffer( GL.GL_ARRAY_BUFFER, buffer )
                        GL.glVertexAttribPointer( programAttribute, size, type, normalized, stride * bytesPerElement, ( startIndex * stride + offset ) * bytesPerElement )

                    else:

                        if hasattr( geometryAttribute, "isInstancedBufferAttribute" ) :

                            state.enableAttributeAndDivisor( programAttribute, geometryAttribute.meshPerAttribute )

                            if geometry.maxInstancedCount is None :

                                geometry.maxInstancedCount = geometryAttribute.meshPerAttribute * geometryAttribute.count

                        else:

                            state.enableAttribute( programAttribute )

                        GL.glBindBuffer( GL.GL_ARRAY_BUFFER, buffer )
                        GL.glVertexAttribPointer( programAttribute, size, type, normalized, 0, startIndex * size * bytesPerElement )

                elif materialDefaultAttributeValues is not None :

                    value = materialDefaultAttributeValues[ name ]

                    if value is not None :

                        if len( value ) == 2:
                            GL.glVertexAttrib2fv( programAttribute, value )

                        elif len( value ) == 3:
                            GL.glVertexAttrib3fv( programAttribute, value )

                        elif len( value ) == 4:
                            GL.glVertexAttrib4fv( programAttribute, value )

                        else:
                            GL.glVertexAttrib1fv( programAttribute, value )

        self.state.disableUnusedAttributes()

    # Compile

    def compile( self, scene, camera ):

        self.lightsArray = []
        self.shadowsArray = []

        def traverse1( self, object ):

            if hasattr( object, "isLight" ) :

                self.lightsArray.append( object )

                if object.castShadow :

                    self.shadowsArray.append( object )
        
        scene.traverse( traverse1 )

        lights.setup( self.lightsArray, self.shadowsArray, camera )

        def traverse2( self, object ):

            if object.material :

                if isinstance( object.material, list ) :

                    for m in object.material :

                        initMaterial( m, scene.fog, object )

                else:

                    initMaterial( object.material, scene.fog, object )
        
        scene.traverse( traverse2 )

    # Rendering

    # def animate( self, callback ):

    #     def onFrame( self ):

    #         callback()

    #         ( vr.getDevice() or window ).requestAnimationFrame( onFrame )

    #     ( vr.getDevice() or window ).requestAnimationFrame( onFrame )

    def render( self, scene, camera, renderTarget = None, forceClear = True ):

        if not ( camera is not None and hasattr( camera, "isCamera" ) ) :

            logging.error( "THREE.WebGLRenderer.render: camera is not an instance of THREE.Camera." )
            return

        if self._isContextLost : return

        # reset caching for self frame

        self._currentGeometryProgram = ""
        self._currentMaterialId = - 1
        self._currentCamera = None

        # update scene graph

        if scene.autoUpdate == True : scene.updateMatrixWorld()

        # update camera matrices and frustum

        if camera.parent is None : camera.updateMatrixWorld()

        if vr.enabled :

            camera = vr.getCamera( camera )

        self._projScreenMatrix.multiplyMatrices( camera.projectionMatrix, camera.matrixWorldInverse )
        self._frustum.setFromMatrix( self._projScreenMatrix )

        self.lightsArray = []
        self.shadowsArray = []

        self.spritesArray = []
        self.flaresArray = []

        self._localClippingEnabled = self.localClippingEnabled
        self._clippingEnabled = self._clipping.init( self.clippingPlanes, self._localClippingEnabled, camera )

        self.currentRenderList = self.renderLists.get( scene, camera )
        self.currentRenderList.init()

        self.projectObject( scene, camera, self.sortObjects )

        if self.sortObjects == True :

            self.currentRenderList.sort()

        #

        if self._clippingEnabled : self._clipping.beginShadows()

        self.shadowMap.render( self.shadowsArray, scene, camera )

        self.lights.setup( self.lightsArray, self.shadowsArray, camera )

        if self._clippingEnabled : self._clipping.endShadows()

        #

        self._infoRender.frame += 1
        self._infoRender.calls = 0
        self._infoRender.vertices = 0
        self._infoRender.faces = 0
        self._infoRender.points = 0

        self.setRenderTarget( renderTarget )

        #

        self.background.render( self.currentRenderList, scene, camera, forceClear )

        # render scene

        opaqueObjects = self.currentRenderList.opaque
        transparentObjects = self.currentRenderList.transparent

        if scene.overrideMaterial :

            overrideMaterial = scene.overrideMaterial

            if len( opaqueObjects ) > 0 : renderObjects( opaqueObjects, scene, camera, overrideMaterial )
            if len( transparentObjects ) > 0 : renderObjects( transparentObjects, scene, camera, overrideMaterial )

        else:

            # opaque pass (front-to-back order)

            if len( opaqueObjects ) > 0 : renderObjects( opaqueObjects, scene, camera )

            # transparent pass (back-to-front order)

            if len( transparentObjects ) > 0 : renderObjects( transparentObjects, scene, camera )

        # custom renderers

        self.spriteRenderer.render( self.spritesArray, scene, camera )
        self.flareRenderer.render( self.flaresArray, scene, camera, self._currentViewport )

        # Generate mipmap if we"re using any kind of mipmap filtering

        if renderTarget :

            self.textures.updateRenderTargetMipmap( renderTarget )

        # Ensure depth buffer writing is enabled so it can be cleared on next render

        self.state.buffers.depth.setTest( True )
        self.state.buffers.depth.setMask( True )
        self.state.buffers.color.setMask( True )

        self.state.setPolygonOffset( False )

        if self.vr.enabled :

            self.vr.submitFrame()

        # GL.glFinish()

    """
    # TODO Duplicated code (Frustum)

    _sphere = sphere.Sphere()

    def isObjectViewable( self, object ):

        geometry = object.geometry

        if geometry.boundingSphere is None :
            geometry.computeBoundingSphere()

        _sphere.copy( geometry.boundingSphere ).
        applyMatrix4( object.matrixWorld )

        return isSphereViewable( _sphere )

    def isSpriteViewable( self, sprite ):

        _sphere.center.set( 0, 0, 0 )
        _sphere.radius = 0.7071067811865476
        _sphere.applyMatrix4( sprite.matrixWorld )

        return isSphereViewable( _sphere )

    def isSphereViewable( self, sphere ):

        if not self._frustum.intersectsSphere( sphere ) : return False

        numPlanes = self._clipping.numPlanes

        if numPlanes == 0 : return True

        planes = self.clippingPlanes,

            center = sphere.center,
            negRad = - sphere.radius,
            i = 0

        do {

            # out when deeper than radius in the negative halfspace
            if planes[ i ].distanceToPoint( center ) < negRad : return False

        } while ( += 1 i != numPlanes )

        return True

    """

    def projectObject( self, object, camera, sortObjects ):

        if not object.visible : return

        visible = object.layers.test( camera.layers )

        if visible :

            if hasattr( object, "isLight" ) :

                self.lightsArray.append( object )

                if object.castShadow :

                    self.shadowsArray.append( object )

            elif hasattr( object, "isSprite" ) :

                if not object.frustumCulled or self._frustum.intersectsSprite( object ) :

                    self.spritesArray.append( object )

            elif hasattr( object, "isLensFlare" ) :

                self.flaresArray.append( object )

            elif hasattr( object, "isImmediateRenderObject" ) :

                if sortObjects :

                    self._vector3.setFromMatrixPosition( object.matrixWorld ).applyMatrix4( self._projScreenMatrix )

                self.currentRenderList.append( object, None, object.material, self._vector3.z, None )

            elif hasattr( object, "isMesh" ) or hasattr( object, "isLine" ) or hasattr( object, "isPoints" ) :

                if hasattr( object, "isSkinnedMesh" ) :

                    object.skeleton.update()

                if not object.frustumCulled or self._frustum.intersectsObject( object ) :

                    if sortObjects :

                        self._vector3.setFromMatrixPosition( object.matrixWorld ).applyMatrix4( self._projScreenMatrix )

                    geometry = objects.update( object )
                    material = object.material

                    if isinstance( material, list ) :

                        groups = geometry.groups

                        for group in groups:

                            groupMaterial = material[ group.materialIndex ]

                            if groupMaterial and groupMaterial.visible :

                                self.currentRenderList.append( object, geometry, groupMaterial, self._vector3.z, group )

                    elif material.visible :

                        self.currentRenderList.append( object, geometry, material, self._vector3.z, None )

        children = object.children

        for child in children:

            projectObject( child, camera, sortObjects )

    def renderObjects( self, renderList, scene, camera, overrideMaterial ):

        for renderItem in renderList:

            object = renderItem.object
            geometry = renderItem.geometry
            material = renderItem.material if overrideMaterial is None else overrideMaterial
            group = renderItem.group

            if hasattr( camera, "isArrayCamera" ) :

                self._currentArrayCamera = camera

                cameras = camera.cameras

                for camera2 in cameras:

                    if object.layers.test( camera2.layers ) :

                        bounds = camera2.bounds

                        x = bounds.x * self._width
                        y = bounds.y * self._height
                        width = bounds.z * self._width
                        height = bounds.w * self._height

                        self.state.viewport( self._currentViewport.set( x, y, width, height ).multiplyScalar( self._pixelRatio ) )
                        self.state.scissor( self._currentScissor.set( x, y, width, height ).multiplyScalar( self._pixelRatio ) )
                        self.state.setScissorTest( True )

                        self.renderObject( object, scene, camera2, geometry, material, group )

            else:

                self._currentArrayCamera = None

                self.renderObject( object, scene, camera, geometry, material, group )

    def renderObject( self, object, scene, camera, geometry, material, group ):

        object.onBeforeRender( self, scene, camera, geometry, material, group )

        object.modelViewMatrix.multiplyMatrices( camera.matrixWorldInverse, object.matrixWorld )
        object.normalMatrix.getNormalMatrix( object.modelViewMatrix )

        if hasattr( object, "isImmediateRenderObject" ) :

            self.state.setMaterial( material )

            program = setProgram( camera, scene.fog, material, object )

            self._currentGeometryProgram = ""

            self.renderObjectImmediate( object, program, material )

        else:

            self.renderBufferDirect( camera, scene.fog, geometry, material, object, group )

        object.onAfterRender( self, scene, camera, geometry, material, group )

    def initMaterial( self, material, fog, object ):

        materialProperties = properties.get( material )

        parameters = programCache.getParameters( material, self.lights.state, self.shadowsArray, fog, self._clipping.numPlanes, self._clipping.numIntersection, object )

        code = self.programCache.getProgramCode( material, parameters )

        program = materialProperties.program
        programChange = True

        if program is None :

            # material
            material.addEventListener( "dispose", onMaterialDispose )

        elif program.code != code :

            # changed glsl or parameters
            self.releaseMaterialProgramReference( material )

        elif parameters.shaderID is not None :

            # same glsl and uniform list
            return

        else:

            # only rebuild uniform list
            programChange = False

        if programChange :

            if parameters.shaderID :

                shader = shaderLib.ShaderLib[ parameters.shaderID ]

                materialProperties.shader = {
                    "name": material.type,
                    "uniforms": uniformsUtils.UniformsUtils.clone( shader.uniforms ),
                    "vertexShader": shader.vertexShader,
                    "fragmentShader": shader.fragmentShader
                }

            else:

                materialProperties.shader = {
                    "name": material.type,
                    "uniforms": material.uniforms,
                    "vertexShader": material.vertexShader,
                    "fragmentShader": material.fragmentShader
                }

            material.onBeforeCompile( materialProperties.shader )

            program = self.programCache.acquireProgram( material, materialProperties.shader, parameters, code )

            materialProperties.program = program
            material.program = program

        programAttributes = program.getAttributes()

        if material.morphTargets :

            material.numSupportedMorphTargets = 0

            for i in range( self.maxMorphTargets ) :

                if programAttributes[ "morphTarget%s" % i ] >= 0 :

                    material.numSupportedMorphTargets += 1

        if material.morphNormals :

            material.numSupportedMorphNormals = 0

            for i in range( self.maxMorphNormals ) :

                if programAttributes[ "morphNormal%s" % i ] >= 0 :

                    material.numSupportedMorphNormals += 1

        uniforms = materialProperties.shader.uniforms

        if  not hasattr( material, "isShaderMaterial" ) and \
            not hasattr( material, "isRawShaderMaterial" ) or \
            material.clipping == True :

            materialProperties.numClippingPlanes = self._clipping.numPlanes
            materialProperties.numIntersection = self._clipping.numIntersection
            uniforms.clippingPlanes = self._clipping.uniform

        materialProperties.fog = fog

        # store the light setup it was created for

        materialProperties.lightsHash = self.lights.state.hash

        if material.lights :

            # wire up the material to self renderer"s lighting state

            uniforms.ambientLightColor.value = lights.state.ambient
            uniforms.directionalLights.value = lights.state.directional
            uniforms.spotLights.value = lights.state.spot
            uniforms.rectAreaLights.value = lights.state.rectArea
            uniforms.pointLights.value = lights.state.point
            uniforms.hemisphereLights.value = lights.state.hemi

            uniforms.directionalShadowMap.value = lights.state.directionalShadowMap
            uniforms.directionalShadowMatrix.value = lights.state.directionalShadowMatrix
            uniforms.spotShadowMap.value = lights.state.spotShadowMap
            uniforms.spotShadowMatrix.value = lights.state.spotShadowMatrix
            uniforms.pointShadowMap.value = lights.state.pointShadowMap
            uniforms.pointShadowMatrix.value = lights.state.pointShadowMatrix
            # TODO "(abelnation)": add area lights shadow info to uniforms

        progUniforms = materialProperties.program.getUniforms()
        uniformsList = webGLUniforms.WebGLUniforms.seqWithValue( progUniforms.seq, uniforms )

        materialProperties.uniformsList = uniformsList

    def setProgram( self, camera, fog, material, object ):

        self._usedTextureUnits = 0

        materialProperties = properties.get( material )

        if self._clippingEnabled :

            if self._localClippingEnabled or camera != self._currentCamera :

                useCache = \
                    camera == self._currentCamera and \
                    material.id == self._currentMaterialId

                # we might want to call self function with some ClippingGroup
                # object instead of the material, once it becomes feasible
                # (#8465, #8379)
                self._clipping.setState(
                    material.clippingPlanes, material.clipIntersection, material.clipShadows,
                    camera, materialProperties, useCache )

        if material.needsUpdate == False :

            if materialProperties.program is None :

                material.needsUpdate = True

            elif material.fog and materialProperties.fog != fog :

                material.needsUpdate = True

            elif material.lights and materialProperties.lightsHash != lights.state.hash :

                material.needsUpdate = True

            elif  materialProperties.numClippingPlanes is not None and \
                ( materialProperties.numClippingPlanes != self._clipping.numPlanes or \
                materialProperties.numIntersection != self._clipping.numIntersection ) :

                material.needsUpdate = True

        if material.needsUpdate :

            self.initMaterial( material, fog, object )
            material.needsUpdate = False

        refreshProgram = False
        refreshMaterial = False
        refreshLights = False

        program = materialProperties.program
        p_uniforms = program.getUniforms()
        m_uniforms = materialProperties.shader.uniforms

        if state.useProgram( program.program ) :

            refreshProgram = True
            refreshMaterial = True
            refreshLights = True

        if material.id != self._currentMaterialId :

            self._currentMaterialId = material.id

            refreshMaterial = True

        if refreshProgram or camera != self._currentCamera :

            p_uniforms.setValue( "projectionMatrix", camera.projectionMatrix )

            if capabilities.logarithmicDepthBuffer :

                p_uniforms.setValue( "logDepthBufFC",
                    2.0 / ( math.log( camera.far + 1.0 ) / math.LN2 ) )

            # Avoid unneeded uniform updates per ArrayCamera"s sub-camera

            if self._currentCamera != ( self._currentArrayCamera or camera ) :

                self._currentCamera = ( self._currentArrayCamera or camera )

                # lighting uniforms depend on the camera so enforce an update
                # now, in case self material supports lights - or later, when
                # the next material that does gets "activated":

                refreshMaterial = True        # set to True on material change
                refreshLights = True        # remains set until update done

            # load material specific uniforms
            # (shader material also gets them for the sake of genericity)

            if  hasattr( material, "isShaderMaterial" ) or \
                hasattr( material, "isMeshPhongMaterial" ) or \
                hasattr( material, "isMeshStandardMaterial" ) or \
                material.envMap :

                uCamPos = p_uniforms.map.cameraPosition

                if uCamPos is not None :

                    uCamPos.setValue( self._vector3.setFromMatrixPosition( camera.matrixWorld ) )

            if  hasattr( material, "isMeshPhongMaterial" ) or \
                hasattr( material, "isMeshLambertMaterial" ) or \
                hasattr( material, "isMeshBasicMaterial" ) or \
                hasattr( material, "isMeshStandardMaterial" ) or \
                hasattr( material, "isShaderMaterial" ) or \
                material.skinning :

                p_uniforms.setValue( "viewMatrix", camera.matrixWorldInverse )

        # skinning uniforms must be set even if material didn"t change
        # auto-setting of texture unit for bone texture must go before other textures
        # not sure why, but otherwise weird things happen

        if material.skinning :

            p_uniforms.setOptional( object, "bindMatrix" )
            p_uniforms.setOptional( object, "bindMatrixInverse" )

            skeleton = object.skeleton

            if skeleton :

                bones = skeleton.bones

                if capabilities.floatVertexTextures :

                    if skeleton.boneTexture is None :

                        # layout (1 matrix = 4 pixels)
                        #      RGBA RGBA RGBA RGBA (=> column1, column2, column3, column4)
                        #  with  8x8  pixel texture max   16 bones * 4 pixels =  (8 * 8)
                        #       16x16 pixel texture max   64 bones * 4 pixels = (16 * 16)
                        #       32x32 pixel texture max  256 bones * 4 pixels = (32 * 32)
                        #       64x64 pixel texture max 1024 bones * 4 pixels = (64 * 64)

                        size = math.sqrt( len( bones ) * 4 ) # 4 pixels needed for 1 matrix
                        size = _Math.nextPowerOfTwo( math.ceil( size ) )
                        size = max( size, 4 )

                        boneMatrices = Float32Array( size * size * 4 ) # 4 floats per RGBA pixel
                        boneMatrices.set( skeleton.boneMatrices ) # copy current values

                        boneTexture = dataTexture.DataTexture( boneMatrices, size, size, RGBAFormat, FloatType )

                        skeleton.boneMatrices = boneMatrices
                        skeleton.boneTexture = boneTexture
                        skeleton.boneTextureSize = size

                    p_uniforms.setValue( "boneTexture", skeleton.boneTexture )
                    p_uniforms.setValue( "boneTextureSize", skeleton.boneTextureSize )

                else:

                    p_uniforms.setOptional( skeleton, "boneMatrices" )

        if refreshMaterial :

            p_uniforms.setValue( "toneMappingExposure", self.toneMappingExposure )
            p_uniforms.setValue( "toneMappingWhitePoint", self.toneMappingWhitePoint )

            if material.lights :

                # the current material requires lighting info

                # "note": all lighting uniforms are always set correctly
                # they simply reference the renderer"s state for their
                # values
                #
                # use the current material"s .needsUpdate flags to set
                # the GL state when required

                self.markUniformsLightsNeedsUpdate( m_uniforms, refreshLights )

            # refresh uniforms common to several materials

            if fog and material.fog :

                self.refreshUniformsFog( m_uniforms, fog )

            if hasattr( material, "isMeshBasicMaterial" ) :

                self.refreshUniformsCommon( m_uniforms, material )

            elif hasattr( material, "isMeshLambertMaterial" ) :

                self.refreshUniformsCommon( m_uniforms, material )
                self.refreshUniformsLambert( m_uniforms, material )

            elif hasattr( material, "isMeshPhongMaterial" ) :

                self.refreshUniformsCommon( m_uniforms, material )

                if hasattr( material, "isMeshToonMaterial" ) :

                    self.refreshUniformsToon( m_uniforms, material )

                else:

                    self.refreshUniformsPhong( m_uniforms, material )

            elif hasattr( material, "isMeshStandardMaterial" ) :

                self.refreshUniformsCommon( m_uniforms, material )

                if hasattr( material, "isMeshPhysicalMaterial" ) :

                    self.refreshUniformsPhysical( m_uniforms, material )

                else:

                    self.refreshUniformsStandard( m_uniforms, material )

            elif hasattr( material, "isMeshNormalMaterial" ) :

                self.refreshUniformsCommon( m_uniforms, material )

            elif hasattr( material, "isMeshDepthMaterial" ) :

                self.refreshUniformsCommon( m_uniforms, material )
                self.refreshUniformsDepth( m_uniforms, material )

            elif hasattr( material, "isMeshDistanceMaterial" ) :

                self.refreshUniformsCommon( m_uniforms, material )
                self.refreshUniformsDistance( m_uniforms, material )

            elif hasattr( material, "isMeshNormalMaterial" ) :

                self.refreshUniformsNormal( m_uniforms, material )

            elif hasattr( material, "isLineBasicMaterial" ) :

                self.refreshUniformsLine( m_uniforms, material )

                if hasattr( material, "isLineDashedMaterial" ) :

                    self.refreshUniformsDash( m_uniforms, material )

            elif hasattr( material, "isPointsMaterial" ) :

                self.refreshUniformsPoints( m_uniforms, material )

            elif hasattr( material, "isShadowMaterial" ) :

                m_uniforms.color.value = material.color
                m_uniforms.opacity.value = material.opacity

            # RectAreaLight Texture
            # TODO "(mrdoob)": Find a nicer implementation

            if m_uniforms.ltcMat is not None : m_uniforms.ltcMat.value = uniformsLib.UniformsLib.LTC_MAT_TEXTURE
            if m_uniforms.ltcMag is not None : m_uniforms.ltcMag.value = uniformsLib.UniformsLib.LTC_MAG_TEXTURE

            webGLUniforms.WebGLUniforms.upload( materialProperties.uniformsList, m_uniforms, self )

        # common matrices

        p_uniforms.setValue( "modelViewMatrix", object.modelViewMatrix )
        p_uniforms.setValue( "normalMatrix", object.normalMatrix )
        p_uniforms.setValue( "modelMatrix", object.matrixWorld )

        return program

    # Uniforms (refresh uniforms objects)

    def refreshUniformsCommon( self, uniforms, material ):

        uniforms.opacity.value = material.opacity

        if material.color :

            uniforms.diffuse.value = material.color

        if material.emissive :

            uniforms.emissive.value.copy( material.emissive ).multiplyScalar( material.emissiveIntensity )

        if material.map :

            uniforms.map.value = material.map

        if material.alphaMap :

            uniforms.alphaMap.value = material.alphaMap

        if material.specularMap :

            uniforms.specularMap.value = material.specularMap

        if material.envMap :

            uniforms.envMap.value = material.envMap

            # don"t flip CubeTexture envMaps, flip everything "else":
            #  WebGLRenderTargetCube will be flipped for backwards compatibility
            #  WebGLRenderTargetCube.texture will be flipped because it"s a Texture and NOT a CubeTexture
            # self check must be handled differently, or removed entirely, if WebGLRenderTargetCube uses a CubeTexture in the future
            uniforms.flipEnvMap.value = 1 if not ( material.envMap and hasattr( material.envMap, "isCubeTexture" ) ) else - 1

            uniforms.reflectivity.value = material.reflectivity
            uniforms.refractionRatio.value = material.refractionRatio

        if material.lightMap :

            uniforms.lightMap.value = material.lightMap
            uniforms.lightMapIntensity.value = material.lightMapIntensity

        if material.aoMap :

            uniforms.aoMap.value = material.aoMap
            uniforms.aoMapIntensity.value = material.aoMapIntensity

        # uv repeat and offset setting priorities
        # 1. color map
        # 2. specular map
        # 3. normal map
        # 4. bump map
        # 5. alpha map
        # 6. emissive map

        uvScaleMap

        if material.map :

            uvScaleMap = material.map

        elif material.specularMap :

            uvScaleMap = material.specularMap

        elif material.displacementMap :

            uvScaleMap = material.displacementMap

        elif material.normalMap :

            uvScaleMap = material.normalMap

        elif material.bumpMap :

            uvScaleMap = material.bumpMap

        elif material.roughnessMap :

            uvScaleMap = material.roughnessMap

        elif material.metalnessMap :

            uvScaleMap = material.metalnessMap

        elif material.alphaMap :

            uvScaleMap = material.alphaMap

        elif material.emissiveMap :

            uvScaleMap = material.emissiveMap

        if uvScaleMap is not None :

            # backwards compatibility
            if hasattr( uvScaleMap, "isWebGLRenderTarget" ) :

                uvScaleMap = uvScaleMap.texture

            offset = uvScaleMap.offset
            repeat = uvScaleMap.repeat

            uniforms.offsetRepeat.value.set( offset.x, offset.y, repeat.x, repeat.y )

    def refreshUniformsLine( self, uniforms, material ):

        uniforms.diffuse.value = material.color
        uniforms.opacity.value = material.opacity

    def refreshUniformsDash( self, uniforms, material ):

        uniforms.dashSize.value = material.dashSize
        uniforms.totalSize.value = material.dashSize + material.gapSize
        uniforms.scale.value = material.scale

    def refreshUniformsPoints( self, uniforms, material ):

        uniforms.diffuse.value = material.color
        uniforms.opacity.value = material.opacity
        uniforms.size.value = material.size * self._pixelRatio
        uniforms.scale.value = self._height * 0.5

        uniforms.map.value = material.map

        if material.map is not None :

            offset = material.map.offset
            repeat = material.map.repeat

            uniforms.offsetRepeat.value.set( offset.x, offset.y, repeat.x, repeat.y )

    def refreshUniformsFog( self, uniforms, fog ):

        uniforms.fogColor.value = fog.color

        if hasattr( fog, "isFog" ) :

            uniforms.fogNear.value = fog.near
            uniforms.fogFar.value = fog.far

        elif hasattr( fog, "isFogExp2" ) :

            uniforms.fogDensity.value = fog.density

    def refreshUniformsLambert( self, uniforms, material ):

        if material.emissiveMap :

            uniforms.emissiveMap.value = material.emissiveMap

    def refreshUniformsPhong( self, uniforms, material ):

        uniforms.specular.value = material.specular
        uniforms.shininess.value = max( material.shininess, 1e-4 ) # to prevent pow( 0.0, 0.0 )

        if material.emissiveMap :

            uniforms.emissiveMap.value = material.emissiveMap

        if material.bumpMap :

            uniforms.bumpMap.value = material.bumpMap
            uniforms.bumpScale.value = material.bumpScale

        if material.normalMap :

            uniforms.normalMap.value = material.normalMap
            uniforms.normalScale.value.copy( material.normalScale )

        if material.displacementMap :

            uniforms.displacementMap.value = material.displacementMap
            uniforms.displacementScale.value = material.displacementScale
            uniforms.displacementBias.value = material.displacementBias

    def refreshUniformsToon( self, uniforms, material ):

        refreshUniformsPhong( uniforms, material )

        if material.gradientMap :

            uniforms.gradientMap.value = material.gradientMap

    def refreshUniformsStandard( self, uniforms, material ):

        uniforms.roughness.value = material.roughness
        uniforms.metalness.value = material.metalness

        if material.roughnessMap :

            uniforms.roughnessMap.value = material.roughnessMap

        if material.metalnessMap :

            uniforms.metalnessMap.value = material.metalnessMap

        if material.emissiveMap :

            uniforms.emissiveMap.value = material.emissiveMap

        if material.bumpMap :

            uniforms.bumpMap.value = material.bumpMap
            uniforms.bumpScale.value = material.bumpScale

        if material.normalMap :

            uniforms.normalMap.value = material.normalMap
            uniforms.normalScale.value.copy( material.normalScale )

        if material.displacementMap :

            uniforms.displacementMap.value = material.displacementMap
            uniforms.displacementScale.value = material.displacementScale
            uniforms.displacementBias.value = material.displacementBias

        if material.envMap :

            #uniforms.envMap.value = material.envMap # part of uniforms common
            uniforms.envMapIntensity.value = material.envMapIntensity

    def refreshUniformsPhysical( self, uniforms, material ):

        uniforms.clearCoat.value = material.clearCoat
        uniforms.clearCoatRoughness.value = material.clearCoatRoughness

        refreshUniformsStandard( uniforms, material )

    def refreshUniformsDepth( self, uniforms, material ):

        if material.displacementMap :

            uniforms.displacementMap.value = material.displacementMap
            uniforms.displacementScale.value = material.displacementScale
            uniforms.displacementBias.value = material.displacementBias

    def refreshUniformsDistance( self, uniforms, material ):

        if material.displacementMap :

            uniforms.displacementMap.value = material.displacementMap
            uniforms.displacementScale.value = material.displacementScale
            uniforms.displacementBias.value = material.displacementBias

        uniforms.referencePosition.value.copy( material.referencePosition )
        uniforms.nearDistance.value = material.nearDistance
        uniforms.farDistance.value = material.farDistance

    def refreshUniformsNormal( self, uniforms, material ):

        if material.bumpMap :

            uniforms.bumpMap.value = material.bumpMap
            uniforms.bumpScale.value = material.bumpScale

        if material.normalMap :

            uniforms.normalMap.value = material.normalMap
            uniforms.normalScale.value.copy( material.normalScale )

        if material.displacementMap :

            uniforms.displacementMap.value = material.displacementMap
            uniforms.displacementScale.value = material.displacementScale
            uniforms.displacementBias.value = material.displacementBias

    # If uniforms are marked as clean, they don"t need to be loaded to the GPU.

    def markUniformsLightsNeedsUpdate( self, uniforms, value ):

        uniforms.ambientLightColor.needsUpdate = value

        uniforms.directionalLights.needsUpdate = value
        uniforms.pointLights.needsUpdate = value
        uniforms.spotLights.needsUpdate = value
        uniforms.rectAreaLights.needsUpdate = value
        uniforms.hemisphereLights.needsUpdate = value

    # GL state setting

    def setFaceCulling( self, cullFace, frontFaceDirection ):

        self.state.setCullFace( cullFace )
        self.state.setFlipSided( frontFaceDirection == FrontFaceDirectionCW )

    # Textures

    def allocTextureUnit( self ):

        textureUnit = self._usedTextureUnits

        if textureUnit >= self.capabilities.maxTextures :

            logging.warning( "THREE.WebGLRenderer: Trying to use %s texture units while self GPU supports only %s" %  ( textureUnit, capabilities.maxTextures ) )

        self._usedTextureUnits += 1

        return textureUnit

    # self.setTexture2D = setTexture2D
    def setTexture2D( self, texture, slot ):

        warned = False

        # backwards "compatibility": peel texture.texture

        if texture and hasattr( texture, "isWebGLRenderTarget" ) :

            if not warned :

                logging.warning( "THREE.WebGLRenderer.setTexture2D: don't use render targets as textures. Use their .texture property instead." )
                warned = True

            texture = texture.texture

        self.textures.setTexture2D( texture, slot )

    def setTexture( self, texture, slot ):

        warned = False

        if not warned :

            logging.warning( "THREE.WebGLRenderer: .setTexture is deprecated, use setTexture2D instead." )
            warned = True

        textures.setTexture2D( texture, slot )

    def setTextureCube( self, texture, slot ):

        warned = False

        # backwards "compatibility": peel texture.texture
        if texture and hasattr( texture, "isWebGLRenderTargetCube" ) :

            if not warned :

                logging.warning( "THREE.WebGLRenderer.setTextureCube: don't use cube render targets as textures. Use their .texture property instead." )
                warned = True

            texture = texture.texture

        # currently relying on the fact that WebGLRenderTargetCube.texture is a Texture and NOT a CubeTexture
        # "TODO": unify these code paths
        if texture and hasattr( texture, "isCubeTexture" ) or \
            ( isinstance( texture.image, list ) and len( texture.image ) == 6 ) :

            # CompressedTexture can have Array in "image":/

            # self function alone should take care of cube textures
            self.textures.setTextureCube( texture, slot )

        else:

            # "assumed": texture property of THREE.WebGLRenderTargetCube

            self.textures.setTextureCubeDynamic( texture, slot )

    def getRenderTarget( self ):

        return self._currentRenderTarget

    def setRenderTarget( self, renderTarget ):

        self._currentRenderTarget = renderTarget

        if renderTarget and self.properties.get( renderTarget ).__webglFramebuffer is None :

            self.textures.setupRenderTarget( renderTarget )

        framebuffer = None
        isCube = False

        if renderTarget :

            __webglFramebuffer = properties.get( renderTarget ).__webglFramebuffer

            if hasattr( renderTarget, "isWebGLRenderTargetCube" ) :

                framebuffer = __webglFramebuffer[ renderTarget.activeCubeFace ]
                isCube = True

            else:

                framebuffer = __webglFramebuffer

            self._currentViewport.copy( renderTarget.viewport )
            self._currentScissor.copy( renderTarget.scissor )
            self._currentScissorTest = renderTarget.scissorTest

        else:

            self._currentViewport.copy( self._viewport ).multiplyScalar( self._pixelRatio )
            self._currentScissor.copy( self._scissor ).multiplyScalar( self._pixelRatio )
            self._currentScissorTest = self._scissorTest

        if self._currentFramebuffer != framebuffer :

            GL.glBindFramebuffer( GL.GL_FRAMEBUFFER, framebuffer )
            self._currentFramebuffer = framebuffer

        state.viewport( self._currentViewport )
        state.scissor( self._currentScissor )
        state.setScissorTest( self._currentScissorTest )

        if isCube :

            textureProperties = self.properties.get( renderTarget.texture )
            GL.glFramebufferTexture2D( GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, GL.GL_TEXTURE_CUBE_MAP_POSITIVE_X + renderTarget.activeCubeFace, textureProperties.__webglTexture, renderTarget.activeMipMapLevel )

    def readRenderTargetPixels( self, renderTarget, x, y, width, height, buffer ):

        if not ( renderTarget and hasattr( renderTarget, "isWebGLRenderTarget" ) ) :

            logging.error( "THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget." )
            return

        framebuffer = self.properties.get( renderTarget ).__webglFramebuffer

        if framebuffer :

            restore = False

            if framebuffer != self._currentFramebuffer :

                GL.glBindFramebuffer( GL.GL_FRAMEBUFFER, framebuffer )

                restore = True

            texture = renderTarget.texture
            textureFormat = texture.format
            textureType = texture.type

            if textureFormat != RGBAFormat and utils.convert( textureFormat ) != GL.glGetParameter( GL.GL_IMPLEMENTATION_COLOR_READ_FORMAT ) :

                logging.error( "THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in RGBA or implementation defined format." )
                return

            if textureType != UnsignedByteType and utils.convert( textureType ) != GL.glGetParameter( GL.GL_IMPLEMENTATION_COLOR_READ_TYPE ) and \
                not ( textureType == FloatType and ( extensions.get( "OES_texture_float" ) or extensions.get( "WEBGL_color_buffer_float" ) ) ) and \
                not ( textureType == HalfFloatType and extensions.get( "EXT_color_buffer_half_float" ) ) :

                logging.error( "THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not in UnsignedByteType or implementation defined type." )
                return

            if GL.glCheckFramebufferStatus( GL.GL_FRAMEBUFFER ) == GL.GL_FRAMEBUFFER_COMPLETE :

                # the following if statement ensures valid read requests (no out-of-bounds pixels, see #8604)

                if ( x >= 0 and x <= ( renderTarget.width - width ) ) and ( y >= 0 and y <= ( renderTarget.height - height ) ) :

                    GL.glReadPixels( x, y, width, height, utils.convert( textureFormat ), utils.convert( textureType ), buffer )

            else:

                logging.error( "THREE.WebGLRenderer.readRenderTargetPixels: readPixels from renderTarget failed. Framebuffer not complete." )

            if restore :

                GL.glBindFramebuffer( GL.GL_FRAMEBUFFER, self._currentFramebuffer )
