#!/usr/bin/env python


import argparse
import datetime
import logging
import os
import random
import string
import sys


def parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', type=int, help="number of files to touch")
    parser.add_argument('-d', '--debug', action='store_true', help="turn on debug logging")
    parser.set_defaults(debug=False)
    return parser


def main ():
    logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger()    

    args = parser().parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    logger.debug("Generating filenames in memory")
    filenames = list(generate_filenames(args.files))
    logger.debug("Generated {0} filenames".format(len(filenames)))

    logger.debug("Ensuring directories")
    directories = ensure_directories(filenames)
    logger.debug("Ensured {0} directories".format(len(directories)))

    logger.debug("Touching files")
    seconds = count_seconds(lambda: touch_files(filenames))
    try:
        rate = 1.0 * len(filenames) / seconds
    except ZeroDivisionError:
        rate = 1.0 * len(filenames)
        logger.debug("Touched {0} files ({1} <1sec)".format(len(filenames), rate))
    else:
        logger.debug("Touched {0} files ({1}/sec)".format(len(filenames), rate))

    print rate


def count_seconds (func):
    start = datetime.datetime.now()
    func()
    end = datetime.datetime.now()
    return total_seconds(end - start)


def touch_files (filenames):
    for filename in filenames:
        prefix, suffix = filename[:2], filename[2:]
        touch_file(os.path.join(prefix, suffix))


def touch_file (filename):
    open(filename, 'a').close()


def generate_filenames (num):
    for _ in xrange(int(num)):
        yield generate_filename()


def generate_filename ():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))


def ensure_directories (filenames):
    prefixes = set(filename[:2] for filename in filenames)
    for prefix in prefixes:
        try:
            os.mkdir(prefix)
        except OSError as ex:
            if ex.errno == 17:
                pass
            else:
                raise
    return prefixes


def total_seconds (td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6


if __name__ == '__main__':
    main()
