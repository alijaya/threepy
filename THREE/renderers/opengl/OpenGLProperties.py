properties = {}

def get( object ):

    uuid = object.uuid
    
    if not uuid in properties: # if not in cache

        properties[ uuid ] = {}
    
    return properties[ uuid ]

def remove( object ):

    del properties[ object.uuid ]
    
def clear():

    properties = {}