from auro.vim.filename import Filename
from pprint import pprint


def test_case_snip(fn: Filename):
    separator = "::"

    # if the only related header is a c file use c style namespace
    if (fn.has_single_existing_related_filename(related_type='header', ft='c')):
        separator = "_"

    namespaces = fn.namespace_parts()
    if len(namespaces) > 1 and namespaces[0] == 'auro':
        namespaces = namespaces[1:]

    test_name = separator.join(namespaces)
    test_name += separator + fn.classname()
    if separator == "_":
        test_name += "_t"
    tags = ''.join(["[%s]" % ns for ns in namespaces])
    snip_body = "TEST_CASE_FAST(\"test %s${1: }\", \"%s${3:[%s]}${4:[${5}]}\")\n" % (
        test_name, tags, fn.classname())
    snip_body += "{\n"
    snip_body += "    ${0}\n"
    snip_body += "}"
    return snip_body
