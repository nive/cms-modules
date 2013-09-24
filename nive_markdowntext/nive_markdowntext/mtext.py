# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
# Copyright 2013 Nive GmbH. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#----------------------------------------------------------------------
__doc__ = """
Markdown text element
---------------------
Nive cms page element with markdown text format support.
"""

import markdown2

from nive.i18n import _
from nive.utils.utils import ConvertHTMLToText, CutText

from nive.definitions import StagPageElement, ObjectConf, FieldConf
from nive.components.objects.base import PageElementBase



class mtext(PageElementBase):
    """
    basic text class
    """
    
    titleLen = 20
    useCache = True

    def Init(self):
        self.ListenEvent("commit", "OnCommit")


    def OnCommit(self):
        if self.useCache:
            self.data["tcache"] = markdown2.markdown(self.data.get("textblock"))
            text = ConvertHTMLToText(self.data["tcache"], removeReST=True)
        else:
            temp = markdown2.markdown(self.data.get("textblock"))
            text = ConvertHTMLToText(temp, removeReST=True)
        self.meta["title"] = CutText(text, self.titleLen, postfix=u"")
        return True
    
    
    def HTML(self):
        return markdown2.markdown(self.data.get("textblock"))



# contact definition ------------------------------------------------------------------

#@nive_module
configuration = ObjectConf(
    id = "mtext",
    name = "Markdown Text",
    dbparam = "mtext",
    context = mtext,
    template = "nive_markdowntext:mtext.pt",
    selectTag = StagPageElement,
    icon = "nive.cms.cmsview:static/images/types/element.png",
    description = __doc__,
)

desc = _(u"""Markdown text format.<br/>Header: # Text<br>Subheader: ## Text<br>Lists: * or Numbers<br>Emphasis: *text* or **text**<br>Links: [link text](link address) <br><br/>See <a href="http://en.wikipedia.org/wiki/Markdown" target="_blank">Wikipedia</a> for a full description.""")
# these are the contact element fields
configuration.data = [
    FieldConf(id="textblock", datatype="text",  size=100000, default=u"", name=_(u"Text"), fulltext=True, description=desc),
    FieldConf(id="tcache",    datatype="htext", size=100000, default=u"", name=_(u"Cached text"), fulltext=False),
]

fields = ["textblock", "pool_groups"]
configuration.forms = {"create": {"fields":fields}, "edit": {"fields":fields}}

configuration.views = []
