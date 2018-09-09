from itertools import product
from pathlib import PurePath, Path
from pprint import pprint
from auro.basename import Basename, BasenameMatcher
from auro.dirname import Dirname, DirnameMatcher

def related_filenames(path: str, info):
    """
    Returns a list of potential related filenames based on info
    @param info
     dictionary with a specific layout to derive the related filenames from,
     see usages.
    """
    basename_matchers = [BasenameMatcher(key, value) for key, value in info['basename_matchers'].items()]
    dirname_matchers = [DirnameMatcher(key, value) for key, value in info['dirname_matchers'].items()]

    from_basename = Basename(basename_matchers , path)
    from_dirname = Dirname(dirname_matchers, path)

    to_basename_type_enums = flatten([from_to_pair['to'] for from_to_pair in info['basename_mapping'] if from_basename.type in from_to_pair['from']])
    to_basename_matchers = [bn_matcher for bn_matcher in basename_matchers if bn_matcher.bn_type in to_basename_type_enums]
    to_basenames = [create_related_basename(from_basename, to_bn_matcher) for to_bn_matcher in to_basename_matchers]

    to_dirname_type_enums = flatten([from_to_pair['to'] for from_to_pair in info['dirname_mapping'] if from_dirname.type in from_to_pair['from']])
    to_dirname_matchers = [dn_matcher for dn_matcher in dirname_matchers if dn_matcher.dn_type in to_dirname_type_enums]
    to_dirnames = [create_related_dirname(from_dirname, to_dn_matcher) for to_dn_matcher in to_dirname_matchers]

    related_filenames = [str(PurePath(dirname) / PurePath(basename)) for dirname, basename in list(product(to_dirnames, to_basenames))]
    return related_filenames

def create_related_dirname(from_dirname: Dirname, to_dn_matcher: DirnameMatcher):
    result = ''
    result += from_dirname.base_dir
    result += to_dn_matcher.dir_part
    result += from_dirname.namespace
    return result

def create_related_basename(from_basename: Basename, to_bn_matcher: BasenameMatcher):
    result = ''
    result += to_bn_matcher.prefix
    result += from_basename.name
    result += to_bn_matcher.suffix
    return result

import itertools
def flatten(list_of_lists):
    return list(itertools.chain(*list_of_lists))

