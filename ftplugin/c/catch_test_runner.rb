# user calls function with cursor on certain line
# ruby script is called with this information
#   - parses the filename to get the current submodule, and the super repository path
#   - parse the file to get the TEST_CASE tags above the current line (later also the )
#   - figure out how to use djamels build stuff
#   - show the output in buffer?
#   - parse output of gcc/clang? or maybe use built in makeprg for build step?
#   - run test
#       - show output
#       - parse output and put in quickfix list
