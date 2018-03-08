from django_nose_qunit import QUnitTestCase as QUnitTestCaseOriginal
from django.shortcuts import render
import json
import logging

from django.core.urlresolvers import reverse

from sbo_selenium import SeleniumTestCase
from six.moves.urllib.parse import quote

logger = logging.getLogger('django.request')
registry = {}
def qualified_class_name(cls):
    module = cls.__module__
    if module:
        return '%s.%s' % (module, cls.__name__)
    else:
        return cls.__name__
class QUnitTestCase(QUnitTestCaseOriginal):
    def _load_case(self):
       self.sel.get(self._case_url())
       msg = """There was a problem rendering the page; check the log for more information (make sure that at least one handler is logging "django.request" messages to file or another persistent source)"""
       try :
         self.wait_for_condition('return QUnit.Django.ready', msg)
       except:
         pass

    def generator(self):

        """
        Load each file in the browser without actually running the tests in
        order to generate a list of all the test cases.  qunit_case() will be
        called for each test case in the list.
        """
        # Need to start and stop server, since tests aren't running yet
        self.__class__.setUpClass()
        # Start the webdriver also
        super(QUnitTestCase, self).setUp()
        failedmodules = []
        print("checking")

        try:
            self.__class__.generating = True
            self._load_case()
            script = 'return JSON.stringify(QUnit.Django.modules)'
            modules = json.loads(self.sel.execute_script(script))

            #failedmodules = json.loads(self.sel.execute_script("return QUnit.Django.results.modules"))
            print("checking")
            #failedmodules = self.sel.execute_script("return QUnit.Django.customFailedAssertions")
            numfailed = self.sel.execute_script("return QUnit.Django.results.failed")

            msg = '\nQUnit Assertion Errors : \n'
            '''
            for item in failedmodules:
                if item["failedAssertions"] != []:
                    for itemy in item["failedAssertions"]:
                       msg += "Test Name {} : {}\n".format(item["name"],itemy)
            if msg != '\nQUnit Assertion Errors : \n':
                raise self.failureException(msg) '''
            if numfailed > 0 :
                raise self.failureException("QUnit Assertion Errors : {} ".format(numfailed))

            for module_name in modules:
                        for test_name in modules[module_name]:
                            yield self.qunit_case, module_name, test_name


        finally:
            del self.__class__.generating
            self.sel.quit()
            self.__class__.tearDownClass()

    def serve_page(self):
        """
        Serve the page with all tests for use in an interactive session.  Runs
        setUp and tearDown once at appropriate times, so test cases can prepare
        templates and database fixtures for use by the page as a whole.
        """
        class_name = qualified_class_name(self.__class__)
        context = {
            'test_file': self.test_file,
            'title': '%s (%s)' % (class_name, self.test_file),
            'dependencies': self.dependencies,
            'raw_script_urls': self.raw_script_urls,
            'fixtures': self.html_fixtures,
            'html_strings': self.html_strings,
            # Can't assume django.core.context_processors.debug is in use
            'autostart': self.autostart,
        }
        self.response = render(self.request, 'test/template.html',
                               context)
class TestingQunit(QUnitTestCase):
   test_file = 'qunit/test.js'
   raw_script_urls = (
                      '/static/build/project/js/jquery.min.js',
                      '/static/build/project/js/compress.min.js',

                      '/static/build/project/js/functions/index.js',
                      )
