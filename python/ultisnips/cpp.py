"""
Module contains functions that get the snip object from Ultisnips and thus must
be included from withing a .snippet file.
"""
from auro.path import AuroPath
from auro.cpp.catch import test_case_snip
import vim

def expand_test_case(snip):
    path = AuroPath(vim.current.buffer.name)
    snip_body = test_case_snip(path, vim.current.buffer)
    snip.expand_anon(snip_body)
    
