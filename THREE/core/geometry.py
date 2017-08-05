from __future__ import division

import logging

import eventDispatcher
import face3
from ..math import matrix3
from ..math import sphere
from ..math import box3
from ..math import vector3
from ..math import matrix4
from ..math import vector2
from ..math import color
import object3D
from ..math import _Math
from ..utils import Expando
"""
 * @author mrdoob / http:#mrdoob.com/
 * @author kile / http:#kile.stravaganza.org/
 * @author alteredq / http:#alteredqualia.com/
 * @author mikael emtinger / http:#gomo.se/
 * @author zz85 / http:#www.lab4games.net/zz85/blog
 * @author bhouston / http:#clara.io
 """

class Geometry( eventDispatcher.EventDispatcher ):

    GeometryId = 0

    @staticmethod
    def getGeometryId():

        ret = Geometry.GeometryId
        Geometry.GeometryId += 1
        return ret

    def __init__( self ):

        self.isGeometry = True

        self.id = Geometry.getGeometryId()
        self.uuid = _Math.generateUUID()

        self.name = ""
        self.type = "Geometry"

        self.vertices = []
        self.colors = []
        self.faces = []
        self.faceVertexUvs = [[]]

        self.morphTargets = []
        self.morphNormals = []

        self.skinWeights = []
        self.skinIndices = []

        self.lineDistances = []

        self.boundingBox = None
        self.boundingSphere = None

        # update flags

        self.elementsNeedUpdate = False
        self.verticesNeedUpdate = False
        self.uvsNeedUpdate = False
        self.normalsNeedUpdate = False
        self.colorsNeedUpdate = False
        self.lineDistancesNeedUpdate = False
        self.groupsNeedUpdate = False

    def applyMatrix( self, matrix ):

        normalMatrix = matrix3.Matrix3().getNormalMatrix( matrix )

        for vertex in self.vertices:

            vertex.applyMatrix4( matrix )

        for face in self.faces:

            face.normal.applyMatrix3( normalMatrix ).normalize()

            for vertexNormal in face.vertexNormals:

                vertexNormal.applyMatrix3( normalMatrix ).normalize()

        if self.boundingBox is not None:

            self.computeBoundingBox()

        if self.boundingSphere is not None:

            self.computeBoundingSphere()

        self.verticesNeedUpdate = True
        self.normalsNeedUpdate = True

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

    def fromBufferGeometry( self, geometry ):

        indices = geometry.index.array if geometry.index is not None else None
        attributes = geometry.attributes

        positions = attributes[ "position" ].array
        normals = attributes[ "normal" ].array if "normal" in attributes else None
        colors = attributes[ "color" ].array if "color" in attributes else None
        uvs = attributes[ "uv" ].array if "uv" in attributes else None
        uvs2 = attributes[ "uv2" ].array if "uv2" in attributes else None

        if uvs2 is not None:
            
            if 1 >= len( self.faceVertexUvs ): self.faceVertexUvs.append( [] )

            self.faceVertexUvs[ 1 ] = []

        tempNormals = []
        tempUVs = []
        tempUVs2 = []

        i = 0
        j = 0
        while i < len( positions ):

            self.vertices.append( vector3.Vector3( positions[ i ], positions[ i + 1 ], positions[ i + 2 ] ) )

            if normals is not None:

                tempNormals.append( vector3.Vector3( normals[ i ], normals[ i + 1 ], normals[ i + 2 ] ) )

            if colors is not None:

                self.colors.append( color.Color( colors[ i ], colors[ i + 1 ], colors[ i + 2 ] ) )

            if uvs is not None:

                tempUVs.append( vector2.Vector2( uvs[ j ], uvs[ j + 1 ] ) )

            if uvs2 is not None:

                tempUVs2.append( vector2.Vector2( uvs2[ j ], uvs2[ j + 1 ] ) )
            
            i += 3
            j += 2

        def addFace( a, b, c, materialIndex = 0 ):

            vertexNormals = [ tempNormals[ a ].clone(), tempNormals[ b ].clone(), tempNormals[ c ].clone() ] if normals is not None else []
            vertexColors = [ self.colors[ a ].clone(), self.colors[ b ].clone(), self.colors[ c ].clone() ] if colors is not None else []

            face = face3.Face3( a, b, c, vertexNormals, vertexColors, materialIndex )

            self.faces.append( face )

            if uvs is not None:

                self.faceVertexUvs[ 0 ].append( [ tempUVs[ a ].clone(), tempUVs[ b ].clone(), tempUVs[ c ].clone() ] )

            if uvs2 is not None:

                self.faceVertexUvs[ 1 ].append( [ tempUVs2[ a ].clone(), tempUVs2[ b ].clone(), tempUVs2[ c ].clone() ] )

        groups = geometry.groups

        if len( groups ) > 0:
            
            for group in groups:

                start = group.start
                count = group.count

                for j in range( start, start + count, 3 ):

                    if indices is not None:

                        addFace( indices[ j ], indices[ j + 1 ], indices[ j + 2 ], group.materialIndex )

                    else:

                        addFace( j, j + 1, j + 2, group.materialIndex )

        else:

            if indices is not None:

                for i in range( 0, len( indices ), 3 ):

                    addFace( indices[ i ], indices[ i + 1 ], indices[ i + 2 ] )

            else:

                for i in range( 0, len( positions ) // 3, 3 ):

                    addFace( i, i + 1, i + 2 )

        self.computeFaceNormals()

        if geometry.boundingBox is not None:

            self.boundingBox = geometry.boundingBox.clone()

        if geometry.boundingSphere is not None:

            self.boundingSphere = geometry.boundingSphere.clone()

        return self

    def center( self ):

        self.computeBoundingBox()

        offset = self.boundingBox.getCenter().negate()

        self.translate( offset.x, offset.y, offset.z )

        return offset

    def normalize( self ):

        self.computeBoundingSphere()

        center = self.boundingSphere.center
        radius = self.boundingSphere.radius

        s = 1 if radius == 0 else 1.0 / radius

        matrix = matrix4.Matrix4()
        matrix.set(
            s, 0, 0, - s * center.x,
            0, s, 0, - s * center.y,
            0, 0, s, - s * center.z,
            0, 0, 0, 1
        )

        self.applyMatrix( matrix )

        return self

    def computeFaceNormals( self ):

        cb = vector3.Vector3()
        ab = vector3.Vector3()

        for face in self.faces:

            vA = self.vertices[ face.a ]
            vB = self.vertices[ face.b ]
            vC = self.vertices[ face.c ]

            cb.subVectors( vC, vB )
            ab.subVectors( vA, vB )
            cb.cross( ab )

            cb.normalize()

            face.normal.copy( cb )

    def computeVertexNormals( self, areaWeighted = True ):

        vertices = [None] * len ( self.vertices )

        for v in range( len( self.vertices ) ):

            vertices[ v ] = vector3.Vector3()

        if areaWeighted:

            # vertex normals weighted by triangle areas
            # http:#www.iquilezles.org/www/articles/normals/normals.htm

            cb = vector3.Vector3()
            ab = vector3.Vector3()

            for face in self.faces:

                vA = self.vertices[ face.a ]
                vB = self.vertices[ face.b ]
                vC = self.vertices[ face.c ]

                cb.subVectors( vC, vB )
                ab.subVectors( vA, vB )
                cb.cross( ab )

                vertices[ face.a ].add( cb )
                vertices[ face.b ].add( cb )
                vertices[ face.c ].add( cb )

        else:

            self.computeFaceNormals()

            for face in self.faces:

                vertices[ face.a ].add( face.normal )
                vertices[ face.b ].add( face.normal )
                vertices[ face.c ].add( face.normal )

        for v in range( len( self.vertices ) ):

            vertices[ v ].normalize()

        for face in self.faces:

            vertexNormals = face.vertexNormals

            if len( vertexNormals ) == 3:

                vertexNormals[ 0 ].copy( vertices[ face.a ] )
                vertexNormals[ 1 ].copy( vertices[ face.b ] )
                vertexNormals[ 2 ].copy( vertices[ face.c ] )

            else:

                vertexNormals[ 0 ] = vertices[ face.a ].clone()
                vertexNormals[ 1 ] = vertices[ face.b ].clone()
                vertexNormals[ 2 ] = vertices[ face.c ].clone()

        if self.faces.length > 0:

            self.normalsNeedUpdate = True

    def computeFlatVertexNormals( self ):

        self.computeFaceNormals()

        for face in self.faces:

            vertexNormals = face.vertexNormals

            if len( vertexNormals ) == 3:

                vertexNormals[ 0 ].copy( face.normal )
                vertexNormals[ 1 ].copy( face.normal )
                vertexNormals[ 2 ].copy( face.normal )

            else:

                vertexNormals[ 0 ] = face.normal.clone()
                vertexNormals[ 1 ] = face.normal.clone()
                vertexNormals[ 2 ] = face.normal.clone()

        if self.faces.length > 0:

            self.normalsNeedUpdate = True

    def computeMorphNormals( self ):

        # save original normals
        # - create temp variables on first access
        #   otherwise just copy (for faster repeated calls)

        for face in self.faces:

            face = self.faces[ f ]

            if not hasattr( face, "__originalFaceNormal" ):

                face.__originalFaceNormal = face.normal.clone()

            else:

                face.__originalFaceNormal.copy( face.normal )

            if not hasattr( face, "__originalVertexNormals" ): face.__originalVertexNormals = []

            for i in range( len( face.vertexNormals ) ):

                if i >= len( face.__originalVertexNormals ): face.__originalVertexNormals.append( None )

                if face.__originalVertexNormals[ i ] is None:

                    face.__originalVertexNormals[ i ] = face.vertexNormals[ i ].clone()

                else:

                    face.__originalVertexNormals[ i ].copy( face.vertexNormals[ i ] )

        # use temp geometry to compute face and vertex normals for each morph

        tmpGeo = Geometry()
        tmpGeo.faces = self.faces

        for i in range( len( self.morphTargets ) ):

            # create on first access

            if i >= len( self.morphNormals ): self.morphNormals.append( None )

            if self.morphNormals[ i ] is None:

                self.morphNormals[ i ] = {}
                self.morphNormals[ i ].faceNormals = []
                self.morphNormals[ i ].vertexNormals = []

                dstNormalsFace = self.morphNormals[ i ].faceNormals 
                dstNormalsVertex = self.morphNormals[ i ].vertexNormals

                for f in range( len( self.faces ) ):

                    faceNormal = vector3.Vector3()
                    vertexNormals = Expando( a = vector3.Vector3(), b = vector3.Vector3(), c = vector3.Vector3() )
                    dstNormalsFace.push( faceNormal )
                    dstNormalsVertex.push( vertexNormals )

            morphNormals = self.morphNormals[ i ]

            # set vertices to morph target

            tmpGeo.vertices = self.morphTargets[ i ].vertices

            # compute morph normals

            tmpGeo.computeFaceNormals()
            tmpGeo.computeVertexNormals()

            # store morph normals

            faceNormal, vertexNormals

            for f in range( len( self.faces ) ):

                face = self.faces[ f ]

                faceNormal = morphNormals.faceNormals[ f ]
                vertexNormals = morphNormals.vertexNormals[ f ]

                faceNormal.copy( face.normal )

                vertexNormals.a.copy( face.vertexNormals[ 0 ] )
                vertexNormals.b.copy( face.vertexNormals[ 1 ] )
                vertexNormals.c.copy( face.vertexNormals[ 2 ] )

        # restore original normals

        for face in self.faces:

            face.normal = face.__originalFaceNormal
            face.vertexNormals = face.__originalVertexNormals

    def computeLineDistances( self ):

        d = 0
        vertices = self.vertices

        for i in range( len( vertices ) ):

            if i > 0:

                d += vertices[ i ].distanceTo( vertices[ i - 1 ] )

            if i >= len( self.lineDistances ): self.lineDistances.append( 0 )

            self.lineDistances[ i ] = d

    def computeBoundingBox( self ):

        if self.boundingBox is None:

            self.boundingBox = box3.Box3()

        self.boundingBox.setFromPoints( self.vertices )

    def computeBoundingSphere( self ):

        if self.boundingSphere is None:

            self.boundingSphere = sphere.Sphere()

        self.boundingSphere.setFromPoints( self.vertices )

    def merge( self, geometry, matrix, materialIndexOffset ):

        if not ( geometry is not None and hasattr( geometry, "isGeometry" ) ):

            logging.error( "THREE.Geometry.merge(): geometry not an instance of THREE.Geometry.", geometry )
            return

        normalMatrix = None
        vertexOffset = len( self.vertices )
        vertices1 = self.vertices
        vertices2 = geometry.vertices
        faces1 = self.faces
        faces2 = geometry.faces
        uvs1 = self.faceVertexUvs[ 0 ]
        uvs2 = geometry.faceVertexUvs[ 0 ]
        colors1 = self.colors
        colors2 = geometry.colors

        if materialIndexOffset is None: materialIndexOffset = 0

        if matrix is not None:

            normalMatrix = matrix3.Matrix3().getNormalMatrix( matrix )

        # vertices

        for vertex in vertices2:

            vertexCopy = vertex.clone()

            if matrix is not None: vertexCopy.applyMatrix4( matrix )

            vertices1.push( vertexCopy )

        # colors

        for i in range( len( color2 ) ):

            colors1.push( colors2[ i ].clone() )

        # faces

        for face in faces2:

            face = faces2[ i ]
            faceVertexNormals = face.vertexNormals
            faceVertexColors = face.vertexColors

            faceCopy = face3.Face3( face.a + vertexOffset, face.b + vertexOffset, face.c + vertexOffset )
            faceCopy.normal.copy( face.normal )

            if normalMatrix is not None:

                faceCopy.normal.applyMatrix3( normalMatrix ).normalize()

            for normal in faceVerxtexNormals:

                normal = normal.clone()

                if normalMatrix is not None:

                    normal.applyMatrix3( normalMatrix ).normalize()

                faceCopy.vertexNormals.push( normal )

            faceCopy.color.copy( face.color )

            for color in faceVertexColors:

                faceCopy.vertexColors.push( color.clone() )

            faceCopy.materialIndex = face.materialIndex + materialIndexOffset

            faces1.push( faceCopy )

        # uvs

        for uv in uvs2:
            
            uvCopy = []

            if uv is None:

                continue

            for j in range( len( uv ) ):

                uvCopy.push( uv[ j ].clone() )

            uvs1.push( uvCopy )

    def mergeMesh( self, mesh ):

        if not ( mesh is not None and hasattr( mesh, "isMesh" ) ):

            logging.error( "THREE.Geometry.mergeMesh(): mesh not an instance of THREE.Mesh.", mesh )
            return

        if mesh.matrixAutoUpdate: mesh.updateMatrix()

        self.merge( mesh.geometry, mesh.matrix )

    """
     * Checks for duplicate vertices with hashmap.
     * Duplicated vertices are removed
     * and faces" vertices are updated.
     """

    def mergeVertices( self ):

        verticesMap = {} # Hashmap for looking up vertices by position coordinates (and making sure they are unique)
        unique = []
        changes = []

        precisionPoints = 4 # number of decimal points, e.g. 4 for epsilon of 0.0001
        precision = pow( 10, precisionPoints )

        for i in range( len( self.vertices ) ):

            v = self.vertices[ i ]
            key = "%d_%d_%d" % ( round( v.x * precision ), round( v.y * precision ), round( v.z * precision ) )

            if not key in verticesMap:

                verticesMap[ key ] = i
                unique.append( self.vertices[ i ] )
                changes.append( len( unique ) - 1 )

            else:

                #console.log("Duplicate vertex found. ", i, " could be using ", verticesMap[key])
                changes.append( changes[ verticesMap[ key ] ] )

        # if faces are completely degenerate after merging vertices, we
        # have to remove them from the geometry.
        faceIndicesToRemove = []

        for i in range( len( self.faces ) ):

            face = self.faces[ i ]

            face.a = changes[ face.a ]
            face.b = changes[ face.b ]
            face.c = changes[ face.c ]

            indices = [ face.a, face.b, face.c ]

            # if any duplicate vertices are found in a face3.Face3
            # we have to remove the face as nothing can be saved
            for n in range( 3 ):

                if indices[ n ] == indices[ ( n + 1 ) % 3 ]:

                    faceIndicesToRemove.append( i )
                    break

        for i in range( len( faceIndicesToRemove ) - 1, -1, -1 ):

            idx = faceIndicesToRemove[ i ]

            del self.faces[ idx ]

            for faceVertexUv in self.faceVertexUvs:

                del faceVertexUv[ idx ]

        # Use unique set of vertices

        diff = len( self.vertices ) - len( unique )
        self.vertices = unique
        return diff

    def sortFacesByMaterialIndex( self ):

        faces = self.faces
        length = len( faces )

        # tag faces

        for i in range( length ):

            faces[ i ]._id = i

        # sort faces

        faces.sort( materialIndexSort, key = lambda v: v.materialIndex )

        # sort uvs

        uvs1 = self.faceVertexUvs[ 0 ]
        uvs2 = self.faceVertexUvs[ 1 ]

        newUvs1, newUvs2

        if uvs1 and len( uvs1 ) == length: newUvs1 = []
        if uvs2 and len( uvs2 ) == length: newUvs2 = []

        for i in range( length ):

            id = faces[ i ]._id

            if newUvs1: newUvs1.push( uvs1[ id ] )
            if newUvs2: newUvs2.push( uvs2[ id ] )

        if newUvs1: self.faceVertexUvs[ 0 ] = newUvs1
        if newUvs2: self.faceVertexUvs[ 1 ] = newUvs2

    def toJSON( self ):

        data = Expando(
            metadata = Expando(
                version = 4.5,
                type = "Geometry",
                generator = "Geometry.toJSON"
            )
        )

        # standard Geometry serialization

        data.uuid = self.uuid
        data.type = self.type
        if self.name != "": data.name = self.name

        if hasattr( self, "parameters" ):

            parameters = self.parameters

            for key in parameters:

                if parameters[ key ] is not None: data[ key ] = parameters[ key ]

            return data

        vertices = []

        for vertex in self.vertices:

            vertices.push( vertex.x, vertex.y, vertex.z )

        faces = []
        normals = []
        normalsHash = {}
        colors = []
        colorsHash = {}
        uvs = []
        uvsHash = {}

        for i in range( len( self.faces ) ):

            face = self.faces[ i ]

            hasMaterial = True
            hasFaceUv = False # deprecated
            hasFaceVertexUv = self.faceVertexUvs[ 0 ][ i ] is not None
            hasFaceNormal = face.normal.length() > 0
            hasFaceVertexNormal = face.vertexNormals.length > 0
            hasFaceColor = face.color.r != 1 or face.color.g != 1 or face.color.b != 1
            hasFaceVertexColor = face.vertexColors.length > 0

            faceType = 0

            faceType = setBit( faceType, 0, 0 ) # isQuad
            faceType = setBit( faceType, 1, hasMaterial )
            faceType = setBit( faceType, 2, hasFaceUv )
            faceType = setBit( faceType, 3, hasFaceVertexUv )
            faceType = setBit( faceType, 4, hasFaceNormal )
            faceType = setBit( faceType, 5, hasFaceVertexNormal )
            faceType = setBit( faceType, 6, hasFaceColor )
            faceType = setBit( faceType, 7, hasFaceVertexColor )

            faces.push( faceType )
            faces.push( face.a, face.b, face.c )
            faces.push( face.materialIndex )

            if hasFaceVertexUv:

                faceVertexUvs = self.faceVertexUvs[ 0 ][ i ]

                faces.push(
                    getUvIndex( faceVertexUvs[ 0 ] ),
                    getUvIndex( faceVertexUvs[ 1 ] ),
                    getUvIndex( faceVertexUvs[ 2 ] )
                )

            if hasFaceNormal:

                faces.push( getNormalIndex( face.normal ) )

            if hasFaceVertexNormal:

                vertexNormals = face.vertexNormals

                faces.push(
                    getNormalIndex( vertexNormals[ 0 ] ),
                    getNormalIndex( vertexNormals[ 1 ] ),
                    getNormalIndex( vertexNormals[ 2 ] )
                )

            if hasFaceColor:

                faces.push( getColorIndex( face.color ) )

            if hasFaceVertexColor:

                vertexColors = face.vertexColors

                faces.push(
                    getColorIndex( vertexColors[ 0 ] ),
                    getColorIndex( vertexColors[ 1 ] ),
                    getColorIndex( vertexColors[ 2 ] )
                )

        def setBit( self, value, position, enabled ):

            return value | ( 1 << position ) if enabled else value & ( ~ ( 1 << position ) )

        def getNormalIndex( self, normal ):

            hash = str( normal.x ) + str( normal.y ) + str( normal.z )

            if hash in normalsHash:

                return normalsHash[ hash ]

            normalsHash[ hash ] = len( normals ) // 3
            normals.extend( [ normal.x, normal.y, normal.z ] )

            return normalsHash[ hash ]

        def getColorIndex( self, color ):

            hash = str( color.r ) + str( color.g ) + str( color.b )

            if hash in colorsHash:

                return colorsHash[ hash ]

            colorsHash[ hash ] = len( colors )
            colors.push( color.getHex() )

            return colorsHash[ hash ]

        def getUvIndex( self, uv ):

            hash = str( uv.x ) + str( uv.y )

            if has in uvsHash[ hash ]:

                return uvsHash[ hash ]

            uvsHash[ hash ] = len( uvs ) // 2
            uvs.extend( [ uv.x, uv.y ] )

            return uvsHash[ hash ]

        data.data = {}

        data.data.vertices = vertices
        data.data.normals = normals
        if len( colors ) > 0: data.data.colors = colors
        if len( uvs ) > 0: data.data.uvs = [ uvs ] # temporal backward compatibility
        data.data.faces = faces

        return data

    def clone( self ):

        """
         # Handle primitives

         parameters = self.parameters

         if parameters != None:

         values = []

         for key in parameters:

         values.push( parameters[ key ] )

         geometry = Object.create( self.constructor.prototype )
         self.constructor.apply( geometry, values )
         return geometry

         return self.constructor().copy( self )
         """

        return Geometry().copy( self )

    def copy( self, source ):

        # reset

        self.vertices = []
        self.colors = []
        self.faces = []
        self.faceVertexUvs = [[]]
        self.morphTargets = []
        self.morphNormals = []
        self.skinWeights = []
        self.skinIndices = []
        self.lineDistances = []
        self.boundingBox = None
        self.boundingSphere = None

        # name

        self.name = source.name

        # vertices

        vertices = source.vertices

        for vertex in vertices:

            self.vertices.push( vertex.clone() )

        # colors

        colors = source.colors

        for color in colors:

            self.colors.push( color.clone() )

        # faces

        faces = source.faces

        for face in faces:

            self.faces.push( face.clone() )

        # face vertex uvs

        for i in range( len( source.faceVertexUvs ) ):

            faceVertexUvs = source.faceVertexUvs[ i ]

            if i >= len( self.faceVertexUvs ): self.faceVertexUvs.append( [] )

            for uvs in faceVertexUvs:

                uvsCopy = []

                for uv in uvs:

                    uvsCopy.append( uv.clone() )

                self.faceVertexUvs[ i ].append( uvsCopy )

        # morph targets

        morphTargets = source.morphTargets

        for mt in morphTargets:

            morphTarget = {}
            morphTarget.name = mt.name

            # vertices

            if "vertices" in mt:

                morphTarget.vertices = []

                for vertex in mt.vertices:

                    morphTarget.vertices.append( vertex.clone() )

            # normals

            if "normals" in mt:

                morphTarget.normals = []

                for normal in mt.normals:

                    morphTarget.normals.push( normal.clone() )

            self.morphTargets.append( morphTarget )

        # morph normals

        morphNormals = source.morphNormals

        for mn in morphNormals:

            morphNormal = {}
            # vertex normals

            if "vertexNormals" in mn:

                morphNormal.vertexNormals = []

                for srcVertexNormal in mn.vertexNormals:

                    destVertexNormal = {}
                    destVertexNormal.a = srcVertexNormal.a.clone()
                    destVertexNormal.b = srcVertexNormal.b.clone()
                    destVertexNormal.c = srcVertexNormal.c.clone()

                    morphNormal.vertexNormals.append( destVertexNormal )

            # face normals

            if "faceNormals" in mn:

                morphNormal.faceNormals = []

                for faceNormal in mn.faceNormals:

                    morphNormal.faceNormals.append( faceNormal.clone() )

            self.morphNormals.push( morphNormal )

        # skin weights

        skinWeights = source.skinWeights

        for skinWeight in skinWeights:

            self.skinWeights.push( skinWeight.clone() )

        # skin indices

        skinIndices = source.skinIndices

        for skinIndex in skinIndices:

            self.skinIndices.push( skinIndex.clone() )

        # line distances

        lineDistances = source.lineDistances

        for lineDistance in lineDistances:

            self.lineDistances.push( lineDistance )

        # bounding box

        boundingBox = source.boundingBox

        if boundingBox is not None:

            self.boundingBox = boundingBox.clone()

        # bounding sphere

        boundingSphere = source.boundingSphere

        if boundingSphere is not None:

            self.boundingSphere = boundingSphere.clone()

        # update flags

        self.elementsNeedUpdate = source.elementsNeedUpdate
        self.verticesNeedUpdate = source.verticesNeedUpdate
        self.uvsNeedUpdate = source.uvsNeedUpdate
        self.normalsNeedUpdate = source.normalsNeedUpdate
        self.colorsNeedUpdate = source.colorsNeedUpdate
        self.lineDistancesNeedUpdate = source.lineDistancesNeedUpdate
        self.groupsNeedUpdate = source.groupsNeedUpdate

        return self

    def dispose( self ):

        self.dispatchEvent( Expando( type = "dispose" ) )
