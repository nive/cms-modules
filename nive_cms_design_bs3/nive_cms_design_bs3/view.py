# Copyright 2012, 2013 Arndt Droullier, Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

__doc__ = """
Website Design
----------------
This module includes everything required to render the public website:

- css, javascript, layout images (in design/static)
- templates for page elements and pages (in design/templates)
- the main template (design/templates/index.pt)
- required views
"""

import os
from time import time
from StringIO import StringIO
from pyramid.renderers import render
from pyramid.httpexceptions import HTTPNotFound

from nive.definitions import ViewModuleConf, ViewConf, ConfigurationError, Conf
from nive.definitions import IWebsite, IWebsiteRoot, IRoot, ICMSRoot, IPage, IPageElement, IObject, IFile, IPortal
from nive.definitions import IViewModuleConf

from nive_cms.i18n import _
from nive_cms.baseobjects import DesignBase

from nive_cms_design_bs3 import elementcss
    
# view module definition ------------------------------------------------------------------

#@nive_module
configuration = ViewModuleConf(
    id = "design",
    name = _(u"Website design based on bootstrap 3"),
    static = "nive_cms_design_bs3:static",
    templates = "nive_cms_design_bs3:templates",
    template = "index.pt",
    permission = "view",
    containment = IWebsite,
    view = "nive_cms_design_bs3.view.Design",
    views = [
        ViewConf(id="appview",  name="",      attr="app",   context=IWebsite,  containment=IPortal),
        ViewConf(id="search",   name="search",attr="search",context=IRoot),
        ViewConf(id="su",       name="su",    attr="open",  context=IRoot),
        ViewConf(id="rootview", name="",      attr="view",  context=IWebsiteRoot),
        ViewConf(id="objview",  name="",      attr="view",  context=IPage,    containment=IWebsiteRoot),
        ViewConf(id="objview",  name="",      attr="view",  context=IPageElement),
        ViewConf(id="objfile",  name="file",  attr="file",  context=IFile),
        # restricted permissions if called in editor
        ViewConf(id="rootview", name="",      attr="view",  context=ICMSRoot, containment=IWebsite),
        ViewConf(id="objview",  name="",      attr="view",  context=IPage,    containment=ICMSRoot),
    ],
    # assets list the requirements for the website
    assets = [
        ('bootstrap.css', 'nive_cms_design_bs3:static/bootstrap-3.1.1/css/bootstrap.min.css'),
        ('cmsview.css', 'nive_cms_design_bs3:static/styles.css'),              # nive css
        ('jquery.js', 'nive_cms_design_bs3:static/jquery-1.10.2.min.js'),
        ('bootstrap.js', 'nive_cms_design_bs3:static/bootstrap-3.1.1/js/bootstrap.min.js'),
    ],
    events = (Conf(event="startRegistration", callback=elementcss.setup),),
    description=__doc__
)


