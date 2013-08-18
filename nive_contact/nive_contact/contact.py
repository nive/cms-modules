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
Contact form
---------
Nive cms page element to send form values by mail.

Uses the `sendMail` module registered with the userdb
"""

from nive.views import Mail
from nive.forms import HTMLForm
from nive.definitions import IWebsiteRoot
from nive.cms.design.view import Design
from nive.components.objects.base import PageElementBase
from nive.definitions import StagPageElement, ObjectConf, FieldConf, ViewConf, Conf



class ContactForm(HTMLForm):
    """
    Contact form
    """
    mail = None
    actions = [
         Conf(id="default",  method="StartForm", name=u"Initialize",   hidden=True),
         Conf(id="send",     method="SendForm",  name=u"Send message", hidden=False, css_class=u"btn btn-primary",  html=u"", tag=u""),
    ]


    def SendForm(self, action, **kw):
        """
        Form action: send the message 
        """
        msgs = []
        result,data,errors = self.Validate(self.request)
        if result:
            user = self.view.User()
            try:
                title = data["topic"] + " - " + self.mail.title
            except:
                title = self.mail.title
            body = self.mail(user=user, data=data, view=self.view)
            tool = self.context.app.portal.userdb.GetTool("sendMail")
            result, value = tool(body=body, title=title, recvmails=[self.mail.recv], force=1)
            if not result:
                msgs.append("Sorry, a error occurred. The email could not be send.")
            else:
                msgs.append("Thanks.")
                return result, self._Msgs(msgs=msgs)
        return result, self.Render(data, msgs=msgs, errors=errors)



class ContactView(Design):
    
    def contact(self):
        context = self.context
        form = ContactForm(context=context, request=self.request, view=self, app=context.app)
        form.fields = context.configuration.contactForm
        form.mail =  Mail(context.data.mailtitle, context.configuration.mailtmpl)
        form.mail.recv = (context.data.receiver, context.data.receiverName)
        form.anchor = u"#contact"+str(context.id)
        form.Setup()
        result, data, action = form.Process()
        return data


class ContactObj(PageElementBase):
    pass


# contact definition ------------------------------------------------------------------

#@nive_module
configuration = ObjectConf(
    id = "contact",
    name = "Contact form",
    dbparam = "contact",
    context = ContactObj,
    template = "nive_contact:contact.pt",
    selectTag = StagPageElement,
    icon = "nive.cms.cmsview:static/images/types/element.png",
    description = __doc__,
    # contact specific configuration
    # the form to be displayed on the web page 
    contactForm = [
       FieldConf(id="name",    datatype="string", size=   50, default="", required=1, name="Name", description=""),
       FieldConf(id="email",   datatype="email",  size=  200, default="", required=1, name="E-Mail", description=""),
       FieldConf(id="company", datatype="string", size=  200, default="", required=0, name="Company", description=""),
       FieldConf(id="topic",   datatype="radio",  size=   30, default="", required=1, name="Topic", description="",
                 listItems = [{'id': 'support', 'name': 'Support'}, 
                              {'id': 'feedback', 'name': 'Feedback'},
                              {'id': 'contract', 'name': 'Contract'},
                             ], 
                 ),
       FieldConf(id="message", datatype="text",   size= 2000, default="", required=1, name="Message", description=""),
    ],
    mailtmpl = "nive_contact:contactmail.pt"
)

# these are the contact element fields
configuration.data = [
    FieldConf(id="receiver",      datatype="email",  size=100, default="", name="Receiver",      description=""),
    FieldConf(id="receiverName",  datatype="string", size=100, default="", name="Receiver name", description=""),
    FieldConf(id="mailtitle",     datatype="string", size=100, default="", name="Mail title",    description="")
]

# define the fields actually to be used in the cms element add and edit forms 
fields = ["title", "receiver", "receiverName", "mailtitle", "pool_groups"]
configuration.forms = {"create": {"fields":fields}, "edit": {"fields":fields}}

# define a new view to link our custom view class (ContactView) with the contact obj (ContactObj)
# this is required to call contact() from the template and process the form
configuration.views = [
    ViewConf(id="contactview", name="", attr="view", context=ContactObj, view=ContactView)
]
