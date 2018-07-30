from auro.c.related_filenames_infos import infos
from auro.path import AuroPath
from auro.related_filenames import related_filenames
from pathlib import PurePath, Path
from pprint import pprint
import vim
import os.path
import json

def python_input(message = 'input'):
  vim.command('call inputsave()')
  vim.command("let user_input = input('" + message + ": ')")
  vim.command('call inputrestore()')
  return vim.eval('user_input')

def python_inputlist(message, choices):
  fmt_choices = ["{nr}. {choice}".format(nr = ix + 1, choice = choice) for ix, choice in enumerate(choices)]
  ary = [message] + fmt_choices
  ary_str = json.dumps(ary)
  #  vim.command('call inputsave()')
  vim.command("let user_input = inputlist( " + ary_str  + " )")
  #  vim.command('call inputrestore()')
  return vim.eval('user_input')

def let_user_choose(message, ary):
    assert len(ary) > 0
    if len(ary) == 1:
        return ary[0]
    answer = int(python_inputlist(message, ary))
    if answer > 0 and answer <= len(ary):
        return ary[answer - 1]
    return None

def create_file(fn):
    path = Path(fn)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    vim.command("silent e " + fn)


def goc_related_filename(key_nr):
    index = key_nr - 1
    #  print("Finding related file for key_nr: {}".format(key_nr))
    if len(infos) < index:
        print("* No info available for key_nr: {}".format(key_nr))
    related_file_info = infos[index]
    fn_buffer = vim.current.buffer.name
    fns_related = related_filenames(fn_buffer, related_file_info)

    if len(fns_related) == 0:
        print("No potential related files found with:")
        print("* filename: " + fn_buffer)
        print("* related_file_info: ")
        pprint(related_file_info)
        return

    existing_fns_related = [fn_related for fn_related in fns_related if os.path.isfile(fn_related)]
    if len(existing_fns_related) == 1:
        vim.command("silent e " + existing_fns_related[0])
    elif len(existing_fns_related) == 0:
        #  print("No related file found. TODO: ask to create one of the following file(s)")  
        #  pprint(fns_related)
        #  if len(fns_related) == 1:
        #      fn_to_create = fns_related[0]
        #  else:
        fn_to_create = let_user_choose("No related file found, create one of the following: ", fns_related)
        if (fn_to_create):
            create_file(fn_to_create)
        #  else:
        #      print("Invalid choice, not creating a file")

    else:
        print("More than one related file found. TODO: ask to open one of the existing")
        pprint(fns_related)

