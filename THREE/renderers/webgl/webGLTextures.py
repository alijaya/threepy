from __future__ import division

import logging

from OpenGL import GL

from ...constants import LinearFilter, NearestFilter, RGBFormat, RGBAFormat, DepthFormat, DepthStencilFormat, UnsignedShortType, UnsignedIntType, UnsignedInt248Type, FloatType, HalfFloatType, ClampToEdgeWrapping, NearestMipMapLinearFilter, NearestMipMapNearestFilter
from ...math import _Math
"""
 * @author mrdoob / "http":#mrdoob.com/
 """

class WebGLTextures( object ):

    def __init__( self, extensions, state, properties, capabilities, utils, infoMemory ):

        self.extensions = extensions
        self.state = state
        self.properties = properties
        self.capabilities = capabilities
        self.utils = utils
        self.infoMemory = infoMemory
        # _isWebGL2 = ( typeof WebGL2RenderingContext != "None" and _gl instanceof WebGL2RenderingContext )

    #

    def clampToMaxSize( self, image, maxSize ):

        # if image.width > maxSize or image.height > maxSize :

        #     # "Warning": Scaling through the canvas will only work with images that use
        #     # premultiplied alpha.

        #     scale = maxSize / max( image.width, image.height )

        #     canvas = document.createElementNS( "http://www.w3.org/1999/xhtml", "canvas" )
        #     canvas.width = math.floor( image.width * scale )
        #     canvas.height = math.floor( image.height * scale )

        #     context = canvas.getContext( "2d" )
        #     context.drawImage( image, 0, 0, image.width, image.height, 0, 0, canvas.width, canvas.height )

        #     logging.warning( "THREE.WebGLRenderer: image is too big (%sx%s). Resized to %sx%s %s" % ( image.width, image.height, canvas.width, canvas.height, image ) )

        #     return canvas

        return image

    def isPowerOfTwo( self, image ):

        return _Math.isPowerOfTwo( image.width ) and _Math.isPowerOfTwo( image.height )

    def makePowerOfTwo( self, image ):

        # if image instanceof HTMLImageElement or image instanceof HTMLCanvasElement :

        #     canvas = document.createElementNS( "http://www.w3.org/1999/xhtml", "canvas" )
        #     canvas.width = _Math.nearestPowerOfTwo( image.width )
        #     canvas.height = _Math.nearestPowerOfTwo( image.height )

        #     context = canvas.getContext( "2d" )
        #     context.drawImage( image, 0, 0, canvas.width, canvas.height )

        #     logging.warning( "THREE.WebGLRenderer: image is not power of two (%sx%s). Resized to %sx%s %s" % ( image.width, image.height, canvas.width, canvas.height, image ) )

        #     return canvas

        return image

    def textureNeedsPowerOfTwo( self, texture ):

        return  ( texture.wrapS != ClampToEdgeWrapping or texture.wrapT != ClampToEdgeWrapping ) or \
                ( texture.minFilter != NearestFilter and texture.minFilter != LinearFilter )

    def textureNeedsGenerateMipmaps( self, texture, isPowerOfTwo ):

        return  texture.generateMipmaps and isPowerOfTwo and \
                texture.minFilter != NearestFilter and texture.minFilter != LinearFilter

    # Fallback filters for non-power-of-2 textures

    def filterFallback( self, f ):

        if f == NearestFilter or f == NearestMipMapNearestFilter or f == NearestMipMapLinearFilter :

            return GL.GL_NEAREST

        return GL.GL_LINEAR

    #

    def onTextureDispose( self, event ):

        texture = event.target

        texture.removeEventListener( "dispose", onTextureDispose )

        deallocateTexture( texture )

        self.infoMemory.textures -= 1

    def onRenderTargetDispose( self, event ):

        renderTarget = event.target

        renderTarget.removeEventListener( "dispose", onRenderTargetDispose )

        deallocateRenderTarget( renderTarget )

        self.infoMemory.textures -= 1

    #

    def deallocateTexture( self, texture ):

        textureProperties = self.properties.get( texture )

        if texture.image and textureProperties.__image__webglTextureCube :

            # cube texture

            GL.glDeleteTexture( textureProperties.__image__webglTextureCube )

        else:

            # 2D texture

            if textureProperties.__webglInit is None : return

            GL.glDeleteTexture( textureProperties.__webglTexture )

        # remove all webgl properties
        self.properties.remove( texture )

    def deallocateRenderTarget( self, renderTarget ):

        renderTargetProperties = self.properties.get( renderTarget )
        textureProperties = self.properties.get( renderTarget.texture )

        if not renderTarget : return

        if textureProperties.__webglTexture is not None :

            GL.glDeleteTexture( textureProperties.__webglTexture )

        if renderTarget.depthTexture :

            renderTarget.depthTexture.dispose()

        if hasattr( renderTarget, "isWebGLRenderTargetCube" ) :

            for i in range( 6 ) :

                GL.glDeleteFramebuffer( renderTargetProperties.__webglFramebuffer[ i ] )
                if renderTargetProperties.__webglDepthbuffer : GL.glDeleteRenderbuffer( renderTargetProperties.__webglDepthbuffer[ i ] )

        else:

            GL.glDeleteFramebuffer( renderTargetProperties.__webglFramebuffer )
            if renderTargetProperties.__webglDepthbuffer : GL.glDeleteRenderbuffer( renderTargetProperties.__webglDepthbuffer )

        self.properties.remove( renderTarget.texture )
        self.properties.remove( renderTarget )

    #

    def setTexture2D( self, texture, slot ):

        textureProperties = self.properties.get( texture )

        if texture.version > 0 and textureProperties.__version != texture.version :

            image = texture.image

            if image is None :

                logging.warning( "THREE.WebGLRenderer: Texture marked for update but image is None %s" % texture )

            elif image.complete == False :

                logging.warning( "THREE.WebGLRenderer: Texture marked for update but image is incomplete %s" % texture )

            else:

                uploadTexture( textureProperties, texture, slot )
                return

        state.activeTexture( GL.GL_TEXTURE0 + slot )
        state.bindTexture( GL.GL_TEXTURE_2D, textureProperties.__webglTexture )

    def setTextureCube( self, texture, slot ):

        textureProperties = self.properties.get( texture )

        if len( texture.image ) == 6 :

            if texture.version > 0 and textureProperties.__version != texture.version :

                if not textureProperties.__image__webglTextureCube :

                    texture.addEventListener( "dispose", onTextureDispose )

                    textureProperties.__image__webglTextureCube = GL.glCreateTexture()

                    self.infoMemory.textures += 1

                state.activeTexture( GL.GL_TEXTURE0 + slot )
                state.bindTexture( GL.GL_TEXTURE_CUBE_MAP, textureProperties.__image__webglTextureCube )

                GL.glPixelStorei( GL.GL_UNPACK_FLIP_Y_WEBGL, texture.flipY )

                isCompressed = ( texture and hasattr( texture, "isCompressedTexture" ) )
                isDataTexture = ( texture.image[ 0 ] and hasattr( texture.image[ 0 ], "isDataTexture" ) )

                cubeImage = []

                for i in range( 6 ):

                    if not isCompressed and not isDataTexture :

                        cubeImage[ i ] = clampToMaxSize( texture.image[ i ], self.capabilities.maxCubemapSize )

                    else:

                        cubeImage[ i ] = texture.image[ i ].image if isDataTexture else texture.image[ i ]

                image = cubeImage[ 0 ],
                isPowerOfTwoImage = isPowerOfTwo( image ),
                glFormat = utils.convert( texture.format ),
                glType = utils.convert( texture.type )

                setTextureParameters( GL.GL_TEXTURE_CUBE_MAP, texture, isPowerOfTwoImage )

                for i in range( 6 ):

                    if not isCompressed :

                        if isDataTexture :

                            state.texImage2D( GL.GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, glFormat, cubeImage[ i ].width, cubeImage[ i ].height, 0, glFormat, glType, cubeImage[ i ].data )

                        else:

                            state.texImage2D( GL.GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, glFormat, glFormat, glType, cubeImage[ i ] )

                    else:

                        mipmap, mipmaps = cubeImage[ i ].mipmaps

                        for j in range( len( mipmaps ) ) :

                            mipmap = mipmaps[ j ]

                            if texture.format != RGBAFormat and texture.format != RGBFormat :

                                if state.getCompressedTextureFormats().indexOf( glFormat ) > - 1 :

                                    state.compressedTexImage2D( GL.GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, j, glFormat, mipmap.width, mipmap.height, 0, mipmap.data )

                                else:

                                    logging.warning( "THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .setTextureCube()" )

                            else:

                                state.texImage2D( GL.GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, j, glFormat, mipmap.width, mipmap.height, 0, glFormat, glType, mipmap.data )

                if textureNeedsGenerateMipmaps( texture, isPowerOfTwoImage ) :

                    GL.glGenerateMipmap( GL.GL_TEXTURE_CUBE_MAP )

                textureProperties.__version = texture.version

                if texture.onUpdate : texture.onUpdate( texture )

            else:

                state.activeTexture( GL.GL_TEXTURE0 + slot )
                state.bindTexture( GL.GL_TEXTURE_CUBE_MAP, textureProperties.__image__webglTextureCube )

    def setTextureCubeDynamic( self, texture, slot ):

        state.activeTexture( GL.GL_TEXTURE0 + slot )
        state.bindTexture( GL.GL_TEXTURE_CUBE_MAP, self.properties.get( texture ).__webglTexture )

    def setTextureParameters( self, textureType, texture, isPowerOfTwoImage ):

        extension

        if isPowerOfTwoImage :

            GL.glTexParameteri( textureType, GL.GL_TEXTURE_WRAP_S, utils.convert( texture.wrapS ) )
            GL.glTexParameteri( textureType, GL.GL_TEXTURE_WRAP_T, utils.convert( texture.wrapT ) )

            GL.glTexParameteri( textureType, GL.GL_TEXTURE_MAG_FILTER, utils.convert( texture.magFilter ) )
            GL.glTexParameteri( textureType, GL.GL_TEXTURE_MIN_FILTER, utils.convert( texture.minFilter ) )

        else:

            GL.glTexParameteri( textureType, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE )
            GL.glTexParameteri( textureType, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE )

            if texture.wrapS != ClampToEdgeWrapping or texture.wrapT != ClampToEdgeWrapping :

                logging.warning( "THREE.WebGLRenderer: Texture is not power of two. Texture.wrapS and Texture.wrapT should be set to THREE.ClampToEdgeWrapping. %s" % texture )

            GL.glTexParameteri( textureType, GL.GL_TEXTURE_MAG_FILTER, filterFallback( texture.magFilter ) )
            GL.glTexParameteri( textureType, GL.GL_TEXTURE_MIN_FILTER, filterFallback( texture.minFilter ) )

            if texture.minFilter != NearestFilter and texture.minFilter != LinearFilter :

                logging.warning( "THREE.WebGLRenderer: Texture is not power of two. Texture.minFilter should be set to THREE.NearestFilter or THREE.LinearFilter. %s" % texture )

        extension = self.extensions.get( "EXT_texture_filter_anisotropic" )

        if extension :

            if texture.type == FloatType and self.extensions.get( "OES_texture_float_linear" ) is None : return
            if texture.type == HalfFloatType and self.extensions.get( "OES_texture_half_float_linear" ) is None : return

            if texture.anisotropy > 1 or self.properties.get( texture ).__currentAnisotropy :

                GL.glTexParameterf( textureType, extension.TEXTURE_MAX_ANISOTROPY_EXT, min( texture.anisotropy, self.capabilities.getMaxAnisotropy() ) )
                self.properties.get( texture ).__currentAnisotropy = texture.anisotropy

    def uploadTexture( self, textureProperties, texture, slot ):

        if textureProperties.__webglInit is None :

            textureProperties.__webglInit = True

            texture.addEventListener( "dispose", onTextureDispose )

            textureProperties.__webglTexture = GL.glCreateTexture()

            self.infoMemory.textures += 1

        self.state.activeTexture( GL.GL_TEXTURE0 + slot )
        self.state.bindTexture( GL.GL_TEXTURE_2D, textureProperties.__webglTexture )

        GL.glPixelStorei( GL.GL_UNPACK_FLIP_Y_WEBGL, texture.flipY )
        GL.glPixelStorei( GL.GL_UNPACK_PREMULTIPLY_ALPHA_WEBGL, texture.premultiplyAlpha )
        GL.glPixelStorei( GL.GL_UNPACK_ALIGNMENT, texture.unpackAlignment )

        image = clampToMaxSize( texture.image, self.capabilities.maxTextureSize )

        if textureNeedsPowerOfTwo( texture ) and isPowerOfTwo( image ) == False :

            image = makePowerOfTwo( image )

        isPowerOfTwoImage = isPowerOfTwo( image ),
        glFormat = self.utils.convert( texture.format ),
        glType = self.utils.convert( texture.type )

        setTextureParameters( GL.GL_TEXTURE_2D, texture, isPowerOfTwoImage )

        mipmap, mipmaps = texture.mipmaps

        if hasattr( texture, "isDepthTexture" ) :

            # populate depth texture with dummy data

            internalFormat = GL.GL_DEPTH_COMPONENT

            if texture.type == FloatType :

                if not_isWebGL2 : raise ValueError("Float Depth Texture only supported in WebGL2.0")
                internalFormat = GL.GL_DEPTH_COMPONENT32F

            elif _isWebGL2 :

                # WebGL 2.0 requires signed internalformat for glTexImage2D
                internalFormat = GL.GL_DEPTH_COMPONENT16

            if texture.format == DepthFormat and internalFormat == GL.GL_DEPTH_COMPONENT :

                # The error INVALID_OPERATION is generated by texImage2D if format and internalformat are
                # DEPTH_COMPONENT and type is not UNSIGNED_SHORT or UNSIGNED_INT
                # "(https":#www.khronos.org/registry/webgl/extensions/WEBGL_depth_texture/)
                if texture.type != UnsignedShortType and texture.type != UnsignedIntType :

                    logging.warning( "THREE.WebGLRenderer: Use UnsignedShortType or UnsignedIntType for DepthFormat DepthTexture." )

                    texture.type = UnsignedShortType
                    glType = self.utils.convert( texture.type )

            # Depth stencil textures need the DEPTH_STENCIL internal format
            # "(https":#www.khronos.org/registry/webgl/extensions/WEBGL_depth_texture/)
            if texture.format == DepthStencilFormat :

                internalFormat = GL.GL_DEPTH_STENCIL

                # The error INVALID_OPERATION is generated by texImage2D if format and internalformat are
                # DEPTH_STENCIL and type is not UNSIGNED_INT_24_8_WEBGL.
                # "(https":#www.khronos.org/registry/webgl/extensions/WEBGL_depth_texture/)
                if texture.type != UnsignedInt248Type :

                    logging.warning( "THREE.WebGLRenderer: Use UnsignedInt248Type for DepthStencilFormat DepthTexture." )

                    texture.type = UnsignedInt248Type
                    glType = self.utils.convert( texture.type )

            self.state.texImage2D( GL.GL_TEXTURE_2D, 0, internalFormat, image.width, image.height, 0, glFormat, glType, None )

        elif hasattr( texture, "isDataTexture" ) :

            # use manually created mipmaps if available
            # if there are no manual mipmaps
            # set 0 level mipmap and then use GL to generate other mipmap levels

            if len( mipmaps ) > 0 and isPowerOfTwoImage :

                for i in range( len( mipmaps ) ) :

                    mipmap = mipmaps[ i ]
                    self.state.texImage2D( GL.GL_TEXTURE_2D, i, glFormat, mipmap.width, mipmap.height, 0, glFormat, glType, mipmap.data )

                texture.generateMipmaps = False

            else:

                self.state.texImage2D( GL.GL_TEXTURE_2D, 0, glFormat, image.width, image.height, 0, glFormat, glType, image.data )

        elif hasattr( texture, "isCompressedTexture" ) :

            for i in range( len( mipmaps ) ) :

                mipmap = mipmaps[ i ]

                if texture.format != RGBAFormat and texture.format != RGBFormat :

                    if self.state.getCompressedTextureFormats().indexOf( glFormat ) > - 1 :

                        self.state.compressedTexImage2D( GL.GL_TEXTURE_2D, i, glFormat, mipmap.width, mipmap.height, 0, mipmap.data )

                    else:

                        logging.warning( "THREE.WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()" )

                else:

                    self.state.texImage2D( GL.GL_TEXTURE_2D, i, glFormat, mipmap.width, mipmap.height, 0, glFormat, glType, mipmap.data )

        else:

            # regular Texture (image, video, canvas)

            # use manually created mipmaps if available
            # if there are no manual mipmaps
            # set 0 level mipmap and then use GL to generate other mipmap levels

            if len( mipmaps ) > 0 and isPowerOfTwoImage :

                for i in range( len( mipmaps ) ) :

                    mipmap = mipmaps[ i ]
                    self.state.texImage2D( GL.GL_TEXTURE_2D, i, glFormat, glFormat, glType, mipmap )

                texture.generateMipmaps = False

            else:

                self.state.texImage2D( GL.GL_TEXTURE_2D, 0, glFormat, glFormat, glType, image )

        if textureNeedsGenerateMipmaps( texture, isPowerOfTwoImage ) : GL.glGenerateMipmap( GL.GL_TEXTURE_2D )

        textureProperties.__version = texture.version

        if texture.onUpdate : texture.onUpdate( texture )

    # Render targets

    # Setup storage for target texture and bind it to correct framebuffer
    def setupFrameBufferTexture( self, framebuffer, renderTarget, attachment, textureTarget ):

        glFormat = self.utils.convert( renderTarget.texture.format )
        glType = self.utils.convert( renderTarget.texture.type )
        self.state.texImage2D( textureTarget, 0, glFormat, renderTarget.width, renderTarget.height, 0, glFormat, glType, None )
        GL.glBindFramebuffer( GL.GL_FRAMEBUFFER, framebuffer )
        GL.glFramebufferTexture2D( GL.GL_FRAMEBUFFER, attachment, textureTarget, self.properties.get( renderTarget.texture ).__webglTexture, 0 )
        GL.glBindFramebuffer( GL.GL_FRAMEBUFFER, None )

    # Setup storage for internal depth/stencil buffers and bind to correct framebuffer
    def setupRenderBufferStorage( self, renderbuffer, renderTarget ):

        GL.glBindRenderbuffer( GL.GL_RENDERBUFFER, renderbuffer )

        if renderTarget.depthBuffer and not renderTarget.stencilBuffer :

            GL.glRenderbufferStorage( GL.GL_RENDERBUFFER, GL.GL_DEPTH_COMPONENT16, renderTarget.width, renderTarget.height )
            GL.glFramebufferRenderbuffer( GL.GL_FRAMEBUFFER, GL.GL_DEPTH_ATTACHMENT, GL.GL_RENDERBUFFER, renderbuffer )

        elif renderTarget.depthBuffer and renderTarget.stencilBuffer :

            GL.glRenderbufferStorage( GL.GL_RENDERBUFFER, GL.GL_DEPTH_STENCIL, renderTarget.width, renderTarget.height )
            GL.glFramebufferRenderbuffer( GL.GL_FRAMEBUFFER, GL.GL_DEPTH_STENCIL_ATTACHMENT, GL.GL_RENDERBUFFER, renderbuffer )

        else:

            # "FIXME": We don"t support notdepth notstencil
            GL.glRenderbufferStorage( GL.GL_RENDERBUFFER, GL.GL_RGBA4, renderTarget.width, renderTarget.height )

        GL.glBindRenderbuffer( GL.GL_RENDERBUFFER, None )

    # Setup resources for a Depth Texture for a FBO (needs an extension)
    def setupDepthTexture( self, framebuffer, renderTarget ):

        isCube = ( renderTarget and hasattr( renderTarget, "isWebGLRenderTargetCube" ) )
        if isCube : raise ValueError( "Depth Texture with cube render targets is not supported" )

        GL.glBindFramebuffer( GL.GL_FRAMEBUFFER, framebuffer )

        if not( renderTarget.depthTexture and hasattr( renderTarget.depthTexture, "isDepthTexture" ) ) :

            raise ValueError( "renderTarget.depthTexture must be an instance of THREE.DepthTexture" )

        # upload an empty depth texture with framebuffer size
        if  notproperties.get( renderTarget.depthTexture ).__webglTexture or \
            renderTarget.depthTexture.image.width != renderTarget.width or \
            renderTarget.depthTexture.image.height != renderTarget.height :

            renderTarget.depthTexture.image.width = renderTarget.width
            renderTarget.depthTexture.image.height = renderTarget.height
            renderTarget.depthTexture.needsUpdate = True

        setTexture2D( renderTarget.depthTexture, 0 )

        webglDepthTexture = self.properties.get( renderTarget.depthTexture ).__webglTexture

        if renderTarget.depthTexture.format == DepthFormat :

            GL.glFramebufferTexture2D( GL.GL_FRAMEBUFFER, GL.GL_DEPTH_ATTACHMENT, GL.GL_TEXTURE_2D, webglDepthTexture, 0 )

        elif renderTarget.depthTexture.format == DepthStencilFormat :

            GL.glFramebufferTexture2D( GL.GL_FRAMEBUFFER, GL.GL_DEPTH_STENCIL_ATTACHMENT, GL.GL_TEXTURE_2D, webglDepthTexture, 0 )

        else:

            raise Error( "Unknown depthTexture format" )

    # Setup GL resources for a non-texture depth buffer
    def setupDepthRenderbuffer( self, renderTarget ):

        renderTargetProperties = self.properties.get( renderTarget )

        isCube = ( hasattr( renderTarget, "isWebGLRenderTargetCube" ) == True )

        if renderTarget.depthTexture :

            if isCube : raise ValueError( "target.depthTexture not supported in Cube render targets" )

            setupDepthTexture( renderTargetProperties.__webglFramebuffer, renderTarget )

        else:

            if isCube :

                renderTargetProperties.__webglDepthbuffer = []

                for i in range( 6 ):

                    GL.glBindFramebuffer( GL.GL_FRAMEBUFFER, renderTargetProperties.__webglFramebuffer[ i ] )
                    renderTargetProperties.__webglDepthbuffer[ i ] = GL.glCreateRenderbuffer()
                    setupRenderBufferStorage( renderTargetProperties.__webglDepthbuffer[ i ], renderTarget )

            else:

                GL.glBindFramebuffer( GL.GL_FRAMEBUFFER, renderTargetProperties.__webglFramebuffer )
                renderTargetProperties.__webglDepthbuffer = GL.glCreateRenderbuffer()
                setupRenderBufferStorage( renderTargetProperties.__webglDepthbuffer, renderTarget )

        GL.glBindFramebuffer( GL.GL_FRAMEBUFFER, None )

    # Set up GL resources for the render target
    def setupRenderTarget( self, renderTarget ):

        renderTargetProperties = self.properties.get( renderTarget )
        textureProperties = self.properties.get( renderTarget.texture )

        renderTarget.addEventListener( "dispose", onRenderTargetDispose )

        textureProperties.__webglTexture = GL.glCreateTexture()

        self.infoMemory.textures += 1

        isCube = ( hasattr( renderTarget, "isWebGLRenderTargetCube" ) == True )
        isTargetPowerOfTwo = isPowerOfTwo( renderTarget )

        # Setup framebuffer

        if isCube :

            renderTargetProperties.__webglFramebuffer = []

            for i in range( 6 ):

                renderTargetProperties.__webglFramebuffer[ i ] = GL.glCreateFramebuffer()

        else:

            renderTargetProperties.__webglFramebuffer = GL.glCreateFramebuffer()

        # Setup color buffer

        if isCube :

            self.state.bindTexture( GL.GL_TEXTURE_CUBE_MAP, textureProperties.__webglTexture )
            setTextureParameters( GL.GL_TEXTURE_CUBE_MAP, renderTarget.texture, isTargetPowerOfTwo )

            for i in range( 6 ):

                setupFrameBufferTexture( renderTargetProperties.__webglFramebuffer[ i ], renderTarget, GL.GL_COLOR_ATTACHMENT0, GL.GL_TEXTURE_CUBE_MAP_POSITIVE_X + i )

            if textureNeedsGenerateMipmaps( renderTarget.texture, isTargetPowerOfTwo ) : GL.glGenerateMipmap( GL.GL_TEXTURE_CUBE_MAP )
            self.state.bindTexture( GL.GL_TEXTURE_CUBE_MAP, None )

        else:

            self.state.bindTexture( GL.GL_TEXTURE_2D, textureProperties.__webglTexture )
            setTextureParameters( GL.GL_TEXTURE_2D, renderTarget.texture, isTargetPowerOfTwo )
            setupFrameBufferTexture( renderTargetProperties.__webglFramebuffer, renderTarget, GL.GL_COLOR_ATTACHMENT0, GL.GL_TEXTURE_2D )

            if textureNeedsGenerateMipmaps( renderTarget.texture, isTargetPowerOfTwo ) : GL.glGenerateMipmap( GL.GL_TEXTURE_2D )
            self.state.bindTexture( GL.GL_TEXTURE_2D, None )

        # Setup depth and stencil buffers

        if renderTarget.depthBuffer :

            setupDepthRenderbuffer( renderTarget )

    def updateRenderTargetMipmap( self, renderTarget ):

        texture = renderTarget.texture
        isTargetPowerOfTwo = isPowerOfTwo( renderTarget )

        if textureNeedsGenerateMipmaps( texture, isTargetPowerOfTwo ) :

            target = GL.GL_TEXTURE_CUBE_MAP if hasattr( renderTarget, "isWebGLRenderTargetCube" ) else GL.GL_TEXTURE_2D
            webglTexture = self.properties.get( texture ).__webglTexture

            self.state.bindTexture( target, webglTexture )
            GL.glGenerateMipmap( target )
            self.state.bindTexture( target, None )
