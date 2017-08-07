from __future__ import division

from OpenGL.GL import *

import logging

from ctypes import c_void_p

from ...constants import LinearFilter, NearestFilter, RGBFormat, RGBAFormat, DepthFormat, DepthStencilFormat, UnsignedShortType, UnsignedIntType, UnsignedInt248Type, FloatType, HalfFloatType, ClampToEdgeWrapping, NearestMipMapLinearFilter, NearestMipMapNearestFilter
from ...math import _Math

import OpenGLState as state
import OpenGLProperties as properties
import OpenGLCapabilities as capabilities
import OpenGLUtils as utils
import OpenGLExtensions as extensions

# TODO _isWebGL2

def isPowerOfTwo( image ):

    return _Math.isPowerOfTwo( image.get_width() ) and _Math.isPowerOfTwo( image.get_height() )

def isRenderTargetPowerOfTwo( renderTarget ):

    return _Math.isPowerOfTwo( renderTarget.width ) and _Math.isPowerOfTwo( renderTarget.height )

def textureNeedsGenerateMipmaps( texture, isPowerOfTwo ):

    return texture.generateMipmaps and isPowerOfTwo and \
        texture.minFilter != NearestFilter and texture.minFilter != LinearFilter

# Fallback filters for non-power-of-2 textures

def filterFallback( f ):

    if f == NearestFilter or f == NearestMipMapNearestFilter or f == NearestMipMapLinearFilter:

        return GL_NEAREST

    return GL_LINEAR

def onTextureDispose( event ):

    from ..OpenGLRenderer import _infoMemory as infoMemory

    texture = event.target

    texture.removeEventListener( "dispose", onTextureDispose )

    deallocateTexture( texture )

    infoMemory.textures -= 1

def onRenderTargetDispose( event ):

    from ..OpenGLRenderer import _infoMemory as infoMemory

    texture = event.target

    texture.removeEventListener( "dispose", onRenderTarget )

    deallocateRenderTarget( renderTarget )

    infoMemory.textures -= 1

def deallocateTexture( texture ):

    textureProperties = properties.get( texture )

    if texture.image and textureProperties._image_openglTextureCube:

        # cube texture

        glDeleteTexture( textureProperties._image_openglTextureCube )

    else:

        # 2D texture

        if not textureProperties._openglInit: return

        glDeleteTexture( textureProperties._openglTexture )

    # remove all opengl properties
    properties.remove( texture )

def deallocateRenderTarget( renderTarget ):

    renderTargetProperties = properties.get( renderTarget )
    textureProperties = properties.get( renderTarget.texture )

    if not renderTarget: return

    if textureProperties._openglTexture:

        glDeleteTexture( textureProperties._openglTexture )

    if renderTarget.depthTexture:

        renderTarget.depthTexture.dispose()

    if hasattr( renderTarget, "isOpenGLRenderTargetCube" ):

        for i in xrange( 6 ):

            glDeleteFramebuffer( renderTargetProperties._openglFramebuffer[ i ] )
            if renderTargetProperties._openglDepthbuffer: glDeleteRenderbuffer( renderTargetProperties._openglDepthbuffer[ i ] )

    else:

        glDeleteFramebuffer( renderTargetProperties._openglFramebuffer )
        if renderTargetProperties._openglDepthbuffer: glDeleteRenderbuffer( renderTargetProperties._openglDepthbuffer )

    properties.remove( renderTarget.texture )
    properties.remove( renderTarget )

def setTexture2D( texture, slot ):

    textureProperties = properties.get( texture )

    if texture.version > 0 and textureProperties._version != texture.version:

        image = texture.image

        if not image:

            logging.warning( "THREE.WebGLRenderer: Texture marked for update but image is undefined %s", texture )

        else:

            uploadTexture( textureProperties, texture, slot )
            return

    state.activeTexture( GL_TEXTURE0 + slot )
    state.bindTexture( GL_TEXTURE_2D, textureProperties._openglTexture )

# TODO setTextureCube

