from ..core import eventDispatcher
from ..constants import UVMapping
from ..constants import MirroredRepeatWrapping, ClampToEdgeWrapping, RepeatWrapping, LinearEncoding, UnsignedByteType, RGBAFormat, LinearMipMapLinearFilter, LinearFilter
from ..math import _Math
from ..math import vector2
from ..utils import Expando

import math

"""
 * @author mrdoob / http://mrdoob.com/
 * @author alteredq / http://alteredqualia.com/
 * @author szimek / https://github.com/szimek/
 """

class Texture( eventDispatcher.EventDispatcher ):

    DEFAULT_IMAGE = None
    DEFAULT_MAPPING = UVMapping

    TextureId = 0

    @staticmethod
    def getTextureId():

        ret = Texture.TextureId
        Texture.TextureId += 1
        return ret

    def __init__( self, image = None, mapping = None, wrapS = ClampToEdgeWrapping, wrapT = ClampToEdgeWrapping, 
                    magFilter = LinearFilter, minFilter = LinearMipMapLinearFilter, format = RGBAFormat, 
                    type = UnsignedByteType, anisotropy = 1, encoding = LinearEncoding ):

        self.id = Texture.getTextureId()
        self.uuid = _Math.generateUUID()
        self.isTexture = True

        self.name = ""

        self.image = image or Texture.DEFAULT_IMAGE
        self.mipmaps = []

        self.mapping = mapping or Texture.DEFAULT_MAPPING

        self.wrapS = wrapS
        self.wrapT = wrapT

        self.magFilter = magFilter
        self.minFilter = minFilter

        self.anisotropy = anisotropy

        self.format = format
        self.type = type

        self.offset = vector2.Vector2( 0, 0 )
        self.repeat = vector2.Vector2( 1, 1 )

        self.generateMipmaps = True
        self.premultiplyAlpha = False
        self.flipY = True
        self.unpackAlignment = 4    # valid "values": 1, 2, 4, 8 (see "http":#www.khronos.org/opengles/sdk/docs/man/xhtml/glPixelStorei.xml)

        # Values of encoding != THREE.LinearEncoding only supported on map, envMap and emissiveMap.
        #
        # Also changing the encoding after already used by a Material will not automatically make the Material
        # update.  You need to explicitly call Material.needsUpdate to trigger it to recompile.
        self.encoding = encoding

        self.version = 0
        self.onUpdate = None

    @property
    def needsUpdate( self ):

        return None

    @needsUpdate.setter
    def needsUpdate( self, value ):

        if value == True: self.version += 1

    def clone( self ):

        return Texture().copy( self )

    def copy( self, source ):

        self.name = source.name

        self.image = source.image
        self.mipmaps = source.mipmaps[:]

        self.mapping = source.mapping

        self.wrapS = source.wrapS
        self.wrapT = source.wrapT

        self.magFilter = source.magFilter
        self.minFilter = source.minFilter

        self.anisotropy = source.anisotropy

        self.format = source.format
        self.type = source.type

        self.offset.copy( source.offset )
        self.repeat.copy( source.repeat )

        self.generateMipmaps = source.generateMipmaps
        self.premultiplyAlpha = source.premultiplyAlpha
        self.flipY = source.flipY
        self.unpackAlignment = source.unpackAlignment
        self.encoding = source.encoding

        return self

    def toJSON( self, meta ):

        if self.uuid in meta.textures:

            return meta.textures[ self.uuid ]

        output = Expando(
            metadata = Expando(
                version = 4.5,
                type = "Texture",
                generator = "Texture.toJSON"
            ),

            uuid = self.uuid,
            name = self.name,

            mapping = self.mapping,

            repeat = [ self.repeat.x, self.repeat.y ],
            offset = [ self.offset.x, self.offset.y ],
            wrap = [ self.wrapS, self.wrapT ],

            minFilter = self.minFilter,
            magFilter = self.magFilter,
            anisotropy = self.anisotropy,

            flipY = self.flipY
        )

        if self.image is not None :

            # TODO: Move to THREE.Image

            image = self.image

            if hasattr( image.uuid ) :

                image.uuid = _Math.generateUUID() # UGH

            if meta.images[ image.uuid ] is None :

                meta.images[ image.uuid ] = Expando(
                    uuid = image.uuid,
                    # url = getDataURL( image )
                )

            output.image = image.uuid

        meta.textures[ self.uuid ] = output

        return output

    def dispose( self ):

        self.dispatchEvent( Expando( type = "dispose" ) )

    def transformUv( self, uv ):

        if self.mapping != UVMapping : return

        uv.multiply( self.repeat )
        uv.add( self.offset )

        if uv.x < 0 or uv.x > 1 :

            if self.wrapS == "RepeatWrapping":

                uv.x = uv.x - math.floor( uv.x )

            elif self.wrapS == "ClampToEdgeWrapping":

                uv.x = 0 if uv.x < 0 else 1

            elif self.wrapS == "MirroredRepeatWrapping":

                if abs( math.floor( uv.x ) % 2 ) == 1 :

                    uv.x = math.ceil( uv.x ) - uv.x

                else:

                    uv.x = uv.x - math.floor( uv.x )

        if uv.y < 0 or uv.y > 1 :

            if self.wrapT == "RepeatWrapping":

                uv.y = uv.y - math.floor( uv.y )

            if self.wrapT == "ClampToEdgeWrapping":

                uv.y = 0 if uv.y < 0 else 1

            if self.wrapT == "MirroredRepeatWrapping":

                if abs( math.floor( uv.y ) % 2 ) == 1 :

                    uv.y = math.ceil( uv.y ) - uv.y

                else:

                    uv.y = uv.y - math.floor( uv.y )

        if self.flipY :

            uv.y = 1 - uv.y
