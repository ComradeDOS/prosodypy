import sys

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
        print plugin, resource, env
        return orig_load_code(plugin, resource, env)
    return load_code

lua_globs = lua.globals()
lua_globs.arg = lua.table_from(sys.argv[1:])
lua_globs.load_code_factory = load_code_factory

execute_lua_file('/usr/bin/prosody')
