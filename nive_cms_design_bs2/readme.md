
# Nive cms design based on bootstrap 2!

Up to the 1.0 release this was the default design. Now released as independent 
package.

See Nive cms: http://cms.nive.co

## Usage

After installation (``pip install nive_cms_design_bs2``) activate the element by
adding ``nive_cms_design_bs2`` to your website project module list.

For a default scaffold installation go to `__init__.py` of your website
and add the following line to the configuration 
``website.modules.append("nive_cms_design_bs2")`` e.g. ::

    website = AppConf("nive.cms.app",
        title=u"My website", 
        id="website",
        ...
    )
    website.modules.append("nive_cms_design_bs2")
 

