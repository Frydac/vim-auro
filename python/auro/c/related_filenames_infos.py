#  from pathlib import Path
#  from pprint import pprint
#  from typing import List
from enum import Enum
import itertools

# Used to identify 'type' of a basename as an enum value so we can refer to it
# later, and when the string is subtracted from the basename, the common
# part/name that is the same for related filenames should remain.
Bt = Enum("BasenameTypeEnum", "hpp cpp c h test asd")
basename_matchers = {
    Bt.hpp: [".hpp", ".hxx"],  # cpp headers
    Bt.cpp: [".cpp"],  # cpp source
    Bt.h: [".h"],  # c headers
    Bt.c: [".c", ".cc"],  # c source
    Bt.test: ["_tests.cpp"],  # c and cpp test
    Bt.asd: [".asd"],
}

c_versions = {"c89", "c95", "c99", "c11", "c17"}
cpp_versions = {"cpp98", "cpp03", "cpp11", "cpp14", "cpp17", "cpp20"}
c_cpp_access = {"private", "protected", "public"}
c_cpp_access_legacy = {"inc", "src"}

combos = []
for c_ver, access in itertools.product(c_versions, c_cpp_access):
    combos.append({"lang": "c", "version": c_ver, "access": access})
for cpp_ver, access in itertools.product(cpp_versions, c_cpp_access):
    combos.append({"lang": "cpp", "version": cpp_ver, "access": access})


def dt_combo(combo):
    return "{ver}_{acc}".format(ver=combo["version"], acc=combo["access"])


def dt_test(access):
    return "test_{acc}".format(acc=access)


version_enum_names = [dt_combo(combo) for combo in combos]
# test dont have a language version
test_enum_names = [dt_test(access) for access in c_cpp_access]
test_legacy_enum_names = [dt_test(access) for access in c_cpp_access_legacy]

enum_names = []
enum_names += c_cpp_access_legacy
enum_names += c_cpp_access  # also legacy by now
enum_names += version_enum_names
enum_names += test_enum_names
enum_names += test_legacy_enum_names
enum_names += ["asd"]

# Used to identify the 'type' of the path as an enum value so we can refer to it later.
# The {base_dir} and {namespace} are common parts between related paths.
Dt = Enum("DirnameType", enum_names)
dirname_matchers = {}
for enum_name in c_cpp_access_legacy.union(c_cpp_access):
    dirname_matchers[Dt[enum_name]] = "{base_dir}/%s/{namespace}" % enum_name
for access in c_cpp_access.union(c_cpp_access_legacy):
    dirname_matchers[Dt[dt_test(access)]] = "{base_dir}/test/%s/{namespace}" % access
for combo in combos:
    dirname_matchers[Dt[dt_combo(combo)]] = "{base_dir}/%s/%s/{namespace}" % (
        combo["version"],
        combo["access"],
    )
dirname_matchers[Dt.asd] = "{base_dir}/asd/{namespace}"


##
# Related Header Info
#
# related filename information to find a related header (so from something to header)
##

related_header_info = {
    # map which basenam type for the target header can be used, based on the basename type of the current buffer
    "basename_mapping": [
        {"from": [Bt.cpp, Bt.test, Bt.asd], "to": [Bt.hpp, Bt.h]},
        {"from": [Bt.c], "to": [Bt.h]},
    ],
    "dirname_mapping": [
        {"from": [Dt.public], "to": [Dt.public, Dt.protected, Dt.private]},
        {"from": [Dt.protected], "to": [Dt.protected, Dt.private]},
        {"from": [Dt.private], "to": [Dt.private]},
        {"from": [Dt.test_private], "to": [Dt.test_private]},
        {"from": [Dt.test_protected], "to": [Dt.test_protected]},
        {"from": [Dt.test_public], "to": [Dt.test_public]},
        {"from": [Dt.src], "to": [Dt.inc, Dt.src]},
    ],
    "basename_dirname_mapping": [],
    "basename_matchers": basename_matchers,
    "dirname_matchers": dirname_matchers,
}

