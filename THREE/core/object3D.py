import json
import logging

from ..math import _Math
from ..math import vector3
from ..math import euler
from ..math import quaternion
from ..math import matrix4
from ..math import matrix3
from ..utils import Expando

import eventDispatcher
import layers

class Object3D( eventDispatcher.EventDispatcher ):

    DefaultUp = vector3.Vector3( 0, 1, 0 )
    DefaultMatrixAutoUpdate = True

    Object3DId = 0

    @staticmethod
    def getObject3DId():

        ret = Object3D.Object3DId
        Object3D.Object3DId += 1
        return ret

    def __init__( self ):

        self.id = Object3D.getObject3DId()

        self.uuid = _Math.generateUUID()

        self.name = ""
        self.type = "Object3D"

        self.parent = None
        self.children = []

        self.up = Object3D.DefaultUp.clone()

        self.position = vector3.Vector3()
        self.rotation = euler.Euler()
        self.quaternion = quaternion.Quaternion()
        self.scale = vector3.Vector3( 1, 1, 1 )

        def onRotationChange():
            
            self.quaternion.setFromEuler( self.rotation, False )
        
        def onQuaternionChange():

            self.rotation.setFromQuaternion( self.quaternion, None, False )

        self.rotation.onChange( onRotationChange )
        self.quaternion.onChange( onQuaternionChange )

        self.modelViewMatrix = matrix4.Matrix4()
        self.normalMatrix = matrix3.Matrix3()

        self.matrix = matrix4.Matrix4()
        self.matrixWorld = matrix4.Matrix4()

        self.matrixAutoUpdate = Object3D.DefaultMatrixAutoUpdate
        self.matrixWorldNeedsUpdate = False

        self.layers = layers.Layers()
        self.visible = True

        self.castShadow = False
        self.receiveShadow = False

        self.frustumCulled = True
        self.renderOrder = 0

        self.userData = {}

        self.isObject3D = True

        self.onBeforeRender = lambda *args: None
        self.onAfterRender = lambda *args: None

    def applyMatrix( self, matrix ):

        self.matrix.multiplyMatrices( matrix, self.matrix )

        self.matrix.decompose( self.position, self.quaternion, self.scale )
    
    def applyQuaternion( self, q ):

        self.quaternion.premultiply( q )

        return self

    def setRotationFromAxisAngle( self, axis, angle ):

        # assumes axis is normalized

        self.quaternion.setFromAxisAngle( axis, angle )

    def setRotationFromEuler( self, euler ):

        self.quaternion.setFromEuler( euler, True )
    
    def setRotationFromMatrix( self, m ):

        # assumes the upper 3x3 of m is a pure rotation matrix (i.e, unscaled)

        self.quaternion.setFromRotationMatrix( m )

    def setRotationFromQuaternion( self, q ):

        # assumes q is normalized

        self.quaternion.copy( q )

    def rotateOnAxis( self, axis, angle ):

        q1 = quaternion.Quaternion()

        q1.setFromAxisAngle( axis, angle )

        self.quaternion.multiply( q1 )

        return self

    def rotateX( self, angle ):

        v1 = vector3.Vector3( 1, 0, 0 )

        return self.rotateOnAxis( v1, angle )

    def rotateY( self, angle ):

        v1 = vector3.Vector3( 0, 1, 0 )

        return self.rotateOnAxis( v1, angle )

    def rotateZ( self, angle ):
        
        v1 = vector3.Vector3( 0, 0, 1 )

        return self.rotateOnAxis( v1, angle )

    def translateOnAxis( self, axis, distance ):

        v1 = vector3.Vector3()

        v1.copy( axis ).applyQuaternion( self.quaternion )

        self.position.add( v1.multiplyScalar( distance ) )

        return self

    def translateX( self, distance ):

        v1 = vector3.Vector3( 1, 0, 0 )

        return self.translateOnAxis( v1, distance )

    def translateY( self, distance ):

        v1 = vector3.Vector3( 0, 1, 0 )

        return self.translateOnAxis( v1, distance )

    def translateZ( self, distance ):

        v1 = vector3.Vector3( 0, 0, 1 )

        return self.translateOnAxis( v1, distance )

    def localToWorld( self, vector ):

        return vector.applyMatrix4( this.matrixWorld )

    def worldToLocal( self, vector ):

        m1 = matrix4.Matrix4()

        return vector.applyMatrix4( m1.getInverse( this.matrixWorld ) )

    def lookAt( self, vector ):

        m1 = matrix4.Matrix4()

        if hasattr( self, "isCamera" ):

            m1.lookAt( self.position, vector, self.up )
        
        else:

            m1.lookAt( vector, self.position, self.up )

        self.quaternion.setFromRotationMatrix( m1 )

    def add( self, *objects ):

        for object in objects:

            if object == self:

                logging.error( "THREE.Object3D.add: object can't be added as a child of itself.", object )
                continue

            if object != None and object.isObject3D:

                if object.parent != None:

                    object.parent.remove( object )
                
                object.parent = self
                object.dispatchEvent( { type: "added" } )

                self.children.append( object )
            
            else:

                logging.error( "THREE.Object3D.add: object not an instance of THREE.Object3D.", object )
                continue
        
        return self

    def remove( self, *objects ):

        for object in objects:

            if object in self.children:

                object.parent = None

                object.dispatchEvent( { type: "removed" } )

                self.children.remove( object )
        
        return self

    def getObjectById( self, id ):

        return self.getObjectByProperty( "id", id )

    def getObjectByName( self, name ):

        return self.getObjectByProperty( "name", name )

    def getObjectByProperty( self, name, value ):

        if getattr( self, name ) == value: return this

        for child in self.children:

            object = child.getObjectByProperty( name, value )

            if object is not None:

                return object

        return None

    def getWorldPosition( self, optionalTarget=None ):

        result = optionalTarget or vector3.Vector3()

        self.updateMatrixWorld( True )

        return result.setFromMatrixPosition( this.matrixWorld )

    def getWorldQuaternion( self, optionalTarget=None ):

        result = optionalTarget or quaternion.Quaternion()

        position = vector3.Vector3()
        scale = vector3.Vector3()

        self.updateMatrixWorld( True )

        self.matrixWorld.decompose( position, result, scale )

        return result

    def getWorldRotation( self, optionalTarget=None ):

        result = optionalTarget or euler.Euler()

        q = quaternion.Quaternion()

        self.getWorldQuaternion( q )

        return result.setFromQuaternion( q, self.rotation.order, False )

    def getWorldScale( self, optionalTarget ):

        result = optionalTarget or vector3.Vector3()

        position = vector3.Vector3()
        quaternion = quaternion.Quaternion()

        self.updateMatrixWorld( True )

        self.matrixWorld.decompose( position, quaternion, result )

        return result

    def getWorldDirection( self, optionalTarget ):

        result = optionalTarget or vector3.Vector3()

        quaternion = quaternion.Quaternion()

        self.getWorldQuaternion( quaternion )

        return result.set( 0, 0, 1 ).applyQuaternion( quaternion )

    def raycast( self ):

        pass
    
    def traverse( self, callback ):

        callback( self )

        for child in self.children:

            child.traverse( callback )
    
    def traverseVisible( self, callback ):

        if self.visible == False: return

        callback( this )

        for child in self.children:

            child.traverseVisible( callback )
    
    def traverseAncestors( self, callback ):

        parent = self.parent

        if parent is not None:

            callback( parent )

            parent.traverseAncestors( callback )
    
    def updateMatrix( self ):

        self.matrix.compose( self.position, self.quaternion, self.scale )

        self.matrixWorldNeedsUpdate = True
    
    def updateMatrixWorld( self, force = False ):

        if self.matrixAutoUpdate: self.updateMatrix()

        if self.matrixWorldNeedsUpdate or force:

            if self.parent is None:

                self.matrixWorld.copy( self.matrix )
            
            else:

                self.matrixWorld.multiplyMatrices( self.parent.matrixWorld, self.matrix )

            self.matrixWorldNeedsUpdate = False
            
            force = True
        
        # update children

        for child in self.children:

            child.updateMatrixWorld( force )
    
    def toJSON( self, meta ):

        # meta is '' when called from JSON.stringify
        isRootObject = meta is None or meta == ""

        output = {}

        # meta is a hash used to collect geometries, materials.
        # not providing it implies that this is the root object
        # being serialized.
        if isRootObject:

            meta = Expando(
                geometries = {},
                materials = {},
                textures = {},
                images = {}
            )

            output.metadata = Expando(
                version = 4.5,
                type = "Object",
                generator = "Object3D.toJSON"
            )
        
        object = Expando()

        object.uuid = self.uuid
        object.type = self.type

        if self.name != "": object.name = self.name
        if json.dumps( self.userdata ) != "{}": object.userdata = self.userData
        if self.castShadow == True: object.castShadow = True
        if self.receiveShadow == True: object.receiveShadow = True
        if self.visible == False: object.visible = False

        object.matrix = self.matrix.toArray()

        #

        def serialize( library, element ):

            if element.uuid not in library:

                library[ element.uuid ] = element.toJSON( meta )
            
            return element.uuid

        if self.geometry is not None:

            object.geometry = serialize( meta.geometries, self.geometry )
        
        if self.material is not None:

            if isinstance( self.material, list ):

                uuids = []

                for mat in self.material:

                    uuids.append( serialize( meta.materials, mat ) )
                
                object.material = uuids
            
            else:

                object.material = serialize( meta.materials, self.material )
        
        #

        if len( self.children ) > 0:

            object.children = []

            for child in self.children:

                object.children.append( child.toJSON( meta ).object )

        if isRootObject:

            geometries = extractFromCache( meta.geometries )
            materials = extractFromCache( meta.materials )
            textures = extractFromCache( meta.textures )
            images = extractFromCache( meta.images )

            if len( geometries ) > 0: output.geometries = geometries
            if len( materials ) > 0: output.materials = materials
            if len( textures ) > 0: output.textures = textures
            if len( images ) > 0: output.images = images
        
        output.object = object

        return output

        # extract data from the cache hash
        # remove metadata on each item
        # and return as array
        def extractFromCache( cache ):

            values = []
            for key in cache:

                data = cache[ key ]
                del data.metadata
                values.append( data )
            
            return values
    
    def clone( self, recursive = True ):

        return Object3D().copy( self, recursive )

    def copy( self, source, recursive = True ):

        self.name = source.name

        self.up.copy( source.up )

        self.position.copy( source.position )
        self.quaternion.copy( source.quaternion )
        self.scale.copy( source.scale )

        self.matrix.copy( source.matrix )
        self.matrixWorld.copy( source.matrixWorld )

        self.matrixAutoUpdate = source.matrixAutoUpdate
        self.matrixWorldNeedsUpdate = source.matrixWorldNeedsUpdate

        self.layers.mask = source.layers.mask
        self.visible = source.visible

        self.castShadow = source.castShadow
        self.receiveShadow = source.receiveShadow

        self.frustumCulled = source.frustumCulled
        self.renderOrder = source.renderOrder

        self.userData = json.loads( json.dumps( source.userData ) )

        if recursive == True:

            for child in source.children:

                self.add( child.clone() )
        
        return self
