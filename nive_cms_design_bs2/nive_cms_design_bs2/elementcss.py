
"""
Contains the grid system css classes to be used in edit forms.
The lists are mapped to the elements' form definitions on startup.

Most of the class names defined here are default bootstrap 2.
"""

from nive.definitions import Conf
from nive_cms.i18n import _


grid_span = (
    {'id': u'span1', 'name': _(u'Span 1')},
    {'id': u'span2', 'name': _(u'Span 2')},
    {'id': u'span3', 'name': _(u'Span 3')},
    {'id': u'span4', 'name': _(u'Span 4')},
    {'id': u'span5', 'name': _(u'Span 5')},
    {'id': u'span6', 'name': _(u'Span 6')},
    {'id': u'span7', 'name': _(u'Span 7')},
    {'id': u'span8', 'name': _(u'Span 8')},
    {'id': u'span9', 'name': _(u'Span 9')},
    {'id': u'span10', 'name': _(u'Span 10')},
    {'id': u'span11', 'name': _(u'Span 11')},
    {'id': u'span12', 'name': _(u'Span 12 (100% width)')},
    {'id': u'jumbotron', 'name': _(u'Top box')}
)

grid_offset = (
    {'id': u'', 'name': _(u'none')},
    {'id': u'offset1', 'name': _(u'Offset 1')},
    {'id': u'offset2', 'name': _(u'Offset 2')},
    {'id': u'offset3', 'name': _(u'Offset 3')},
    {'id': u'offset4', 'name': _(u'Offset 4')},
    {'id': u'offset5', 'name': _(u'Offset 5')},
    {'id': u'offset6', 'name': _(u'Offset 6')},
    {'id': u'offset7', 'name': _(u'Offset 7')},
    {'id': u'offset8', 'name': _(u'Offset 8')},
    {'id': u'offset9', 'name': _(u'Offset 9')},
    {'id': u'offset10', 'name': _(u'Offset 10')},
    {'id': u'offset11', 'name': _(u'Offset 11')}
)
        
responsive = (
    {'id': u'visible-desktop', 'name': _(u'Visible in desktop viewports')},
    {'id': u'visible-tablet', 'name': _(u'Visible in tablet viewports')},
    {'id': u'visible-phone', 'name': _(u'Visible in phone viewports')}
)  

colors = (
    {"id": u"", "name": _(u"none")}, 
    {"id": u"btn-primary", "name": _(u"Primary")}, 
    {"id": u"btn-info", "name": _(u"Info")}, 
    {"id": u"btn-success", "name": _(u"Success")}, 
    {"id": u"btn-warning", "name": _(u"Warning")}, 
    {"id": u"btn-danger", "name": _(u"Danger")}, 
    {"id": u"btn-inverse", "name": _(u"Inverse")}
)


image_classes = (
    {"id": u"default", "name": _(u"Simple")}, 
    {"id": u"left",    "name": _(u"Float right")}, 
    {"id": u"teaser",  "name": _(u"Teaser")},
    {"id": u"teaserl", "name": _(u"Teaser large")},
    {"id": u"teasers", "name": _(u"Teaser small")}
)

link_classes = (
    {"id": u"", "name": _(u"none")}, 
    {"id": u"btn", "name": _(u"Simple button")}, 
    {"id": u"btn btn-large", "name": _(u"Large button")}, 
    {"id": u"btn btn-small", "name": _(u"Small button")}
)
                 
news_classes = (
    {"id": u"simple", "name": _(u"Block")},
    {"id": u"teaser", "name": _(u"Teaser")},
    {"id": u"teasers", "name": _(u"Teaser small")},
    {"id": u"line", "name": _(u"Single line, fold out")}
)

spacer_classes = (
    {'id': u'bo', 'name': _(u'Border')},
    {'id': u'h0', 'name': _(u'Invisible')},
    {'id': u'h1', 'name': _(u'1 line')},
    {'id': u'h2', 'name': _(u'2 lines')},
    {'id': u'h3', 'name': _(u'3 lines')},
    {'id': u'h4', 'name': _(u'4 lines')},
)

def setup(app, pyramidConfig):
    """
    process all configurations and set form list fields for css selection
    """
    # box
    box = app.GetObjectConf("box")
    if box:
        for field in box.data:
            if field.id == "span":
                if not field.listItems:
                    field.listItems = grid_span
            elif field.id == "spanoffset":
                if not field.listItems:
                    field.listItems = grid_offset
            elif field.id == "responsive":
                if not field.listItems:
                    field.listItems = responsive
    
    # image
    image = app.GetObjectConf("image")
    if image:
        for field in image.data:
            if field.id == "cssClass":
                if not field.listItems:
                    field.listItems = image_classes
    
    # link
    link = app.GetObjectConf("link")
    if link:
        for field in link.data:
            if field.id == "style":
                if not field.listItems:
                    field.listItems = link_classes
            if field.id == "color":
                if not field.listItems:
                    field.listItems = colors
    
    # news
    news = app.GetObjectConf("news")
    if news:
        for field in news.data:
            if field.id == "cssClass":
                if not field.listItems:
                    field.listItems = news_classes
    
    # spacer
    spacer = app.GetObjectConf("spacer")
    if spacer:
        for field in spacer.data:
            if field.id == "cssClass":
                if not field.listItems:
                    field.listItems = spacer_classes                        
    
    
