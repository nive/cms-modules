# -*- coding: utf-8 -*-

import time
import unittest

from pyramid.httpexceptions import HTTPNotFound, HTTPFound, HTTPOk, HTTPForbidden
from pyramid import testing 
from pyramid.renderers import render

from nive_cms.tests.db_app import *
from nive_cms.tests import __local
from nive_cms_design_bs2.view import *


class tDesign(object):

    def setUp(self):
        request = testing.DummyRequest()
        request._LOCALE_ = "en"
        request.content_type = ""
        self.config = testing.setUp(request=request)
        self.config.include('pyramid_chameleon')
        self.request = request
        self._loadApp(["nive_cms_design_bs2.view"])
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


    def test_functions(self):
        view = Design(self.root, self.request)
        view.HtmlTitle()
        view.IsEditmode()
        self.assertRaises(HTTPFound, view.app)
        self.assertRaises(HTTPNotFound, view.open)

    
    def test_views1(self):
        # root
        view = Design(self.root, self.request)
        view.__configuration__ = lambda: configuration
        view.HtmlTitle()
        view.index_tmpl()
        view.view()
        view.navigationTop(addHome=1)
        view.navigationTop(addHome=0)
        view.navigationTree(addHome=1, page=None)
        view.navigationTree(addHome=0, page=None)
        view.navigationTree(addHome=1, page=self.page)
        view.navigationSub(page=None)
        view.navigationSub(page=self.page)
        view.breadcrumbs(addHome=0)
        view.breadcrumbs(addHome=1)
        view.doc()
    

    def test_views2(self):
        # page
        view = Design(self.page, self.request)
        view.__configuration__ = lambda: configuration
        view.HtmlTitle()
        view.index_tmpl()
        view.view()
        view.navigationTop(addHome=1)
        view.navigationTop(addHome=0)
        view.navigationTree(addHome=1, page=None)
        view.navigationTree(addHome=0, page=None)
        view.navigationSub(page=None)
        view.breadcrumbs(addHome=0)
        view.breadcrumbs(addHome=1)
        
        
    def test_templates(self):
        user = User(u"test")
        user.groups.append("group:editor")
        view = Design(self.page, self.request)
        view.__configuration__ = lambda: configuration
        vrender = {"context":self.page, "view":view, "request": self.request, "cmsview":None}
        
        render("nive_cms_design_bs2:templates/page.pt", vrender)
        render("nive_cms_design_bs2:templates/root.pt", {"context":self.page.dataroot, "view":view, "cmsview":None})

        b1 = create_box(self.page, user)
        render("nive_cms_design_bs2:templates/box.pt", {"context":b1, "view":view})
        b2 = create_column(self.page, user)
        render("nive_cms_design_bs2:templates/column.pt", {"context":b2, "view":view})
        b3 = create_file(self.page, user)
        render("nive_cms_design_bs2:templates/file.pt", {"context":b3, "view":view})
        b4 = create_image(self.page, user)
        render("nive_cms_design_bs2:templates/image.pt", {"context":b4, "view":view})
        b5 = create_media(self.page, user)
        render("nive_cms_design_bs2:templates/media.pt", {"context":b5, "view":view})
        b6 = create_note(self.page, user)
        render("nive_cms_design_bs2:templates/note.pt", {"context":b6, "view":view})
        b7 = create_text(self.page, user)
        render("nive_cms_design_bs2:templates/text.pt", {"context":b7, "view":view})
        b8 = create_spacer(self.page, user)
        render("nive_cms_design_bs2:templates/spacer.pt", {"context":b8, "view":view})
        b9 = create_link(self.page, user)
        render("nive_cms_design_bs2:templates/link.pt", {"context":b9, "view":view})
        b0 = create_menublock(self.page, user)
        render("nive_cms_design_bs2:templates/menublock.pt", {"context":b0, "view":view, "request": self.request})
        b10 = create_code(self.page, user)
        render("nive_cms_design_bs2:templates/code.pt", {"context":b10, "view":view})
        b11 = create_news(self.page, user)
        render("nive_cms_design_bs2:templates/news.pt", {"context":b11, "view":view})
        
        # add to box
        b3 = create_file(b1, user)
        b4 = create_image(b1, user)
        b5 = create_media(b1, user)
        b6 = create_note(b1, user)
        b7 = create_text(b1, user)
        b8 = create_spacer(b1, user)
        b9 = create_link(b1, user)
        b0 = create_menublock(b1, user)
        b10 = create_code(b1, user)
        b11 = create_news(b1, user)
        render("nive_cms_design_bs2:templates/box.pt", {"context":b1, "view":view})
        
        # add to column
        b3 = create_file(b2, user)
        b4 = create_image(b2, user)
        b5 = create_media(b2, user)
        b6 = create_note(b2, user)
        b7 = create_text(b2, user)
        b8 = create_spacer(b2, user)
        b9 = create_link(b2, user)
        b0 = create_menublock(b2, user)
        b10 = create_code(b2, user)
        b11 = create_news(b2, user)
        render("nive_cms_design_bs2:templates/column.pt", {"context":b2, "view":view})
        
        # render page with elements
        render("nive_cms_design_bs2:templates/page.pt", {"context":self.page, "view":view, "cmsview":None})
        render("nive_cms_design_bs2:templates/root.pt", {"context":self.page.dataroot, "view":view, "cmsview":None})
        r=view.view()
        self.assertEqual(r.status_int, 200)
        self.assertGreater(r.content_length, 2000)
        
        # search
        self.request.POST = {"phrase": "a"}
        r=view.search()
        self.assertEqual(r.status_int, 200)
        self.assertGreater(r.content_length, 1000)


class tDesign_db(tDesign, __local.DefaultTestCase):
    pass