import unittest

import THREE

class TestEventDispatcher( unittest.TestCase ):

	def test_addEventListener( self ):

		eventDispatcher = THREE.EventDispatcher()

		listener = {}
		eventDispatcher.addEventListener( "anyType", listener )

		self.assertEqual( len( eventDispatcher._listeners[ "anyType" ] ), 1 ) # listener with unknown type was added
		self.assertEqual( eventDispatcher._listeners[ "anyType" ][ 0 ], listener ) # listener with unknown type was added

		eventDispatcher.addEventListener( "anyType", listener )

		self.assertEqual( len( eventDispatcher._listeners[ "anyType" ] ), 1 ) # can't add one listener twice to same type
		self.assertEqual( eventDispatcher._listeners[ "anyType" ][ 0 ], listener ) # listener is still there

	def test_hasEventListener( self ):

		eventDispatcher = THREE.EventDispatcher()

		listener = {}
		eventDispatcher.addEventListener( "anyType", listener )

		self.assertTrue( eventDispatcher.hasEventListener( "anyType", listener ) ) # listener was found
		self.assertFalse( eventDispatcher.hasEventListener( "anotherType", listener ) ) # listener was not found which is good

	def test_removeEventListener( self ):

		eventDispatcher = THREE.EventDispatcher()

		listener = {}

		self.assertIsNone( eventDispatcher._listeners ) # there are no listeners by default

		eventDispatcher.addEventListener( "anyType", listener )
		self.assertTrue( len( eventDispatcher._listeners ) == 1 and \
			len( eventDispatcher._listeners[ "anyType" ] ) == 1 ) # if a listener was added, there is a key

		eventDispatcher.removeEventListener( "anyType", listener )
		self.assertEqual( len( eventDispatcher._listeners[ "anyType" ] ), 0 ) # listener was deleted

		eventDispatcher.removeEventListener( "unknownType", listener )
		self.assertFalse( "unknownType" in eventDispatcher._listeners ) # unknown types will be ignored

		eventDispatcher.removeEventListener( "anyType", None )
		self.assertEqual( len( eventDispatcher._listeners[ "anyType" ] ), 0 ) # undefined listeners are ignored

	def test_dispatchEvent( self ):

		eventDispatcher = THREE.EventDispatcher()


		scope = { "callCount": 0 }

		def listener( event ):
			scope[ "callCount" ] += 1

		eventDispatcher.addEventListener( "anyType", listener )
		self.assertEqual( scope[ "callCount" ], 0 ) # no event, no call

		eventDispatcher.dispatchEvent( { "type": "anyType" } )
		self.assertEqual( scope[ "callCount" ], 1 ) # one event, one call

		eventDispatcher.dispatchEvent( { "type": "anyType" } )
		self.assertEqual( scope[ "callCount" ], 2 ) # two events, two calls
