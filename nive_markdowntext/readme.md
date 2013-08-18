
# Markdown text element for Nive cms

See Nive cms: http://cms.nive.co

Adds a markdown text page element to the list of available elements.
Markdown syntax is automatically converted to html.

## Usage

After installation (``pip install nive_markdowntext``) activate the element by
adding ``nive_markdowntext`` to your website project module list.

For a default scaffold installation go to `__init__.py` of your website
and add the following line to the configuration 
``website.modules.append("nive_markdowntext")`` e.g. ::

    website = AppConf("nive.cms.app",
        title=u"My website", 
        id="website",
        ...
    )
    website.modules.append("nive_markdowntext")
 

