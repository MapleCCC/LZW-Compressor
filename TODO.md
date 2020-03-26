# TODO

- implement trie data structure to speedup performance
- profile to find performance bottleneck, and try to optimize
- add unit test for code dict and str dict
- why is our encode output different with the example one?
- hypothesis custom build strategy
- compute test coverage rate
- implement write_lzw_header for existed lzwfile
- use hypothesis' inference from type hinting feature
- add test suit for map-interface data structure
- use hypothesis' iterables strategy

# Done

- handle the corner case of zero file is input for compression
- handle the corner case of empty file
- add max_len restriction to code dict
- reserve the last code of code dict as virtual EOF
- the testing doesn't cover the case that code dict grows beyond capacity.
- consider rewriting in lazy evaluation / generator style, so as to save runtime space cost. Another importance of writing in stream style is that so our script can handle input that is infinitely large
- preserve newline format. Disable Python's builtin default universal newline support feature.
- ask for clarification of spec: should we handle the case of zero compressed file?
