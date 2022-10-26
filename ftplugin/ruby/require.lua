if not pcall(require, "related_files.file") then return end
if not pcall(require, 'emi.util') then return end

local RFile = require('related_files.file')
local str = require('emi/util').string

vim.keymap.set('n', 'ydi', function()
    local rfile = RFile:new(vim.api.nvim_buf_get_name(0))
    local line = "require '" .. rfile.namespace .. str.snake_case(rfile.name).."'"
    local linewise = "l"
    vim.fn.setreg('"', line, linewise)
    print("Changed unnamed register to: "..line)
end, { buffer = true, noremap = true })
