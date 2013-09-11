# -*- coding: utf-8 -*-

import time
import unittest
from pyramid.renderers import render
from pyramid import testing 

from nive.definitions import Conf
from nive.helper import FormatConfTestFailure
from nive.views import BaseView
from nive.views import Mail
from nive_contact import contact


class DummyContact(object):
    useCache = False
    configuration =  contact.configuration
    data = Conf(receiverName=u"no one", receiver=u"no@one.com", mailtitle=u"contact mail")
    meta = Conf(title=u"a contact form")
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
    @property
    def portal(self):
        return self
    @property
    def userdb(self):
        return self
    def GetTool(self, name):
        class DummyTool(object):
            def __call__(self, **kw):
                return True, "value"
        return DummyTool()

    
class DummyView(object):
    def contact(self):
        return "placeholder"
    
class TestConf(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_conf(self):
        r=contact.configuration.test()
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
        text = DummyContact()
        html = render("nive_contact:contact.pt", {"context": text, "view": DummyView()})
        self.assert_(html)
        self.assert_(html.find("placeholder")!=-1)

    def test_tmplmail(self):
        data = {
            "topic":"topic", 
            "name":"name", 
            "email":"email@email.com", 
            "company":"company", 
            "message":"message"
        }
        html = render("nive_contact:contactmail.pt", {"data": data, "view": BaseView(None,None)})
        self.assert_(html)
        self.assert_(html.find("topic")!=-1)


       
class TestForm(unittest.TestCase):

    def setUp(self):
        request = testing.DummyRequest()
        request._LOCALE_ = "en"
        self.request = request
        self.config = testing.setUp(request=request)

    def tearDown(self):
        testing.tearDown()
        
    def test_form(self):
        context = DummyContact()
        self.request.POST = {
            "topic":"topic", 
            "name":"name", 
            "email":"email@email.com", 
            "company":"company", 
            "message":"message",
        }
        form = contact.ContactForm(view=BaseView(context,self.request), app=context)
        form.fields = contact.configuration.contactForm
        form.mail =  Mail(context.data.mailtitle, context.configuration.mailtmpl)
        form.mail.recv = (context.data.receiver, context.data.receiverName)
        form.Setup()
        result, data = form.SendForm(action="send")
 