from ..core import object3D
from ..math import color

"""
 * @author mrdoob / "http":#mrdoob.com/
 * @author alteredq / "http":#alteredqualia.com/
 """

class Light( object3D.Object3D ):

    def __init__( self, col = 0xffffff, intensity = 1 ):

        super( Light, self ).__init__()

        self.isLight = True

        self.type = "Light"

        self.color = color.Color( col )
        self.intensity = intensity

        self.receiveShadow = None

    def copy( self, source ):

        super( Light, self ).copy( source )

        self.color.copy( source.color )
        self.intensity = source.intensity

        return self

    def toJSON( self, meta ):

        data = super( Light, self ).toJSON( meta )

        data.object.color = self.color.getHex()
        data.object.intensity = self.intensity

        if self.groundColor is not None : data.object.groundColor = self.groundColor.getHex()

        if self.distance is not None : data.object.distance = self.distance
        if self.angle is not None : data.object.angle = self.angle
        if self.decay is not None : data.object.decay = self.decay
        if self.penumbra is not None : data.object.penumbra = self.penumbra

        if self.shadow is not None : data.object.shadow = self.shadow.toJSON()

        return data
