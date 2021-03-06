import itertools
from itertools import product
from pathlib import PurePath
from pprint import pformat, pprint
from auro.basename import Basename, BasenameMatcher
from auro.dirname import Dirname, DirnameMatcher
from difflib import SequenceMatcher
import logging
# logging.basicConfig(level=logging.INFO)


def sort_related_fns(input_path, related_fns):
    """
    Sort by distance from input string
    """
    # TODO: better sort, same parent dir first, then use string distance or maybe use input order of dirname/basename matchers?
    distances_fns = {}
    for fn in related_fns:
        distances_fns.setdefault(SequenceMatcher(
            None, input_path, fn).ratio(), []).append(fn)
    sorted_related_fns = []
    for dist in sorted(distances_fns, reverse=True):
        sorted_related_fns.extend(distances_fns[dist])

    return sorted_related_fns


# TODO: deprecate this function? used in ut
def related_filenames(path: str, info):
    """
    Returns a list of potential related filenames based on info
    @param info
     dictionary with a specific layout to derive the related filenames from,
     see usages.
    """
    # Instantiat matchers (this is done globally when loading all the matchers)
    info_cpy = info.copy()
    info_cpy['basename_matchers'] = [BasenameMatcher(
        key, value) for key, value in info['basename_matchers'].items()]
    info_cpy['dirname_matchers'] = [DirnameMatcher(
        key, value) for key, value in info['dirname_matchers'].items()]

    return related_filenames_instantiated_matchers(path, info_cpy)


def related_filenames_instantiated_matchers(path: str, info):
    from_basename = Basename(info['basename_matchers'], path)
    #  logging.info("\n█ from_basename:\n %s", pformat(from_basename))
    from_dirname = Dirname(info['dirname_matchers'], path)
    #  logging.info("\n█ from_dirname:\n %s", pformat(from_dirname))

    #  print("█ info['basename_mapping']:")
    #  pprint(info['basename_mapping'])
    to_basename_type_enums = flatten(
        [from_to_pair['to'] for from_to_pair in info['basename_mapping'] if from_basename.type in from_to_pair['from']])
    if not to_basename_type_enums:
        raise Exception("Can't generate a basename to map to, given current mapping rules, starting from: {}\n{}".format(path, from_basename))
    #  print("█ to_basename_type_enums:")
    #  pprint(to_basename_type_enums)
    to_basename_matchers = [bn_matcher for bn_matcher in info['basename_matchers']
                            if bn_matcher.bn_type in to_basename_type_enums]
    to_basenames = [create_related_basename(
        from_basename, to_bn_matcher) for to_bn_matcher in to_basename_matchers]
    #  print("█ to_basenames:")
    #  pprint(to_basenames)

    #  print("█ info['dirname_mapping']:")
    #  pprint(info['dirname_mapping'])
    to_dirname_type_enums = flatten(
        [from_to_pair['to'] for from_to_pair in info['dirname_mapping'] if from_dirname.type in from_to_pair['from']])
    if not to_dirname_type_enums:
        raise Exception("Can't generate a dirname to map to, given current mapping rules, starting from:\n{}".format(from_dirname))
    #  print("█ to_dirname_type_enums:")
    #  pprint(to_dirname_type_enums)
    to_dirname_matchers = [dn_matcher for dn_matcher in info['dirname_matchers']
                           if dn_matcher.dn_type in to_dirname_type_enums]
    to_dirnames = [create_related_dirname(
        from_dirname, to_dn_matcher) for to_dn_matcher in to_dirname_matchers]

    # TODO: replace product by allowed combos
    related_filenames = [str(PurePath(dirname) / PurePath(basename))
                         for dirname, basename in list(product(to_dirnames, to_basenames))]

    sorted_related_fns = sort_related_fns(path, related_filenames)

    return sorted_related_fns


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


def flatten(list_of_lists):
    return list(itertools.chain(*list_of_lists))
