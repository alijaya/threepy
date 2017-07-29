from ..core import object3D

"""
 * @author mrdoob / http:#mrdoob.com/
 """

class Scene( object3D.Object3D ):

    def __init__( self ):

        super( Scene, self ).__init__()

        self.type = "Scene"

        self.background = None
        self.fog = None
        self.overrideMaterial = None

        self.autoUpdate = True # checked by the renderer
    
    def clone( self ):

        return Scene().copy( self )

    def copy( self, source, recursive = True ):

        super( Scene, self ).copy( source, recursive )

        if source.background is not None: self.background = source.background.clone()
        if source.fog is not None: self.fog = source.fog.clone()
        if source.overrideMaterial is not None: self.overrideMaterial = source.overrideMaterial.clone()

        self.autoUpdate = source.autoUpdate
        self.matrixAutoUpdate = source.matrixAutoUpdate

        return self

    def toJSON( self, meta ):

        data = super( Scene, self ).toJSON( meta )

        if self.background != None: data.object.background = self.background.toJSON( meta )
        if self.fog != None: data.object.fog = self.fog.toJSON()

        return data
