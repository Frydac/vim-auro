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
    # parse and determine this paths basename type depending on the related filename info for its language
    from_basename = Basename(info['basename_matchers'], path)
    #  print("█ from_basename:")
    #  pprint(from_basename)

    # for the given from_basename, find all the basename types that are related to it given the info (e.g. .cpp -> .h .hpp)
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

    # parse and determine this paths dirname type depending on the related filename info for its language
    try:
        from_dirname = Dirname(info['dirname_matchers'], path)
    except Exception:
        # if we can't parse the dirname, just fall back to same path matches
        return related_filenames_from_same_dir(path, to_basenames)
    #  print("█ from_dirname:")
    #  pprint(from_dirname)

    # Now given the from_dirname, find all the dirname types that are related to it
    #  print("█ info['dirname_mapping']:")
    #  pprint(info['dirname_mapping'])
    to_dirname_type_enums = flatten(
        [from_to_pair['to'] for from_to_pair in info['dirname_mapping'] if from_dirname.type in from_to_pair['from']])
    #  print("█ info['dirname_mapping']:")
    #  pprint(info['dirname_mapping'])
    if not to_dirname_type_enums:
        #  raise Exception("Can't generate a dirname to map to, given current mapping rules, starting from:\n{}".format(from_dirname))
        # if we can't find a matching diranme for the current from_basename and from_dirname combo, fall back to same path matches
        return related_filenames_from_same_dir(path, to_basenames)
    else:
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

def related_filenames_from_same_dir(path: str, to_basenames):
    dirname = PurePath(path).parent
    #  print("█ dirame:")
    #  pprint(dirname)
    related_filenames = [str(dirname / PurePath(basename)) for basename in to_basenames]
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


def flatten(list_of_lists):
    return list(itertools.chain(*list_of_lists))
