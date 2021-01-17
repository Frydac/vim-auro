"""
Module contains functions that get the snip object from Ultisnips and thus must
be included from withing a .snippet file.
"""
from auro.cpp.catch import test_case_snip
from auro.vim.filename import Filename
import vim

def expand_test_case(snip):
    fn = Filename()
    snip_body = test_case_snip(fn)
    snip.expand_anon(snip_body)
    
