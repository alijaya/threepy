from ..math import color
from ..math import vector3

"""
 * @author mrdoob / http:#mrdoob.com/
 * @author alteredq / http:#alteredqualia.com/
 """

class Face3( object ):

    def __init__( self, a, b, c, normal = None, col = None, materialIndex = 0 ):

        self.a = a
        self.b = b
        self.c = c

        self.normal = normal if ( normal is not None and hasattr( normal, "isVector3" ) ) else vector3.Vector3()
        self.vertexNormals = normal if isinstance( normal, list ) else []

        self.color = col if ( col is not None and hasattr( col, "isColor" ) ) else color.Color()
        self.vertexColors = col if isinstance( col, list ) else []

        self.materialIndex = materialIndex

    def clone( self ):

        return Face3( 0, 0, 0 ).copy( self )

    def copy( self, source ):

        self.a = source.a
        self.b = source.b
        self.c = source.c

        self.normal.copy( source.normal )
        self.color.copy( source.color )

        self.materialIndex = source.materialIndex

        for i in xrange( len( source.vertexNormals ) ):

            self.vertexNormals[ i ] = source.vertexNormals[ i ].clone()

        for i in xrange( len( source.vertexColors ) ):

            self.vertexColors[ i ] = source.vertexColors[ i ].clone()

        return self
