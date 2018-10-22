# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

import logging
import sys
from contextlib import contextmanager

# Create your tests here.
from link_checker.models import *



@contextmanager
def streamhandler_to_console(lggr):
    # Use 'up to date' value of sys.stdout for StreamHandler,
    # as set by test runner.
    stream_handler = logging.StreamHandler(sys.stdout)
    lggr.addHandler(stream_handler)
    yield
    lggr.removeHandler(stream_handler)

def testcase_log_console(lggr):
    def testcase_decorator(func):
        def testcase_log_console(*args, **kwargs):
            with streamhandler_to_console(lggr):
                return func(*args, **kwargs)
        return testcase_log_console
    return testcase_decorator

# Get an instance of a logger
logger = logging.getLogger(__name__)



class TestLinkChecker(TestCase):

	listOfUrlsToTest = ['http://www.cnn.com',
						'jttp://www.cnn.com',
						'http://fogettaboutit',
						]
	@testcase_log_console(logger)
	def testLinks(self):
			results = []
	
			log = logger.debug
			log("in testLinks")
			for uri in self.listOfUrlsToTest:
				log("\nTest: %s\n" % uri)
				lc = LinkObj()
				rtn = lc.check_link(uri)
				log(rtn)

				results.append(rtn)

