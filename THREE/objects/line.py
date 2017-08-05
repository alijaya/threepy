from __future__ import division

import random

from ..math import sphere
from ..math import ray
from ..math import matrix4
from ..core import object3D
from ..math import vector3
from ..materials import lineBasicMaterial
from ..core import bufferGeometry

"""
 * @author mrdoob / http://mrdoob.com/
 """

class Line( object3D.Object3D ):

    def __init__( self, geometry = None, material = None ):

        super( Line, self ).__init__()

        self.isLine = True

        self.type = "Line"

        self.geometry = geometry or bufferGeometry.BufferGeometry()
        self.material = material or lineBasicMaterial.LineBasicMaterial( color = random.randint( 0, 0xffffff ) )

    def raycast( self, raycaster, intersects ):

        inverseMatrix = matrix4.Matrix4()
        ray = ray.Ray()
        sphere = sphere.Sphere()

        precision = raycaster.linePrecision
        precisionSq = precision * precision

        geometry = self.geometry
        matrixWorld = self.matrixWorld

        # Checking boundingSphere distance to ray

        if geometry.boundingSphere is None : geometry.computeBoundingSphere()

        sphere.copy( geometry.boundingSphere )
        sphere.applyMatrix4( matrixWorld )

        if raycaster.ray.intersectsSphere( sphere ) == False: return

        #

        inverseMatrix.getInverse( matrixWorld )
        ray.copy( raycaster.ray ).applyMatrix4( inverseMatrix )

        vStart = vector3.Vector3()
        vEnd = vector3.Vector3()
        interSegment = vector3.Vector3()
        interRay = vector3.Vector3()
        step = 2 if self and hasattr( self, "isLineSegments" ) else 1

        if hasattr( geometry, "isBufferGeometry" ) :

            index = geometry.index
            attributes = geometry.attributes
            positions = attributes.position.array

            if index:

                indices = index.array

                for i in xrange( len( indices ) - 1 ):

                    a = indices[ i ]
                    b = indices[ i + 1 ]

                    vStart.fromArray( positions, a * 3 )
                    vEnd.fromArray( positions, b * 3 )

                    distSq = ray.distanceSqToSegment( vStart, vEnd, interRay, interSegment )

                    if distSq > precisionSq: continue

                    interRay.applyMatrix4( self.matrixWorld ) #Move back to world space for distance calculation

                    distance = raycaster.ray.origin.distanceTo( interRay )

                    if distance < raycaster.near or distance > raycaster.far: continue

                    intersects.append( Expando(

                        distance = distance,
                        # What do we want? intersection point on the ray or on the segment??
                        # point = raycaster.ray.at( distance ),
                        point = interSegment.clone().applyMatrix4( self.matrixWorld ),
                        index = i,
                        face = None,
                        faceIndex = None,
                        object = self

                    ) )

            else:

                for i in xrange( len( positions ) // 3 - 1 ):

                    vStart.fromArray( positions, 3 * i )
                    vEnd.fromArray( positions, 3 * i + 3 )

                    distSq = ray.distanceSqToSegment( vStart, vEnd, interRay, interSegment )

                    if distSq > precisionSq: continue

                    interRay.applyMatrix4( self.matrixWorld ) #Move back to world space for distance calculation

                    distance = raycaster.ray.origin.distanceTo( interRay )

                    if distance < raycaster.near or distance > raycaster.far: continue

                    intersects.append( Expando(

                        distance = distance,
                        # What do we want? intersection point on the ray or on the segment??
                        # point = raycaster.ray.at( distance ),
                        point = interSegment.clone().applyMatrix4( self.matrixWorld ),
                        index = i,
                        face = None,
                        faceIndex = None,
                        object = self

                    ) )

        elif hasattr( geometry, "isGeometry" ) :

            vertices = geometry.vertices
            nbVertices = len( vertices )

            for i in xrange( nbVertices - 1):

                distSq = ray.distanceSqToSegment( vertices[ i ], vertices[ i + 1 ], interRay, interSegment )

                if distSq > precisionSq: continue

                interRay.applyMatrix4( self.matrixWorld ) #Move back to world space for distance calculation

                distance = raycaster.ray.origin.distanceTo( interRay )

                if distance < raycaster.near or distance > raycaster.far: continue

                intersects.append( Expando(

                    distance = distance,
                    # What do we want? intersection point on the ray or on the segment??
                    # point = raycaster.ray.at( distance ),
                    point = interSegment.clone().applyMatrix4( self.matrixWorld ),
                    index = i,
                    face = None,
                    faceIndex = None,
                    object = self
                
                ) )

    def clone( self ):

        return Line( self.geometry, self.material ).copy( self )
