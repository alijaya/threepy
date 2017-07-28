class Layers( object ):

    def __init__( self ):

        self.mask = 1 | 0

    def set( self, channel ):

        self.mask = 1 << channel | 0

    def enable( self, channel ):

        self.mask |= 1 << channel | 0

    def toggle( self, channel ):

        self.mask ^= 1 << channel | 0

    def disable( self, channel ):

        self.mask &= ~ ( 1 << channel | 0 )

    def test( self, layers ):

        return ( self.mask & layers.mask ) != 0
