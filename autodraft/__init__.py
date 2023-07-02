from __future__ import absolute_import

import pkg_resources
__version__ = pkg_resources.require("autodraft")[0].version.split('-')[0]

from .draft_writer import *
