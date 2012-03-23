import site, os
site.addsitedir(os.path.dirname(__file__))

from wampws import app as application
