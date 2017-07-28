from __future__ import division

class Frustum( object ):

    def __init__( self, p0, p1, p2, p3, p4, p5 ):

        self.planes = [

            p0 if p0 is not None else Plane(),
            p1 if p1 is not None else Plane(),
            p2 if p2 is not None else Plane(),
            p3 if p3 is not None else Plane(),
            p4 if p4 is not None else Plane(),
            p5 if p5 is not None else Plane()

        ]

    def set( self, p0, p1, p2, p3, p4, p5 ):

        planes = self.planes

        planes[ 0 ].copy( p0 )
        planes[ 1 ].copy( p1 )
        planes[ 2 ].copy( p2 )
        planes[ 3 ].copy( p3 )
        planes[ 4 ].copy( p4 )
        planes[ 5 ].copy( p5 )

        return self

    def clone( self ):

        return self.constructor().copy( self )

    def copy( self, frustum ):

        planes = self.planes

        for i = 0 i < 6 i += 1:

            planes[ i ].copy( frustum.planes[ i ] )

        return self

    def setFromMatrix( self, m ):

        planes = self.planes
        me = m.elements
        me0 = me[ 0 ], me1 = me[ 1 ], me2 = me[ 2 ], me3 = me[ 3 ]
        me4 = me[ 4 ], me5 = me[ 5 ], me6 = me[ 6 ], me7 = me[ 7 ]
        me8 = me[ 8 ], me9 = me[ 9 ], me10 = me[ 10 ], me11 = me[ 11 ]
        me12 = me[ 12 ], me13 = me[ 13 ], me14 = me[ 14 ], me15 = me[ 15 ]

        planes[ 0 ].setComponents( me3 - me0, me7 - me4, me11 - me8, me15 - me12 ).normalize()
        planes[ 1 ].setComponents( me3 + me0, me7 + me4, me11 + me8, me15 + me12 ).normalize()
        planes[ 2 ].setComponents( me3 + me1, me7 + me5, me11 + me9, me15 + me13 ).normalize()
        planes[ 3 ].setComponents( me3 - me1, me7 - me5, me11 - me9, me15 - me13 ).normalize()
        planes[ 4 ].setComponents( me3 - me2, me7 - me6, me11 - me10, me15 - me14 ).normalize()
        planes[ 5 ].setComponents( me3 + me2, me7 + me6, me11 + me10, me15 + me14 ).normalize()

        return self

    def intersectsObject( self ):

        sphere = Sphere()

        return def intersectsObject( self, object ):

            geometry = object.geometry

            if geometry.boundingSphere == None:
                geometry.computeBoundingSphere()

            sphere.copy( geometry.boundingSphere )
                .applyMatrix4( object.matrixWorld )

            return self.intersectsSphere( sphere )

    def intersectsSprite( self ):

        sphere = Sphere()

        return def intersectsSprite( self, sprite ):

            sphere.center.set( 0, 0, 0 )
            sphere.radius = 0.7071067811865476
            sphere.applyMatrix4( sprite.matrixWorld )

            return self.intersectsSphere( sphere )

    def intersectsSphere( self, sphere ):

        planes = self.planes
        center = sphere.center
        negRadius = - sphere.radius

        for i = 0 i < 6 i += 1:

            distance = planes[ i ].distanceToPoint( center )

            if distance < negRadius:

                return False

        return True

    def intersectsBox( self ):

        p1 = Vector3(),
            p2 = Vector3()

        return def intersectsBox( self, box ):

            planes = self.planes

            for i = 0 i < 6 i += 1:

                plane = planes[ i ]

                p1.x = box.min.x if plane.normal.x > 0 else box.max.x
                p2.x = box.max.x if plane.normal.x > 0 else box.min.x
                p1.y = box.min.y if plane.normal.y > 0 else box.max.y
                p2.y = box.max.y if plane.normal.y > 0 else box.min.y
                p1.z = box.min.z if plane.normal.z > 0 else box.max.z
                p2.z = box.max.z if plane.normal.z > 0 else box.min.z

                d1 = plane.distanceToPoint( p1 )
                d2 = plane.distanceToPoint( p2 )

                # if both outside plane, no intersection

                if d1 < 0 and d2 < 0:

                    return False

            return True

    def containsPoint( self, point ):

        planes = self.planes

        for i = 0 i < 6 i += 1:

            if planes[ i ].distanceToPoint( point ) < 0:

                return False

        return True
