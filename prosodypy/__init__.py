from __future__ import unicode_literals
lua = None


def execute_lua_file(lua, filename):
    with open(filename, 'rb') as lua_file:
        code = lua_file.read()
    if code.startswith(b'#!'):
        code = code[code.find(b'\n'):]
    lua.execute(code)
