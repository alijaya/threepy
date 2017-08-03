class LoadingManager( object ):

    def __init__( self, onLoad = None, onProgress = None, onError = None ):

        self.isLoading = False
        self.itemsLoaded = 0
        self.itemsTotal = 0

        self.onStart = None
        self.onLoad = onLoad
        self.onProgress = onProgress
        self.onError = onError

    def itemStart( self, url ):

        self.itemsTotal += 1

        if self.isLoading == False:

            if self.onStart: self.onStart( url, self.itemsLoaded, self.itemsTotal )
        
        self.isLoading = True

    def itemEnd( self, url ):

        self.itemsLoaded += 1

        if self.onProgress: self.onProgress( url, self.itemsLoaded, self.itemsTotal )

        if self.itemsLoaded == self.itemsTotal:

            self.isLoading = False

            if self.onLoad:

                self.onLoad()

    def itemError( self, url ):

        if self.onError: self.onError( url )
    
DefaultLoadingManager = LoadingManager()