import re

import pygame

import loadingManager
import imageLoader
from ..constants import RGBAFormat, RGBFormat
from ..textures import texture

class TextureLoader( object ):

    cache = {}

    def __init__( self, manager = None ):

        self.manager = manager or loadingManager.DefaultLoadingManager
        self.path = None
    
    def load( self, url, onLoad = None, onProgress = None, onError = None ):

        if self.path: url = self.path + url

        cached = TextureLoader.cache.get( url )

        if cached:

            self.manager.itemStart( url )
            if onLoad: onLoad( cached )
            self.manager.itemEnd( url )

            return cached

        loader = imageLoader.ImageLoader( self.manager )
        loader.setPath( self.path )

        tex = texture.Texture()

        def onLoadInternal( image, *args ):
            
            # need to flip it vertically for OpenGL
            tex.image = pygame.transform.flip( image, False, True )
            bytesize = tex.image.get_bytesize()

            if bytesize == 1: # indexed

                tex.image = tex.image.convert( ( 0xff, 0xff00, 0xff0000, 0xff000000 ) )
                bytesize = tex.image.get_bytesize()

            tex.format = RGBAFormat if bytesize == 4 else RGBFormat
            tex.needsUpdate = True

            if onLoad: onLoad( tex )

        loader.load( url, onLoadInternal, onProgress, onError )

        TextureLoader.cache[ url ] = tex

        return tex

    def setPath( self, value ):

        self.path = value