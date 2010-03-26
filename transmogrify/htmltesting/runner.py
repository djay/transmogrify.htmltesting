from collective.transmogrifier.tests import registerConfig
from collective.transmogrifier.transmogrifier import Transmogrifier
from pkg_resources import resource_string, resource_filename
from collective.transmogrifier.transmogrifier import configuration_registry
from Products.Five import zcml
from zope.component import provideUtility
from zope.interface import classProvides, implements
import transmogrify.htmltesting

class Context:
    pass


config = """
[transmogrifier]
pipeline =
    source
    middle
    clean
    printer
    

[clean]
blueprint = collective.transmogrifier.sections.manipulator
delete = 
    _content

[printer]
blueprint = collective.transmogrifier.sections.tests.pprinter

"""



def testtransmogrifier(source=None, middle=None):
    import pdb; pdb.set_trace()
    
    if source:
        config = re.replace('[(.*)]',config, 'source')
    if source:
        config = re.replace('[(.*)]',config, 'source')
    
    transmogrify(config)
 
def runner(config, args):
    from collective.transmogrifier.transmogrifier import Transmogrifier
#    test.globs['transmogrifier'] = Transmogrifier(test.globs['plone'])

    import zope.component
    import collective.transmogrifier.sections
    zcml.load_config('meta.zcml', zope.app.component)
    zcml.load_config('meta.zcml', collective.transmogrifier)
    zcml.load_config('configure.zcml', collective.transmogrifier.sections)
    zcml.load_config('configure.zcml', transmogrify.htmltesting)


    context = Context()
    configuration_registry.registerConfiguration(
        u'transmogrify.config.funnelweb',
        u"",
        u'', config)

    transmogrifier = Transmogrifier(context)
    overrides = {}
    if type(args) == type(''):
      for arg in args:
        section,keyvalue = arg.split(':',1)
        key,value = keyvalue.split('=',1)
        overrides.setdefault('section',{})[key] = value
    else:
        overrides = args

    transmogrifier(u'transmogrify.config.funnelweb', **overrides)

if __name__ == '__main__':
       main()
