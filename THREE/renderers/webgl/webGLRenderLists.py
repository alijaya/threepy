from __future__ import division

import logging

from OpenGL import GL

"""
 * @author mrdoob / "http":#mrdoob.com/
 """

def painterSortStable( a, b ):

    if a.renderOrder != b.renderOrder :

        return a.renderOrder - b.renderOrder

    elif a.program and b.program and a.program != b.program :

        return a.program.id - b.program.id

    elif a.material.id != b.material.id :

        return a.material.id - b.material.id

    elif a.z != b.z :

        return a.z - b.z

    else:

        return a.id - b.id

def reversePainterSortStable( a, b ):

    if a.renderOrder != b.renderOrder :

        return a.renderOrder - b.renderOrder

    elif a.z != b.z :

        return b.z - a.z

    else:

        return a.id - b.id

class WebGLRenderList( object ):

    def __init__( self ):

        self.renderItems = []
        self.renderItemsIndex = 0

        self.opaque = []
        self.transparent = []

    def init( self ):

        self.renderItemsIndex = 0

        self.opaque = []
        self.transparent = []

    def push( self, object, geometry, material, z, group ):

        renderItem = self.renderItems[ self.renderItemsIndex ] if self.renderItemsIndex < len( self.renderItems ) else None

        if renderItem is None :

            renderItem = {
                "id": object.id,
                "object": object,
                "geometry": geometry,
                "material": material,
                "program": getattr( material, "program", None ),
                "renderOrder": object.renderOrder,
                "z": z,
                "group": group
            }

            while self.renderItemsIndex >= len( self.renderItems ) : self.renderItems.append( None )
            self.renderItems[ self.renderItemsIndex ] = renderItem

        else:

            renderItem.id = object.id
            renderItem.object = object
            renderItem.geometry = geometry
            renderItem.material = material
            renderItem.program = getattr( material, "program", None )
            renderItem.renderOrder = object.renderOrder
            renderItem.z = z
            renderItem.group = group

        ( self.transparent if material.transparent == True else self.opaque ).append( renderItem )

        self.renderItemsIndex += 1

    def sort( self ):

        if len( self.opaque ) > 1 : sorted( self.opaque, cmp = painterSortStable )
        if len( self.transparent ) > 1 : sorted( self.transparent, cmp = reversePainterSortStable )

class WebGLRenderLists( object ):

    def __init__( self ):

        self.lists = {}

    def get( self, scene, camera ):

        hash = "%s,%s" % ( scene.id, camera.id )
        list = self.lists.get( hash )

        if list is None :

            # logging.info( ""THREE.WebGLRenderLists":", hash )

            list = WebGLRenderList()
            self.lists[ hash ] = list

        return list

    def dispose( self ):

        self.lists = {}
