from ...utils import Expando

def painterSortStable( a, b ):

    ret = 0

    if a.renderOrder != b.renderOrder:

        ret = a.renderOrder - b.renderOrder

    elif a.program and b.program and a.program != b.program:

        ret = a.program.id - b.program.id

    elif a.material.id != b.material.id:

        ret = a.material.id - b.material.id

    elif a.z != b.z:

        ret = a.z - b.z

    else:

        ret = a.id - b.id

    return 1 if ret > 0 else -1 if ret < 0 else 0

def reversePainterSortStable( a, b ):

    ret = 0

    if a.renderOrder != b.renderOrder:

        ret = a.renderOrder - b.renderOrder

    elif a.z != b.z:

        ret = b.z - a.z

    else:

        ret = a.id - b.id
        
    return 1 if ret > 0 else -1 if ret < 0 else 0

class OpenGLRenderList( object ):

    def __init__( self ):

        self.renderItems = []

        self.opaque = []
        self.transparent = []

    def init( self ):

        self.renderItems = []
        
        self.opaque = []
        self.transparent = []

    def push( self, object, geometry, material, z, group ):

        renderItem = Expando(
            id = object.id,
            object = object,
            geometry = geometry,
            material = material,
            program = getattr( material, "program", None ),
            renderOrder = object.renderOrder,
            z = z,
            group = group
        )

        if material.transparent: self.transparent.append( renderItem )
        else: self.opaque.append( renderItem )

        self.renderItems.append( renderItem )

    def sort( self ):

        self.opaque.sort( cmp = painterSortStable )
        self.opaque.sort( cmp = reversePainterSortStable )

###

lists = {}

def get( scene, camera ):

    hash = "%s,%s" % ( scene.id, camera.id )

    if hash in lists: return lists[ hash ]
    
    list = OpenGLRenderList()
    lists[ hash ] = list

    return list

def dispose():

    lists = {}