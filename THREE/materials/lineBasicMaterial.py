import material
from ..math import color

"""
 * @author mrdoob / "http":#mrdoob.com/
 * @author alteredq / "http":#alteredqualia.com/
 *
 * parameters = {
 *  "color": <hex>,
 *  "opacity": <float>,
 *
 *  "linewidth": <float>,
 *  "linecap": "round",
 *  "linejoin": "round"
 * """

class LineBasicMaterial( material.Material ):

    def __init__( self, **parameters ):
        
        super( LineBasicMaterial, self ).__init__()

        self.isLineBasicMaterial = True

        self.type = "LineBasicMaterial"

        self.color = color.Color( 0xffffff )

        self.linewidth = 1
        self.linecap = "round"
        self.linejoin = "round"

        self.lights = False

        self.setValues( **parameters )

    def copy( self, source ):

        super( LineBasicMaterial, self ).copy( source )

        self.color.copy( source.color )

        self.linewidth = source.linewidth
        self.linecap = source.linecap
        self.linejoin = source.linejoin

        return self