# list allowed combinations of target header dirname/basename (if certain
# dirnames and basenames are not used in this, all combinations of those
# dirnames with any of those basenames is allowed)
def basename_dirname_mapping():
    result = [{"dirname": [Dt.asd], "basename": [Bt.asd]}]
    for combo in combos:
        if combo["lang"] == "c":
            result.append({"dirname": [Dt[dt_combo(combo)]], "basename": [Bt.h, Bt.c]})
        elif combo["lang"] == "cpp":
            result.append(
                {"dirname": [Dt[dt_combo(combo)]], "basename": [Bt.hpp, Bt.cpp]}
            )
    result.append(
        {"dirname": [dt_test(acc) for acc in c_cpp_access], "basename": [Bt.test]}
    )
    return result


def add_common_versions_dn_mapping(versions, to_info):
    for ver in versions:
        # to public header
        to_info["dirname_mapping"].append(
            {
                "from": [
                    Dt[dt_test("public")],
                    Dt[dt_test("protected")],
                    Dt[dt_test("private")],
                    Dt.asd,
                ],
                "to": [Dt[dt_combo({"version": ver, "access": "public"})]],
            }
        )
        # to protected header
        to_info["dirname_mapping"].append(
            {
                "from": [Dt[dt_test("protected")], Dt[dt_test("private")], Dt.asd],
                "to": [Dt[dt_combo({"version": ver, "access": "protected"})]],
            }
        )
        # to private header
        to_info["dirname_mapping"].append(
            {
                "from": [Dt[dt_test("private")], Dt.asd],
                "to": [Dt[dt_combo({"version": ver, "access": "private"})]],
            }
        )


def add_cpp_to_hpp_dn_mapping():
    for cpp_ver in cpp_versions:
        # to public header
        for cpp_ver2, acc in itertools.product(cpp_versions, c_cpp_access):
            related_header_info["dirname_mapping"].append(
                {
                    "from": [Dt[dt_combo({"version": cpp_ver2, "access": acc})]],
                    "to": [Dt[dt_combo({"version": cpp_ver, "access": "public"})]],
                }
            )

        # to protected header
        for cpp_ver2, acc in itertools.product(cpp_versions, c_cpp_access):
            if acc == "public":
                continue
            related_header_info["dirname_mapping"].append(
                {
                    "from": [Dt[dt_combo({"version": cpp_ver2, "access": acc})]],
                    "to": [Dt[dt_combo({"version": cpp_ver, "access": "protected"})]],
                }
            )

        # to private header
        for cpp_ver2 in cpp_versions:
            related_header_info["dirname_mapping"].append(
                {
                    "from": [Dt[dt_combo({"version": cpp_ver2, "access": "private"})]],
                    "to": [Dt[dt_combo({"version": cpp_ver, "access": "private"})]],
                }
            )


def add_c_cpp_to_h_dn_mapping():
    """
    Note: cpp dir/files can have h dir/headers
    """
    for c_ver in c_versions:
        # to public header
        for c_ver2, acc in itertools.product(c_versions, c_cpp_access):
            related_header_info["dirname_mapping"].append(
                {
                    "from": [Dt[dt_combo({"version": c_ver2, "access": acc})]],
                    "to": [Dt[dt_combo({"version": c_ver, "access": "public"})]],
                }
            )
        for cpp_ver, acc in itertools.product(cpp_versions, c_cpp_access):
            related_header_info["dirname_mapping"].append(
                {
                    "from": [Dt[dt_combo({"version": cpp_ver, "access": acc})]],
                    "to": [Dt[dt_combo({"version": c_ver, "access": "public"})]],
                }
            )

        # to protected header
        for c_ver2, acc in itertools.product(c_versions, c_cpp_access):
            if acc == "public":
                continue
            related_header_info["dirname_mapping"].append(
                {
                    "from": [Dt[dt_combo({"version": c_ver2, "access": acc})]],
                    "to": [Dt[dt_combo({"version": c_ver, "access": "protected"})]],
                }
            )
        for cpp_ver, acc in itertools.product(cpp_versions, c_cpp_access):
            if acc == "public":
                continue
            related_header_info["dirname_mapping"].append(
                {
                    "from": [Dt[dt_combo({"version": cpp_ver, "access": acc})]],
                    "to": [Dt[dt_combo({"version": c_ver, "access": "protected"})]],
                }
            )

        # to private header
        for c_ver2 in c_versions:
            related_header_info["dirname_mapping"].append(
                {
                    "from": [Dt[dt_combo({"version": c_ver2, "access": "private"})]],
                    "to": [Dt[dt_combo({"version": c_ver, "access": "private"})]],
                }
            )
        for cpp_ver in cpp_versions:
            related_header_info["dirname_mapping"].append(
                {
                    "from": [Dt[dt_combo({"version": cpp_ver, "access": "private"})]],
                    "to": [Dt[dt_combo({"version": c_ver, "access": "private"})]],
                }
            )