def setTextureParameters( textureType, texture, isPowerOfTwoImage ):

    if isPowerOfTwoImage:

        glTexParameteri( textureType, GL_TEXTURE_WRAP_S, utils.convert( texture.wrapS ) )
        glTexParameteri( textureType, GL_TEXTURE_WRAP_T, utils.convert( texture.wrapT ) )

        glTexParameteri( textureType, GL_TEXTURE_MAG_FILTER, utils.convert( texture.magFilter ) )
        glTexParameteri( textureType, GL_TEXTURE_MIN_FILTER, utils.convert( texture.minFilter ) )
    
    else:

        glTexParameteri( textureType, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE )
        glTexParameteri( textureType, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE )

        if texture.wrapS != ClampToEdgeWrapping or texture.wrapT != ClampToEdgeWrapping:

            logging.warning( "THREE.WebGLRenderer: Texture is not power of two. Texture.wrapS and Texture.wrapT should be set to THREE.ClampToEdgeWrapping. %s" % texture )


        glTexParameteri( textureType, GL_TEXTURE_MAG_FILTER, filterFallback( texture.magFilter ) )
        glTexParameteri( textureType, GL_TEXTURE_MIN_FILTER, filterFallback( texture.minFilter ) )

        if texture.minFilter != NearestFilter and texture.minFilter != LinearFilter:

            logging.warning( "THREE.WebGLRenderer: Texture is not power of two. Texture.minFilter should be set to THREE.NearestFilter or THREE.LinearFilter. %s" % texture )
    
    extension = extensions.get( "EXT_texture_filter_anisotropic" )

    if extension:

        if texture.type == FloatType and extensions.get( "OES_texture_float_linear" ) is None: return
        if texture.type == HalfFloatType and extensions.get( "OES_texture_half_float_linear" ) is None: return

        if texture.anisotropy > 1 or properties.get( texture ).__currentAnisotropy:

            glTexParameterf( textureType, extension.GL_TEXTURE_MAX_ANISOTROPY_EXT, min( texture.anisotropy, capabilities.getMaxAnisotropy() ) )
            properties.get( texture ).__currentAnisotropy = texture.anisotropy

def uploadTexture( textureProperties, texture, slot ):

    from ..OpenGLRenderer import _infoMemory as infoMemory

    if not textureProperties._openglInit:

        textureProperties._openglInit = True

        texture.addEventListener( "dispose", onTextureDispose )

        textureProperties._openglTexture = glGenTextures( 1 )

        infoMemory.textures += 1
    
    state.activeTexture( GL_TEXTURE0 + slot )
    state.bindTexture( GL_TEXTURE_2D, textureProperties._openglTexture )

    # glPixelStorei( GL_UNPACK_FLIP_Y_WEBGL, texture.flipY )
    # glPixelStorei( GL_UNPACK_PREMULTIPLY_ALPHA_WEBGL, texture.premultiplyAlpha )
    glPixelStorei( GL_UNPACK_ALIGNMENT, texture.unpackAlignment )

    # image = clampToMaxSize( texture.image, capabilities.maxTextureSize )
    image = texture.image

    # if textureNeedsPowerOfTwo( texture ) and isPowerOfTwo( image ) == False:

    #     image = makePowerOfTwo( image )

    isPowerOfTwoImage = isPowerOfTwo( image )
    glFormat = utils.convert( texture.format )
    glType = utils.convert( texture.type )

    setTextureParameters( GL_TEXTURE_2D, texture, isPowerOfTwoImage )

    mipmaps = texture.mipmaps

    if hasattr( texture, "isDepthTexture" ):

        # TODO
        pass

    elif hasattr( texture, "isDataTexture" ):

        # TODO
        pass
    
    elif hasattr( texture, "isCompressedTexture" ):

        # TODO
        pass
    
    else:

        # regular Texture (pygame.Surface)

        # use manually created mipmaps if available
        # if there are no manual mipmaps
        # set 0 level mipmap and then use GL to generate other mipmap levels

        if len( mipmaps ) and isPowerOfTwoImage:

            for i in xrange( len( mipmaps ) ):

                mipmap = mipmaps[ i ]
                state.texImage2D( GL_TEXTURE_2D, i, glFormat, glFormat, glType, mipmap )
            
            texture.generateMipmaps = False
        
        else:

            state.texImage2D( GL_TEXTURE_2D, 0, glFormat, image.get_width(), image.get_height(), 0, glFormat, glType, c_void_p( image._pixels_address ) )

    if ( textureNeedsGenerateMipmaps( texture, isPowerOfTwoImage ) ): glGenerateMipmap( GL_TEXTURE_2D )

    textureProperties._version = texture.version

    if texture.onUpdate: texture.onUpdate( texture )

