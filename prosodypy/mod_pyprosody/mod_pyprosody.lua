--
-- mod_pyprosody starts prosody under lupa allowing to write modules
-- for prosody on python
--


local pluginloader = require"util.pluginloader";
local os = require"os";

local start_under_lupa = function()
    -- starts prosody under lupa
    local command = "python -m prosodypy " .. table.concat(arg, " ");
    module:log("debug", "starting prosody.py with %s...", command);
    os.execute(command); -- XXX: should use luaposix and exec?
end

module:log("debug", "Initializing mod_pyprosody...");

if load_code_factory == nil then
    -- we are not running under lupa, let's fix that!
    module:log("debug", "Could not find lupa");
    prosody.shutdown('restarting over lupa...');

    local virtualenv_command = module:get_option_string("python_ve_activate_command", "");
    local virtualenv_exit_code = 0;
    if #virtualenv_command > 0 then
        module:log("debug", "Activating python virtual environment using command %s", virtualenv_command);
        virtualenv_exit_code = os.execute(virtualenv_command);
    end
    if virtualenv_exit_code == 0 then
        module:hook_global("server-stopped", start_under_lupa, -1000);
    else
        module:log("error", "VE script exited with non-zero status %s", virtualenv_exit_code);
    end
else
    -- already under lupa, monkey patch the plugin loader to accept python
    -- files
    pluginloader.load_code = load_code_factory(pluginloader.load_code);
end
