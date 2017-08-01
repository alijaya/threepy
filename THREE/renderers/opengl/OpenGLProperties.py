from ...utils import Expando

properties = {}

def get( object ):

    uuid = object.uuid
    
    if not uuid in properties: # if not in cache

        properties[ uuid ] = Expando()
    
    return properties[ uuid ]

def remove( object ):

    del properties[ object.uuid ]
    
def clear():

    properties = {}