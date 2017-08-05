from __future__ import division
import math

from ..core import geometry
import polyhedronGeometry
from ..utils import Expando

"""
 * @author timothypratley / https://github.com/timothypratley
 * @author Mugen87 / https://github.com/Mugen87
 """

# OctahedronGeometry

class OctahedronGeometry( geometry.Geometry ):

    def __init__( self, radius = 1, detail = 0 ):

        super( OctahedronGeometry, self ).__init__()

        self.type = "OctahedronGeometry"

        self.parameters = Expando(
            radius = radius,
            detail = detail
        )

        self.fromBufferGeometry( OctahedronBufferGeometry( radius, detail ) )
        self.mergeVertices()

# OctahedronBufferGeometry

class OctahedronBufferGeometry( polyhedronGeometry.PolyhedronBufferGeometry ):

    def __init__( self, radius = 1, detail = 0 ):

        vertices = [
            1, 0, 0,   - 1, 0, 0,    0, 1, 0,    0, - 1, 0,    0, 0, 1,    0, 0, - 1
        ]

        indices = [
            0, 2, 4,    0, 4, 3,    0, 3, 5,    0, 5, 2,    1, 2, 5,    1, 5, 3,    1, 3, 4,    1, 4, 2
        ]

        super( OctahedronBufferGeometry, self ).__init__( vertices, indices, radius, detail )

        self.type = "OctahedronBufferGeometry"

        self.parameters = Expando(
            radius = radius,
            detail = detail
        )
