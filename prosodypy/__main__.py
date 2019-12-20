from __future__ import unicode_literals
import sys
import os
import importlib
import traceback

dlopen_flags = os.RTLD_NOW | os.RTLD_GLOBAL
old_flags = sys.getdlopenflags()
sys.setdlopenflags(dlopen_flags)
from lupa import LuaRuntime
sys.setdlopenflags(old_flags)

lua = LuaRuntime(unpack_returned_tuples=True)
sys.modules['prosodypy'].lua = lua
execute_lua_file = sys.modules['prosodypy'].execute_lua_file


def load_code_factory(orig_load_code):
    def load_code(plugin, resource, env):
        install_pymodule_paths()
        if plugin.startswith('!py:'):
            try:
                plugin = importlib.import_module(plugin[4:]).ProsodyPlugin(
                        env, lua)
            except Exception as e:
                return False, traceback.format_exc()
            return plugin, ""
        else:
            return orig_load_code(plugin, resource, env)
    return load_code


def install_pymodule_paths():
    config = lua.require("core.configmanager")
    paths = config.get("*", "plugin_paths")
    for i in paths:
        if paths[i] not in sys.path:
            sys.path.insert(0, paths[i])


lua_globs = lua.globals()
lua_globs.arg = lua.table_from(sys.argv[1:])
lua_globs.load_code_factory = load_code_factory

orig_lua_select = lua_globs.select
lua.eval('''
function(load_code_factory, orig_lua_select)
    package.path = '/usr/lib/prosody/?.lua;' .. package.path;
    local events = require 'util.events';
    local old_new = events.new;
    events.new = function(...)
        local result = old_new(...);
        local old_fire_event = result.fire_event;
        result.fire_event = function(event, ...)
            if event == 'server-starting' then
                local pluginloader = require "util.pluginloader";
                pluginloader.load_code = load_code_factory(
                    pluginloader.load_code);
            end
            return old_fire_event(event, ...);
        end
        return result;
    end
end
''')(load_code_factory, orig_lua_select)

execute_lua_file(lua, '/usr/bin/prosody')  # TODO: don't hardcode
