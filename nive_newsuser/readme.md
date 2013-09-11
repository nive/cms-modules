
# News user form element for Nive cms!

See Nive cms: http://cms.nive.co

Adds a simple email registration and unrigistration form element to the cms.
Website users can sign up with their email e.g. for a newsletter and remove 
their subsrciption again by entering their email. Confirmation emails are send 
to activate subscriptions.

This actually adds two objects: the cms page element providing the form 
functions and the newsuser object to storage the emails. 

Newsletter handling or backend functionlaity is not included.

## Usage

After installation (``pip install nive_newsuser``) activate the element by
adding ``nive_newsuser`` to your website project module list.

For a default scaffold installation go to `__init__.py` of your website
and add the following line to the configuration: 
``website.modules.append("nive_newsuser:configuration")``  e.g. ::

    website = AppConf("nive.cms.app",
        # ...
    )
    website.modules.append("nive_newsuser")