# Render targets

def setupFrameBufferTexture( framebuffer, renderTarget, attachment, textureTarget ):

    glFormat = utils.convert( renderTarget.texture.format )
    glType = utils.convert( renderTarget.texture.type )
    state.texImage2D( textureTarget, 0, glFormat, renderTarget.width, renderTarget.height, 0, glFormat, glType, None )
    glBindFramebuffer( GL_FRAMEBUFFER, framebuffer )
    glFramebufferTexture2D( GL_FRAMEBUFFER, attachment, textureTarget, properties.get( renderTarget.texture )._openglTexture, 0 )
    glBindFramebuffer( GL_FRAMEBUFFER, 0 )

# Setup storage for internal depth/stencil buffers and bind to correct framebuffer
def setupRenderBufferStorage( renderbuffer, renderTarget ):

    glBindRenderbuffer( GL_RENDERBUFFER, renderbuffer )

    if renderTarget.depthBuffer and not renderTarget.stencilBuffer:

        glRenderbufferStorage( GL_RENDERBUFFER, GL_DEPTH_COMPONENT16, renderTarget.width, renderTarget.height )
        glFramebufferRenderbuffer( GL_FRAMEUBFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, renderbuffer )

    elif renderTarget.depthBuffer and renderTarget.stencilBuffer:

        glRenderbufferStorage( GL_RENDERBUFFER, GL_DEPTH_STENCIL, renderTarget.width, renderTarget.height )
        glFramebufferRenderbuffer( GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, renderbuffer )

    else:

        # FIXME: We don't support !depth !stencil
        glRenderbufferStorage( GL_RENDERBUFFER, GL_RGBA4, renderTarget.width, renderTarget.height )

    glBindRenderbuffer( GL_RENDERBUFFER, 0 )

# Setup resources for a Depth Texture for a FBO (needs an extension)
def setupDepthTexture( framebuffer, renderTarget ):

    isCUbe = renderTarget and hasattr( renderTarget, "isWebGLRenderTargetCube" )
    if isCube: raise ValueError( "Depth Texture with cube render targets is not supported" )

    glBindFramebuffer( GL_FRAMEBUFFER, framebuffer )

    if not ( renderTarget.depthTexture and hasattr( renderTarget.depthTexture, "isDepthTexture" ) ):

        raise ValueError( "renderTarget.depthTexture must be an instance of THREE.DepthTexture" )

    # upload an empty depth texture with framebuffer size
    if not properties.get( renderTarget.depthTexture )._openglTexture or \
        renderTarget.depthTexture.image.width != renderTarget.width or \
        renderTarget.depthTexture.image.height != renderTarget.height:

        renderTarget.depthTexture.image.width = renderTarget.width # TODO, pygame.Surface cannot do this
        renderTarget.depthTexture.image.height = renderTarget.height
        renderTarget.depthTexture.needsUpdate = True

    setTexture2D( renderTarget.depthTexture, 0 )

    openglDepthTexture = properties.get( renderTarget.depthTexture )._openglTexture

    if renderTarget.depthTexture.format == DepthFormat:

        glFramebufferTexture2D( GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, openglDepthTexture, 0 )

    elif renderTarget.depthTexture.format == DepthStencilFormat:

        glFramebufferTexture2D( GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_TEXTURE_2D, openglDepthTexture, 0 )
    
    else:

        raise ValueError( "Unknown depthTexture format" )

