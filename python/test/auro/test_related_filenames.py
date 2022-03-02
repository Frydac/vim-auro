import unittest
from typing import List, Dict

#  from pprint import pprint
#  from enum import Enum
#  from auro.path import AuroPath, include_path
from auro.related_filenames import related_filenames
from auro.c.related_filenames_infos import related_header_info, related_source_info, related_test_info
from pprint import pprint

#  from pprint import pprint


def print_related_fns(from_fns: List[str], info: Dict) -> None:
    for fn in from_fns:
        print("█ from fn:")
        pprint(fn)
        related_fns = related_filenames(fn, info)
        print(" to related_fns:")
        pprint(related_fns)


class TestRelatedFiles(unittest.TestCase):
    def test_to_header(self):
        fns = [
                "/test/audio/src/tf/log.cpp",
            "/home/emile/repos/all/comp/headphones/test/public/auro/headphones/v2/Renderer_tests.cpp",
            "/home/emile/repos/all/comp/headphones/test/protected/auro/headphones/v2/Renderer_tests.cpp",
            "/home/emile/repos/all/comp/headphones/test/private/auro/headphones/v2/Renderer_tests.cpp",
            "/home/emile/repos/all/comp/headphones/c99/public/auro/headphones/v2/Renderer.c",
            "/home/emile/repos/all/comp/headphones/c89/protected/auro/headphones/v2/Renderer.c",
            "/home/emile/repos/all/comp/headphones/c17/private/auro/headphones/v2/Renderer.c",
            "/home/emile/repos/all/comp/headphones/cpp98/public/auro/headphones/v2/Renderer.cpp",
            "/home/emile/repos/all/comp/headphones/cpp11/protected/auro/headphones/v2/Renderer.cpp",
            "/home/emile/repos/all/comp/headphones/cpp20/private/auro/headphones/v2/Renderer.cpp",
            "/home/emile/repos/all/comp/headphones/asd/auro/headphones/v2/parameter/Gains.asd",
        ]
        print_related_fns(fns, related_header_info)

    def test_to_source(self):
        fns = [
                "test/audio/src/tf/log.hpp",
            "/home/emile/repos/all/comp/headphones/test/public/auro/headphones/v2/Renderer_tests.cpp",
            "/home/emile/repos/all/comp/headphones/test/protected/auro/headphones/v2/Renderer_tests.cpp",
            "/home/emile/repos/all/comp/headphones/test/private/auro/headphones/v2/Renderer_tests.cpp",
            "/home/emile/repos/all/comp/headphones/c99/public/auro/headphones/v2/Renderer.h",
            "/home/emile/repos/all/comp/headphones/c89/protected/auro/headphones/v2/Renderer.h",
            "/home/emile/repos/all/comp/headphones/c17/private/auro/headphones/v2/Renderer.h",
            "/home/emile/repos/all/comp/headphones/cpp98/public/auro/headphones/v2/Renderer.hpp",
            "/home/emile/repos/all/comp/headphones/cpp11/protected/auro/headphones/v2/Renderer.hpp",
            "/home/emile/repos/all/comp/headphones/cpp20/private/auro/headphones/v2/Renderer.hpp",
            "/home/emile/repos/all/comp/headphones/asd/auro/headphones/v2/parameter/Gains.asd",
        ]
        print_related_fns(fns, related_source_info)

    def test_to_test(self):
        fns = [
            "/home/emile/repos/all/comp/headphones/c99/public/auro/headphones/v2/Renderer.h",
            "/home/emile/repos/all/comp/headphones/c89/protected/auro/headphones/v2/Renderer.h",
            "/home/emile/repos/all/comp/headphones/c17/private/auro/headphones/v2/Renderer.h",
            "/home/emile/repos/all/comp/headphones/cpp98/public/auro/headphones/v2/Renderer.hpp",
            "/home/emile/repos/all/comp/headphones/cpp11/protected/auro/headphones/v2/Renderer.hpp",
            "/home/emile/repos/all/comp/headphones/cpp20/private/auro/headphones/v2/Renderer.hpp",
            "/home/emile/repos/all/comp/headphones/c99/public/auro/headphones/v2/Renderer.c",
            "/home/emile/repos/all/comp/headphones/c89/protected/auro/headphones/v2/Renderer.c",
            "/home/emile/repos/all/comp/headphones/c17/private/auro/headphones/v2/Renderer.c",
            "/home/emile/repos/all/comp/headphones/cpp98/public/auro/headphones/v2/Renderer.cpp",
            "/home/emile/repos/all/comp/headphones/cpp11/protected/auro/headphones/v2/Renderer.cpp",
            "/home/emile/repos/all/comp/headphones/cpp20/private/auro/headphones/v2/Renderer.cpp",
        ]
        print_related_fns(fns, related_test_info)

    def test_to_asd(self):
        pass

    def test_error(self):
        fns = [
                # header in same dir -> test cpp should also match test hpp
                "/home/emile/repos/all/comp/apm/test/protected/auro/apm/v1/reader/test/utility.cpp"
        ]
        print_related_fns(fns, related_header_info)

    def test_same_file(self):
        fns = [ 
                #  "/home/emile/repos/pannersuite/Auro-Encoder/inc/AuroLoudness.h",
                "/home/emile/repos/pannersuite/Auro-Settings/Auro-Settings-App/Src/AuroSettingsBackend.h",
                ]
        print_related_fns(fns, related_source_info)


if __name__ == "__main__":
    unittest.main()
