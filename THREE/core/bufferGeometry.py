from __future__ import division
import math

import logging

from ..math import vector3
from ..math import box3
import eventDispatcher
from bufferAttribute import BufferAttribute, Float32BufferAttribute, Uint16BufferAttribute, Uint32BufferAttribute
from ..math import sphere
import directGeometry
import object3D
from ..math import matrix4
from ..math import matrix3
from ..math import _Math
from ..utils import Expando
from ..utils import ctypesArray
import geometry

"""
 * @author alteredq / http:#alteredqualia.com/
 * @author mrdoob / http:#mrdoob.com/
 """

class BufferGeometry( eventDispatcher.EventDispatcher ):

    MaxIndex = 65535

    def __init__( self ):

        self.isBufferGeometry = True

        self.id = geometry.Geometry.getGeometryId()
        self.uuid = _Math.generateUUID()

        self.name = ""
        self.type = "BufferGeometry"

        self.index = None
        self.attributes = {}
        self.morphAttributes = {}
        self.groups = []

        self.boundingBox = None
        self.boundingSphere = None

        self.drawRange = Expando( start = 0, count = float( "inf" ) )

    def getIndex( self ):

        return self.index

    def setIndex( self, index ):

        if isinstance( index, list ):

            self.index = ( Uint32BufferAttribute if max( index ) > 65535 else Uint16BufferAttribute )( index, 1 )

        else:

            self.index = index

    def addAttribute( self, name, attribute ):

        self.attributes[ name ] = attribute

        return self

    def getAttribute( self, name ):

        return self.attributes[ name ]

    def removeAttribute( self, name ):

        del self.attributes[ name ]

        return self

    def addGroup( self, start, count, materialIndex = 0 ):

        self.groups.append( Expando(

            start = start,
            count = count,
            materialIndex = materialIndex

        ) )

    def clearGroups( self ):

        self.groups = []

    def setDrawRange( self, start, count ):

        self.drawRange.start = start
        self.drawRange.count = count

    def applyMatrix( self, matrix ):

        position = self.attributes.get( "position" )

        if position is not None:

            matrix.applyToBufferAttribute( position )
            position.needsUpdate = True

        normal = self.attributes.get( "normal" )

        if normal is not None:

            normalMatrix = matrix3.Matrix3().getNormalMatrix( matrix )
            
            normalMatrix.applyToBufferAttribute( normal )
            normal.needsUpdate = True

        if self.boundingBox is not None:

            self.computeBoundingBox()

        if self.boundingSphere is not None:

            self.computeBoundingSphere()

        return self

    def rotateX( self, angle ):

        # rotate geometry around world x-axis

        m1 = matrix4.Matrix4()

        m1.makeRotationX( angle )

        self.applyMatrix( m1 )

        return self

    def rotateY( self, angle ):

        # rotate geometry around world y-axis

        m1 = matrix4.Matrix4()

        m1.makeRotationY( angle )

        self.applyMatrix( m1 )

        return self

    def rotateZ( self, angle ):

        # rotate geometry around world z-axis

        m1 = matrix4.Matrix4()

        m1.makeRotationZ( angle )

        self.applyMatrix( m1 )

        return self

    def translate( self, x, y, z ):

        # translate geometry

        m1 = matrix4.Matrix4()

        m1.makeTranslation( x, y, z )

        self.applyMatrix( m1 )

        return self

    def scale( self, x, y, z ):

        # scale geometry

        m1 = matrix4.Matrix4()

        m1.makeScale( x, y, z )

        self.applyMatrix( m1 )

        return self

    def lookAt( self, vector ):

        obj = object3D.Object3D()

        obj.lookAt( vector )

        obj.updateMatrix()

        self.applyMatrix( obj.matrix )

    def center( self ):

        self.computeBoundingBox()

        offset = self.boundingBox.getCenter().negate()

        self.translate( offset.x, offset.y, offset.z )

        return offset

    def setFromObject( self, object ):

        # console.log( "THREE.BufferGeometry.setFromObject(). Converting", object, self )

        geometry = object.geometry

        if hasattr( object, "isPoints" ) or hasattr( object, "isLine" ):

            positions = Float32BufferAttribute( len( geometry.vertices ) * 3, 3 )
            colors = Float32BufferAttribute( len( geometry.colors ) * 3, 3 )

            self.addAttribute( "position", positions.copyVector3sArray( geometry.vertices ) )
            self.addAttribute( "color", colors.copyColorsArray( geometry.colors ) )

            if geometry.lineDistances and len( geometry.lineDistances ) == len( geometry.vertices ):

                lineDistances = Float32BufferAttribute( len( geometry.lineDistances ), 1 )

                self.addAttribute( "lineDistance", lineDistances.copyArray( geometry.lineDistances ) )

            if geometry.boundingSphere is not None:

                self.boundingSphere = geometry.boundingSphere.clone()

            if geometry.boundingBox is not None:

                self.boundingBox = geometry.boundingBox.clone()

        elif hasattr( object, "isMesh" ):

            if geometry and hasattr( geometry, "isGeometry" ):

                self.fromGeometry( geometry )

        return self

    def updateFromObject( self, object ):

        geometry = object.geometry

        if hasattr( object, "isMesh" ):

            direct = getattr( geometry, "_directGeometry", None )

            if geometry.elementsNeedUpdate == True:

                direct = None
                geometry.elementsNeedUpdate = False

            if direct is None:

                return self.fromGeometry( geometry )

            direct.verticesNeedUpdate = geometry.verticesNeedUpdate
            direct.normalsNeedUpdate = geometry.normalsNeedUpdate
            direct.colorsNeedUpdate = geometry.colorsNeedUpdate
            direct.uvsNeedUpdate = geometry.uvsNeedUpdate
            direct.groupsNeedUpdate = geometry.groupsNeedUpdate

            geometry.verticesNeedUpdate = False
            geometry.normalsNeedUpdate = False
            geometry.colorsNeedUpdate = False
            geometry.uvsNeedUpdate = False
            geometry.groupsNeedUpdate = False

            geometry = direct

        if geometry.verticesNeedUpdate == True:

            attribute = self.attributes.position

            if attribute is not None:

                attribute.copyVector3sArray( geometry.vertices )
                attribute.needsUpdate = True

            geometry.verticesNeedUpdate = False

        if geometry.normalsNeedUpdate == True:

            attribute = self.attributes.normal

            if attribute is not None:

                attribute.copyVector3sArray( geometry.normals )
                attribute.needsUpdate = True

            geometry.normalsNeedUpdate = False

        if geometry.colorsNeedUpdate == True:

            attribute = self.attributes.color

            if attribute is not None:

                attribute.copyColorsArray( geometry.colors )
                attribute.needsUpdate = True

            geometry.colorsNeedUpdate = False

        if geometry.uvsNeedUpdate:

            attribute = self.attributes.uv

            if attribute is not None:

                attribute.copyVector2sArray( geometry.uvs )
                attribute.needsUpdate = True

            geometry.uvsNeedUpdate = False

        if geometry.lineDistancesNeedUpdate:

            attribute = self.attributes.lineDistance

            if attribute is not None:

                attribute.copyArray( geometry.lineDistances )
                attribute.needsUpdate = True

            geometry.lineDistancesNeedUpdate = False

        if geometry.groupsNeedUpdate:

            geometry.computeGroups( object.geometry )
            self.groups = geometry.groups

            geometry.groupsNeedUpdate = False

        return self

    def fromGeometry( self, geometry ):

        geometry._directGeometry = directGeometry.DirectGeometry().fromGeometry( geometry )

        return self.fromDirectGeometry( geometry._directGeometry )

    def fromDirectGeometry( self, geometry ):

        positions = ctypesArray( "f", len( geometry.vertices ) * 3 )
        self.addAttribute( "position", BufferAttribute( positions, 3 ).copyVector3sArray( geometry.vertices ) )

        if len( geometry.normals ) > 0:

            normals = ctypesArray( "f", len( geometry.normals ) * 3 )
            self.addAttribute( "normal", BufferAttribute( normals, 3 ).copyVector3sArray( geometry.normals ) )

        if len( geometry.colors ) > 0:

            colors = ctypesArray( "f", len( geometry.colors ) * 3 )
            self.addAttribute( "color", BufferAttribute( colors, 3 ).copyColorsArray( geometry.colors ) )

        if len( geometry.uvs ) > 0:

            uvs = ctypesArray( "f", len( geometry.uvs ) * 2 )
            self.addAttribute( "uv", BufferAttribute( uvs, 2 ).copyVector2sArray( geometry.uvs ) )

        if len( geometry.uvs2 ) > 0:

            uvs2 = ctypesArray( "f", len( geometry.uvs2 ) * 2 )
            self.addAttribute( "uv2", BufferAttribute( uvs2, 2 ).copyVector2sArray( geometry.uvs2 ) )

        if len( geometry.indices ) > 0:

            TypeArray = "L" if max( geometry.indices ) > 65535 else "H"
            indices = ctypesArray( TypeArray, len( geometry.indices ) * 3 )
            self.setIndex( BufferAttribute( indices, 1 ).copyIndicesArray( geometry.indices ) )

        # groups

        self.groups = geometry.groups

        # morphs

        for name in geometry.morphTargets:

            array = []
            morphTargets = geometry.morphTargets[ name ]

            for morphTarget in morphTargets:

                attribute = Float32BufferAttribute( len( morphTarget ) * 3, 3 )

                array.append( attribute.copyVector3sArray( morphTarget ) )

            self.morphAttributes[ name ] = array

        # skinning

        if len( geometry.skinIndices ) > 0:

            skinIndices = Float32BufferAttribute( len( geometry.skinIndices ) * 4, 4 )
            self.addAttribute( "skinIndex", skinIndices.copyVector4sArray( geometry.skinIndices ) )

        if len( geometry.skinWeights ) > 0:

            skinWeights = Float32BufferAttribute( len( geometry.skinWeights ) * 4, 4 )
            self.addAttribute( "skinWeight", skinWeights.copyVector4sArray( geometry.skinWeights ) )

        #

        if geometry.boundingSphere is not None:

            self.boundingSphere = geometry.boundingSphere.clone()

        if geometry.boundingBox is not None:

            self.boundingBox = geometry.boundingBox.clone()

        return self

    def computeBoundingBox( self ):

        if self.boundingBox is None:

            self.boundingBox = box3.Box3()

        position = self.attributes.get( "position" )

        if position is not None:

            self.boundingBox.setFromBufferAttribute( position )

        else:

            self.boundingBox.makeEmpty()

        if math.isnan( self.boundingBox.min.x ) or math.isnan( self.boundingBox.min.y ) or math.isnan( self.boundingBox.min.z ):

            logging.error( "THREE.BufferGeometry.computeBoundingBox: Computed min/max have NaN values. The \"position\" attribute is likely to have NaN values.", self )

    def computeBoundingSphere( self ):

        box = box3.Box3()
        vector = vector3.Vector3()

        if self.boundingSphere is None:

            self.boundingSphere = sphere.Sphere()

        position = self.attributes.get( "position" )

        if position:

            center = self.boundingSphere.center

            box.setFromBufferAttribute( position )
            box.getCenter( center )

            # hoping to find a boundingSphere with a radius smaller than the
            # boundingSphere of the boundingBox: sqrt(3) smaller in the best case

            maxRadiusSq = 0

            for i in xrange( position.count ):

                vector.x = position.getX( i )
                vector.y = position.getY( i )
                vector.z = position.getZ( i )
                maxRadiusSq = max( maxRadiusSq, center.distanceToSquared( vector ) )

            self.boundingSphere.radius = math.sqrt( maxRadiusSq )

            if math.isnan( self.boundingSphere.radius ):

                logging.error( "THREE.BufferGeometry.computeBoundingSphere(): Computed radius is NaN. The \"position\" attribute is likely to have NaN values.", self )

    def computeFaceNormals( self ):

        # backwards compatibility

        pass

    def computeVertexNormals( self ):

        index = self.index
        attributes = self.attributes
        groups = self.groups

        if "position" in attributes:

            positions = attributes[ "position" ].array

            if "normal" not in attributes:

                self.addAttribute( "normal", BufferAttribute( ctypesArray( "f", len( positions ) ), 3 ) )

            else:

                # reset existing normals to zero

                arr = attributes[ "normal" ].array

                for i in xrange( len( arr ) ):

                    arr[ i ] = 0

            normals = attributes[ "normal" ].array

            pA = vector3.Vector3()
            pB = vector3.Vector3()
            pC = vector3.Vector3()
            cb = vector3.Vector3()
            ab = vector3.Vector3()

            # indexed elements

            if index:

                indices = index.array

                if len( groups ) == 0:

                    self.addGroup( 0, len( indices ) )

                for group in groups:

                    start = group.start
                    count = group.count

                    for i in xrange( start, start + count, 3 ):

                        vA = indices[ i + 0 ] * 3
                        vB = indices[ i + 1 ] * 3
                        vC = indices[ i + 2 ] * 3

                        pA.fromArray( positions, vA )
                        pB.fromArray( positions, vB )
                        pC.fromArray( positions, vC )

                        cb.subVectors( pC, pB )
                        ab.subVectors( pA, pB )
                        cb.cross( ab )

                        normals[ vA ] += cb.x
                        normals[ vA + 1 ] += cb.y
                        normals[ vA + 2 ] += cb.z

                        normals[ vB ] += cb.x
                        normals[ vB + 1 ] += cb.y
                        normals[ vB + 2 ] += cb.z

                        normals[ vC ] += cb.x
                        normals[ vC + 1 ] += cb.y
                        normals[ vC + 2 ] += cb.z

            else:

                # non-indexed elements (unconnected triangle soup)

                for i in xrange( 0, len( positions ), 9 ):

                    pA.fromArray( positions, i )
                    pB.fromArray( positions, i + 3 )
                    pC.fromArray( positions, i + 6 )

                    cb.subVectors( pC, pB )
                    ab.subVectors( pA, pB )
                    cb.cross( ab )

                    normals[ i ] = cb.x
                    normals[ i + 1 ] = cb.y
                    normals[ i + 2 ] = cb.z

                    normals[ i + 3 ] = cb.x
                    normals[ i + 4 ] = cb.y
                    normals[ i + 5 ] = cb.z

                    normals[ i + 6 ] = cb.x
                    normals[ i + 7 ] = cb.y
                    normals[ i + 8 ] = cb.z

            self.normalizeNormals()

            attributes[ "normal" ].needsUpdate = True

    def merge( self, geometry, offset = 0 ):

        if not ( geometry is not None and hasattr( geometry, "isBufferGeometry" ) ):

            logging.error( "THREE.BufferGeometry.merge(): geometry not an instance of THREE.BufferGeometry.", geometry )
            return

        attributes = self.attributes

        for key in attributes:

            if geometry.attributes[ key ] is None: continue

            attribute1 = attributes[ key ]
            attributeArray1 = attribute1.array

            attribute2 = geometry.attributes[ key ]
            attributeArray2 = attribute2.array

            attributeSize = attribute2.itemSize

            i = 0
            j = attributeSize * offset
            while i < len( attributeArray2 ):

                attributeArray1[ j ] = attributeArray2[ i ]

                i += 1
                j += 1

        return self

    def normalizeNormals( self ):

        vector = vector3.Vector3()

        normals = self.attributes[ "normal" ]

        for i in xrange( normals.count ):

            vector.x = normals.getX( i )
            vector.y = normals.getY( i )
            vector.z = normals.getZ( i )

            vector.normalize()

            normals.setXYZ( i, vector.x, vector.y, vector.z )

    def toNonIndexed( self ):

        if self.index is None:

            logging.warning( "THREE.BufferGeometry.toNonIndexed(): Geometry is already non-indexed." )
            return self

        geometry2 = BufferGeometry()

        indices = self.index.array
        attributes = self.attributes

        for name in attributes:

            attribute = attributes[ name ]

            array = attribute.array
            itemSize = attribute.itemSize

            array2 = type(array)( [ 0 ] * ( len( indices ) * itemSize ) )

            index = 0
            index2 = 0

            for i in xrange( len( indices ) ):

                index = indices[ i ] * itemSize

                for j in xrange( itemSize ):

                    array2[ index2 ] = array[ index ]
                    index += 1
                    index2 += 1

            geometry2.addAttribute( name, BufferAttribute( array2, itemSize ) )

        return geometry2

    def toJSON( self ):

        data = Expando(
            metadata = Expando(
                version = 4.5,
                type = "BufferGeometry",
                generator = "BufferGeometry.toJSON"
            )
        )

        # standard BufferGeometry serialization

        data.uuid = self.uuid
        data.type = self.type
        if self.name != "": data.name = self.name

        if self.parameters is not None:

            parameters = self.parameters

            for key in parameters:

                if parameters[ key ] is not None: data[ key ] = parameters[ key ]

            return data

        data.data = Expando( attributes = {} )
        index = self.index

        if index is not None:

            array = list( index.array )

            data.data.index = Expando(
                type = index.array.dtype,
                array = array
            )

        attributes = self.attributes

        for key in attributes:

            attribute = attributes[ key ]

            array =list( attribute.array )

            data.data.attributes[ key ] = Expando(
                itemSize = attribute.itemSize,
                type = attribute.array.dtype,
                array = array,
                normalized = attribute.normalized
            )

        groups = self.groups

        if len( groups ) > 0:

            data.data.groups = json.loads( json.dumps( groups ) )

        boundingSphere = self.boundingSphere

        if boundingSphere is not None:

            data.data.boundingSphere = Expando(
                center = boundingSphere.center.toArray(),
                radius = boundingSphere.radius
            )

        return data

    def clone( self ):

        """
         # Handle primitives

         parameters = self.parameters

         if parameters is not None:

         values = []

         for key in parameters:

         values.append( parameters[ key ] )

         geometry = Object.create( self.constructor.prototype )
         self.constructor.apply( geometry, values )
         return geometry

         return self.constructor().copy( self )
         """

        return BufferGeometry().copy( self )

    def copy( self, source ):

        # reset

        self.index = None
        self.attributes = {}
        self.morphAttributes = {}
        self.groups = []
        self.boundingBox = None
        self.boundingSphere = None

        # name

        self.name = source.name

        # index

        index = source.index

        if index is not None:

            self.setIndex( index.clone() )

        # attributes

        attributes = source.attributes

        for name in attributes:

            attribute = attributes[ name ]
            self.addAttribute( name, attribute.clone() )

        # morph attributes

        morphAttributes = source.morphAttributes

        for name in morphAttributes:

            array = []
            morphAttribute = morphAttributes[ name ] # morphAttribute: array of Float32BufferAttributes

            for ma in morphAttribute:

                array.append( ma.clone() )

            self.morphAttributes[ name ] = array

        # groups

        groups = source.groups

        for group in groups:

            self.addGroup( group.start, group.count, group.materialIndex )

        # bounding box

        boundingBox = source.boundingBox

        if boundingBox is not None:

            self.boundingBox = boundingBox.clone()

        # bounding sphere

        boundingSphere = source.boundingSphere

        if boundingSphere is not None:

            self.boundingSphere = boundingSphere.clone()

        # draw range

        self.drawRange.start = source.drawRange.start
        self.drawRange.count = source.drawRange.count

        return self

    def dispose( self ):

        self.dispatchEvent( Expando( type = "dispose" ) )
