from ..math import color
from ..utils import Expando

"""
 * @author mrdoob / "http":#mrdoob.com/
 * @author alteredq / "http":#alteredqualia.com/
 """

class Fog( object ):

    def __init__( self, col, near = 1, far = 1000 ):

        self.isFog = True

        self.name = ""

        self.color = color.Color( col )

        self.near = near
        self.far = far

    def clone( self ):

        return Fog( self.color.getHex(), self.near, self.far )

    def toJSON( self, meta ):

        return Expando(
            type = "Fog",
            color = self.color.getHex(),
            near = self.near,
            far = self.far
        )
