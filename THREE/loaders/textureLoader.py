import re

import loadingManager
import imageLoader
from ..constants import RGBAFormat, RGBFormat
from ..textures import texture

class TextureLoader( object ):

    def __init__( self, manager = None ):

        self.manager = manager or loadingManager.DefaultLoadingManager
        self.path = None
    
    def load( self, url, onLoad = None, onProgress = None, onError = None ):

        loader = imageLoader.ImageLoader( self.manager )
        loader.setPath( self.path )

        tex = texture.Texture()

        def onLoadInternal( *args ):

            isJPEG = bool( re.search( "\.(jpg|jpeg)$", url ) )

            tex.format = RGBFormat if isJPEG else RGBAFormat

            if onLoad: onLoad( tex )

        tex.image = loader.load( url, onLoadInternal, onProgress, onError )

        return texture

    def setPath( self, value ):

        self.path = value