add_common_versions_dn_mapping(c_versions, related_header_info)
add_common_versions_dn_mapping(cpp_versions, related_header_info)
add_c_cpp_to_h_dn_mapping()
add_cpp_to_hpp_dn_mapping()
related_header_info["basename_dirname_mapping"] = basename_dirname_mapping()

##
# Related Source Info
#
# related filename information to find a related source file (.c .cpp) (so from something to source)
##

related_source_info = {
    "basename_mapping": [
        {"from": [Bt.h, Bt.test, Bt.hpp, Bt.asd], "to": [Bt.cpp]},
        {"from": [Bt.h, Bt.test, Bt.asd], "to": [Bt.c]},
    ],
    "dirname_mapping": [
        {"from": [Dt.public], "to": [Dt.public]},
        {"from": [Dt.protected], "to": [Dt.protected, Dt.public]},
        {"from": [Dt.private], "to": [Dt.private, Dt.protected, Dt.public]},
        {"from": [Dt.test_private], "to": [Dt.test_private]},
        {"from": [Dt.test_protected], "to": [Dt.test_protected]},
        {"from": [Dt.test_public], "to": [Dt.test_public]},
        {"from": [Dt.inc], "to": [Dt.src]},
    ],
    "basename_dirname_mapping": related_header_info["basename_dirname_mapping"],
    "basename_matchers": basename_matchers,
    "dirname_matchers": dirname_matchers,
}


def add_h_to_c_cpp_dn_mapping():
    for c_ver in c_versions:
        # to public c file
        for c_ver2 in c_versions:
            related_source_info["dirname_mapping"].append(
                {
                    "from": [Dt[dt_combo({"version": c_ver2, "access": "public"})]],
                    "to": [Dt[dt_combo({"version": c_ver, "access": "public"})]],
                }
            )
        for cpp_ver2 in cpp_versions:
            related_source_info["dirname_mapping"].append(
                {
                    "from": [Dt[dt_combo({"version": c_ver, "access": "public"})]],
                    "to": [Dt[dt_combo({"version": cpp_ver2, "access": "public"})]],
                }
            )

        # to protected c file
        for c_ver2, acc in itertools.product(c_versions, c_cpp_access):
            if acc == "private":
                continue
            related_source_info["dirname_mapping"].append(
                {
                    "from": [Dt[dt_combo({"version": c_ver2, "access": acc})]],
                    "to": [Dt[dt_combo({"version": c_ver, "access": "protected"})]],
                }
            )
        for cpp_ver2, acc in itertools.product(cpp_versions, c_cpp_access):
            if acc == "private":
                continue
            related_source_info["dirname_mapping"].append(
                {
                    "from": [Dt[dt_combo({"version": c_ver, "access": acc})]],
                    "to": [Dt[dt_combo({"version": cpp_ver2, "access": "protected"})]],
                }
            )

        # to private c file
        for c_ver2, acc in itertools.product(c_versions, c_cpp_access):
            related_source_info["dirname_mapping"].append(
                {
                    "from": [Dt[dt_combo({"version": c_ver2, "access": acc})]],
                    "to": [Dt[dt_combo({"version": c_ver, "access": "private"})]],
                }
            )
        for cpp_ver2, acc in itertools.product(cpp_versions, c_cpp_access):
            related_source_info["dirname_mapping"].append(
                {
                    "from": [Dt[dt_combo({"version": c_ver, "access": acc})]],
                    "to": [Dt[dt_combo({"version": cpp_ver2, "access": "private"})]],
                }
            )