# Setup GL resources for a non-texture depth buffer
def setupDepthRenderbuffer( renderTarget ):

    renderTargetProperties = properties.get( renderTarget )

    isCube = hasattr( renderTarget, "isWebGLRenderTargetCube" )

    if renderTarget.depthTexture:

        if isCube: raise ValueError( "target.depthTexture not supported in Cube render targets" )

        setupDepthTexture( renderTargetProperties._openglFramebuffer, renderTarget )

    else:

        if isCube:

            renderTargetProperties._openglDepthbuffer = []

            for i in xrange( 6 ):

                glBindFramebuffer( GL_FRAMEBUFFER, renderTargetProperties._openglFramebuffer[ i ] )
                renderTargetProperties._openglDepthbuffer[ i ] = glGenRenderbuffers( 1 )
                setupRenderBufferStorage( renderTargetProperties._openglDepthbuffer[ i ], renderTarget )

        else:

            glBindFramebuffer( GL_FRAMEBUFFER, renderTargetProperties._openglFramebuffer )
            renderTargetProperties._openglDepthbuffer = glGenRenderbuffers( 1 )
            setupRenderBufferStorage( renderTargetProperties._openglDepthbuffer, renderTarget )

    glBindFramebuffer( GL_FRAMEBUFFER, 0 )

# Setup GL resources for the render target
def setupRenderTarget( renderTarget ):

    from ..OpenGLRenderer import _infoMemory as infoMemory

    renderTargetProperties = properties.get( renderTarget )
    textureProperties = properties.get( renderTarget.texture )

    renderTarget.addEventListener( "dispose", onRenderTargetDispose )

    textureProperties._openglTexture = glGenTextures( 1 )

    infoMemory.textures += 1

    isCube = hasattr( renderTarget, "isOpenGLRenderTargetCube" )
    isTargetPowerOfTwo = isRenderTargetPowerOfTwo( renderTarget )
    isTargetPowerOfTwo = False

    # Setup framebuffer

    if isCube:

        renderTargetProperties._openglFramebuffer = []

        for i in xrange( 6 ):

            renderTargetProperties._openglFramebuffer.append( glGenFramebuffers( 1 ) )

    else:

        renderTargetProperties._openglFramebuffer = glGenFramebuffers( 1 )

    # Setup color buffer

    if isCube:

        state.bindTexture( GL_TEXTUE_CUBE_MAP, textureProperties._openglTexture )
        setTextureParameters( GL_TEXTURE_CUBE_MAP, renderTarget.texture, isTargetPowerOfTwo )

        for i in xrange( 6 ):

            setupFrameBufferTexture( renderTargetProperties._openglFramebuffer[ i ], renderTarget, GL_COLOR_ATTACHMENT0, GL_TEXTURE_CUBE_MAP_POSITIVE_X + i )
        
        if textureNeedsGenerateMipmaps( renderTarget.texture, isTargetPowerOfTwo ): glGenerateMipmap( GL_TEXTURE_CUBE_MAP )
        state.bindTexture( GL_TEXTURE_CUBE_MAP, 0 )
    
    else:

        state.bindTexture( GL_TEXTURE_2D, textureProperties._openglTexture )
        setTextureParameters( GL_TEXTURE_2D, renderTarget.texture, isTargetPowerOfTwo )
        setupFrameBufferTexture( renderTargetProperties._openglFramebuffer, renderTarget, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D )

        if textureNeedsGenerateMipmaps( renderTarget.texture, isTargetPowerOfTwo ): glGenerateMipmap( GL_TEXTURE_2D )
        state.bindTexture( GL_TEXTURE_2D, 0 )

    if renderTarget.depthBuffer:

        setupDepthRenderbuffer( renderTarget )

def updateRenderTargetMipmap( renderTarget ):

    texture = renderTarget.texture
    # TODO isTargetPowerOfTwo = isPowerOfTwo( renderTarget )
    isTargetPowerOfTwo = False

    if textureNeedsGenerateMipmaps( texture, isTargetPowerOfTwo ):

        target = GL_TEXTURE_CUBE_MAP if hasattr( renderTarget, "isOpenGLRenderTargetCube" ) else GL_TEXTURE_2D
        openglTexture = properties.get( texture )._openglTexture

        state.bindTexture( target, openglTexture )
        glGenerateMipmap( target )
        state.bindTexture( target, 0 )