class Design(DesignBase):
    """
    get view module as attr for view class
    """

    # routed views -------------------------------------------------------------------------------------
    
    def search(self):
        values = {u"cmsview": self.editorview, u"context": self.context, u"view": self}
        name = u"search.pt"
        return self.DefaultTemplateRenderer(values, templatename=name)


    # redirects ----------------------------------------------------

    def app(self):
        root = self.context.GetRoot()
        url = self.PageUrl(root)
        self.Redirect(url)
    
    def open(self):
        ref = self.GetFormValue(u"r")
        page = self.context.LookupObj(ref)
        if not page:
            raise HTTPNotFound, unicode(ref)
        page = page.GetPage()
        url = self.PageUrl(page)
        self.Redirect(url)
    
        
    # html widgets ----------------------------------------------------
    
    def breadcrumbs(self, addHome=0):
        """
        """
        base = self.context.GetPage()
        parents = base.GetParents()
        parents.reverse()
        if not addHome:
            parents = parents[1:]
        if len(parents)==0 and not addHome:
            return u""
        html = StringIO()
        for page in parents:
            html.write(u"""<li><a href="%s">%s</a></li> """ % (self.PageUrl(page), page.GetTitle()))
        html.write(u"""<li class="active">%s</li>""" % (base.GetTitle()))
        return html.getvalue()
    

    def navigationTop(self, addHome=1):
        """
        only first level pages
        """
        html = StringIO()
        page = self.context
        root = page.dataroot
        if addHome:
            highlight = u""
            if page.id == root.id:
                highlight = u"active"
            html.write(u"""<li class="%s"><a href="%s">%s</a></li>""" % (highlight, 
                                                                         self.PageUrl(root, usePageLink=1), 
                                                                         root.GetTitle()))
        
        path = page.GetParentIDs()
        pages = root.GetPages(securityContext=self.request, permission='view')
        for page in pages:
            if page.data.get("navHidden"):
                continue
            # highlight, current
            if page.id == self.context.id or page.id in path:
                highlight = u"active"
            else:
                highlight = u""
            # link
            html.write(u"""<li class="%s"><a href="%s">%s</a></li>""" % (highlight, 
                                                                         self.PageUrl(page, usePageLink=not self.IsEditmode()), 
                                                                         page.GetTitle()))
        return html.getvalue()


    def navigationTree(self, addHome=1, page=None, ulclass="nav nav-tabs nav-stacked"):
        """
        tree navigation for all levels
        """
        if not page:
            page = self.context.GetPage()
        root = page.dataroot
        html = StringIO()
        html.write(u"""<ul id="level1" class="%s">""" % (ulclass))
        if addHome:
            highlight = u""
            selected = u""
            if page.id == root.id:
                selected = u"current"
                highlight = u"active"
            html.write(u"""<li class="%s"><a href="%s" class="%s">%s</a></li>""" % (highlight, 
                                                                                    self.PageUrl(root, usePageLink=not self.IsEditmode()), 
                                                                                    selected, 
                                                                                    root.GetTitle()))
        
        path = page.GetParentIDs()
        level = 1
        html = self._navigationLevel(root, level, page, path, html, ulclass)
        html.write(u"""</ul>""")   #str(DateTime().timeTime()-t)   
        return html.getvalue()


    def navigationSub(self, page=None, ulclass="nav nav-tabs nav-stacked"):
        """
        tree subpages of current first level page
        """
        if not page:
            page = self.context.GetPage()
        base = page.parent
        if page.GetID()<=0:
            base = page
        elif base.GetID()<=0:
            base = page
        else:
            while base.parent.GetID() > 0:
                base = base.parent
        
        path = page.GetParentIDs()
        level = 1
        html = StringIO()
        html.write(u"""<ul id="level1" class="%s">""" % (ulclass))
        html = self._navigationLevel(base, level, page, path, html, ulclass)
        html.write(u"""</ul>""")
        return html.getvalue()


    def _navigationLevel(self, current, level, active, path, io, ulclass):
        """
        """
        pages = current.GetPages(securityContext=self.request, permission='view')
        # sublevel
        if len(pages) and level > 1:
            io.write(u"""<li><ul id="level%d" class="%s">""" % (level, ulclass))
        
        for page in pages:
            if page.data.get("navHidden"):
                continue
        
            # highlight, current
            highlight = u""
            selected = u""
            if active.id == page.id:
                selected = u"current"
                highlight = u"active"
            elif page.id in path:
                highlight = u"active"
            
            # link
            io.write(u"""<li class="%s"><a href="%s" class="%s">%s</a></li>""" % (highlight, 
                                                                                  self.PageUrl(page, usePageLink=not self.IsEditmode()), 
                                                                                  selected, 
                                                                                  page.GetTitle()))
            
            if highlight or selected:
                io = self._navigationLevel(page, level+1, active, path, io, ulclass)
        
        if len(pages) and level > 1:
            io.write(u"""</ul></li>\r\n""")
        return io


    def getGridCls(self, name, to=u"col-md-"):
        """
        To stay compatible with bootstrap 2 grid system as long 12 columns are used.
        Old class names are simply translated to bootstrap 3 names.
        """
        # image gallery
        if name=="teaserl":
            name = u"span4"
        elif name=="teasers":
            name = u"span2"
        elif name in (u"teaser",u"default",u"left"):
            name = u"span3"
        # boxes
        if name.startswith(u"span"):
            return name.replace(u"span", to)
        if name.startswith(u"offset"):
            return name.replace(u"offset", to+u"offset-")
        if name == u"hero-unit":
            return u"jumbotron"
        # buttons
        if name.find(u"btn-small")!=-1:
            return name.replace(u"btn-small", u"btn-xs")
        if name.find(u"btn-large")!=-1:
            return name.replace(u"btn-large", u"btn-lg")
        return name
        

    def getResponsiveCls(self, name, editmode=False):
        """
        Returns the responsive class to be attached to the box.
        In edit mode all boxes are visible and the data.responsive setting
        is prefixed with `pe_`. (e.g. pe_visible-tablet pe_visible-phone)
        
        To make boxes always accessible in edit mode the responsive setting is
        disabled and boxes are highlighted appropriately.
        """
        if isinstance(name, basestring):
            name=name.split(u", ")
        if not editmode or not name:
            parsed = []
            for n in name:
                if n == u"visible-desktop":
                    n = u"visible-md"
                elif n == u"visible-tablet":
                    n = u"visible-sm"
                elif n == u"visible-phone":
                    n = u"visible-xs"
                parsed.append(n)
            return u" ".join(parsed)
        return u" ".join([u"pe_"+c for c in name])


    # linked documentation, first start message 
    
    def doc(self, template=u"default.pt"):
        """
        renders the doc template
        """
        return render(u"nive_cms:doc/"+template, {u"context":self.context, u"view":self, u"request": self.request}, request=self.request)


    def HtmlTitle(self):
        return u"%s - %s" % (self.context.app.configuration.title, self.context.GetTitle())


    # bw 0.9.9
    @property
    def cmsview(self):
        return self.editorview

    
    
