from enum import Enum
import re
from typing import NamedTuple, List, Dict, Optional, NewType

class Include(NamedTuple):
    name: str
    line_nr: int
    line: str

class Type(Enum):
    Auro = 0
    Std = 1
    Other = 2

Lines = List[str]
Includes = Dict[Type, List[Include]]

_auro_inc_re = re.compile(r'#include\s+"(auro.+)"')
_std_inc_re = re.compile(r'#include\s+<(.+)>')
_other_inc_re = re.compile(r'#include\s+"(.+)"')
_regexs = {Type.Auro: _auro_inc_re, Type.Std: _std_inc_re, Type.Other: _other_inc_re }
def find_includes(lines: Lines) -> Includes:
    """
    Find includes in Lines
    @return a hash with key Type, value is array of Include tupples of that Type
    """
    result = {} # type: Includes
    for inc_type in Type:
        result[inc_type] = []
    for ix, line in enumerate(lines):
        for inc_type, regex in _regexs.items():
            match = regex.match(line)
            if match:
                result[inc_type].append(Include(name = match.group(1), line_nr = ix, line = line))
                break #we don't want to match more than once, order of regexs is important, _other_inc_re would catch auro includes.
    return result

class IncludeGuard(NamedTuple):
    name: str
    line_begin: int
    line_end: int

_ifndef_re = re.compile(r'#ifndef\s+(\w+)')
_define_re = re.compile(r'#define\s+(\w+)')
def find_include_guard(lines: Lines) -> Optional[IncludeGuard]:
    state = 'idle'
    for ix, line in enumerate(lines):
        if state == 'idle':
            match = _ifndef_re.match(line)
            if match:
                name = match.group(1)
                line_begin = ix
                state = 'ifndef_found'
        elif state == 'ifndef_found':
            match = _define_re.match(line)
            if match and match.group(1) == name:
                line_end = ix
                return IncludeGuard(name, line_begin, line_end)
    return None
