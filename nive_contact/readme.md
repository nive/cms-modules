
# Contact form element for Nive cms!

See Nive cms: http://cms.nive.co

Adds a simple contact form page element to the list of available elements.
Website users can fill out the form and submit it so that the contents are
send by mail to a configured receiver.

## Usage

After installation (``pip install nive_contact``) activate the element by
adding ``nive_contact`` to your website project module list.

For a default scaffold installation go to `__init__.py` of your website
and add the following line to the configuration 
``website.modules.append("nive_contact")`` e.g. ::

    website = AppConf("nive.cms.app",
        title=u"My website", 
        id="website",
        ...
    )
    website.modules.append("nive_contact")
 

