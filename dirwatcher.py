#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
"""

__author__ = "Bethsheba Zebata"

import sys
import signal
import logger
import os
import argparse

exit_flag = False
filesfound = []
magic_word_pos = {}


def search_for_magic(filename, start_line, magic_string):
    """Searches for the magic string in the filename and
    keeps track of the last line searched"""
    global magic_word_pos
    with open(start_line + '/' + filename) as f:
        for i, line in enumerate(f.readlines(), 1):
            if magic_string in line and i > magic_word_pos[filename]:
                logger.info('Woohoo! Magic word {} on line {} in file {}'
                            .format(magic_string, i, filename))
            if i > magic_word_pos[filename]:
                magic_word_pos[filename] += 1


def watch_directory(path, magic_string, extension, interval):
    """Watches directory,reports when files matching the
    given extension are added or removed.  Calls search_for_magic to search
    files for a magic word"""
    global filesfound
    global magic_word_pos
    logger.info('Watching dir {}, magic string: {}, extension: {},interval: {}'
                .format(path, magic_string, extension, interval))
    directory = os.path.abspath(path)
    file_in_dir = os.listdir(directory)
    for file in file_in_dir:
        if file.endswith(extension) and file not in filesfound:
            logger.info('new file: {} found in {}'.format(file, path))
            filesfound.append(file)
            magic_word_pos[file] = 0
    for file in filesfound:
        if file not in file_in_dir:
            logger.info('file {} removed from {}'.format(file, path))
            filesfound.remove(file)
            del magic_word_pos[file]
    for file in filesfound:
        search_for_magic(file, magic_string, directory)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interval', type=float, default=1,
                        help='polling interval')
    parser.add_argument('magic', help='magic text to watch for')
    parser.add_argument('-e', '--ext', type=str, default='.txt',
                        help="file extension to look for")
    # Your code here
    return


def signal_handler(sig_num, frame):
    """Looks for SIGINT and SIGTERM"""
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
