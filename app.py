#!/usr/bin/env python3

import sys

from mltm.cli import add_entry, show_entries


if __name__ == '__main__':
    n = len(sys.argv[1:])
    if n == 0:
        show_entries()
    elif sys.argv[1] == 'add':
        add_entry()
    else:
        show_entries(sys.argv[1])
