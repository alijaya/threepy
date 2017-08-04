from __future__ import division

from ..math import vector3
from ..math import vector2
from ..math import sphere
from ..math import ray
from ..math import matrix4
from ..core import object3D
from ..math import triangle
from ..core import face3
from ..constants import DoubleSide, BackSide, TrianglesDrawMode
from ..materials import meshBasicMaterial
from ..core import bufferGeometry
from ..utils import Expando

"""
 * @author mrdoob / http:#mrdoob.com/
 * @author alteredq / http:#alteredqualia.com/
 * @author mikael emtinger / http:#gomo.se/
 * @author jonobr1 / http:#jonobr1.com/
 """

class Mesh( object3D.Object3D ):

    def __init__( self, geometry = None, material = None ):

        super( Mesh, self ).__init__()

        self.isMesh = True

        self.type = "Mesh"

        self.geometry = geometry or bufferGeometry.BufferGeometry()
        self.material = material or meshBasicMaterial.MeshBasicMaterial( Expando( color = math.random() * 0xffffff ) )
        self.drawMode = TrianglesDrawMode

        self.updateMorphTargets()

    def setDrawMode( self, value ):

        self.drawMode = value

    def copy( self, source ):

        super( Mesh, self ).copy( source )

        self.drawMode = source.drawMode

        return self

    def updateMorphTargets( self ):

        geometry = self.geometry

        if hasattr( geometry, "isBufferGeometry" ) :

            morphAttributes = geometry.morphAttributes
            keys = morphAttributes.keys()

            if len( keys ) > 0 :

                morphAttribute = morphAttributes[ keys[ 0 ] ]

                if morphAttribute is not None :

                    self.morphTargetInfluences = []
                    self.morphTargetDictionary = {}
                    for m in xrange( len( morphAttribute ) ) :

                        name = morphAttribute[ m ].name or str( m )

                        self.morphTargetInfluences.append( 0 )
                        self.morphTargetDictionary[ name ] = m

        else:

            morphTargets = geometry.morphTargets

            if morphTargets is not None and len( morphTargets ) > 0 :

                self.morphTargetInfluences = []
                self.morphTargetDictionary = {}
                for m in xrange( len( morphTargets ) ) :

                    name = morphTargets[ m ].name or str( m )

                    self.morphTargetInfluences.append( 0 )
                    self.morphTargetDictionary[ name ] = m

    def raycast( self, raycaster, intersects ):

        inverseMatrix = matrix4.Matrix4()
        ray = ray.Ray()
        sphere = sphere.Sphere()

        vA = vector3.Vector3()
        vB = vector3.Vector3()
        vC = vector3.Vector3()

        tempA = vector3.Vector3()
        tempB = vector3.Vector3()
        tempC = vector3.Vector3()

        uvA = vector2.Vector2()
        uvB = vector2.Vector2()
        uvC = vector2.Vector2()

        barycoord = vector3.Vector3()

        intersectionPoint = vector3.Vector3()
        intersectionPointWorld = vector3.Vector3()

        def uvIntersection( point, p1, p2, p3, uv1, uv2, uv3 ):

            triangle.Triangle.barycoordFromPoint( point, p1, p2, p3, barycoord )

            uv1.multiplyScalar( barycoord.x )
            uv2.multiplyScalar( barycoord.y )
            uv3.multiplyScalar( barycoord.z )

            uv1.add( uv2 ).add( uv3 )

            return uv1.clone()

        def checkIntersection( object, material, raycaster, ray, pA, pB, pC, point ):

            intersect= None

            if material.side == BackSide :

                intersect = ray.intersectTriangle( pC, pB, pA, True, point )

            else:

                intersect = ray.intersectTriangle( pA, pB, pC, material.side != DoubleSide, point )

            if intersect is None : return None

            intersectionPointWorld.copy( point )
            intersectionPointWorld.applyMatrix4( object.matrixWorld )

            distance = raycaster.ray.origin.distanceTo( intersectionPointWorld )

            if distance < raycaster.near or distance > raycaster.far : return None

            return Expando(
                distance = distance,
                point = intersectionPointWorld.clone(),
                object = object
            )

        def checkBufferGeometryIntersection( object, raycaster, ray, position, uv, a, b, c ):

            vA.fromBufferAttribute( position, a )
            vB.fromBufferAttribute( position, b )
            vC.fromBufferAttribute( position, c )

            intersection = checkIntersection( object, object.material, raycaster, ray, vA, vB, vC, intersectionPoint )

            if intersection :

                if uv :

                    uvA.fromBufferAttribute( uv, a )
                    uvB.fromBufferAttribute( uv, b )
                    uvC.fromBufferAttribute( uv, c )

                    intersection.uv = uvIntersection( intersectionPoint, vA, vB, vC, uvA, uvB, uvC )

                intersection.face = face3.Face3( a, b, c, triangle.Triangle.normal( vA, vB, vC ) )
                intersection.faceIndex = a

            return intersection

        # end

        geometry = self.geometry
        material = self.material
        matrixWorld = self.matrixWorld

        if material is None : return

        # Checking boundingSphere distance to ray

        if geometry.boundingSphere is None : geometry.computeBoundingSphere()

        sphere.copy( geometry.boundingSphere )
        sphere.applyMatrix4( matrixWorld )

        if raycaster.ray.intersectsSphere( sphere ) == False : return

        #

        inverseMatrix.getInverse( matrixWorld )
        ray.copy( raycaster.ray ).applyMatrix4( inverseMatrix )

        # Check boundingBox before continuing

        if geometry.boundingBox is not None :

            if ray.intersectsBox( geometry.boundingBox ) == False : return

        if hasattr( geometry, "isBufferGeometry" ) :

            a, b, c
            index = geometry.index
            position = geometry.attributes.position
            uv = geometry.attributes.uv

            if index is not None :

                # indexed buffer geometry

                for i in xrange( 0, index.count, 3 ) :

                    a = index.getX( i )
                    b = index.getX( i + 1 )
                    c = index.getX( i + 2 )

                    intersection = checkBufferGeometryIntersection( self, raycaster, ray, position, uv, a, b, c )

                    if intersection :

                        intersection.faceIndex = i // 3 # triangle number in indices buffer semantics
                        intersects.append( intersection )

            else:

                # non-indexed buffer geometry

                for i in xrange( 0, position.count, 3 ) :

                    a = i
                    b = i + 1
                    c = i + 2

                    intersection = checkBufferGeometryIntersection( self, raycaster, ray, position, uv, a, b, c )

                    if intersection :

                        intersection.index = a # triangle number in positions buffer semantics
                        intersects.append( intersection )

        elif hasattr( geometry, "isGeometry" ) :

            fvA, fvB, fvC
            isMultiMaterial = isinstance( material, list )

            vertices = geometry.vertices
            faces = geometry.faces
            uvs = None

            faceVertexUvs = geometry.faceVertexUvs[ 0 ]
            if len( faceVertexUvs ) > 0 : uvs = faceVertexUvs

            for f in xrange( len( faces ) ) :

                face = faces[ f ]
                faceMaterial = material[ face.materialIndex ] if isMultiMaterial else material

                if faceMaterial is None : continue

                fvA = vertices[ face.a ]
                fvB = vertices[ face.b ]
                fvC = vertices[ face.c ]

                if faceMaterial.morphTargets == True :

                    morphTargets = geometry.morphTargets
                    morphInfluences = self.morphTargetInfluences

                    vA.set( 0, 0, 0 )
                    vB.set( 0, 0, 0 )
                    vC.set( 0, 0, 0 )

                    for t in xrange( len( morphTargets ) ) :

                        influence = morphInfluences[ t ]

                        if influence == 0 : continue

                        targets = morphTargets[ t ].vertices

                        vA.addScaledVector( tempA.subVectors( targets[ face.a ], fvA ), influence )
                        vB.addScaledVector( tempB.subVectors( targets[ face.b ], fvB ), influence )
                        vC.addScaledVector( tempC.subVectors( targets[ face.c ], fvC ), influence )

                    vA.add( fvA )
                    vB.add( fvB )
                    vC.add( fvC )

                    fvA = vA
                    fvB = vB
                    fvC = vC

                intersection = checkIntersection( self, faceMaterial, raycaster, ray, fvA, fvB, fvC, intersectionPoint )

                if intersection :

                    if uvs and uvs[ f ] :

                        uvs_f = uvs[ f ]
                        uvA.copy( uvs_f[ 0 ] )
                        uvB.copy( uvs_f[ 1 ] )
                        uvC.copy( uvs_f[ 2 ] )

                        intersection.uv = uvIntersection( intersectionPoint, fvA, fvB, fvC, uvA, uvB, uvC )

                    intersection.face = face
                    intersection.faceIndex = f
                    intersects.append( intersection )

    def clone( self ):

        return Mesh( self.geometry, self.material ).copy( self )
