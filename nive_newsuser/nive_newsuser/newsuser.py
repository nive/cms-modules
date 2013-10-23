# -*- coding: utf-8 -*-
# Copyright 2013 Nive GmbH. All rights reserved.
# Released under GPL3. see license.txt

__doc__ = """
E-Mail registration form
------------------------
Adds a simple email registration and unrigistration form element to the cms.
Website users can sign up with their email e.g. for a newsletter and remove 
their subsrciption again by entering their email. Confirmation emails are send 
to activate subscriptions.

The actual newsusers are stored in the userdb database by default. 
Also the `sendMail` module registered with the userdb is used to send activation
codes.
To change this please have a look at the configuration values `sendMailProvider`
and `storageApplication`.
"""

import uuid

from nive.views import Mail
from nive.forms import HTMLForm
from nive.definitions import IWebsiteRoot
from nive.definitions import ConfigurationError
from nive_cms.design.view import Design
from nive_cms.baseobjects import PageElementBase
from nive.components.objects.base import ObjectBase
from nive.definitions import StagPageElement, StagRessource
from nive.definitions import ObjectConf, FieldConf, ViewConf, Conf



class SubscriptionForm(HTMLForm):
    """
    Contact form
    """
    mail = None
    actions = [
         Conf(id="default",          method="StartForm", name=u"Initialize",   hidden=True),
         Conf(id="sendsubscription", method="Subscribe", name=u"Subscribe",    hidden=False, css_class=u"btn btn-info",  html=u"", tag=u""),
    ]

    def GenerateID(self, length=20, repl="-"):
        # generates a id
        return str(uuid.uuid4()).replace(repl,"")[:length]
        

    def Subscribe(self, action, **kw):
        """
        Form action: send the message 
        """
        msgs = []
        # lookup storage application
        storageID = self.context.configuration.storageApplication
        try:
            storage = self.context.app.portal[storageID]
        except KeyError:
            raise ConfigurationError, "Newsuser storage application not defined"
        storage = storage.root()
        # maybe the email is actually the activation id?
        aid = self.GetFormValue("email")
        if aid:
            newsusers = storage.Select(pool_type=u"newsuser", parameter={u"activationID":aid}, fields=[u"id"], max=2)
            if len(newsusers):
                user = storage.GetObj(newsuser[0][0])
                if user.Activate():
                    msgs.append("Finished. The subscription has been activated.")
                    return True, self._Msgs(msgs=msgs)
        # process the form
        result,data,errors = self.Validate(self.request)
        if result:
            # lookup email
            email = data["email"]
            newsusers = storage.Select(pool_type=u"newsuser", parameter={u"email":email}, fields=[u"id"], max=2)
            if len(newsusers)==0:
                # not found -> add a new subscription
                data = {u"email":email, 
                        u"newsgroup":self.newsgroup, 
                        u"pool_state": 0, 
                        u"notify": self.notify,
                        u"activationID": self.GenerateID()}
                # send mail
                body = self.mail(data=data, form=self, view=self.view)
                # lookup mail tool
                app = self.context.configuration.sendMailProvider
                try:
                    app = self.context.app.portal[app]
                except KeyError:
                    raise ConfigurationError, "Newsuser sendMail tool not defined"
                tool = app.GetTool("sendMail")
                result, value = tool(body=body, title=self.mail.title, recvmails=[(email,"")], force=1)
                if not result:
                    msgs.append("Sorry, a error occurred. The email could not be send.")
                else:
                    result = storage.Create(u"newsuser", data=data, user=self.view.User())
                    if result:
                        msgs.append("Thanks. Please follow the steps described in the email we have just send to complete the subscription.")
                        return result, self._Msgs(msgs=msgs)
            else:
                # found -> remove subscription(s)
                for user in newsusers:
                    storage.Delete(user[0], user=self.view.User())
                msgs.append("Finished. The subscription has been removed.")
                return result, self._Msgs(msgs=msgs)
        return result, self.Render(data, msgs=msgs, errors=errors)



class SubscriptionView(Design):
    
    def subscribe(self):
        context = self.context
        form = SubscriptionForm(context=context, request=self.request, view=self, app=context.app)
        form.fields = context.configuration.subscriptionForm
        form.anchor = u"#reg"+str(context.id)
        form.Setup()
        # required values for subscriptions: passed as form attributes 
        form.mail =  Mail(context.data.mailtitle, context.configuration.mailtmpl)
        form.mailtext = context.data.mailtext
        form.mailfooter = context.data.mailfooter
        form.notify = context.data.notify
        form.newsgroup = context.data.newsgroup
        form.activationUrl = self.CurrentUrl()
        result, data, action = form.Process()
        return data


    def activate(self):
        context = self.context
        # lookup storage application
        storageID = self.context.configuration.storageApplication
        try:
            storage = self.context.app.portal[storageID]
        except KeyError:
            raise ConfigurationError, "Newsuser storage application not defined"
        storage = storage.root()
        # try for valid activation id
        aid = self.GetFormValue("aid")
        if aid:
            newsusers = storage.Select(pool_type=u"newsuser", parameter={u"activationID":aid}, fields=[u"id"], max=2)
            if len(newsusers):
                user = storage.GetObj(newsusers[0][0])
                if user.Activate(self.User()):
                    return "Finished. The subscription has been activated."
            else:
                return "Sorry. The activation token is invalid. Maybe your subscription is already active."
        return ""


