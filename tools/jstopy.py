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
    ( "Math.PI", "math.pi" ),
    ( "Math", "math" ),
    ( "\+\+", "+= 1" ),
    ( " = (.*) \? (.*) : ([^\n]*)", " = \g<2> if \g<1> else \g<3>" ),
    ( "if ?\( (.*) \)( {)?", "if \g<1>:" ),
    ( "for ?\( (.*) \)( {)?", "for \g<1>:" ),
]

rulesClass = [
    ( "[^\n]*\.prototype = ", "" ),
    ( "Object\.assign\( [^\n]*\n", "" ),
    ( "([\S]*): function \((.*)\) {", "def \g<1>( self,\g<2>):" ),
    ( "function (.*)\((.*)\) {", "def \g<1>( self,\g<2>):" ),
    ( "\( self,\)", "( self )" )
]

rulesTest = [
    ( "QUnit\.module\( \"(.*)\" \)", "class Test\g<1>( unittest.TestCase ):" ),
    ( "QUnit\.test\( \"(.*)\"[^\n]*", "def test_\g<1>( self ):\n" ),
    ( "(\S*) = function\((.*)\) {", "def \g<1>(\g<2>):\n" ),
    ( "assert\.ok\( (.*) == (.*)", "self.assertEqual( \g<1>, \g<2>" ),
    ( "assert\.ok\( (.*)", "self.assertTrue( \g<1>" ),
    ( "assert.numEqual\( (.*), (.*)", "self.assertAlmostEqual( \g<1>, \g<2>" ),
    ( ", \"(.*)\" \)", " ) # \g<1>" )
]

rulesClean = [
    ( " *\n", "\n" ),
    ( "\n\n\n*", "\n\n" ),
    ( "\n\n$", "\n" )
]

ruleClass = "import { (.*) } from '(.*)';"

jspath = sys.argv[1]
pypath = re.sub( "\.js", ".py", jspath )
test = len( sys.argv ) > 2

jsfile = open( jspath, "r" )
pyfile = open( pypath, "w" )

jstext = jsfile.read()
pytext = jstext

classes = []

for m in re.finditer( ruleClass, pytext ):

    temp = list( m.groups() )
    temp.append( temp[0][0].lower() + temp[0][1:] )
    classes.append( temp )

for rule in rules:

    pytext = re.sub( rule[0], rule[1], pytext )

if not test:

    for rule in rulesClass:

        pytext = re.sub( rule[0], rule[1], pytext )

    for c in classes:

        bef = " " + c[0]
        aft = " " + c[2] + "." + c[0]
        pytext = re.sub( bef, aft, pytext )

    importStatement = ""

    for c in classes:

        s = c[1]
        s = re.sub( "\.\.\/", ".", s )
        s = re.sub( "^(\.*)", "\g<1>.", s)
        s = re.sub( "\/", ".", s )
        s = re.sub( c[0], c[2], s )
        importStatement += "from %s import %s\n" % ( s, c[0] )

    pytext = importStatement + pytext
    
else:

    for rule in rulesTest:

        pytext = re.sub( rule[0], rule[1], pytext )
    

    pytext = "from __future__ import division\n\nimport unittest\n\nimport THREE\n\n" + pytext

for rule in rulesClean:

    pytext = re.sub( rule[0], rule[1], pytext )

pyfile.write( pytext )

jsfile.close()
pyfile.close()