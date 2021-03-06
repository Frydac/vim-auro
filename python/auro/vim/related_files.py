from auro.related_filenames_infos import infos
from auro.related_filenames import related_filenames_instantiated_matchers as related_filenames
from auro.path import AuroPath2
from auro.vim.utils import vim_filetype
from auro.basename import BasenameMatcher
from auro.dirname import DirnameMatcher
from pathlib import PurePath, Path
from pprint import pprint
import vim
import os.path
import json
import re

def vim_input(message = 'input'):
    vim.command('call inputsave()')
    vim.command("let user_input = input('" + message + ": ')")
    vim.command('call inputrestore()')
    return vim.eval('user_input')

def vim_inputlist(message, choices):
    fmt_choices = ["{nr}. {choice}".format(nr = ix + 1, choice = choice) for ix, choice in enumerate(choices)]
    ary = [message] + fmt_choices
    ary_str = json.dumps(ary)
    vim.command('call inputsave()')
    vim.command('let user_input = inputlist( ' + ary_str  + ' )')
    vim.command('call inputrestore()')
    return vim.eval('user_input')

def let_user_choose_list(message, choices):
    assert len(choices) > 0
    if len(choices) == 1:
        return choices[0]
    answer = int(vim_inputlist(message, choices))
    if answer > 0 and answer <= len(choices):
        return choices[answer - 1]
    return None

def create_open_file(fn):
    """
    vim always opens a buffer, and creates a file on write if the file doesn't
    exist. This hopefully creates a more consistent experience: the file will
    always 'physically' exist on disk.
    """
    path = Path(fn)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
    vim.command("silent e " + fn)

def let_user_choose_to_create_file(non_existing_fns_related):
    assert(len(non_existing_fns_related) > 0)
    if len(non_existing_fns_related) == 1:
        fn = non_existing_fns_related[0]
        assert(os.path.isfile(fn) != True)
        answer = vim_input("Related file does not exist, create %s? (y/<esc>)" % fn)
        if answer == 'y':
            create_open_file(non_existing_fns_related[0])
    else:
        fn_to_create = let_user_choose_list("No related file found, create one of the following: ", non_existing_fns_related)
        if (fn_to_create):
            create_open_file(fn_to_create)

def let_user_choose_to_open_file(existing_fns_related):
    fn = let_user_choose_list("Multiple potential related files exist, open: ", existing_fns_related)
    if fn:
        create_open_file(fn)
#  inputlist( "["Multiple potential related files exist, open: ", "1. /home/emile/repos/toplevel-fusion/comp-avs/protected/auro/avs/v1/metadata/QuantizerPosition.hpp", "2. /home/emile/repos/toplevel-fusion/comp-avs/protected/auro/avs/v1/metadata/QuantizerPosition.h"]" )
#  inputlist(["bla", "1. one", "2. two"])
def goc_related_filename(key_nr):
    """
    key_nr is the keyboard key to press, for now this is hardcoded on the
    numberkeys starting with 1, which corresponds to the first info entry for
    the current buffer's filetyp
    """
    index = key_nr - 1
    filetype = vim_filetype()

    if not filetype in infos or index > len(infos[filetype]):
        print("No info available for key_nr: {}".format(key_nr))
        return 

    related_fns_info = infos[filetype][index]

    if not related_fns_info:
        print("No related filenames info specified for filetype: %s and key: %s " % (filetype, key_nr))
        return

    fn_buffer = vim.current.buffer.name
    fns_related = related_filenames(fn_buffer, related_fns_info)

    if len(fns_related) == 0:
        print("No potential related files found for:")
        print("* filename: " + fn_buffer)
        #  print("* related_fns_info: ")
        #  pprint(related_fns_info)
        return

    existing_fns_related = [fn_related for fn_related in fns_related if os.path.isfile(fn_related)]

    if len(existing_fns_related) == 1:
        create_open_file(existing_fns_related[0])
    elif len(existing_fns_related) == 0:
        let_user_choose_to_create_file(fns_related)
    else:
        let_user_choose_to_open_file(existing_fns_related)

def get_related_filenames(key_nr):
    """
    same as goc_related_filename, but doesn't create
    """
    index = key_nr - 1
    filetype = vim_filetype()

    if not filetype in infos or index > len(infos[filetype]):
        print("No info available for key_nr: {}".format(key_nr))
        return 

    related_fns_info = infos[filetype][index]

    if not related_fns_info:
        print("No related filenames info specified for filetype: %s and key: %s " % (filetype, key_nr))
        return

    fn_buffer = vim.current.buffer.name
    return related_filenames(fn_buffer, related_fns_info)

def dn_bn_matchers_current_buffer():
    filetype = vim_filetype()
    infos_ft = infos[filetype]
    if not infos_ft:
        print("No info available for filetype {}".format(filetype))
        return
    # TODO: should find and merge all matchers, probably do in AuroPath2 (this could crash)
    basename_matchers = [BasenameMatcher(key, value) for key, value in infos_ft[1]['basename_matchers'].items()]
    dirname_matchers = [DirnameMatcher(key, value) for key, value in infos_ft[1]['dirname_matchers'].items()]
    return basename_matchers, dirname_matchers 

