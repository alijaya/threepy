enabled = False
files = {}

def add( key, file ):

    if enabled == False: return

    files[ key ] = file

def get( key ):

    if enabled == False: return

    return files.get( key )

def remove( key ):

    del files[ key ]

def clear():

    global files
    files = {}