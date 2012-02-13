from raptus.mailcone.app.startup import debug_application_factory, application_factory

import warnings
from exceptions import Warning
warnings.filterwarnings('ignore', '.*', Warning, r'grokcore.view.templatereg', 0,)