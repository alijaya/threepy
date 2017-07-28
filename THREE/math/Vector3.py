from __future__ import division
import math

import _Math
import matrix4

class Vector3( object ):

    def __init__( self, x = 0, y = 0, z = 0 ):

        self.x = x
        self.y = y
        self.z = z

        self.isVector3 = True
    
    def set( self, x, y, z ):

        self.x = x
        self.y = y
        self.z = z

        return self

    def setScalar( self, scalar ):
        
        self.x = scalar
        self.y = scalar
        self.z = scalar

        return self

    def setX( self, x ):

        self.x = x

        return self

    def setY( self, y ):

        self.y = y

        return self

    def setZ( self, z ):

        self.z = z

        return self

    def setComponent( self, index, value ):

        if   index == 0: self.x = value
        elif index == 1: self.y = value
        elif index == 2: self.z = value
        else: raise ValueError( "index is out of range: " + index )

        return self

    def getComponent( self, index ):

        if   index == 0: return self.x
        elif index == 1: return self.y
        elif index == 2: return self.z
        else: raise ValueError( "index is out of range: " + index )

    def clone( self ):

        return Vector3( self.x, self.y, self.z )

    def copy( self, v ):

        self.x = v.x
        self.y = v.y
        self.z = v.z

        return self
    
    def add( self, v ):

        self.x += v.x
        self.y += v.y
        self.z += v.z

        return self

    def addScalar( self, s ):

        self.x += s
        self.y += s
        self.z += s

        return self

    def addVectors( self, a, b ):

        self.x = a.x + b.x
        self.y = a.y + b.y
        self.z = a.z + b.z

        return self

    def addScaledVector( self, v, s ):

        self.x += v.x * s
        self.y += v.y * s
        self.z += v.z * s

        return self

    def sub( self, v ):

        self.x -= v.x
        self.y -= v.y
        self.z -= v.z

        return self

    def subScalar( self, s ):

        self.x -= s
        self.y -= s
        self.z -= s
        
        return self

    def subVectors( self, a, b ):

        self.x = a.x - b.x
        self.y = a.y - b.y
        self.z = a.z - b.z

        return self

    def multiply( self, v ):

        self.x *= v.x
        self.y *= v.y
        self.z *= v.z

        return self

    def multiplyScalar( self, scalar ):

        self.x *= scalar
        self.y *= scalar
        self.z *= scalar

        return self

    def multiplyVectors( self, a, b ):

        self.x = a.x * b.x
        self.y = a.y * b.y
        self.z = a.z * b.z

        return self

    def applyEuler( self, euler ):

        quaternion = Quaternion()

        if not ( euler is not None and euler.isEuler ):

            raise ValueError( "THREE.Vector3: .applyEuler() now expects an Euler rotation rather than a Vector3 and order." )

        self.applyQuaternion( quaternion.setFromEuler( euler ) )

    def applyAxisAngle( self, axis, angle ):

        quaternion = Quaternion()

        return self.applyQuaternion( quaternion.setFromAxisAngle( axis, angle ) )

    def applyMatrix3( self, m ):

        x = self.x
        y = self.y
        z = self.z
        e = m.elements

        self.x = e[ 0 ] * x + e[ 3 ] * y + e[ 6 ] * z
        self.y = e[ 1 ] * x + e[ 4 ] * y + e[ 7 ] * z
        self.z = e[ 2 ] * x + e[ 5 ] * y + e[ 8 ] * z

        return self

    def applyMatrix4( self, m ):

        x = self.x
        y = self.y
        z = self.z
        e = m.elements

        w = 1. / ( e[ 3 ] * x + e[ 7 ] * y + e[ 11 ] * z + e[ 15 ] )

        self.x = ( e[ 0 ] * x + e[ 4 ] * y + e[ 8 ]  * z + e[ 12 ] ) * w
        self.y = ( e[ 1 ] * x + e[ 5 ] * y + e[ 9 ]  * z + e[ 13 ] ) * w
        self.z = ( e[ 2 ] * x + e[ 6 ] * y + e[ 10 ] * z + e[ 14 ] ) * w

        return self

    def applyQuaternion( self, q ):

        x = self.x
        y = self.y
        z = self.z
        qx = q.x
        qy = q.y
        qz = q.z
        qw = q.w

        # calculate quat * vector

        ix = qw * x + qy * z - qz * y
        iy = qw * y + qz * x - qx * z
        iz = qw * z + qx * y - qy * x
        iw = - qx * x - qy * y - qz * z

        # calculate result * inverse quat

        self.x = ix * qw + iw * - qx + iy * - qz - iz * - qy
        self.y = iy * qw + iw * - qy + iz * - qx - ix * - qz
        self.z = iz * qw + iw * - qz + ix * - qy - iy * - qx

        return self

    def project( self, camera ):

        matrix = Matrix4()

        matrix.multiplyMatrices( camera.projectionMatrix, matrix.getInverse( camera.matrixWorld ) )
        return self.applyMatrix4( matrix )

    def unproject( self, camera ):

        matrix = Matrix4()

        matrix.multiplyMatrices( camera.matrixWorld, matrix.getInverse( camera.projectionMatrix ) )
        return self.applyMatrix4( matrix )

    def transformDirection( self, m ):

        # input: THREE.Matrix4 affine matrix
        # vector interpreted as a direction

        x = self.x
        y = self.y
        z = self.z
        e = m.elements

        self.x = e[ 0 ] * x + e[ 4 ] * y + e[ 8 ]  * z
        self.y = e[ 1 ] * x + e[ 5 ] * y + e[ 9 ]  * z
        self.z = e[ 2 ] * x + e[ 6 ] * y + e[ 10 ] * z

        return self.normalize()

    def divide( self, v ):

        self.x /= v.x
        self.y /= v.y
        self.z /= v.z

        return self

    def divideScalar( self, scalar ):

        return self.multiplyScalar( 1. / scalar )

    def min( self, v ):

        self.x = min( self.x, v.x )
        self.y = min( self.y, v.y )
        self.z = min( self.z, v.z )

        return self

    def max( self, v ):

        self.x = max( self.x, v.x )
        self.y = max( self.y, v.y )
        self.z = max( self.z, v.z )
        
        return self

    def clamp( self, mn, mx ):

        self.x = max( mn.x, min( mx.x, self.x ) )
        self.y = max( mn.y, min( mx.y, self.y ) )
        self.z = max( mn.z, min( mx.z, self.z ) )

        return self
    
    def clampScalar( self, minVal, maxVal ):

        mn = Vector3()
        mx = Vector3()

        mn.set( minVal, minVal, minVal )
        mx.set( maxVal, maxVal, maxVal )

        return self.clamp( mn, mx )

    def clampLength( self, mn, mx ):

        length = self.length()

        return self.divideScalar( length or 1 ).multiplyScalar( max( mn, min( mx, length ) ) )

    def floor( self ):

        self.x = math.floor( self.x )
        self.y = math.floor( self.y )
        self.z = math.floor( self.z )

        return self

    def ceil( self ):

        self.x = math.ceil( self.x )
        self.y = math.ceil( self.y )
        self.z = math.ceil( self.z )

        return self

    def round( self ):

        self.x = round( self.x )
        self.y = round( self.y )
        self.z = round( self.z )

        return self

    def roundToZero( self ):

        self.x = math.ceil( self.x ) if self.x < 0 else math.floor( self.x )
        self.y = math.ceil( self.y ) if self.y < 0 else math.floor( self.y )
        self.z = math.ceil( self.z ) if self.z < 0 else math.floor( self.z )

        return self

    def negate( self ):

        self.x = - self.x
        self.y = - self.y
        self.z = - self.z

        return self

    def dot( self, v ):

        return self.x * v.x + self.y * v.y + self.z * v.z

    # TODO lengthSquared?

    def lengthSq( self ):

        return self.x * self.x + self.y * self.y + self.z * self.z

    def length( self ):

        return math.sqrt( self.x * self.x + self.y * self.y + self.z * self.z )

    def lengthManhattan( self ):

        return abs( self.x ) + abs( self.y ) + abs( self.z )

    def normalize( self ):

        return self.divideScalar( self.length() or 1 )

    def setLength( self, length ):

        return self.normalize().multiplyScalar( length )

    def lerp( self, v, alpha ):

        self.x += ( v.x - self.x ) * alpha
        self.y += ( v.y - self.y ) * alpha
        self.z += ( v.z - self.z ) * alpha

        return self

    def lerpVector( self, v1, v2, alpha ):

        return self.subVectors( v2, v1 ).multiplyScalar( alpha ).add( v1 )

    def cross( self, v ):

        x = self.x
        y = self.y
        z = self.z

        self.x = y * v.z - z * v.y
        self.y = z * v.x - x * v.z
        self.z = x * v.y - y * v.x

        return self

    def crossVectors( self, a, b ):

        ax = a.x
        ay = a.y
        az = a.z
        bx = b.x
        by = b.y
        bz = b.z

        self.x = ay * bz - az * by
        self.y = az * bx - ax * bz
        self.z = ax * by - ay * bx

        return self

    def projectOnVector( self, vector ):

        scalar = vector.dot( self ) / vector.lengthSq()

        return self.copy( vector ).multiplyScalar( scalar )

    def projectOnPlane( self, planeNormal ):

        v1 = Vector3()

        v1.copy( self ).projectOnVector( planeNormal )

        return self.sub( v1 )

    def reflect( self, normal ):

        # reflect incident vector off plane orthogonal to normal
        # normal is assumed to have unit length

        v1 = Vector3()

        return self.sub( v1.copy( normal ).multiplyScalar( 2 * self.dot( normal ) ) )



    def angleTo( self, v ):

        theta = self.dot( v ) / math.sqrt( self.lengthSq() * v.lengthSq() )

        # clamp, to handle numerical problems

        return math.acos( _Math.clamp( theta, - 1, 1 ) )

    def distanceTo( self, v ):

        return math.sqrt( self.distanceToSquared( v ) )

    def distanceToSquared( self, v ):

        dx = self.x - v.x
        dy = self.y - v.y
        dz = self.z - v.z

        return dx * dx + dy * dy + dz * dz

    def distanceToManhattan( self, v ):

        return abs( self.x - v.x ) + abs( self.y - v.y ) + abs( self.z - v.z )

    def setFromSpherical( self, s ):

        sinPhiRadius = math.sin( s.phi ) * s.radius

        self.x = sinPhiRadius * Math.sin( s.theta )
        self.y = math.cos( s.phi ) * s.radius
        self.z = sinPhiRadius * Math.cos( s.theta )

        return self

    def setFromCylindrical( self, c ):

        self.x = c.radius * math.sin( c.theta )
        self.y = c.y
        self.z = c.radius * math.cos( c.theta )

        return self

    def setFromMatrixPosition( self, m ):

        e = m.elements

        self.x = e[ 12 ]
        self.y = e[ 13 ]
        self.z = e[ 14 ]

        return self

    def setFromMatrixScale( self, m ):

        sx = self.setFromMatrixColumn( m, 0 ).length()
        sy = self.setFromMatrixColumn( m, 1 ).length()
        sz = self.setFromMatrixColumn( m, 2 ).length()

        self.x = sx
        self.y = sy
        self.z = sz

        return self

    def setFromMatrixColumn( self, m, index ):

        return self.fromArray( m.elements, index * 4 )

    def equals( self, v ):

        return ( v.x == self.x ) and ( v.y == self.y ) and ( v.z == self.z )

    def fromArray( self, array, offset = 0 ):

        self.x = array[ offset ]
        self.y = array[ offset + 1 ]
        self.z = array[ offset + 2 ]

        return self

    def toArray( self, array = None, offset = 0 ):

        if array is None: array = []

        array[ offset ] = self.x
        array[ offset + 1 ] = self.y
        array[ offset + 2 ] = self.z

        return array

    def fromBufferAttribute( self, attribute, index ):

        self.x = attribute.getX( index )
        self.y = attribute.getY( index )
        self.z = attribute.getZ( index )

        return self
