from auro_path import AuroPath, possible_headers, find_includes
from auro.vim.filename import Filename
from auro.c.init import *
import vim

def expand_init(snip):
    path = AuroPath(vim.current.buffer.name)
    snip_body = init_snip(path)
    snip.expand_anon(snip_body)
    
# TODO when no includes, only includes starting at 0?, search for include guard if header.


def expand_include(snip):
    snippet_body = '#include <${0:vector}>'
    snip.expand_anon(snippet_body)

def expand_include_auro(snip):
    snippet_body = '#include "${1:auro/}$0"'
    snip.expand_anon(snippet_body)

def expand_include_auro_pathidi(snip):
    #  path = AuroPath(vim.current.buffer.name)
    path = Filename()
    print("█ path:")
    pprint(path)
    #  namespace = ''
    #  for ns in path.namespaces:
    #          namespace += ns + '/'
    #  snippet_body = '#include "%s"$0' % path.dirname.namespace
    snip.expand_anon(path)
	

def add_current_cursor_pos_to_jumplist():
    vim.command(":normal m'")

def del_current_line(snip):
    del(snip.buffer[snip.line])


def del_line_and_move_cursor_to_includes(snip):
    includes = find_includes(AuroPath(vim.current.buffer.name))
    if not includes:
            print("vim-auro snippet warning: No includes found inserting on current line")		
            # TODO: if header find include guard, if cpp goto 0
            return
    del_current_line(snip)
    last_include_lineix = max(includes.keys())
    add_current_cursor_pos_to_jumplist()
    snip.buffer.append('', last_include_lineix + 1)
    snip.cursor.set(last_include_lineix + 1, 0)

