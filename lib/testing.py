import os
import vim

def hello():
    print(vim.command("echom expand('%')"))
