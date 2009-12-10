import unittest

import zope.testing.doctest
import doctest

from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
# For directive tests

from zope.interface import Interface
from zope import schema

from plone.tiles import Tile, PersistentTile

class IDummySchema(Interface):
    foo = schema.TextLine(title=u"Foo")

class IDummyContext(Interface):
    pass

class IDummyLayer(Interface):
    pass

class DummyTile(Tile):
    def __call__(self):
        return u"dummy"

class DummyTileWithTemplate(PersistentTile):
    pass

@onsetup
def setup_product():
    """Set up the package and its dependencies."""
    fiveconfigure.debug_mode = True
    import plone.tiles    
    zcml.load_config('configure.zcml', plone.tiles)
    fiveconfigure.debug_mode = False
    
setup_product()
ptc.setupPloneSite(products=['plone.tiles'])

def test_suite():
    return unittest.TestSuite([
        
        #zope.testing.doctest.DocFileSuite('tiles.txt',
        #             setUp=zope.app.testing.placelesssetup.setUp,
        #             tearDown=zope.app.testing.placelesssetup.tearDown),
        #
        #zope.testing.doctest.DocFileSuite('directives.txt',
        #             setUp=zope.app.testing.placelesssetup.setUp,
        #             tearDown=zope.app.testing.placelesssetup.tearDown),
        #
        #zope.testing.doctest.DocFileSuite('data.txt',
        #             setUp=zope.app.testing.placelesssetup.setUp,
        #             tearDown=zope.app.testing.placelesssetup.tearDown),

        ztc.ZopeDocFileSuite(
            'tests/applicationtiles.txt', package='plone.tiles',
            test_class=ptc.FunctionalTestCase, 
            #optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
            ),
        
        ])
        