import sys
import re

rules = [
    ( "\t", "    " ),
    ( "var ", "" ),
    ( "new ", "" ),
    ( ";", "" ),
    ( "import [^\n]*\n", "" ),
    ( "export [^\n]*\n", "" ),
    ( "Object\.assign\( [^\n]*\n", "" ),
    ( "}\n", "" ),
    ( "},\n", "" ),
    ( "}\(\)\n", "" ),
    ( "}\(\),\n", "" ),
    ( "} \)\n", "" ),
    ( "true", "True" ),
    ( "false", "False" ),
    ( "===", "==" ),
    ( "!==", "!=" ),
    ( "null", "None" ),
    ( "undefined", "None" ),
    ( "//", "#" ),
    ( "\|\|", "or" ),
    ( "&&", "and" ),
    ( "this", "self" ),
    ( "\+\+", "+= 1" ),
    ( " = (.*) \? (.*) : ([^\n]*)", " = \g<2> if \g<1> else \g<3>" ),
    ( "if \( (.*) \)( {)?", "if \g<1>:" ),
    ( "for \( (.*) \)( {)?", "for \g<1>:" ),
    ( "([\S]*): function \((.*)\) {", "def \g<1>( self,\g<2>):" ),
    ( "function (.*)\((.*)\) {", "def \g<1>( self,\g<2>):" ),
    ( "\( self,\)", "( self )" ),
    ( " *\n", "\n" ),
    ( "\n\n\n*", "\n\n" ),
    ( "\n\n$", "\n" )
]

jspath = sys.argv[1]
pypath = sys.argv[2]

jsfile = open( jspath, "r" )
pyfile = open( pypath, "w" )

jstext = jsfile.read()
pytext = jstext

for rule in rules:

    pytext = re.sub( rule[0], rule[1], pytext )

pyfile.write( pytext )

jsfile.close()
pyfile.close()