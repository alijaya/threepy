from __future__ import division
import random

from ..math import sphere
from ..math import ray
from ..math import matrix4
from ..core import object3D
from ..math import vector3
from ..materials import pointsMaterial
from ..core import bufferGeometry
from ..utils import Expando

"""
 * @author alteredq / "http":#alteredqualia.com/
 """

class Points( object3D.Object3D ):

    def __init__( self, geometry = None, material = None ):

        super( Points, self ).__init__()

        self.isPoints = True

        self.type = "Points"

        self.geometry = geometry or bufferGeometry.BufferGeometry()
        self.material = material or pointsMaterial.PointsMaterial( color = random.randint( 0x000000, 0xffffff ) )

    def raycast( self, raycaster, intersects ):

        inverseMatrix = matrix4.Matrix4()
        ray = ray.Ray()
        sphere = sphere.Sphere()

        geometry = self.geometry
        matrixWorld = self.matrixWorld
        threshold = raycaster.params.Points.threshold

        # Checking boundingSphere distance to ray

        if geometry.boundingSphere is None : geometry.computeBoundingSphere()

        sphere.copy( geometry.boundingSphere )
        sphere.applyMatrix4( matrixWorld )
        sphere.radius += threshold

        if raycaster.ray.intersectsSphere( sphere ) == False: return

        #

        inverseMatrix.getInverse( matrixWorld )
        ray.copy( raycaster.ray ).applyMatrix4( inverseMatrix )

        localThreshold = threshold / ( ( self.scale.x + self.scale.y + self.scale.z ) / 3 )
        localThresholdSq = localThreshold * localThreshold
        position = vector3.Vector3()

        def testPoint( self, point, index ):

            rayPointDistanceSq = ray.distanceSqToPoint( point )

            if rayPointDistanceSq < localThresholdSq :

                intersectPoint = ray.closestPointToPoint( point )
                intersectPoint.applyMatrix4( matrixWorld )

                distance = raycaster.ray.origin.distanceTo( intersectPoint )

                if distance < raycaster.near or distance > raycaster.far: return

                intersects.append( Expando(

                    distance = distance,
                    distanceToRay = math.sqrt( rayPointDistanceSq ),
                    point = intersectPoint.clone(),
                    index = index,
                    face = None,
                    object = self
                
                ) )

        if hasattr( geometry, "isBufferGeometry" ) :

            index = geometry.index
            attributes = geometry.attributes
            positions = attributes.position.array

            if index:

                indices = index.array

                for a in indices:

                    position.fromArray( positions, a * 3 )

                    testPoint( position, a )

            else:

                for i in xrange( len( positions ) // 3 ):

                    position.fromArray( positions, i * 3 )

                    testPoint( position, i )

        else:

            vertices = geometry.vertices

            for i in xrange( len( vertices ) ):

                testPoint( vertices[ i ], i )

    def clone( self ):

        return Points( self.geometry, self.material ).copy( self )
