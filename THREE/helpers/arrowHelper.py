from ..core import bufferAttribute
from ..core import bufferGeometry
from ..core import object3D
from ..geometries import cylinderGeometry
from ..materials import meshBasicMaterial
from ..materials import lineBasicMaterial
from ..objects import mesh
from ..objects import line
from ..math import vector3
"""
 * @author WestLangley / "http":#github.com/WestLangley
 * @author zz85 / "http":#github.com/zz85
 * @author bhouston / "http":#clara.io
 *
 * Creates an arrow for visualizing directions
 *
 * "Parameters":
 *  dir - vector3.Vector3
 *  origin - vector3.Vector3
 *  length - Number
 *  color - color in hex value
 *  headLength - Number
 *  headWidth - Number
 """

class ArrowHelper( object3D.Object3D ):

    lineGeometry = None
    coneGeometry = None

    def __init__( self, dir, origin, length = 1, color = 0xffff00, headLength = None, headWidth = None ):

        # dir is assumed to be normalized

        super( ArrowHelper, self ).__init__()

        headLength = headLength or 0.2 * length
        headWidth = headWidth or 0.2 * headLength

        if ArrowHelper.lineGeometry is None :

            ArrowHelper.lineGeometry = bufferGeometry.BufferGeometry()
            ArrowHelper.lineGeometry.addAttribute( "position", bufferAttribute.Float32BufferAttribute( [ 0, 0, 0, 0, 1, 0 ], 3 ) )

            ArrowHelper.coneGeometry = cylinderGeometry.CylinderBufferGeometry( 0, 0.5, 1, 5, 1 )
            ArrowHelper.coneGeometry.translate( 0, - 0.5, 0 )

        self.position.copy( origin )

        self.line = line.Line( ArrowHelper.lineGeometry, lineBasicMaterial.LineBasicMaterial( color = color ) )
        self.line.matrixAutoUpdate = False
        self.add( self.line )

        self.cone = mesh.Mesh( ArrowHelper.coneGeometry, meshBasicMaterial.MeshBasicMaterial( color = color ) )
        self.cone.matrixAutoUpdate = False
        self.add( self.cone )

        self.setDirection( dir )
        self.setLength( length, headLength, headWidth )

    def setDirection( self, dir ):

        axis = vector3.Vector3()

        # dir is assumed to be normalized

        if dir.y > 0.99999 :

            self.quaternion.set( 0, 0, 0, 1 )

        elif dir.y < - 0.99999 :

            self.quaternion.set( 1, 0, 0, 0 )

        else:

            axis.set( dir.z, 0, - dir.x ).normalize()

            radians = math.acos( dir.y )

            self.quaternion.setFromAxisAngle( axis, radians )

    def setLength( self, length, headLength = None, headWidth = None ):

        headLength = headLength or 0.2 * length
        headWidth = headWidth or 0.2 * headLength

        self.line.scale.set( 1, max( 0, length - headLength ), 1 )
        self.line.updateMatrix()

        self.cone.scale.set( headWidth, headLength, headWidth )
        self.cone.position.y = length
        self.cone.updateMatrix()

    def setColor( self, color ):

        self.line.material.color.copy( color )
        self.cone.material.color.copy( color )
