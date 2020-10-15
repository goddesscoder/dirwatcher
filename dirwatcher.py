#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
"""

__author__ = "Bethsheba Zebata"

import sys
import signal
import logger

exit_flag = False


def search_for_magic(filename, start_line, magic_string):
    # Your code here
    return


def watch_directory(path, magic_string, extension, interval):
    # Your code here
    return


def create_parser():
    # Your code here
    return


def signal_handler(sig_num, frame):
    # Your code here
    global exit_flag
    signals = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
                   if v.startswith('SIG') and not v.startswith('SIG_'))
    logger.warning('Signal Received:' + signals[sig_num])
    if sig_num == signal.SIGINT or signal.SIGTERM:
        exit_flag = True
    return


def main(args):
    # Your code here
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    return


if __name__ == '__main__':
    main(sys.argv[1:])
