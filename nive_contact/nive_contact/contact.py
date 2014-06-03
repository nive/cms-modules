# -*- coding: utf-8 -*-
# Copyright 2013 Nive GmbH. All rights reserved.
# Released under GPL3. See license.txt
#

__doc__ = """
Contact form
---------
Nive cms page element to send form values by mail.

Uses the `sendMail` module registered with the userdb
"""

from nive.views import Mail
from nive.forms import HTMLForm
from nive.definitions import IWebsiteRoot
from nive_cms.design.view import Design
from nive_cms.baseobjects import PageElementBase
from nive.definitions import StagPageElement, ObjectConf, FieldConf, ViewConf, Conf



class ContactForm(HTMLForm):
    """
    Contact form
    """
    mail = None
    actions = [
         Conf(id="default",    method="StartForm", name=u"Initialize",   hidden=True),
         Conf(id="sendcontact",method="SendForm",  name=u"Send message", hidden=False, css_class=u"btn btn-info",  html=u"", tag=u""),
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
            # lookup mail tool
            app = self.context.configuration.sendMailProvider
            try:
                app = self.context.app.portal[app]
            except KeyError:
                raise ConfigurationError, "Contact sendMail tool not defined"
            body = self.mail(user=user, data=data, view=self.view)
            tool = app.GetTool("sendMail")
            result, value = tool(body=body, title=title, recvmails=[self.mail.recv], force=1)
            if not result:
                msgs.append("Sorry, a error occurred. The email could not be send.")
            else:
                msgs.append("Thanks. We have received your message.")
                return result, self._Msgs(msgs=msgs)
        return result, self.Render(data, msgs=msgs, errors=errors)



class ContactView(Design):
    
    def contact(self):
        context = self.context
        # add topic if choices available
        fields = context.configuration.contactForm
        topics = context.data.topics
        if topics:
            li = []
            for t in topics.split("\n"):
                t = t.replace("\r","")
                li.append({"id":t, "name":t})
            fc = FieldConf(id="topic", datatype="radio", size= 200, default="", required=1, name="Topic", listItems = li)
            # make a new field list
            fn = [fc]
            for f in fields:
                fn.append(f)
            fields = fn
        # setup the form
        form = ContactForm(context=context, request=self.request, view=self, app=context.app)
        form.fields = fields
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
    icon = "nive_cms.cmsview:static/images/types/element.png",
    description = __doc__,
    # contact specific configuration
    sendMailProvider = "userdb",
    # the form to be displayed on the web page 
    contactForm = [
       FieldConf(id="name",    datatype="string", size=   50, default="", required=1, name="Name", description=""),
       FieldConf(id="email",   datatype="email",  size=  200, default="", required=1, name="E-Mail", description=""),
       FieldConf(id="company", datatype="string", size=  200, default="", required=0, name="Company", description=""),
       FieldConf(id="message", datatype="text",   size= 2000, default="", required=1, name="Message", description=""),
    ],
    mailtmpl = "nive_contact:contactmail.pt"
)

# these are the contact element fields
configuration.data = [
    FieldConf(id="topics",        datatype="text",   size=200, default="", name="Topics by line",description=""),
    FieldConf(id="receiver",      datatype="email",  size=100, default="", name="Receiver",      description=""),
    FieldConf(id="receiverName",  datatype="string", size=100, default="", name="Receiver name", description=""),
    FieldConf(id="mailtitle",     datatype="string", size=100, default="", name="Mail title",    description="")
]

# define the fields actually to be used in the cms element add and edit forms 
fields = ["title", "topics", "receiver", "receiverName", "mailtitle", "pool_groups"]
configuration.forms = {"create": {"fields":fields}, "edit": {"fields":fields}}

# define a new view to link our custom view class (ContactView) with the contact obj (ContactObj)
# this is required to call contact() from the template and process the form
configuration.views = [
    ViewConf(id="contactview", name="", attr="view", context=ContactObj, view=ContactView)
]
