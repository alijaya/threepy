from ..math import color
from ..utils import Expando

"""
 * @author mrdoob / "http":#mrdoob.com/
 * @author alteredq / "http":#alteredqualia.com/
 """

class FogExp2( object ):

    def __init__( self, col, density = 0.00025 ):

        self.isFogExp2 = True

        self.name = ""

        self.color = color.Color( col )
        self.density = density

    def clone( self ):

        return FogExp2( self.color.getHex(), self.density )

    def toJSON( self, meta ):

        return Expando(
            type = "FogExp2",
            color = self.color.getHex(),
            density = self.density
        )
