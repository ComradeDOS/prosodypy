from prosodypy import lua

assert lua

import os
config = lua.require("core.configmanager")
settings_module = config.get("*", "django_settings_module")
os.environ['DJANGO_SETTINGS_MODULE'] = settings_module
import django
django.setup()
