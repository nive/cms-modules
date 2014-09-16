
__doc__ = """
Website Design
----------------
Extends `nive_cms_design_bs3` by the grayscale bootstrap single page template set
"""

from nive.definitions import ViewModuleConf, Conf

from nive_cms_design_bs3 import elementcss
    
# view module definition ------------------------------------------------------------------

#@nive_module
configuration = ViewModuleConf("nive_cms_design_bs3",
    id = "design",
    name = u"Single page design",
    static = "nive_cms_design_bs_grayscale:static",
    templates = "nive_cms_design_bs_grayscale:templates",
    template = "index.pt",
    # assets list the requirements for the website
    assets = [
        ('bootstrap.css', 'nive_cms_design_bs_grayscale:static/css/bootstrap.min.css'),
        ('grayscale.css', 'nive_cms_design_bs_grayscale:static/css/grayscale.css'),
        ('cmsview.css', 'nive_cms_design_bs_grayscale:static/styles.css'),              # nive css
        ('font-awesome.min.css', 'nive_cms_design_bs_grayscale:static/font-awesome-4.1.0/css/font-awesome.min.css'),
        ('jquery.js', 'nive_cms_design_bs_grayscale:static/js/jquery-1.11.0.js'),
        ('bootstrap.js', 'nive_cms_design_bs_grayscale:static/js/bootstrap.min.js'),
        ('jquery.easing.js', 'nive_cms_design_bs_grayscale:static/js/jquery.easing.min.js'),
        ('grayscale.js', 'nive_cms_design_bs_grayscale:static/js/grayscale.js'),
    ],
    events = (Conf(event="startRegistration", callback=elementcss.setup),),
    description=__doc__
)