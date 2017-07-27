class EventDispatcher( object ):

    def __init__( self ):
        
        self._listeners = None

    def addEventListener( self, type, listener ):

        if self._listeners is None: self._listeners = {}

        listeners = self._listeners

        if type not in listeners:

            listeners[ type ] = []

        if listener not in listeners[ type ]:

            listeners[ type ].append( listener )
    
    def hasEventListener( self, type, listener ):

        if self._listeners is None: return False

        listeners = self._listeners

        return type in listeners and listener in listeners[ type ]

    def removeEventListener( self, type, listener ):

        if self._listeners is None: return

        listeners = self._listeners
        
        if type in listeners and listener in listeners[ type ]:

            listeners[ type ].remove( listener )
    
    def dispatchEvent( self, event ):

        if self._listeners is None: return

        listeners = self._listeners

        if event[ "type" ] in listeners:

            event[ "target" ] = self

            array = list( listeners[ event[ "type" ] ] )

            for item in array:

                item( event )