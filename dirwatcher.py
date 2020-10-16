#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
"""

__author__ = "Bethsheba Zebata"

import sys
import signal
import logging
import os
import argparse
import time
import datetime

exit_flag = False
filesfound = []
magic_word_pos = {}
logger = logging.getLogger(__file__)


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
            logger.info('file {} not found in {}'.format(file, path))
            # filesfound.remove(file)
            # del magic_word_pos[file]
    for file in filesfound:
        search_for_magic(file, magic_string, directory)


def create_parser():
    """Creates Parser
       Sets up command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interval', type=float, default=1,
                        help='polling interval')
    parser.add_argument('magic', help='magic text to watch for')
    parser.add_argument('-e', '--ext', type=str, default='.txt',
                        help="file extension to look for")
    return parser


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
    """
    Includes a startup and shutdown banner in logs and reports the total
    runtime (uptime) within shutdown log banner
    """

    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s'
        '[%(threadName)-12s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logger.setLevel(logging.DEBUG)
    start_time = datetime.datetime.now()

    logger.info(
        '\n'
        '-------------------------------------------------------------------\n'
        '    Running {0}\n'
        '    Started on {1}\n'
        '-------------------------------------------------------------------\n'
        .format(__file__, start_time.isoformat())
    )

    parser = create_parser()
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while not exit_flag:
        try:
            watch_directory(args)
        except OSError:
            logger.error('Directory {} does not exist'.format(args.path))
            time.sleep(args.interval * 2)
        except Exception as e:
            logger.error('Unhandled exception:{}'.format(e))
        time.sleep(args.interval)

    uptime = datetime.datetime.now()-start_time
    logger.info(
        '\n'
        '-------------------------------------------------------------------\n'
        '    Stopped {0}\n'
        '    Uptime was {1}\n'
        '-------------------------------------------------------------------\n'
        .format(__file__, str(uptime))
    )


if __name__ == '__main__':
    main(sys.argv[1:])
