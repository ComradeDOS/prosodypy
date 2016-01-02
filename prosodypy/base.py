from prosodypy.decorators import lua_object_method

class ProsodyBasePlugin(object):
    """
    Base Prosody plugin class to be derived by all different plugins.

    Mimics the module:* callbacks from prosody as object methods.

    Has self.env and self.module attributes to access prosody APIs.
    """

    def __init__(self, env, lua):
        self.env = env
        self.module = env.module
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
