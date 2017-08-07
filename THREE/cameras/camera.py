from __future__ import division
import math

from ..core import object3D
from ..math import matrix4
from ..math import quaternion
from ..math import vector3

class Camera( object3D.Object3D ):

    def __init__( self ):

        super( Camera, self ).__init__()

        self.type = "Camera"

        self.matrixWorldInverse = matrix4.Matrix4()
        self.projectionMatrix = matrix4.Matrix4()

        self.isCamera = True

    def copy( self, source, recursive = True ):

        super( Camera, self ).copy( source, recursive )

        self.matrixWorldInverse.copy( source.matrixWorldInverse )
        self.projectionMatrix.copy( source.projectionMatrix )

        return self

    def getWorldDirection( self, optionalTarget ):

        quaternion = matrix4.Quaternion()

        result = optionalTarget or vector3.Vector3()

        self.getWorldQuaternion( quaternion )

        return result.set( 0, 0, - 1 ).applyQuaternion( quaternion )

    def updateMatrixWorld( self, force = False ):

        super( Camera, self ).updateMatrixWorld( force )

        self.matrixWorldInverse.getInverse( self.matrixWorld )

    def clone( self ):

        return Camera().copy( self )
