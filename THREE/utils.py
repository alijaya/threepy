class Expando( object ):

    def __init__( self, *args, **kwargs ):

        self.__dict__.update( kwargs )
    
    def __getattr__( self, name ):

        return self.__dict__.get( name )

    def __setattr__( self, name, value ):

        self.__dict__[ name ] = value

    def __delattr__( self, name ):

        del self.__dict__[ name ]

    def __getitem__( self, key ):

        return self.__dict__.get( key )

    def __setitem__( self, key, value ):

        self.__dict__[ key ] = value

    def __delitem__( self, key ):

        del self.__dict__[ key ]

    def __iter__( self ):

        return self.__dict__.iterkeys()

    def __contains__( self, key ):

        return key in self.__dict__

    def __str__( self ):

        return self.__dict__.__str__()