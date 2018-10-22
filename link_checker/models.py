# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# import the logging library
import logging

import requests
from requests.exceptions import InvalidSchema
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

# Get an instance of a logger
logger = logging.getLogger(__name__)

#
# Create your models here.
class LinkStatus(object):
    
    def __init__(self, uri):
        self.uri = uri
        self.canCall = False
        self.canReach = False
        self.httpReturnCode = None
        self.errorMessage = None
        self.canParseResults = False
        self.responseObj = None

    def __str__(self):
        sb = []
        for key in self.__dict__:
            sb.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))
     
        return ', '.join(sb)
 
    def __repr__(self):
        return self.__str__() 

class LinkTester(object):
    
    uri = None
    def testLink(self, uri):
        log = logger.debug
        log("uri:%s" % uri)

        self.uri = uri
        self.linkStatus = LinkStatus(uri)
        rtn = []
        for testMethod in self.ListOfTests:
            testMethod(self)

        return self.linkStatus
        
    def pingAttempt(self):

        #Attempt to ping uri
        rtn = False
        
        self.linkStatus.canPing = rtn 
        return self.linkStatus.canPing

    def callURIAttempt(self):
        #Call website
        rtn = False
        try:
            page = requests.get(self.uri)
            rtn = True
            self.linkStatus.responseObj = page
            self.linkStatus.httpReturnCode = page.status_code
            self.linkStatus.canReach = True
            self.linkStatus.canCall = True
        
        except InvalidSchema as e:
            self.linkStatus.errorMessage = "%s" % e

        except ConnectionError as e:
            self.linkStatus.errorMessage = "%s" % e
        
        
        return self.linkStatus.httpReturnCode

    def parseResultsAttempt(self):
        rtn = False
        #Read markup - attempt to parse it
        if (self.linkStatus.responseObj is None):
            return rtn

        markup = self.linkStatus.responseObj.text

        #for chunk in self.linkStatus.responseObj.iter_content(chunk_size=128):
        #    markup+="%s" % chunk
        try:    
            rtn = BeautifulSoup(markup, "lxml")
            self.linkStatus.canParseResults = True
            #print "parseResults did occur"
        except:
            pass
            #Could do more here

        return self.linkStatus.canParseResults

    #Instance variable - store list of tests as an array
    #Want to add more diagnostic tests ?  Build a function and add the function name to the list below
    ListOfTests = [callURIAttempt, parseResultsAttempt]

class LinkObj(object):
    
    originalURL = None

    def check_link(self, uri):
        lt = LinkTester()
        myStatus = lt.testLink(uri)

        return myStatus

