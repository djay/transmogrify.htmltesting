
import unittest

from zope.testing import doctest
from zope.component import provideUtility
from Products.Five import zcml
from zope.component import provideUtility
from zope.interface import classProvides, implements
from collective.transmogrifier.interfaces import ISectionBlueprint, ISection

from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.Five import zcml
from Products.Five import fiveconfigure

from collective.transmogrifier.tests import setUp as baseSetUp
from collective.transmogrifier.tests import tearDown
from collective.transmogrifier.sections.tests import PrettyPrinter
from collective.transmogrifier.sections.tests import SampleSource

from transmogrify.htmltesting.webcrawler import WebCrawler
from transmogrify.htmltesting.treeserializer import TreeSerializer
from transmogrify.htmltesting.typerecognitor import TypeRecognitor
from transmogrify.htmltesting.safeportaltransforms import  SafePortalTransforms
from transmogrify.htmltesting.makeattachments import MakeAttachments
from templatefinder import TemplateFinder
from transmogrify.htmltesting.relinker import Relinker
from transmogrify.htmltesting.simplexpath import SimpleXPath
from plone.i18n.normalizer import urlnormalizer
from lxml import etree
import lxml.html
import lxml.html.soupparser
from lxml.html.clean import Cleaner
import urlparse
import transmogrify.htmltesting
from os.path import dirname, abspath
import urllib



def setUp(test):
    baseSetUp(test)

    from collective.transmogrifier.transmogrifier import Transmogrifier
    test.globs['transmogrifier'] = Transmogrifier(test.globs['plone'])

    import zope.component
    import collective.transmogrifier.sections
    zcml.load_config('meta.zcml', zope.app.component)
    zcml.load_config('configure.zcml', collective.transmogrifier.sections)

    test.globs['plone'].portal_transforms = MockPortalTransforms()

    provideUtility(PrettyPrinter,
        name=u'collective.transmogrifier.sections.tests.pprinter')
    provideUtility(WebCrawler,
        name=u'transmogrify.htmltesting.webcrawler')
    provideUtility(TreeSerializer,
        name=u'transmogrify.htmltesting.treeserializer')
    provideUtility(TypeRecognitor,
        name=u'transmogrify.htmltesting.typerecognitor')
    provideUtility(TemplateFinder,
        name=u'transmogrify.htmltesting.templatefinder')
    provideUtility(urlnormalizer)
    provideUtility(Relinker,
        name=u'transmogrify.htmltesting.relinker')
    provideUtility(SimpleXPath,
        name=u'transmogrify.htmltesting.simplexpath')
    provideUtility(SafePortalTransforms,
        name=u'transmogrify.htmltesting.safeportaltransforms')
    from backlinkstitle import BacklinksTitle
    provideUtility(BacklinksTitle,
        name=u'transmogrify.htmltesting.backlinkstitle')
    from isindex import IsIndex
    provideUtility(IsIndex,
        name=u'transmogrify.htmltesting.isindex')
    from pathmover import PathMover
    provideUtility(PathMover,
        name=u'transmogrify.htmltesting.pathmover')
    from safeatschemaupdater import SafeATSchemaUpdaterSection
    provideUtility(SafeATSchemaUpdaterSection,
        name=u'transmogrify.htmltesting.safeatschemaupdater')
    from constructor import SafeConstructorSection
    provideUtility(SafeConstructorSection,
        name=u'transmogrify.htmltesting.constructor')
    from makeattachments import MakeAttachments
    provideUtility(MakeAttachments,
        name=u'transmogrify.htmltesting.makeattachments')
    from debugsection import DebugSection
    provideUtility(DebugSection,
        name=u'transmogrify.htmltesting.debugsection')
    from staticcreator import StaticCreatorSection
    provideUtility(StaticCreatorSection,
        name=u'transmogrify.htmltesting.staticcreator')

    provideUtility(HTMLSource,
        name=u'transmogrify.htmltesting.test.htmlsource')
    provideUtility(HTMLBacklinkSource,
        name=u'transmogrify.htmltesting.test.htmlbacklinksource')


@onsetup
def setup_product():
    """ """
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', transmogrify.htmltesting)
    fiveconfigure.debug_mode = False
    ztc.installPackage('plone.app.z3cform')
#    ztc.installPackage('lovely.remotetask')
    ztc.installPackage('transmogrify.htmltesting')


setup_product()
#ptc.setupPloneSite(extension_profiles=('transmogrify.htmltesting:default',), with_default_memberarea=False)
ptc.setupPloneSite(products=['transmogrify.htmltesting'])

class TestCase(ptc.FunctionalTestCase):
    """ We use this base class for all the tests in this package. If necessary,
        we can put common utility or setup code in here. This applies to unit
        test cases. """
    _configure_portal = False

    def beforeTearDown(self):
        pass

    def afterSetUp(self):
        here = abspath(dirname(__file__))
        url = urllib.pathname2url(here)
        self.testsite = 'file://%s/test_staticsite' % url

        self.portal.error_log._ignored_exceptions = ()

        self.portal.acl_users.portal_role_manager.updateRolesList()

        self.portal.acl_users._doAddUser('manager', 'pass', ('Manager',), [])
        self.login('manager')



        from Products.Five.testbrowser import Browser
        self.browser = Browser()
#        self.setRoles(('Manager',))
        self.browser.open(self.portal.absolute_url()+'/login_form')
        self.browser.getControl(name='__ac_name').value = 'manager'
        self.browser.getControl(name='__ac_password').value = 'pass'
        self.browser.getControl(name='submit').click()
        self.browser.open(self.portal.absolute_url())


def test_suite():
    flags = optionflags = doctest.ELLIPSIS | doctest.REPORT_ONLY_FIRST_FAILURE | \
                        doctest.NORMALIZE_WHITESPACE | doctest.REPORT_UDIFF

    return unittest.TestSuite((
        doctest.DocFileSuite('webcrawler.txt', 
                setUp=setUp, 
                optionflags = flags,
                tearDown=tearDown),



    ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')


