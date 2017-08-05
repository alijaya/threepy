import material
from ..math import color

"""
 * @author mrdoob / "http":#mrdoob.com/
 * @author alteredq / "http":#alteredqualia.com/
 *
 * parameters = {
 *  "color": <hex>,
 *  "opacity": <float>,
 *  "map": THREE.Texture( <Image> ),
 *
 *  "size": <float>,
 *  "sizeAttenuation": <bool>
 * """

class PointsMaterial( material.Material ):

    def __init__( self, **parameters ):

        super( PointsMaterial, self ).__init__()

        self.isPointsMaterial = True

        self.type = "PointsMaterial"

        self.color = color.Color( 0xffffff )

        self.map = None

        self.size = 1
        self.sizeAttenuation = True

        self.lights = False

        self.setValues( **parameters )

    def copy( self, source ):

        super( PointsMaterial, self ).copy( source )

        self.color.copy( source.color )

        self.map = source.map

        self.size = source.size
        self.sizeAttenuation = source.sizeAttenuation

        return self
