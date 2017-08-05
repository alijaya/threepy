from __future__ import division
import math

from ..core import geometry
import polyhedronGeometry
from ..utils import Expando

"""
 * @author timothypratley / https:#github.com/timothypratley
 * @author Mugen87 / https:#github.com/Mugen87
 """

# TetrahedronGeometry

class TetrahedronGeometry( geometry.Geometry ):

    def __init__( self, radius = 1, detail = 0 ):

        super( TetrahedronGeometry, self ).__init__()

        self.type = "TetrahedronGeometry"

        self.parameters = Expando(
            radius = radius,
            detail = detail
        )

        self.fromBufferGeometry( TetrahedronBufferGeometry( radius, detail ) )
        self.mergeVertices()

# TetrahedronBufferGeometry

class TetrahedronBufferGeometry( polyhedronGeometry.PolyhedronBufferGeometry ):

    def __init__( self, radius = 1, detail = 0 ):

        vertices = [
            1,  1,  1,   - 1, - 1,  1,   - 1,  1, - 1,    1, - 1, - 1
        ]

        indices = [
            2,  1,  0,    0,  3,  2,    1,  3,  0,    2,  3,  1
        ]

        super( TetrahedronBufferGeometry, self ).__init__( vertices, indices, radius, detail )

        self.type = "TetrahedronBufferGeometry"

        self.parameters = Expando(
            radius = radius,
            detail = detail
        )
