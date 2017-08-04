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

# TODO _isWebGL2

def isPowerOfTwo( image ):

    return _Math.isPowerOfTwo( image.get_width() ) and _Math.isPowerOfTwo( image.get_height() )

def textureNeedsGenerateMipmaps( texture, isPowerOfTwo ):

    return texture.generateMipmaps and isPowerOfTwo and \
        texture.minFilter != NearestFilter and texture.minFilter != LinearFilter

# Fallback filters for non-power-of-2 textures

def filterFallback( f ):

    if f == NearestFilter or f == NearestMipMapNearestFilter or f == NearestMipMapLinearFilter:

        return GL_NEAREST

    return GL_LINEAR

# def onTextureDispose( event ):

#     texture = event.target

#     texture.removeEventListener( "dispose", onTextureDispose )

#     deallocateTexture( texture )

#     infoMemory.textures -= 1

# def onRenderTargetDispose( event ):

#     texture = event.target

#     texture.removeEventListener( "dispose", onRenderTarget )

#     deallocateRenderTarget( renderTarget )

#     infoMemory.textures -= 1

# TODO deallocate

def setTexture2D( texture, slot ):

    textureProperties = properties.get( texture )

    if texture.version > 0 and textureProperties.__version != texture.version:

        image = texture.image

        if not image:

            logging.warning( "THREE.WebGLRenderer: Texture marked for update but image is undefined %s", texture )

        else:

            uploadTexture( textureProperties, texture, slot )
            return

    state.activeTexture( GL_TEXTURE0 + slot )
    state.bindTexture( GL_TEXTURE_2D, textureProperties.__openglTexture )

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
    
    # TODO extension

def uploadTexture( textureProperties, texture, slot ):

    from ..OpenGLRenderer import _infoMemory as infoMemory

    if not textureProperties.__openglInit:

        textureProperties.__openglInit = True

        # texture.addEventListener( "dispose", onTextureDispose )

        textureProperties.__openglTexture = glGenTextures( 1 )

        infoMemory.textures += 1
    
    state.activeTexture( GL_TEXTURE0 + slot )
    state.bindTexture( GL_TEXTURE_2D, textureProperties.__openglTexture )

    # glPixelStorei( GL_UNPACK_FLIP_Y_WEBGL, texture.flipY )
    # glPixelStorei( GL_UNPACK_PREMULTIPLY_ALPHA_WEBGL, texture.premultiplyAlpha )
    # glPixelStorei( GL_UNPACK_ALIGNMENT, texture.unpackAlignment )

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

    textureProperties.__version = texture.version

    if texture.onUpdate: texture.onUpdate( texture )