def add_hpp_to_cpp_mapping():
    for cpp_ver in cpp_versions:
        # to public cpp file
        for cpp_ver2 in cpp_versions:
            related_source_info["dirname_mapping"].append(
                {
                    "from": [Dt[dt_combo({"version": cpp_ver2, "access": "public"})]],
                    "to": [Dt[dt_combo({"version": cpp_ver, "access": "public"})]],
                }
            )

        # to protected cpp file
        for cpp_ver2, acc in itertools.product(cpp_versions, c_cpp_access):
            if acc == "private":
                continue
            related_source_info["dirname_mapping"].append(
                {
                    "from": [Dt[dt_combo({"version": cpp_ver2, "access": acc})]],
                    "to": [Dt[dt_combo({"version": cpp_ver, "access": "protected"})]],
                }
            )

        # to private cpp file
        for cpp_ver2, acc in itertools.product(cpp_versions, c_cpp_access):
            related_source_info["dirname_mapping"].append(
                {
                    "from": [Dt[dt_combo({"version": cpp_ver2, "access": acc})]],
                    "to": [Dt[dt_combo({"version": cpp_ver, "access": "private"})]],
                }
            )


add_common_versions_dn_mapping(c_versions, related_source_info)
add_common_versions_dn_mapping(cpp_versions, related_source_info)
add_h_to_c_cpp_dn_mapping()
add_hpp_to_cpp_mapping()

related_test_info = {
    "basename_mapping": [{"from": [Bt.h, Bt.hpp, Bt.c, Bt.cpp], "to": [Bt.test]}],
    "dirname_mapping": [
        {"from": [Dt.public], "to": [Dt.test_public, Dt.test_private]},
        {"from": [Dt.test_public], "to": [Dt.test_public]},
        {"from": [Dt.test_private], "to": [Dt.test_private]},
        {"from": [Dt.protected, Dt.test_protected], "to": [Dt.test_protected]},
        {"from": [Dt.private], "to": [Dt.test_private]},
        {"from": [Dt.inc], "to": [Dt.test_inc, Dt.test_src]},
        {"from": [Dt.src], "to": [Dt.test_src]},
    ],
    "basename_matchers": basename_matchers,
    "dirname_matchers": dirname_matchers,
}

for ver in cpp_versions.union(c_versions):
    # to public test
    related_test_info["dirname_mapping"].append(
        {
            "from": [Dt[dt_combo({"version": ver, "access": "public"})]],
            "to": [Dt[dt_test("public")]],
        }
    )

    # to protected test
    for acc in c_cpp_access:
        if acc == "private":
            continue
        related_test_info["dirname_mapping"].append(
            {
                "from": [Dt[dt_combo({"version": ver, "access": acc})]],
                "to": [Dt[dt_test("protected")]],
            }
        )

    # to private test
    for acc in c_cpp_access:
        related_test_info["dirname_mapping"].append(
            {
                "from": [Dt[dt_combo({"version": ver, "access": acc})]],
                "to": [Dt[dt_test("private")]],
            }
        )

related_asd_info = {
    "basename_mapping": [{"from": [Bt.h, Bt.test, Bt.hpp], "to": [Bt.asd]}],
    "dirname_mapping": [
        {"from": [Dt.public, Dt.protected, Dt.private], "to": [Dt.asd]}
    ],
    "basename_matchers": basename_matchers,
    "dirname_matchers": dirname_matchers,
}

for ver, acc in itertools.product(cpp_versions.union(c_versions), c_cpp_access):
    related_asd_info["dirname_mapping"].append(
        {"from": [Dt[dt_combo({"version": ver, "access": acc})]], "to": [Dt.asd]}
    )

related_header_info_from_asd = {
    "basename_mapping": [{"from": [Bt.asd], "to": [Bt.hpp, Bt.h]}],
    "dirname_mapping": [
        {"from": [Dt.asd], "to": [Dt.public, Dt.protected, Dt.private]}
    ],
    "basename_matchers": basename_matchers,
    "dirname_matchers": dirname_matchers,
}

for ver, acc in itertools.product(cpp_versions.union(c_versions), c_cpp_access):
    related_header_info_from_asd["dirname_mapping"].append(
        {"from": [Dt.asd], "to": [Dt[dt_combo({"version": ver, "access": acc})]]}
    )

c_cpp_infos = [
    related_header_info,
    related_source_info,
    related_test_info,
    related_asd_info,
]
asd_infos = [related_header_info_from_asd]

infos = {}
infos["c"] = c_cpp_infos
infos["cpp"] = c_cpp_infos
infos["tree"] = asd_infos
infos["asd"] = asd_infos
