# -*- coding: utf-8 -*-

import time
import unittest
from pyramid.renderers import render
from pyramid import testing 

from nive.helper import FormatConfTestFailure
from nive.definitions import Conf

from nive_markdowntext import mtext


class DummyText(object):
    useCache = False
    data = Conf(tcache=u"<p>Cached Text</p>", textblock=u"Markdown text!")
    meta = Conf(title=u"")
    def GetID(self):
        return 1
    def HTML(self):
        return u"<p>Text</p>"""
    

class TestConf(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_conf(self):
        r=mtext.configuration.test()
        if not r:
            return
        print FormatConfTestFailure(r)
        self.assert_(False, "Configuration Error")


class TestTemplate(unittest.TestCase):

    def setUp(self):
        request = testing.DummyRequest()
        request._LOCALE_ = "en"
        self.request = request
        self.config = testing.setUp(request=request)
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()

    def test_tmpl(self):
        text = DummyText()
        html = render("nive_markdowntext:mtext.pt", {"context": text})
        self.assert_(html)
        self.assert_(html.find(text.HTML())!=-1)

    def test_tmplcache(self):
        text = DummyText()
        text.useCache = True
        html = render("nive_markdowntext:mtext.pt", {"context": text})
        self.assert_(html)
        self.assert_(html.find(text.data.tcache)!=-1)
        
        
class TestObject(unittest.TestCase):

    def setUp(self):
        request = testing.DummyRequest()
        request._LOCALE_ = "en"
        self.request = request
        self.config = testing.setUp(request=request)
        self.config.include('pyramid_chameleon')

    def tearDown(self):
        testing.tearDown()
        
    def test_event(self):
        text = mtext.mtext(1, DummyText(), None, mtext.configuration)
        text.Init()
        
    def test_oncommit(self):
        text = mtext.mtext(1, DummyText(), None, mtext.configuration)
        text.useCache = False
        text.OnCommit()
        self.assertEqual(text.meta.title.replace("\n",""), text.data.textblock)
        text.useCache = True
        text.OnCommit()
        self.assertEqual(text.data.tcache.replace("\n",""), u'<p>Markdown text!</p>')
        
    def test_html(self):
        text = mtext.mtext(1, DummyText(), None, mtext.configuration)
        self.assertEqual(text.HTML().replace("\n",""), u'<p>Markdown text!</p>')
        
