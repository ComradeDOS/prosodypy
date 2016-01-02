from prosodypy.decorators import lua_object_method

class ModuleWrapper(object):
    def __init__(self, module):
        self.module = module

    def __getattr__(self, key):
        if key == 'module':
            return super(ModuleWrapper, self).__getattr__(key)
        value = getattr(self.module, key)
        if callable(value):
            return lambda *args: value(self.module, *args)
        return value

    def __setattr__(self, key, value):
        if key == 'module':
            return super(ModuleWrapper, self).__setattr__(key, value)
        return setattr(self.module, key, value)

    def __hasattr__(self, key):
        return hasattr(self.module, key)


class ProsodyBasePlugin(object):
    """
    Base Prosody plugin class to be derived by all different plugins.

    Mimics the module:* callbacks from prosody as object methods.

    Has self.env and self.module attributes to access prosody APIs.
    """

    def __init__(self, env, lua):
        self.env = env
        self._module = env.module
        self.module = ModuleWrapper(self._module)
        self.prosody = env.prosody
        self.lua = lua
        for module_method in (
            'load',
            'save',
            'restore',
            'unload',
            'add_host',
        ):
            if hasattr(self, module_method):
                setattr(
                    self.module, module_method,
                    lua_object_method(getattr(self, module_method), lua)
                )

    def __call__(self, *args):
        pass

