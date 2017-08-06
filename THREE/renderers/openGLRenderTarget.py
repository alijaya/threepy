from ..core import eventDispatcher
from ..textures import texture
from ..constants import LinearFilter
from ..math import vector4
from ..math import _Math
from ..utils import Expando

"""
 * @author szimek / "https":#github.com/szimek/
 * @author alteredq / "http":#alteredqualia.com/
 * @author Marius Kintel / "https":#github.com/kintel
 """

"""
 In options, we can "specify":
 * texture.Texture parameters for an auto-generated target texture
 * "depthBuffer/stencilBuffer": Booleans to indicate if we should generate these buffers
"""

class OpenGLRenderTarget( eventDispatcher.EventDispatcher ):

    def __init__( self, width, height, **kwargs ):

        self.isOpenGLRenderTarget = True

        self.uuid = _Math.generateUUID()

        self.width = width
        self.height = height

        self.scissor = vector4.Vector4( 0, 0, width, height )
        self.scissorTest = False

        self.viewport = vector4.Vector4( 0, 0, width, height )

        if "minFilter" not in kwargs: kwargs[ "minFilter" ] = LinearFilter

        self.texture = texture.Texture( None, None, **kwargs )

        self.depthBuffer = kwargs.get( "depthBuffer", True )
        self.stencilBuffer = kwargs.get( "stencilBuffer", True )
        self.depthTexture = kwargs.get( "depthTexture", None )

    def setSize( self, width, height ):

        if self.width != width or self.height != height :

            self.width = width
            self.height = height

            self.dispose()

        self.viewport.set( 0, 0, width, height )
        self.scissor.set( 0, 0, width, height )

    def clone( self ):

        return OpenGLRenderTarget.copy( self )

    def copy( self, source ):

        self.width = source.width
        self.height = source.height

        self.viewport.copy( source.viewport )

        self.texture = source.texture.clone()

        self.depthBuffer = source.depthBuffer
        self.stencilBuffer = source.stencilBuffer
        self.depthTexture = source.depthTexture

        return self

    def dispose( self ):

        self.dispatchEvent( Expando( type = "dispose" ) )
