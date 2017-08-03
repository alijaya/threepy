import Cache
import loadingManager

class FileLoader( object ):

    def __init__( self, manager = None ):

        self.manager = manager or loadingManager.DefaultLoadingManager
        self.path = None

    def load( self, url = "", onLoad = None, onProgress = None, onError = None ):

        if self.path: url = self.path + url

        cached = Cache.get( url )

        if cached:

            self.manager.itemStart( url )
            if onLoad: onLoad( cached )
            self.manager.itemEnd( url )

            return cached

        try:

            self.manager.itemStart( url )
            cached = open( url, "rb" )

        except IOError as error:

            if onErorr: onError( error )

            self.manager.itemEnd( url )
            self.manager.itemError( url )

        if onProgress: onProgress()

        Cache.add( url, cached )

        if onLoad: onLoad( cached )

        self.manager.itemEnd( url )

        return cached

    def setPath( self, value ):

        self.path = value
        return self