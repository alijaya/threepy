from ..objects import lineSegments
from ..constants import VertexColors
from ..materials import lineBasicMaterial
from ..core import bufferAttribute
from ..core import bufferGeometry
"""
 * @author sroucheray / "http":#sroucheray.org/
 * @author mrdoob / "http":#mrdoob.com/
 """

class AxisHelper( lineSegments.LineSegments ):

    def __init__( self, size = 1 ):

        vertices = [
            0, 0, 0,  size, 0, 0,
            0, 0, 0,  0, size, 0,
            0, 0, 0,  0, 0, size
        ]

        colors = [
            1, 0, 0,  1, 0.6, 0,
            0, 1, 0,  0.6, 1, 0,
            0, 0, 1,  0, 0.6, 1
        ]

        geometry = bufferGeometry.BufferGeometry()
        geometry.addAttribute( "position", bufferAttribute.Float32BufferAttribute( vertices, 3 ) )
        geometry.addAttribute( "color", bufferAttribute.Float32BufferAttribute( colors, 3 ) )

        material = lineBasicMaterial.LineBasicMaterial( vertexColors = VertexColors )
        super( AxisHelper, self ).__init__( geometry, material )
