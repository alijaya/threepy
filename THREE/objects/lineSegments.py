import line

"""
 * @author mrdoob / http://mrdoob.com/
 """

class LineSegments( line.Line ):

    def __init__( self, geometry = None, material = None ):

        super( LineSegments, self ).__init__( geometry, material )

        self.isLineSegments = True

        self.type = "LineSegments"