class CmsFormObj(PageElementBase):
    pass


# cms registration form definition ------------------------------------------------------------------

def SetupNewsuser(app):
    """
    Called on system startup to add the newsuser as module to the 
    current userdb by default. The behaviour can be changed by setting
    `configuration.storageApplication` to a different application id.
    Makes the step to manually add the newsuser 
    to the userdb obsolete (e.g. ``userdb.modules.append("nive_newsuser:newsuser_configuration")``)
    """
    conf = app.GetObjectConf("regform", True)
    # lookup storage application
    storageID = conf.storageApplication
    try:
        storage = app.portal[storageID]
    except KeyError:
        raise ConfigurationError, "Newsuser storage application not defined"
    storage.Register("nive_newsuser:newsuser_configuration")


#@nive_module
configuration = ObjectConf(
    id = "regform",
    name = "Subscriptions",
    dbparam = "regform",
    context = CmsFormObj,
    template = "nive_newsuser:form.pt",
    selectTag = StagPageElement,
    icon = "nive_cms.cmsview:static/images/types/element.png",
    description = __doc__,

    # system registration event to trigger userdb.newsuser installation
    events = (Conf(event="startup", callback=SetupNewsuser),),
    # the form to be displayed on the web page 
    subscriptionForm = [
       FieldConf(id="email",   datatype="email",  size=  200, default="", required=1, name="E-Mail", description=""),
    ],
    mailtmpl = "nive_newsuser:activationmail.pt",
    adminNotification = None,
    # Select the application for newsuser storage and the sendMail tool provider.
    # The value must be the application id registered in the portal (by default userdb) 
    sendMailProvider = "userdb",
    storageApplication = "userdb"
)

# these are the newsuser element fields
configuration.data = [
    FieldConf(id="mailtitle",    datatype="string",    size=255,  default="",  name="Activation mail title",description="Used as email title."),
    FieldConf(id="mailtext",     datatype="htext",     size=5000, default="",  name="Activation mail text", description="Added to the activation mail as header."),
    FieldConf(id="mailfooter",   datatype="htext",     size=5000, default="",  name="Activation mail footer",description="Added to the activation mail as footer."),
    FieldConf(id="notify",       datatype="bool",      size= 4,   default=1,   name="Notify by mail",       description="Can be used to assign different levels of notification."),
    FieldConf(id="newsgroup",    datatype="string",    size= 4,   default="",  name="Newsgroup assignment", description="If you have multiple sections on your website, you can automatically assign different newsgroups by filling the field. The user cannot change this value."),
]

# define the fields actually to be used in the cms element add and edit forms 
fields = ["title", "mailtitle", "mailtext", "mailfooter", "newsgroup", "pool_groups"]
configuration.forms = {"create": {"fields":fields}, "edit": {"fields":fields}}

# define a new view to link our custom view class (SubscriptionView) with the form obj (CmsFormObj)
# this is required to call subscribe() from the template and process the form
configuration.views = [
    ViewConf(id="subscriptionview", name="", attr="view", context=CmsFormObj, view=SubscriptionView)
]


# newsuser definition ------------------------------------------------------------------

class NewsuserObj(ObjectBase):

    def Activate(self, currentUser):
        """
        Activate newsuser and remove activation id
        calls workflow commit, if possible
        
        signals event: activate
        """
        wf = self.GetWf()
        if wf:
            result = wf.Action("commit", self, user=currentUser)
        else:
            self.meta.set("pool_state", 1)
            self.data.set("activationID", "")
            result = True
        if result:
            self.Signal("activate")
            self.Commit(currentUser)
        return result



#@nive_module
newsuser_configuration = ObjectConf(
    id = "newsuser",
    name = "E-Mail registration",
    dbparam = "newsuser",
    context = NewsuserObj,
    selectTag = StagPageElement,
    icon = "nive_cms.cmsview:static/images/types/element.png",
    description = __doc__,
)

# these are the newsuser element fields
newsuser_configuration.data = [
    FieldConf(id="email",      datatype="email",       size= 255, required=True, default="", name="E-Mail", description=""),
    FieldConf(id="notify",     datatype="bool",        size= 4,   default=1,   name="Notify by mail",       description="Can be used to assign different levels of notification."),
    FieldConf(id="newsgroup",  datatype="string",      size= 4,   default="",  name="Newsgroup assignment", description="If you have multiple sections on your website, you can automatically assign different newsgroups by filling the field. The user cannot change this value."),
    FieldConf(id="activationID", datatype="string",    size=30,   default="",  name="Activation ID",        description=""),
]


