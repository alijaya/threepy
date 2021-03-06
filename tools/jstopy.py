import sys
import re

rules = [
    ( "\t", "    " ),
    ( "var ", "" ),
    ( "new ", "" ),
    ( "delete ", "del " ),
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
    ( "== None", "is None" ),
    ( "!= None", "is not None" ),
    ( "//", "#" ),
    ( "\|\|", "or" ),
    ( "&&", "and" ),
    ( "this", "self" ),
    ( "Infinity", "float( \"inf\" )" ),
    ( "Math\.pow", "pow" ),
    ( "Math\.abs", "abs" ),
    ( "Math\.round", "round" ),
    ( "Math\.max", "max" ),
    ( "Math\.min", "min" ),
    ( "Math\.PI", "math.pi" ),
    ( "Math", "math" ),
    ( "_math", "_Math" ),
    ( "isNaN", "math.isnan" ),
    ( "Number.EPSILON", "sys.float_info.epsilon" ),
    ( "(\S+)\.length", "len( \g<1> )" ),
    ( "\.push", ".append" ),
    ( "console\.log", "logging.info" ),
    ( "console\.warn", "logging.warning" ),
    ( "console\.error", "logging.error" ),
    ( "throw ", "raise " ),
    ( "\/\*\*", "\"\"\"" ),
    ( "\/\*", "\"\"\"" ),
    ( "\*\/", "\"\"\"" ),
    ( "\+\+", "+= 1" ),
    ( "--", "-= 1" ),
    ( " ?= ?(.*?) ?\? ?(.*?) ?: ?([^\n]*)", " = \g<2> if \g<1> else \g<3>" ),
    ( "(\S+) ?:", "\"\g<1>\":" ),
    ( "if ?\( ?(.*) ?\)( {)?", "if \g<1>:" ),
    ( "} ?else if", "elif" ),
    ( "} ?else ?{", "else:" ),
    ( "for ?\( ?(.*) ?\)( {)?", "for \g<1>:" ),
]

rulesClass = [
    ( "[^\n]*\.prototype = ", "" ),
    ( "Object\.assign\( [^\n]*", "" ),
    ( "\"([\S]*)\": function ?\((.*)\) {", "def \g<1>( self,\g<2>):" ),
    ( "function ?(.*)\((.*)\) {", "def \g<1>( self,\g<2>):" ),
    ( "\( self,\)", "( self )" ),
    ( "(\S+)\.(is\S+)", "hasattr( \g<1>, \"\g<2>\" )" )
]

rulesTest = [
    ( "QUnit\.module ?\( ?\"(.*)\" ?\)", "class Test\g<1>( unittest.TestCase ):" ),
    ( "QUnit\.test ?\( ?\"(.*)\"[^\n]*", "def test_\g<1>( self ):\n" ),
    ( "(\S*) = function ?\( ?(.*) ?\) {", "def \g<1>( \g<2> ):\n" ),
    ( "function (\S*) ?\( ?(.*) ?\) {", "def \g<1>( \g<2> ):\n" ),
    ( "assert\.ok ?\( ?(.*) == (.*)", "self.assertEqual( \g<1>, \g<2>" ),
    ( "assert\.ok ?\( ?(.*)", "self.assertTrue( \g<1>" ),
    ( "assert.numEqual ?\( ?(.*), (.*)", "self.assertAlmostEqual( \g<1>, \g<2>" ),
    ( ", ?\"(.*)\" ?\)", " ) # \g<1>" )
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
        s = re.sub( "\.\/", "", s )
        s = re.sub( "^(\.+)", "\g<1>.", s)
        s = re.sub( "\/", ".", s )
        s = re.sub( "\." + c[0], "", s )

        if s == c[0]:

            importStatement += "import %s\n" % c[2]
        
        else:

            importStatement += "from %s import %s\n" % ( s, c[2] )

    pytext = importStatement + pytext

    # OpenGL

    pytext = re.sub( "gl\.([A-Z])", "GL.GL_\g<1>", pytext )
    pytext = re.sub( "gl\.([a-z])", lambda pat: "GL.gl" + pat.group(1).upper(), pytext )
    
else:

    for rule in rulesTest:

        pytext = re.sub( rule[0], rule[1], pytext )
    

    pytext = "from __future__ import division\nimport math\n\nimport unittest\n\nimport THREE\n\n" + pytext

for rule in rulesClean:

    pytext = re.sub( rule[0], rule[1], pytext )

pyfile.write( pytext )

jsfile.close()
pyfile.close()