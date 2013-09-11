# -*- coding: utf-8 -*-

import time
import unittest
from pyramid.renderers import render
from pyramid import testing 

from nive.definitions import Conf
from nive.helper import FormatConfTestFailure
from nive.views import BaseView
from nive.views import Mail
from nive_newsuser import newsuser


class DummyNewsuser(object):
    useCache = False
    id=123
    configuration =  newsuser.configuration
    data = Conf(mailtitle=u"a mail", mailtext=u"contact mail", mailfooter=u"no one", newsgroup=u"one.com", notify=1)
    meta = Conf(title=u"a form")
    frontendCodepage = ""
    def GetID(self):
        return 1
    def root(self):
        return self
    def LoadListItems(self, field, context):
        return []
    @property
    def app(self):
        return self
    def GetTool(self, name):
        class DummyTool(object):
            def __call__(self, **kw):
                return True, "value"
        return DummyTool()
    def QueryConfByName(self, a, b):
        return self
    
class DummyView(object):
    def subscribe(self):
        return "placeholder"
    def activate(self):
        return ""
    
class TestConf(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_conf1(self):
        r=newsuser.configuration.test()
        if not r:
            return
        print FormatConfTestFailure(r)
        self.assert_(False, "Configuration Error")

    def test_conf2(self):
        r=newsuser.newsuser_configuration.test()
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

    def tearDown(self):
        testing.tearDown()

    def test_tmpl(self):
        text = DummyNewsuser()
        html = render("nive_newsuser:form.pt", {"context": text, "view": DummyView()})
        self.assert_(html)
        self.assert_(html.find("placeholder")!=-1)

    def test_tmplmail(self):
        data = Conf(activationID="1234567890")
        form = Conf(activationUrl="http://123.com", mailtext="header", mailfooter="footer")
        html = render("nive_newsuser:activationmail.pt", {"data": data, "form": form, "view": BaseView(None,None)})
        self.assert_(html)
        self.assert_(html.find(data.activationID)!=-1)
        self.assert_(html.find(form.activationUrl)!=-1)


       
class TestForm(unittest.TestCase):

    def setUp(self):
        request = testing.DummyRequest()
        request._LOCALE_ = "en"
        self.request = request
        self.config = testing.setUp(request=request)

    def tearDown(self):
        testing.tearDown()
        
    def test_form1(self):
        context = DummyNewsuser()
        self.request.POST = {
        }
        view = newsuser.SubscriptionView(context,self.request)
        view.subscribe()

    def test_form2(self):
        context = DummyNewsuser()
        self.request.POST = {
            "email": "no@aaa.com"
        }
        view = newsuser.SubscriptionView(context,self.request)
        view.subscribe()
