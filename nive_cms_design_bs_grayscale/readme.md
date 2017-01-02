
# Single page cms design based on bootstrap 3 grayscale!

The design renders a series of pages on the level on a single page. The navigation allows the user to scroll smoothly
to the selected content without leaving the page. The editor shows only the single page for easier handling.

## ABOUT GRAYSCALE

Grayscale is a free Bootstrap 3 theme created by Start Bootstrap. It can be yours right now, simply download the 
template on the preview page. The theme is open source, and you can use it for any purpose, personal or commercial.

This theme features stock photos by Gratisography along with a custom Google Maps skin courtesy of Snazzy Maps.

Grayscale includes full HTML, CSS, and custom JavaScript files along with LESS files for easy customization.

See http://startbootstrap.com/template-overviews/grayscale/

## Usage

After installation (``pip install nive_cms_design_bs_grayscale``) activate the element by
adding ``nive_cms_design_bs_grayscale`` to your websites' project module list.

For a default scaffold installation go to `__init__.py` of your website
and add the following line to the configuration ``website.modules.append("nive_cms_design_bs_grayscale")`` e.g. ::

    website = AppConf("nive.cms.app",
        title=u"My website", 
        id="website",
        ...
    )
    website.modules.append("nive_cms_design_bs_grayscale")
 

See Nive cms: http://cms.nive.co
