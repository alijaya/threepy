import sys
import re

rules = [
    ( "\t", "    " ),
    ( "var ", "" ),
    ( "new ", "" ),
    ( ";", "" ),
    ( "import [^\n]*\n", "" ),
    ( "export [^\n]*\n", "" ),
    ( " *}\n", "" ),
    ( " *},\n", "" ),
    ( " *}\(\)\n", "" ),
    ( " *}\(\),\n", "" ),
    ( " *}\)\n", "" ),
    ( " *} \)\n", "" ),
    ( "true", "True" ),
    ( "false", "False" ),
    ( "===", "==" ),
    ( "!==", "!=" ),
    ( "!([^=])", "not\g<1>" ),
    ( "'", "\"" ),
    ( "null", "None" ),
    ( "undefined", "None" ),
    ( "//", "#" ),
    ( "\|\|", "or" ),
    ( "&&", "and" ),
    ( "this", "self" ),
    ( "Math.abs", "abs" ),
    ( "Math.round", "round" ),
    ( "Math.max", "max" ),
    ( "Math.min", "min" ),
    ( "Math", "math" ),
    ( "\+\+", "+= 1" ),
    ( " = (.*) \? (.*) : ([^\n]*)", " = \g<2> if \g<1> else \g<3>" ),
    ( "if ?\( (.*) \)( {)?", "if \g<1>:" ),
    ( "for ?\( (.*) \)( {)?", "for \g<1>:" ),
]

rulesClass = [
    ( "Object\.assign\( [^\n]*\n", "" ),
    ( "([\S]*): function \((.*)\) {", "def \g<1>( self,\g<2>):" ),
    ( "function (.*)\((.*)\) {", "def \g<1>( self,\g<2>):" ),
    ( "\( self,\)", "( self )" )
]

rulesTest = [
    ( "QUnit\.module\( \"(.*)\" \)", "class Test\g<1>( unittest.TestCase ):" ),
    ( "QUnit\.test\( \"(.*)\"[^\n]*", "def test_\g<1>( self ):\n" ),
    ( "(\S*) = function\((.*)\) {", "def \g<1>(\g<2>):\n" ),
    ( "assert\.ok\( (.*) == (.*), \"(.*)\" \)", "self.assertEqual( \g<1>, \g<2> ) # \g<3>" ),
    ( "assert\.ok\( (.*) == (.*) \)", "self.assertEqual( \g<1>, \g<2> )" ),
    ( "assert\.ok\( (.*), \"(.*)\" \)", "self.assertTrue( \g<1> ) # \g<2>" ),
    ( "assert\.ok\( (.*) \)", "self.assertTrue( \g<1> )" )
]

rulesClean = [
    ( " *\n", "\n" ),
    ( "\n\n\n*", "\n\n" ),
    ( "\n\n$", "\n" )
]

jspath = sys.argv[1]
pypath = sys.argv[2]
test = len( sys.argv ) > 3

jsfile = open( jspath, "r" )
pyfile = open( pypath, "w" )

jstext = jsfile.read()
pytext = jstext

for rule in rules:

    pytext = re.sub( rule[0], rule[1], pytext )

if not test:

    for rule in rulesClass:

        pytext = re.sub( rule[0], rule[1], pytext )
    
else:

    for rule in rulesTest:

        pytext = re.sub( rule[0], rule[1], pytext )

for rule in rulesClean:

    pytext = re.sub( rule[0], rule[1], pytext )

if test:

    pytext = "from __future__ import division\n\nimport unittest\n\nimport THREE\n\n" + pytext

pyfile.write( pytext )

jsfile.close()
pyfile.close()