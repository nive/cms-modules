# -*- coding: utf-8 -*-

import time
import unittest

from pyramid import testing
from pyramid.renderers import render

from nive_cms.tests.db_app import *
from nive_cms_design_bs_grayscale.view import *
from nive_cms_design_bs3.view import Design
from nive_cms.tests import __local


class tDesign(__local.DefaultTestCase, unittest.TestCase):

    def setUp(self):
        request = testing.DummyRequest()
        request._LOCALE_ = "en"
        request.content_type = ""
        self.config = testing.setUp(request=request)
        self.config.include('pyramid_chameleon')
        self.request = request
        self._loadApp(["nive_cms_design_bs_grayscale"])
        self.app.Startup(self.config)        
        self.root = self.app.root()
        user = User(u"test")
        user.groups.append("group:editor")
        self.page = create_page(self.root, user)
        self.request.context = self.page

    def tearDown(self):
        user = User(u"test")
        testing.tearDown()
        root = self.app.root()
        self.root.Delete(self.page.id, user=user)
        self.app.Close()

    def test_templates(self):
        user = User(u"test")
        user.groups.append("group:editor")
        view = Design(self.page, self.request)
        view.__configuration__ = lambda: configuration
        vrender = {"context":self.page, "view":view, "request": self.request, "cmsview":None}
        
        render("nive_cms_design_bs_grayscale:templates/index.pt", vrender)

        render("nive_cms_design_bs_grayscale:templates/page.pt", vrender)
        render("nive_cms_design_bs_grayscale:templates/root.pt", {"context":self.page.dataroot, "view":view, "cmsview":None})

        # search
        self.request.POST = {"phrase": "a"}
        r=view.search()
        self.assertEqual(r.status_int, 200)
        self.assertGreater(r.content_length, 1000)
