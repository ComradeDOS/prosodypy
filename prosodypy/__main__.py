import sys
import importlib

import lupa
from lupa import LuaRuntime

lua = LuaRuntime(unpack_returned_tuples=True)

def execute_lua_file(filename):
    with open(filename, 'rb') as lua_file:
        code = lua_file.read()
    if code.startswith('#!'):
        code = code[code.find('\n'):]
    lua.execute(code)

def load_code_factory(orig_load_code):
    def load_code(plugin, resource, env):
        if plugin.startswith('!py:'):
            try:
                plugin = importlib.import_module(plugin[4:]).ProsodyPlugin(env, lua)
            except Exception as e:
                return False, unicode(e)
            return plugin, ""
        else:
            return orig_load_code(plugin, resource, env)
    return load_code

lua_globs = lua.globals()
lua_globs.arg = lua.table_from(sys.argv[1:])
lua_globs.load_code_factory = load_code_factory

orig_lua_select = lua_globs.select
lua.eval('''
function(load_code_factory, orig_lua_select)
    local swapped = false;
    _G.select = function(...)
        if not swapped then
            swapped = true;
            local pluginloader = require "util.pluginloader";
            pluginloader.load_code = load_code_factory(pluginloader.load_code);
            _G.select = orig_lua_select;
        end
        return _G.select(...);
    end
end
''')(load_code_factory, orig_lua_select)

execute_lua_file('/usr/bin/prosody') # TODO: don't hardcode
